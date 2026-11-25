# Ruben Svanerud – portfolio

A static portfolio site for Ruben Svanerud (filmmaker and photographer, Uppsala/Stockholm). It is built by Elevate Studio.
The site is plain HTML, CSS and JS with no framework and no runtime dependencies. The site is served from the repository root.

## Structure
- `index.html`, `about.html`, `projects.html`, `stills.html`, `projects/*.html`, `brand/index.html` – **generated**, do not edit by hand
- `src/site_data.py` – all content: person, projects, image alt texts, short-form reels
- `src/templates/*.html` – Jinja2 templates (`base.html` holds nav, menu, footer and the video dialog)
- `assets/css/tokens.css` – every colour, type size, space and timing; `assets/css/site.css` uses only these
- `assets/js/site.js` – nav state, full-screen menu, one reveal pattern, YouTube facade and dialog
- `src/images.py` – turns `src/raw/*.jpg` into WebP sets in `assets/img/` and writes `src/images.json`
- `src/brand/logos.py` – the logo suite as SVG (Figtree outlines via HarfBuzz; the rune is painted strokes built with shapely) → `brand/logos/` and currentColor copies in `assets/logo/` that the templates inline
- `src/brand/shapes.py` – the four organic shapes → `assets/shapes/`
- `src/brand/render.py` – PNG exports, templates (avatar, YouTube banner, end card, lower third, watermark, business card, IG post) and `brand/ruben-svanerud-brand-kit.zip`
- `assets/css/brand.css` – styles for the brand kit page only
- `tools/screenshots.py` – full-page screenshots at 390 / 768 / 1440 and an overflow check

## Commands
```bash
pip install jinja2 pillow            # build needs only these
python3 src/images.py                # after adding or changing images in src/raw/
python3 src/build.py                 # regenerate all HTML, robots.txt, llms.txt (and sitemap.xml when SITE_URL is set)
python3 -m http.server 8123          # preview at http://localhost:8123
python3 tools/screenshots.py /tmp/shots   # optional, needs playwright + chromium (BASE=…, CHROME=… env vars)
pip install uharfbuzz fonttools shapely   # only to regenerate logos
python3 src/brand/logos.py && python3 src/brand/shapes.py && python3 src/brand/render.py   # brand kit
```

## Rules
- **Nothing invented.** Every fact, title, year, runtime, client and link comes from Ruben's public profiles
  (Instagram/TikTok @rubens.cut, YouTube @RubensCut) or the films themselves. If something is missing, leave it out.
  Never add testimonials, prices, client logos or numbers that are not confirmed.
- **Only Ruben's own material.** No stock photos and no AI images. New images go in `src/raw/` and are registered in `IMAGES` in
  `src/images.py`, with an alt text in `ALT` in `src/site_data.py`.
- **Design system.** Forest `#12392a`, pine `#1f6b47`, leaf `#9fcb6b`, sage `#c6dcc0`, cream `#f2ebdd` (page), ink `#0e1a14`.
  Signal `#e5432d` (from the red jacket and gondola in his films) only on clickable things – the play dot.
  Figtree for everything (headings 700, tracking −3.5 %, **sentence case, never all caps**), DM Mono only for small labels.
  Rounded corners (`--r-lg`/`--r-xl`), pill buttons and chips, colour-block sections, organic shapes used big and tone on tone.
  The client likes image-heavy layouts, bento grids, scroll rows, colour blocks and overlapping cards; avoid purely
  typographic sections, tables, text lists, centred minimal sections and split image/text heroes.
  Do not hard-code values in components; add a token instead.
- **Logo.** The symbol is a painted rune that hides a camera on a tripod seen from the front: ring + dot = lens,
  top stroke = viewfinder, arms = rig handles, three legs = tripod. It should look wild at first and only make
  sense once explained (brand page section "The idea", linked from the home hero chip). Put it on calm parts of photos
  (`HERO.focus` in `src/site_data.py`), never over faces. The "cut" lives in the type (the R and rubens.cut).
  Never redraw the logo by hand – change `src/brand/logos.py` and regenerate.
- **Motion.** One entrance pattern (`data-reveal`, 560 ms, once). No parallax on text and no scroll-jacking.
  `prefers-reduced-motion` must give a complete static page.
- **Mobile first.** Check 390, 768 and 1440 after every visual change: no horizontal scroll, tap targets ≥ 44 px, and no
  single word alone on the last line of a heading (`|keep` filter in templates).
- **Video.** YouTube loads only on click (youtube-nocookie). Keep the "Open on YouTube" fallback.
- Copy is in English unless Ruben asks otherwise: short and concrete, with no exclamation marks and no emoji.

## Before launch
- Set `PREVIEW = False` in `src/site_data.py` (removes noindex and the robots.txt block).
- Set `SITE_URL` in `src/site_data.py` and rebuild (adds canonical, OG image, sitemap).
- Ruben confirms the use of the material and replaces the web-resolution frame grabs with original files.
