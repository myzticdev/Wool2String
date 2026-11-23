"""Regression checks for crafting data, overlay selection, and reproducible ZIPs."""
import copy, hashlib, io, json, sys, unittest, zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build

class TestRecipes(unittest.TestCase):
    def test_every_schema(self):
        for schema in ("plain","legacy","stack","strings"):
            value=build.expected_recipe(schema)
            build.check_recipe(value,schema)
            for other in ("plain","legacy","stack","strings"):
                if other!=schema:
                    with self.assertRaises(ValueError): build.check_recipe(value,other)
            for key,bad in (("result",{"id":"minecraft:string","count":1}),
                            ("result",{"id":"minecraft:string","count":True}),
                            ("ingredients",[{"item":"minecraft:white_wool"}]),
                            ("ingredients",["#minecraft:planks"]),
                            ("type","minecraft:crafting_shaped")):
                edited=copy.deepcopy(value)
                edited[key]=bad
                with self.assertRaises(ValueError): build.check_recipe(edited,schema)
    def test_strict_json(self):
        for s in ('{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}','{nope}'):
            with self.assertRaises(ValueError): build.parse(s)

class TestBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.outputs=build.release_files()
    def test_all_packs(self):
        for target in build.TARGETS:
            name=f"Wool2String-{target[0]}.zip"
            with zipfile.ZipFile(io.BytesIO(self.outputs[name])) as z:
                data={p:z.read(p) for p in z.namelist()}
                build.check_pack(data,target)
                self.assertEqual(data["pack.png"],(build.ROOT/"src/pack.png").read_bytes())
                self.assertIsNone(z.testzip())
    def test_overlay_boundaries(self):
        with zipfile.ZipFile(io.BytesIO(self.outputs["Wool2String-1.20.2-26.3.zip"])) as z:
            data={p:z.read(p) for p in z.namelist()}
        entries=build.meta(build.TARGETS[-2])["overlays"]["entries"]
        for fmt in (18,40,41,47,48,56,57,81,94,101,107,121):
            active=build.active_recipes(data,fmt,entries)
            self.assertEqual(set(active),{build.recipe_path(fmt)})
            schema="legacy" if fmt<41 else "stack" if fmt<57 else "strings"
            build.check_recipe(build.parse(active[build.recipe_path(fmt)]),schema)
        broken=dict(data)
        broken.pop("ov_ingredient/"+build.recipe_path(57))
        with self.assertRaises((ValueError,KeyError)):
            build.check_pack(broken,build.TARGETS[-2])
    def test_snapshot_bound(self):
        pack=build.meta(build.TARGETS[-1])["pack"]
        self.assertEqual(pack["min_format"],[122,0])
        self.assertEqual(pack["max_format"],[128,0])
        self.assertNotIn("pack_format",pack)
        self.assertEqual(build.SNAPSHOTS["26.4-snapshot-10"],(128,0))
    def test_bundle_and_repeatability(self):
        self.assertEqual(self.outputs,build.release_files())
        lines=self.outputs["SHA256SUMS.txt"].decode().splitlines()
        self.assertEqual(len(lines),len(build.TARGETS))
        for line in lines:
            digest,name=line.split("  ")
            self.assertEqual(digest,hashlib.sha256(self.outputs[name]).hexdigest())
        with zipfile.ZipFile(io.BytesIO(self.outputs[build.MASTER])) as z:
            self.assertEqual(set(z.namelist()),set(self.outputs)-{build.MASTER})
            for name in z.namelist():
                self.assertEqual(z.read(name),self.outputs[name])
if __name__=="__main__": unittest.main()
