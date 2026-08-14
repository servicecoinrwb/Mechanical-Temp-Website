# Blog generator

```
blog-pages/
  post-template.html    the shell every post uses
  index-template.html   the shell blog.html uses
  posts/*.md            one file per post — this is what you edit
  build.py
```

## Write a new post

Create `posts/my-new-post.md`. The filename is the URL slug, so
`my-new-post.md` becomes `mechanicaltemp.com/my-new-post.html`.

```markdown
---
title: Why Your AC Freezes Up in July
subtitle: One line under the headline in the hero.
description: Meta description for Google. Aim for 150-160 characters.
category: AC Maintenance
date: 2026-07-14
image: https://cdn.mechanicaltemp.com/photos/blog/frozen-coil.jpg
excerpt: Shows on the blog index card. One or two sentences.
managed: true
---

Body starts here in markdown.

## A heading

A paragraph with **bold** and a [link](index.html).

![alt text](https://cdn.mechanicaltemp.com/photos/blog/whatever.jpg)
```

Commit it. The Action rebuilds the post, blog.html, and the related-post
strips on every other article.

Optional fields: `updated` (defaults to `date`), `subtitle` (defaults to
`excerpt`), `managed` (defaults to true).

## The 8 posts marked `managed: false`

Those articles are live and working, but their bodies were never migrated
into markdown. The stub files exist so blog.html can list them.

`managed: false` means: **list this post on blog.html, but don't touch its
.html file.** The live page stays exactly as it is.

To migrate one:

1. Open the live `.html`, copy the article body out of `<div class="blog-content">`
2. Paste it into the `.md` as markdown (or as raw HTML — markdown passes it through)
3. Change `managed: false` to `managed: true`
4. Commit

Now that post gets the new template: proper schema, related posts, the
corrected hours, everything.

No rush. Migrate one at a time or never — blog.html works either way.

## Change something on every post

Edit `post-template.html` and commit. Every `managed: true` post rebuilds.
Nav, footer, Tempi's prompt, the CTA box, the schema — one edit.

## What build.py checks

- frontmatter present and closed
- all required fields filled
- date parses as YYYY-MM-DD
- no duplicate slugs
- every token replaced (no `{{...}}` shipped)
- exactly one JSON-LD block, and it parses
- the schema `@id` matches the page's own URL

Anything that fails is skipped and printed. Non-zero exit if anything failed.

## What's different from the old hand-written posts

- **Shared publisher `@id`** pointing at the homepage business, so Google
  links every article to the same entity instead of nine anonymous ones
- **`articleSection`** from the category
- **Open Graph + Twitter card tags** — these were missing, which is why
  posts shared to Facebook looked plain
- **Related posts strip** — same category first, then most recent
- **Corrected hours** in the scheduler and Tempi (was 8am-4pm, now 8am-8pm)
- **Tempi's article list is generated**, so it can never go stale. The old
  blog.html had the list hardcoded in the prompt.

## Images

`smart-thermostat-upgrade-benefits` uses a CDN path with a space in it
(`hvac controls`). That's URL-encoded to `hvac%20controls` in the stub.
Renaming the folder to `hvac-controls` would be cleaner.

Two posts still point at Unsplash (humidifier, Thanksgiving) and they'll
keep working, but your own photos would serve you better.

`5-signs-furnace-repair-fall` was on imgur; the stub points it at a CDN
furnace photo instead. Swap it for something better when you have one.

## Known, not fixed

**Tailwind CDN.** Same as the city pages — `cdn.tailwindcss.com` instead of
your built stylesheet. Slower, logs a production warning. Left alone.
