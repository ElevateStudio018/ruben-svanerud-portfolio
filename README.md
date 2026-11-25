# Ruben Svanerud – portfolio

A portfolio site for **Ruben Svanerud**, a filmmaker and photographer in Uppsala and Stockholm.
It is static HTML/CSS/JS with no build step needed to host it: serve the repository root as it is.

**Pages:** Home · Projects · Stills · About · a brand kit at `/brand/` · one page each for *For the Love of Ski*, *EP.01 Betting Everything on Popcorn*,
*A Different Planet*, *Kebnekaise* and *EM26 Is Next*.

## Preview locally
```bash
python3 -m http.server 8123
# open http://localhost:8123
```

## Edit content
All text and links are in `src/site_data.py`, and the markup is in `src/templates/`. After a change:
```bash
pip install jinja2 pillow
python3 src/build.py
```
New images: put them in `src/raw/`, add them to `IMAGES` in `src/images.py` and to `ALT` in `src/site_data.py`, and run
`python3 src/images.py` before `src/build.py`. See `CLAUDE.md` for the full rules and design system.

## Brand kit
`brand/` holds the identity: logos (SVG + transparent PNG), the four organic shapes, templates (profile picture, YouTube banner,
video end card, lower third, watermark, business card, Instagram post) and `ruben-svanerud-brand-kit.zip`. The guide is
`brand/index.html`. Regenerate with `python3 src/brand/logos.py && python3 src/brand/shapes.py && python3 src/brand/render.py`.

## Hosting
Any static host works: GitHub Pages (from the root of `main`; `.nojekyll` is included), Netlify, Vercel, Cloudflare Pages or one.com.
Before launch, set `SITE_URL` in `src/site_data.py` and rebuild, so that canonical tags, Open Graph images and `sitemap.xml`
are added.

## Material and rights
All photos and stills are Ruben's own work, taken from his public Instagram (@rubens.cut) and YouTube (@RubensCut).
They are web-resolution frame grabs and should be replaced with original files. Confirm with Ruben, and with the people
seen in the films, before the site is made public.

## Tech
- Self-hosted fonts: Figtree and DM Mono (SIL OFL)
- WebP images with `srcset`, lazy loading, and a portrait hero crop for mobile
- YouTube loads only on click, so nothing is tracked before playback
- `prefers-reduced-motion` support, keyboard focus states, one `h1` per page, JSON-LD (`Person`, `CreativeWork`, `VideoObject`)
- `robots.txt` and `llms.txt`
