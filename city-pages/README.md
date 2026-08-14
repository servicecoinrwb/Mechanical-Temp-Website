# City page generator

Three files. No more find/replace.

```
city-pages/
  template.html   the one page you edit
  cities.json     28 cities, 4 fields each
  build.py        writes {slug}.html for every city
```

## Build

```bash
cd city-pages
python3 build.py
```

Writes all 28 pages to the parent directory (repo root). Then commit and push.

```bash
python3 build.py --only detroit      # one city
python3 build.py --out ./preview     # somewhere else, to eyeball first
```

## Change something on every page

Edit `template.html`, run `build.py`. Done. Hours, phone, service list,
Tempi's prompt, the facts strip — one edit, 28 pages.

## Add a city

Add four fields to `cities.json`, rerun. Also add it to `areaServed` in
index.html and to the LOCATIONS list, and link it there (the homepage
currently lists unlinked cities as plain `<span>`).

## Tokens

Only these four get replaced:

| token | example |
|---|---|
| `{{CITY}}` | Royal Oak |
| `{{SLUG}}` | royal-oak |
| `{{LANDMARK}}` | the Detroit Zoo |
| `{{ROAD}}` | Woodward Avenue |

Everything else is identical on every page — including **Southfield**,
which appears six times (JSON-LD address, "why choose us", footer address,
Tempi's opening line, Tempi's address line, and the service-area list).
That's the bug the old find/replace caused: it rewrote the office city.
The generator can't do that because it only touches tokens.

## What build.py checks before writing

- every token got replaced (no stray `{{...}}` shipped)
- the JSON-LD block parses as valid JSON
- there is exactly one JSON-LD block
- its `@id` is the shared business id, not a per-page one
- `areaServed` matches the city being built
- no duplicate slugs in cities.json

Any failure skips that page and prints why. Exit code is non-zero if
anything failed, so it won't quietly half-build.

## Verify the landmarks

`cities.json` landmarks are best guesses and need your eyes. The old
Northville page referenced Northville Downs, which closed in 2024 — a
dead venue in the intro dates the whole page. Anything you're not sure
about, swap for "downtown [City]", which never goes stale.

## Known, not fixed

- **Tailwind CDN.** Pages load `cdn.tailwindcss.com`, which is slower than
  the built `tailwind.css` index.html uses and logs a production warning.
  Switching means making sure your build includes the classes these pages
  use. Left alone deliberately.
