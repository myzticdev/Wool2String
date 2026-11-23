"""Generate and validate reproducible Java Edition Wool2String datapacks."""
import hashlib, io, json, shutil, sys, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DESC="Wool2String by myzticdev - Craft one wool into four string."
MASTER="Wool2String-myzticdev-All-Versions.zip"
TARGETS=[
("1.13-1.13.2",4,"plain"),("1.14-1.14.4",4,"legacy"),
("1.15-1.16.1",5,"legacy"),("1.16.2-1.16.5",6,"legacy"),
("1.17-1.17.1",7,"legacy"),("1.18-1.18.1",8,"legacy"),
("1.18.2",9,"legacy"),("1.19-1.19.3",10,"legacy"),
("1.19.4",12,"legacy"),("1.20-1.20.1",15,"legacy"),
("1.20.2-26.3",18,"modern"),("26.4-snapshot-1-10",122,"snapshot")]
OVERLAYS=[("ov_result",41,47,"stack"),("ov_path",48,56,"stack"),
          ("ov_ingredient",57,121,"strings")]
SNAPSHOTS={"26.4-snapshot-1":(122,0),"26.4-snapshot-2":(122,1),
"26.4-snapshot-3":(123,0),"26.4-snapshot-4":(124,0),
"26.4-snapshot-5":(125,0),"26.4-snapshot-6":(125,1),
"26.4-snapshot-7":(126,0),"26.4-snapshot-8":(127,0),
"26.4-snapshot-9":(128,0),"26.4-snapshot-10":(128,0)}

def require(condition,message):
    if not condition: raise ValueError(message)
def strict_pairs(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,"Duplicate JSON key: "+key)
        result[key]=value
    return result
def invalid_constant(value): raise ValueError("JSON constant "+value)
def parse(s):
    return json.loads(s,object_pairs_hook=strict_pairs,parse_constant=invalid_constant)
def encode(x): return (json.dumps(x,indent=2,ensure_ascii=False)+"\n").encode("utf-8")
def expected_recipe(schema):
    require(schema in {"plain","legacy","stack","strings"},"Unknown schema")
    return {"type":"crafting_shapeless" if schema=="plain" else "minecraft:crafting_shapeless",
        "ingredients":["#minecraft:wool"] if schema=="strings" else [{"tag":"minecraft:wool"}],
        "result":{"id" if schema in {"stack","strings"} else "item":"minecraft:string","count":4}}
def check_recipe(value,schema):
    require(json.dumps(value,sort_keys=True)==json.dumps(expected_recipe(schema),sort_keys=True),
            "Invalid recipe or count for "+schema)
def recipe_path(fmt):
    return "data/wool2string/"+("recipe" if fmt>=48 else "recipes")+"/wool_to_string.json"
def meta(target):
    name,fmt,schema=target
    pack={"description":DESC}
    if schema=="snapshot":
        pack.update(min_format=[122,0],max_format=[128,0])
        return {"pack":pack}
    pack["pack_format"]=fmt
    if schema=="modern":
        pack.update(supported_formats={"min_inclusive":18,"max_inclusive":81},
                    min_format=[18,0],max_format=[121,0])
        return {"pack":pack,"overlays":{"entries":[{
            "directory":directory,"formats":{"min_inclusive":low,"max_inclusive":high},
            "min_format":[low,0],"max_format":[high,0 if high==121 else 2147483647]}
            for directory,low,high,_ in OVERLAYS]}}
    return {"pack":pack}
def active_recipes(files,fmt,entries):
    active={p:v for p,v in files.items() if p.startswith("data/")}
    for entry in entries:
        bounds=entry["formats"]
        if bounds["min_inclusive"]<=fmt<=bounds["max_inclusive"]:
            prefix=entry["directory"]+"/"
            active.update({p[len(prefix):]:v for p,v in files.items() if p.startswith(prefix)})
    folder="/recipe/" if fmt>=48 else "/recipes/"
    return {p:v for p,v in active.items() if folder in p}
