#!/usr/bin/env python3
"""Full-page screenshots of every page at 390 / 768 / 1440 (needs Playwright + Chrome).
Serve the repo first:  python3 -m http.server 8123
usage: python3 tools/screenshots.py OUTDIR [w=390,1440] [page ...]   (pages default to all)
Also reports horizontal overflow and small tap targets per page/width.
"""
import sys, os, json
from playwright.sync_api import sync_playwright

import os as _os
BASE = _os.environ.get('BASE', 'http://localhost:8123/')
PAGES = ['index.html', 'about.html', 'projects.html', 'stills.html',
         'projects/for-the-love-of-ski.html', 'projects/betting-everything-on-popcorn.html',
         'projects/a-different-planet.html', 'projects/kebnekaise.html', 'projects/em26-is-next.html']
WIDTHS = [390, 768, 1440]
out = sys.argv[1]
pages = sys.argv[2:] or PAGES
widths = WIDTHS
if pages and pages[0].startswith('w='):
    widths = [int(x) for x in pages[0][2:].split(',')]
    pages = pages[1:] or PAGES
os.makedirs(out, exist_ok=True)

CHECK = r"""
() => {
  const vw = document.documentElement.clientWidth;
  const over = [...document.querySelectorAll('body *')].filter(e => {
    const r = e.getBoundingClientRect();
    if (!r.width) return false;
    const st = getComputedStyle(e);
    if (e.closest('.short__list') && e !== document.querySelector('.short__list')) return false;
    if (e.closest('.menu')) return false;
    return r.right > vw + 1 || r.left < -1;
  }).slice(0, 6).map(e => e.tagName + '.' + [...e.classList].join('.') + ' ' + Math.round(e.getBoundingClientRect().right));
  const small = [...document.querySelectorAll('a, button')].filter(e => {
    if (e.closest('.menu') || e.classList.contains('skip')) return false;
    const r = e.getBoundingClientRect();
    return r.width > 0 && (r.height < 24);
  }).slice(0, 8).map(e => (e.textContent || '').trim().slice(0, 30) + ' ' + Math.round(e.getBoundingClientRect().height));
  return {scrollW: document.documentElement.scrollWidth, vw, over, small};
}
"""

with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=_os.environ.get('CHROME') or None, args=['--no-sandbox', '--hide-scrollbars'])
    for w in widths:
        ctx = br.new_context(viewport={'width': w, 'height': 900 if w > 500 else 844}, device_scale_factor=1,
                             reduced_motion='reduce')
        pg = ctx.new_page()
        for path in pages:
            pg.goto(BASE + path, wait_until='load')
            pg.evaluate("""async () => {
                document.querySelectorAll('img[loading=lazy]').forEach(i => { i.loading = 'eager'; });
                const H = document.documentElement.scrollHeight;
                for (let y = 0; y < H; y += innerHeight * 0.8) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); }
                window.scrollTo(0, 0);
                const wait = Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
                await Promise.race([wait, new Promise(r => setTimeout(r, 8000))]);
                await document.fonts.ready;
            }""")
            pg.wait_for_timeout(250)
            res = pg.evaluate(CHECK)
            name = path.replace('projects/', 'p-').replace('.html', '') + f'-{w}.png'
            pg.screenshot(path=os.path.join(out, name), full_page=True)
            flag = '' if res['scrollW'] <= res['vw'] and not res['over'] else '  OVERFLOW ' + json.dumps(res['over'])
            sm = ('  SMALL ' + json.dumps(res['small'])) if res['small'] else ''
            print(f'{name:42s} scrollW={res["scrollW"]}{flag}{sm}')
        ctx.close()
    br.close()
