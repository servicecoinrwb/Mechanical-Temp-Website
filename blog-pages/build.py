#!/usr/bin/env python3
"""
Build blog posts + blog.html from post-template.html, index-template.html,
and the markdown files in posts/.

Usage:
    python3 build.py                 # build everything into ../
    python3 build.py --out ./preview # build somewhere else first
    python3 build.py --only smart-thermostat-upgrade-benefits

Each post is a markdown file in posts/ with a frontmatter block:

    ---
    title: Repair or Replace? How to Know When Your Furnace is Dead Money
    subtitle: Stop paying for endless repairs.
    description: Meta description, 150-160 chars.
    category: HVAC Buying Guide
    date: 2026-01-08
    updated: 2026-01-08
    image: https://cdn.mechanicaltemp.com/photos/blog/whatever.jpg
    excerpt: One or two sentences for the blog index card.
    managed: true
    ---

    Body in markdown starts here.

managed: false  -> the post appears on blog.html but its .html file is NOT
regenerated. Use this for posts whose body hasn't been migrated yet.
The filename (minus .md) is the slug.
"""

import argparse
import html
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Missing dependency. Run: pip install markdown")

HERE = Path(__file__).parent
POST_TEMPLATE = HERE / "post-template.html"
INDEX_TEMPLATE = HERE / "index-template.html"
POSTS_DIR = HERE / "posts"

RELATED_COUNT = 3
HERO_IMAGE = "https://cdn.mechanicaltemp.com/photos/vehicles/van-rear-loaded.jpg"

REQUIRED = ("title", "description", "category", "date", "image", "excerpt")


# ---------------------------------------------------------------- parsing

