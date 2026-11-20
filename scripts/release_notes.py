"""Require a matching dated changelog entry before publishing a tag."""
import re,sys
from build import ROOT,require
def get(tag):
    require(re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+",tag),"Expected vMAJOR.MINOR.PATCH")
    changelog=(ROOT/"CHANGELOG.md").read_text(encoding="utf-8")
    match=re.search(r"^## \["+re.escape(tag[1:])+r"\] - \d{4}-\d{2}-\d{2}\n(.*?)(?=^## |\Z)",
                    changelog,re.MULTILINE|re.DOTALL)
    require(match and match.group(1).strip(),"Missing dated release entry")
    return match.group(1).strip()
if __name__=="__main__":
    try: print(get(sys.argv[1] if len(sys.argv)==2 else ""))
    except (OSError,ValueError) as exc: sys.exit(str(exc))
