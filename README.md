# Wool2String

**Wool2String** is a small Minecraft **Java Edition** datapack by [myzticdev](https://github.com/myzticdev). Craft **one block of any of the 16 wool colors into four string** in a 2×2 inventory grid or a crafting table. Uses the vanilla `minecraft:wool` item tag; adds exactly one shapeless recipe, `wool2string:wool_to_string`.

No resource pack, mod, functions, commands, tick loop, or recipe changes beyond this.

## Downloads

Build with `python scripts/build.py` or download the matching version ZIP from [GitHub Releases](https://github.com/myzticdev/Wool2String/releases) after publication.

| Java Edition | Datapack ZIP |
| --- | --- |
| 1.13–1.13.2 | `Wool2String-1.13-1.13.2.zip` |
| 1.14–1.14.4 | `Wool2String-1.14-1.14.4.zip` |
| 1.15–1.16.1 | `Wool2String-1.15-1.16.1.zip` |
| 1.16.2–1.16.5 | `Wool2String-1.16.2-1.16.5.zip` |
| 1.17–1.17.1 | `Wool2String-1.17-1.17.1.zip` |
| 1.18–1.18.1 | `Wool2String-1.18-1.18.1.zip` |
| 1.18.2 | `Wool2String-1.18.2.zip` |
| 1.19–1.19.3 | `Wool2String-1.19-1.19.3.zip` |
| 1.19.4 | `Wool2String-1.19.4.zip` |
| 1.20–1.20.1 | `Wool2String-1.20-1.20.1.zip` |
| 1.20.2–26.3 | `Wool2String-1.20.2-26.3.zip` |
| 26.4 snapshots 1–10 (preview only) | `Wool2String-26.4-snapshot-1-10.zip` |

**Stable support target:** 1.13 through 26.3. **Snapshot preview target:** 26.4 snapshots 1–10 (format 122.0–128.0). The snapshot ZIP is separate; later snapshots and final 26.4 are not covered. These are format-checked compatibility targets, **not claims of successful in-game testing**.

### Installation

1. Place the ZIP for your Minecraft Java version in your world's `datapacks/` directory.
2. Reopen the world or run `/reload` (operator permission may be needed).
3. Check `/datapack list enabled`, then craft any wool block into four string.

Install **one version-specific datapack**. If downloading `Wool2String-myzticdev-All-Versions.zip`, **extract it first** and install only the matching inner ZIP, never the whole bundle. Recipe book auto-unlocking is not included; with vanilla `doLimitedCrafting=false`, manual crafting works.

## Development

Requires Python 3.11+, no external dependencies.

```sh
python -m unittest discover -s scripts -p "test_*.py"
python scripts/build.py
```

Generated files in ignored `dist/`: 12 individual ZIPs, a `SHA256SUMS.txt` checksum manifest, and a master bundle. ZIPs are reproducible with fixed timestamps and sorted entries. CI builds all formats and retains the generated archives; pushing a `v*` tag runs release validation and publishes them to GitHub Releases.

Editable recipes live in `src/recipes/`, versions in `src/targets.json`. The builder validates both against explicit schemas, pack metadata and overlay rules. The stable modern pack uses format 18 plus overlays at 41 (result), 48 (recipe folder), and 57 (ingredient). Compatibility is capped at 121.0; the snapshot preview uses modern `min_format`/`max_format` for 122.0–128.0.

Before releasing, test representative versions in the game: **1.13.2, 1.14.4, 1.20.4, 1.20.5, 1.21, 1.21.2, 1.21.11, 26.3, and a 26.4 snapshot**. For each, verify pack enablement, all 16 wool colors, 1 wool consumed and 4 string produced, invalid ingredients rejected, and reload behavior. Automated tests do not substitute for this.

Developed using the compatibility approach of [Flesh2Leather](https://github.com/myzticdev/flesh2leather) and [CraftSaddles](https://github.com/myzticdev/CraftSaddles). Sources: [1.20.5](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-20-5), [1.21](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21), [1.21.2](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21-2), [26.3](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3), [26.4 snapshot 9/10](https://www.minecraft.net/en-us/article/minecraft-26-4-snapshot-9).
