#!/usr/bin/env python3
"""
Build city landing pages from template.html + cities.json.

Usage:
    python3 build.py              # build all cities into ../
    python3 build.py --out ./dist # build into a different directory
    python3 build.py --only novi  # build one city (by slug)

Tokens replaced in template.html:
    {{CITY}}      city name          e.g. "Royal Oak"
    {{SLUG}}      url/id slug        e.g. "royal-oak"
    {{LANDMARK}}  intro landmark     e.g. "the Detroit Zoo"
    {{ROAD}}      intro major road   e.g. "Woodward Avenue"

Anything not tokenized stays identical across every page. That includes
"Southfield" (the office location), the service-area list, and the
JSON-LD @id — all of which must NOT vary per city.
"""

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
TEMPLATE = HERE / "template.html"
CITIES = HERE / "cities.json"

TOKENS = ("CITY", "SLUG", "LANDMARK", "ROAD")


def load():
    if not TEMPLATE.exists():
        sys.exit(f"missing {TEMPLATE}")
    if not CITIES.exists():
        sys.exit(f"missing {CITIES}")
    tpl = TEMPLATE.read_text(encoding="utf-8")
    try:
        cities = json.loads(CITIES.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"cities.json is not valid JSON: {e}")
    return tpl, cities


def check_template(tpl):
    """Fail loudly if the template is missing tokens or has stray ones."""
    found = set(re.findall(r"\{\{(\w+)\}\}", tpl))
    unknown = found - set(TOKENS)
    if unknown:
        sys.exit(f"template has unknown tokens: {sorted(unknown)}")
    missing = set(TOKENS) - found
    if missing:
        print(f"  warning: template never uses {sorted(missing)}")
    return found


def extract_jsonld(html):
    """Return list of parsed JSON-LD blocks, or raise on bad JSON."""
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>',
        html,
        re.DOTALL,
    )
    return [json.loads(b) for b in blocks]


def build_one(tpl, entry, outdir):
    for key in ("city", "slug", "landmark", "road"):
        if not entry.get(key):
            print(f"  SKIP {entry.get('slug') or entry.get('city') or '?'}: missing '{key}'")
            return None

    html = tpl
    html = html.replace("{{CITY}}", entry["city"])
    html = html.replace("{{SLUG}}", entry["slug"])
    html = html.replace("{{LANDMARK}}", entry["landmark"])
    html = html.replace("{{ROAD}}", entry["road"])

    leftover = re.findall(r"\{\{(\w+)\}\}", html)
    if leftover:
        print(f"  FAIL {entry['slug']}: unreplaced tokens {sorted(set(leftover))}")
        return None

    try:
        blocks = extract_jsonld(html)
    except json.JSONDecodeError as e:
        print(f"  FAIL {entry['slug']}: JSON-LD did not parse — {e}")
        return None

    if len(blocks) != 1:
        print(f"  FAIL {entry['slug']}: expected 1 JSON-LD block, found {len(blocks)}")
        return None

    ld = blocks[0]
    if ld.get("@id") != "https://mechanicaltemp.com/#business":
        print(f"  FAIL {entry['slug']}: JSON-LD @id is not the shared business id")
        return None
    if ld.get("areaServed", {}).get("name") != entry["city"]:
        print(f"  FAIL {entry['slug']}: areaServed does not match city")
        return None

    path = outdir / f"{entry['slug']}.html"
    path.write_text(html, encoding="utf-8")
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="..", help="output directory (default: parent)")
    ap.add_argument("--only", help="build a single city by slug")
    args = ap.parse_args()

    outdir = (HERE / args.out).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    tpl, cities = load()
    check_template(tpl)

    slugs = [c.get("slug") for c in cities]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        sys.exit(f"duplicate slugs in cities.json: {sorted(dupes)}")

    if args.only:
        cities = [c for c in cities if c.get("slug") == args.only]
        if not cities:
            sys.exit(f"no city with slug '{args.only}'")

    print(f"template: {TEMPLATE.name}  ({len(tpl):,} chars)")
    print(f"output:   {outdir}\n")

    written, failed = [], 0
    for entry in cities:
        path = build_one(tpl, entry, outdir)
        if path:
            written.append(path)
            print(f"  ok   {path.name}")
        else:
            failed += 1

    print(f"\n{len(written)} written, {failed} skipped/failed")
    if written:
        print("\nRemember: verify the landmark and road in cities.json are")
        print("current and real. A closed venue in the intro dates the page.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