def check_pack(files,target):
    name,fmt,schema=target
    require(parse(files["pack.mcmeta"])==meta(target),"Invalid metadata "+name)
    required={"pack.mcmeta","pack.png",recipe_path(fmt)}
    require(files["pack.png"].startswith(b"\x89PNG\r\n\x1a\n"),"Invalid PNG icon")
    base="strings" if schema=="snapshot" else "legacy" if schema=="modern" else schema
    check_recipe(parse(files[recipe_path(fmt)]),base)
    if schema=="modern":
        for directory,low,_,overlay_schema in OVERLAYS:
            path=directory+"/"+recipe_path(low)
            required.add(path)
            check_recipe(parse(files[path]),overlay_schema)
        entries=meta(target)["overlays"]["entries"]
        for current in range(18,122):
            active=active_recipes(files,current,entries)
            require(set(active)=={recipe_path(current)},"Overlay/path error at "+str(current))
            current_schema="legacy" if current<41 else "stack" if current<57 else "strings"
            check_recipe(parse(active[recipe_path(current)]),current_schema)
    require(set(files)==required,"Unexpected pack files for "+name)
def archive(files):
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,"w",compression=zipfile.ZIP_STORED) as z:
        for path,data in sorted(files.items()):
            require(not path.startswith("/") and ".." not in Path(path).parts,"Unsafe ZIP path")
            info=zipfile.ZipInfo(path,(1980,1,1,0,0,0))
            info.create_system=3
            info.external_attr=0o100644<<16
            z.writestr(info,data)
    result=stream.getvalue()
    with zipfile.ZipFile(io.BytesIO(result)) as z:
        require(z.testzip() is None and z.namelist()==sorted(files),"ZIP integrity error")
        for path,data in files.items():
            require(z.read(path)==data,"ZIP mismatch "+path)
    return result
def safe_dir(path):
    require(not path.is_symlink() and path.resolve()==path,"Unsafe directory")
    if path.exists():
        require(path.is_dir(),"Not a directory")
        for child in path.rglob("*"):
            require(not child.is_symlink() and child.resolve()==child,"Linked path")
def release_files(root=ROOT):
    src=root/"src"
    safe_dir(src)
    expected={"targets.json","pack.png"}|{f"recipes/{s}.json" for s in ("plain","legacy","stack","strings")}
    require({p.relative_to(src).as_posix() for p in src.rglob("*") if p.is_file()}==expected,
            "Unexpected/missing source")
    require(parse((src/"targets.json").read_bytes())==
        [dict(range=name,pack_format=fmt,schema=schema) for name,fmt,schema in TARGETS],
        "Targets file differs")
    for schema in ("plain","legacy","stack","strings"):
        check_recipe(parse((src/f"recipes/{schema}.json").read_bytes()),schema)
    icon=(src/"pack.png").read_bytes()
    output={}
    for target in TARGETS:
        name,fmt,schema=target
        base="strings" if schema=="snapshot" else "legacy" if schema=="modern" else schema
        files={"pack.png":icon,"pack.mcmeta":encode(meta(target)),recipe_path(fmt):encode(expected_recipe(base))}
        if schema=="modern":
            for directory,low,_,overlay_schema in OVERLAYS:
                files[directory+"/"+recipe_path(low)]=encode(expected_recipe(overlay_schema))
        check_pack(files,target)
        output[f"Wool2String-{name}.zip"]=archive(files)
    output["SHA256SUMS.txt"]="".join(
        hashlib.sha256(data).hexdigest()+"  "+name+"\n"
        for name,data in sorted(output.items())).encode("ascii")
    output[MASTER]=archive(output)
    return output
def build(root=ROOT):
    require(sys.version_info>=(3,11),"Python 3.11+ required")
    outputs=release_files(root)
    dist=root/"dist"
    safe_dir(dist)
    if dist.exists(): shutil.rmtree(dist)
    dist.mkdir()
    for name,data in outputs.items():
        (dist/name).write_bytes(data)
        require((dist/name).read_bytes()==data,"Bad output "+name)
    print(f"Validated {len(TARGETS)} packs; produced {len(outputs)} release files.")
if __name__=="__main__":
    try: build()
    except (ValueError,OSError,KeyError,TypeError,zipfile.BadZipFile) as exc:
        print("Build failed: "+str(exc),file=sys.stderr)
        raise SystemExit(1)
