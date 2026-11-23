# Wool2String development

Requires Python 3.11+, no external dependencies.

```sh
python -m unittest discover -s scripts -p "test_*.py"
python scripts/build.py
```

Generated files in ignored `dist/`: 12 individual ZIPs, a `SHA256SUMS.txt` checksum manifest, and a master bundle. ZIPs are reproducible with fixed timestamps and sorted entries. CI builds all formats and retains the generated archives; pushing a `v*` tag runs release validation and publishes them to GitHub Releases.

Editable recipes live in `src/recipes/`, versions in `src/targets.json`. The builder validates both against explicit schemas, pack metadata and overlay rules. The stable modern pack uses format 18 plus overlays at 41 (result), 48 (recipe folder), and 57 (ingredient). Compatibility is capped at 121.0; the snapshot preview uses modern `min_format`/`max_format` for 122.0–128.0.

Before releasing, test representative versions in the game: **1.13.2, 1.14.4, 1.20.4, 1.20.5, 1.21, 1.21.2, 1.21.11, 26.3, and a 26.4 snapshot**. For each, verify pack enablement, all 16 wool colors, 1 wool consumed and 4 string produced, invalid ingredients rejected, and reload behavior. Automated tests do not substitute for this.

Developed using the compatibility approach of [Flesh2Leather](https://github.com/myzticdev/flesh2leather) and [CraftSaddles](https://github.com/myzticdev/CraftSaddles). Sources: [1.20.5](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-20-5), [1.21](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21), [1.21.2](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21-2), [26.3](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3), [26.4 snapshot 9/10](https://www.minecraft.net/en-us/article/minecraft-26-4-snapshot-9).
