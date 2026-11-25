# Ruben Svanerud – portfolio

A static portfolio site for Ruben Svanerud (filmmaker and photographer, Uppsala/Stockholm). It is built by Elevate Studio.
The site is plain HTML, CSS and JS with no framework and no runtime dependencies. The site is served from the repository root.

## Structure
- `index.html`, `about.html`, `projects.html`, `projects/*.html` – **generated**, do not edit by hand
- `src/site_data.py` – all content: person, projects, image alt texts, short-form reels
- `src/templates/*.html` – Jinja2 templates (`base.html` holds nav, menu, footer and the video dialog)
- `assets/css/tokens.css` – every colour, type size, space and timing; `assets/css/site.css` uses only these
- `assets/js/site.js` – nav state, full-screen menu, one reveal pattern, YouTube facade and dialog
- `src/images.py` – turns `src/raw/*.jpg` into WebP sets in `assets/img/` and writes `src/images.json`
- `tools/screenshots.py` – full-page screenshots at 390 / 768 / 1440 and an overflow check

## Commands
```bash
pip install jinja2 pillow            # build needs only these
python3 src/images.py                # after adding or changing images in src/raw/
python3 src/build.py                 # regenerate all HTML, robots.txt, llms.txt (and sitemap.xml when SITE_URL is set)
python3 -m http.server 8123          # preview at http://localhost:8123
python3 tools/screenshots.py /tmp/shots   # optional, needs playwright + chromium
```

## Rules
- **Nothing invented.** Every fact, title, year, runtime, client and link comes from Ruben's public profiles
  (Instagram/TikTok @rubens.cut, YouTube @RubensCut) or the films themselves. If something is missing, leave it out.
  Never add testimonials, prices, client logos or numbers that are not confirmed.
- **Only Ruben's own material.** No stock photos and no AI images. New images go in `src/raw/` and are registered in `IMAGES` in
  `src/images.py`, with an alt text in `ALT` in `src/site_data.py`.
- **Design system.** Dark ink `#0d0d0e` with paper `#f2f1ed`, Archivo (wide, 700–800) for display, Instrument Sans for text,
  IBM Plex Mono for small labels. Corner radius is 0. The one accent `#ff5533` is used only on clickable things (the play dot).
  Do not hard-code values in components; add a token instead.
- **Motion.** One entrance pattern (`data-reveal`, 560 ms, once). No parallax on text and no scroll-jacking.
  `prefers-reduced-motion` must give a complete static page.
- **Mobile first.** Check 390, 768 and 1440 after every visual change: no horizontal scroll, tap targets ≥ 44 px, and no
  single word alone on the last line of a heading (`|keep` filter in templates).
- **Video.** YouTube loads only on click (youtube-nocookie). Keep the "Open on YouTube" fallback.
- Copy is in English unless Ruben asks otherwise: short and concrete, with no exclamation marks and no emoji.

## Before launch
- Set `SITE_URL` in `src/site_data.py` and rebuild (adds canonical, OG image, sitemap).
- Ruben confirms the use of the material and replaces the web-resolution frame grabs with original files.