def parse_post(path):
    """Split frontmatter from body. Returns dict or raises ValueError."""
    raw = path.read_text(encoding="utf-8")
    if not raw.lstrip().startswith("---"):
        raise ValueError("no frontmatter block (file must start with ---)")

    raw = raw.lstrip()
    parts = raw.split("---", 2)
    if len(parts) < 3:
        raise ValueError("frontmatter not closed with a second ---")

    meta = {}
    for line in parts[1].strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"bad frontmatter line: {line!r}")
        key, _, val = line.partition(":")
        val = val.strip()
        # allow quoted values so titles containing a colon stay valid YAML
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
            val = val[1:-1]
        meta[key.strip().lower()] = val

    meta["slug"] = path.stem
    meta["body_md"] = parts[2].strip()

    missing = [k for k in REQUIRED if not meta.get(k)]
    if missing:
        raise ValueError(f"missing frontmatter: {', '.join(missing)}")

    try:
        meta["date_obj"] = datetime.strptime(meta["date"], "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"date must be YYYY-MM-DD, got {meta['date']!r}")

    meta.setdefault("updated", meta["date"])
    meta.setdefault("subtitle", meta["excerpt"])
    meta["managed"] = meta.get("managed", "true").strip().lower() != "false"

    return meta


def human_date(d):
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def esc(s):
    return html.escape(s, quote=True)


def jstr(s):
    """JSON string literal — safe inside both JSON-LD and JS."""
    return json.dumps(s, ensure_ascii=False)


# ---------------------------------------------------------------- rendering

def render_body(meta):
    md = markdown.Markdown(extensions=["extra", "sane_lists", "smarty"])
    inner = md.convert(meta["body_md"])
    return "\n".join("                    " + ln for ln in inner.splitlines())


def pick_related(post, posts, count=RELATED_COUNT):
    others = [p for p in posts if p["slug"] != post["slug"]]
    same = [p for p in others if p["category"].lower() == post["category"].lower()]
    rest = [p for p in others if p not in same]
    same.sort(key=lambda p: p["date_obj"], reverse=True)
    rest.sort(key=lambda p: p["date_obj"], reverse=True)
    return (same + rest)[:count]


def related_html(post, posts):
    cards = []
    for p in pick_related(post, posts):
        cards.append(f'''                    <div class="bg-white rounded-lg shadow-sm overflow-hidden flex flex-col group border border-slate-200">
                        <a href="{p['slug']}.html" class="block">
                            <img src="{esc(p['image'])}" alt="{esc(p['title'])}" loading="lazy" class="w-full h-40 object-cover group-hover:opacity-90 transition-opacity">
                        </a>
                        <div class="p-5 flex flex-col flex-grow">
                            <p class="text-xs text-slate-500 mb-1 uppercase tracking-wide">{esc(p['category'])}</p>
                            <h3 class="font-bold mb-2 leading-snug"><a href="{p['slug']}.html" class="hover:text-sky-600">{esc(p['title'])}</a></h3>
                            <a href="{p['slug']}.html" class="text-sky-600 text-sm font-bold hover:underline mt-auto">Read article &rarr;</a>
                        </div>
                    </div>''')
    return "\n".join(cards)


def render_post(tpl, meta, posts):
    out = tpl
    subs = {
        "{{TITLE}}": esc(meta["title"]),
        "{{TITLE_JSON}}": jstr(meta["title"]),
        "{{SUBTITLE}}": esc(meta["subtitle"]),
        "{{DESCRIPTION}}": esc(meta["description"]),
        "{{DESCRIPTION_JSON}}": jstr(meta["description"]),
        "{{CATEGORY}}": esc(meta["category"]),
        "{{CATEGORY_JSON}}": jstr(meta["category"]),
        "{{SLUG}}": meta["slug"],
        "{{IMAGE}}": esc(meta["image"]),
        "{{DATE_ISO}}": meta["date"],
        "{{UPDATED_ISO}}": meta["updated"],
        "{{DATE_HUMAN}}": human_date(meta["date_obj"]),
        "{{BODY}}": render_body(meta),
        "{{RELATED}}": related_html(meta, posts),
    }
    for k, v in subs.items():
        out = out.replace(k, v)
    return out


def index_cards(posts):
    cards = []
    for i, p in enumerate(posts):
        badge = ('\n                            <span class="absolute top-4 right-4 bg-sky-600 text-white '
                 'text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">New</span>') if i == 0 else ""
        border = " border-2 border-sky-100" if i == 0 else ""
        cards.append(f'''                    <div class="bg-slate-50 rounded-lg shadow-md overflow-hidden flex flex-col group{border}">
                        <a href="{p['slug']}.html" class="block relative">{badge}
                            <img src="{esc(p['image'])}" alt="{esc(p['title'])}" loading="lazy" class="w-full h-56 object-cover group-hover:opacity-90 transition-opacity">
                        </a>
                        <div class="p-6 flex flex-col flex-grow">
                            <p class="text-sm text-slate-500 mb-2">{human_date(p['date_obj'])} &bull; {esc(p['category'])}</p>
                            <h2 class="text-2xl font-bold mb-3">
                                <a href="{p['slug']}.html" class="hover:text-sky-600 transition-colors">{esc(p['title'])}</a>
                            </h2>
                            <p class="text-slate-600 mb-6 flex-grow">{esc(p['excerpt'])}</p>
                            <a href="{p['slug']}.html" class="text-sky-600 font-bold hover:underline self-start">Read Full Article &rarr;</a>
                        </div>
                    </div>''')
    return "\n\n".join(cards)


def index_schema(posts):
    items = []
    for p in posts:
        items.append("        " + json.dumps({
            "@type": "BlogPosting",
            "headline": p["title"],
            "url": f"https://mechanicaltemp.com/{p['slug']}.html",
            "datePublished": p["date"],
            "image": p["image"],
        }, ensure_ascii=False))
    return ",\n".join(items)


def index_post_list(posts):
    return "\\n".join(
        f"- {p['slug']}.html — \\\"{p['title']}\\\" ({p['category']})" for p in posts
    )


def render_index(tpl, posts):
    out = tpl
    out = out.replace("{{CARDS}}", index_cards(posts))
    out = out.replace("{{POST_SCHEMA}}", index_schema(posts))
    out = out.replace("{{POST_LIST}}", index_post_list(posts))
    out = out.replace("{{HERO_IMAGE}}", HERO_IMAGE)
    return out


# ---------------------------------------------------------------- checks

def check(html_text, label, expect_slug=None):
    stray = re.findall(r"\{\{[A-Z_]+\}\}", html_text)
    if stray:
        print(f"  FAIL {label}: unreplaced tokens {sorted(set(stray))}")
        return False

    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                        html_text, re.DOTALL)
    if len(blocks) != 1:
        print(f"  FAIL {label}: expected 1 JSON-LD block, found {len(blocks)}")
        return False
    try:
        ld = json.loads(blocks[0])
    except json.JSONDecodeError as e:
        print(f"  FAIL {label}: JSON-LD did not parse — {e}")
        return False

    if expect_slug:
        want = f"https://mechanicaltemp.com/{expect_slug}.html"
        got = ld.get("mainEntityOfPage", {}).get("@id")
        if got != want:
            print(f"  FAIL {label}: schema @id is {got}, expected {want}")
            return False
    return True


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="..", help="output directory (default: parent)")
    ap.add_argument("--only", help="build a single post by slug")
    args = ap.parse_args()

    for f in (POST_TEMPLATE, INDEX_TEMPLATE):
        if not f.exists():
            sys.exit(f"missing {f}")
    if not POSTS_DIR.is_dir():
        sys.exit(f"missing {POSTS_DIR}")

    outdir = (HERE / args.out).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    posts, bad = [], 0
    for path in sorted(POSTS_DIR.glob("*.md")):
        try:
            posts.append(parse_post(path))
        except ValueError as e:
            print(f"  FAIL {path.name}: {e}")
            bad += 1

    if not posts:
        sys.exit("no valid posts found")

    posts.sort(key=lambda p: p["date_obj"], reverse=True)

    slugs = [p["slug"] for p in posts]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        sys.exit(f"duplicate slugs: {sorted(dupes)}")

    print(f"output: {outdir}")
    print(f"posts:  {len(posts)} found\n")

    post_tpl = POST_TEMPLATE.read_text(encoding="utf-8")
    targets = [p for p in posts if not args.only or p["slug"] == args.only]
    if args.only and not targets:
        sys.exit(f"no post with slug '{args.only}'")

    written = 0
    for p in targets:
        if not p["managed"]:
            print(f"  keep {p['slug']}.html (managed: false — listed but not rebuilt)")
            continue
        rendered = render_post(post_tpl, p, posts)
        if not check(rendered, p["slug"], expect_slug=p["slug"]):
            bad += 1
            continue
        (outdir / f"{p['slug']}.html").write_text(rendered, encoding="utf-8")
        print(f"  ok   {p['slug']}.html")
        written += 1

    if not args.only:
        idx = render_index(INDEX_TEMPLATE.read_text(encoding="utf-8"), posts)
        if check(idx, "blog.html"):
            (outdir / "blog.html").write_text(idx, encoding="utf-8")
            print(f"  ok   blog.html ({len(posts)} cards)")
            written += 1
        else:
            bad += 1

    print(f"\n{written} written, {bad} failed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
