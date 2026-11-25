#!/usr/bin/env python3
"""Render the brand kit: PNG exports of every logo, ready-to-use applications and a downloadable zip.

usage: python3 src/brand/render.py          (needs playwright + chromium; set CHROME=/path/to/chrome if needed)
outputs: brand/logos/png/*.png · brand/applications/*.png · brand/ruben-svanerud-brand-kit.zip
"""
import glob, os, re, zipfile
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
LOGOS = os.path.join(ROOT, 'brand', 'logos')
APPS = os.path.join(ROOT, 'brand', 'applications')
os.makedirs(os.path.join(LOGOS, 'png'), exist_ok=True)
os.makedirs(APPS, exist_ok=True)

C = {'forest': '#12392a', 'pine': '#1f6b47', 'leaf': '#9fcb6b', 'sage': '#c6dcc0', 'cream': '#f2ebdd',
     'ink': '#0e1a14', 'signal': '#e5432d'}
FONT = 'file://' + os.path.join(ROOT, 'assets', 'fonts', 'figtree-latin-wght-normal.woff2')
MONO = 'file://' + os.path.join(ROOT, 'assets', 'fonts', 'dm-mono-latin-400-normal.woff2')
IMG = lambda name, w: 'file://' + os.path.join(ROOT, 'assets', 'img', f'{name}-{w}.webp')


def inline(name, color):
    raw = open(os.path.join(ROOT, 'assets', 'logo', name + '.svg')).read()
    raw = re.sub(r'<title>.*?</title>', '', raw)
    raw = re.sub(r'\s(width|height)="[^"]*"', '', raw, count=2)
    return f'<span style="color:{color};display:block">{raw}</span>'


def shape(n, color):
    raw = open(os.path.join(ROOT, 'assets', 'shapes', f'shape-{n}.svg')).read()
    return f'<span style="color:{color};display:block">{raw}</span>'


BASE_CSS = f"""
@font-face {{ font-family: Figtree; src: url({FONT}) format('woff2'); font-weight: 300 900; }}
@font-face {{ font-family: 'DM Mono'; src: url({MONO}) format('woff2'); }}
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ background: transparent; }}
body {{ font-family: Figtree, sans-serif; -webkit-font-smoothing: antialiased; }}
svg {{ display: block; width: 100%; height: auto; }}
.mono {{ font-family: 'DM Mono', monospace; }}
"""

APPLICATIONS = {
    # name: (width, height, transparent, html body)
    'instagram-avatar': (1080, 1080, False, f"""
      <div style="width:1080px;height:1080px;background:{C['forest']};display:grid;place-items:center;border-radius:0">
        <div style="width:640px">{inline('symbol', C['cream'])}</div></div>"""),
    'youtube-banner': (2560, 1440, False, f"""
      <div style="position:relative;width:2560px;height:1440px;background:{C['forest']};overflow:hidden">
        <div style="position:absolute;width:1500px;right:-260px;top:-380px">{shape(1, C['pine'])}</div>
        <div style="position:absolute;width:900px;left:-200px;bottom:-420px">{shape(3, '#0d2b1f')}</div>
        <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:1400px;display:grid;gap:34px;justify-items:center">
          <div style="width:1100px">{inline('lockup', C['cream'])}</div>
          <p class="mono" style="color:{C['sage']};font-size:40px;letter-spacing:.02em">Film &amp; photo · Uppsala / Stockholm</p>
        </div></div>"""),
    'video-end-card': (1920, 1080, False, f"""
      <div style="position:relative;width:1920px;height:1080px;overflow:hidden;background:#557f96">
        <img src="{IMG('ski-gondola', 2072)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
        <div style="position:absolute;inset:0;background:linear-gradient(to top, rgba(10,28,20,.7), rgba(10,28,20,0) 55%)"></div>
        <div style="position:absolute;left:{0.5*1920 - 150}px;top:{0.3*1080 - 150}px;width:300px">{inline('symbol', C['cream'])}</div>
        <div style="position:absolute;left:96px;right:96px;bottom:84px;display:flex;justify-content:space-between;align-items:end">
          <div style="width:700px">{inline('handle', C['cream'])}</div>
          <p style="color:{C['cream']};font-size:38px;font-weight:600;text-align:right;line-height:1.35">Instagram &amp; TikTok @rubens.cut<br>YouTube @RubensCut</p>
        </div></div>"""),
    'lower-third': (1920, 1080, True, f"""
      <div style="position:relative;width:1920px;height:1080px">
        <div style="position:absolute;left:96px;bottom:110px;display:flex;align-items:center;gap:26px;background:{C['cream']};border-radius:999px;padding:22px 44px 22px 26px">
          <div style="width:84px;height:84px;border-radius:50%;background:{C['forest']};display:grid;place-items:center"><div style="width:58px">{inline('symbol', C['cream'])}</div></div>
          <div><p style="font-size:48px;font-weight:700;letter-spacing:-.03em;color:{C['forest']};line-height:1.05">Ruben Svanerud</p>
          <p class="mono" style="font-size:26px;color:{C['pine']};margin-top:6px">Film &amp; photo · rubens.cut</p></div>
        </div></div>"""),
    'lower-third-preview': (1920, 1080, False, f"""
      <div style="position:relative;width:1920px;height:1080px;overflow:hidden">
        <img src="{IMG('pop-station', 1456)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
        <div style="position:absolute;left:96px;bottom:110px;display:flex;align-items:center;gap:26px;background:{C['cream']};border-radius:999px;padding:22px 44px 22px 26px">
          <div style="width:84px;height:84px;border-radius:50%;background:{C['forest']};display:grid;place-items:center"><div style="width:58px">{inline('symbol', C['cream'])}</div></div>
          <div><p style="font-size:48px;font-weight:700;letter-spacing:-.03em;color:{C['forest']};line-height:1.05">Ruben Svanerud</p>
          <p class="mono" style="font-size:26px;color:{C['pine']};margin-top:6px">Film &amp; photo · rubens.cut</p></div>
        </div></div>"""),
    'watermark-preview': (1080, 1080, False, f"""
      <div style="position:relative;width:1080px;height:1080px;overflow:hidden">
        <img src="{IMG('dive-wreck', 2072)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
        <div style="position:absolute;right:56px;bottom:48px;width:130px;opacity:.85">{inline('symbol', C['cream'])}</div>
      </div>"""),
    'watermark': (600, 600, True, f"""
      <div style="width:600px;height:600px;display:grid;place-items:center"><div style="width:360px;opacity:.85">{inline('symbol', C['cream'])}</div></div>"""),
    'business-card-front': (1050, 600, False, f"""
      <div style="position:relative;width:1050px;height:600px;background:{C['forest']};overflow:hidden;border-radius:28px">
        <div style="position:absolute;width:640px;right:-170px;top:-190px">{shape(4, C['pine'])}</div>
        <div style="position:absolute;left:62px;top:56px;width:130px">{inline('symbol', C['cream'])}</div>
        <div style="position:absolute;left:70px;bottom:62px;width:560px">{inline('wordmark-stacked', C['cream'])}</div>
      </div>"""),
    'business-card-back': (1050, 600, False, f"""
      <div style="position:relative;width:1050px;height:600px;background:{C['cream']};overflow:hidden;border-radius:28px;color:{C['forest']}">
        <div style="position:absolute;width:520px;right:-150px;bottom:-200px">{shape(2, C['sage'])}</div>
        <div style="position:absolute;left:70px;top:66px;display:grid;gap:10px">
          <p style="font-size:44px;font-weight:700;letter-spacing:-.03em">Ruben Svanerud</p>
          <p class="mono" style="font-size:24px;color:{C['pine']}">Film &amp; photo · Uppsala / Stockholm</p></div>
        <div style="position:absolute;left:70px;bottom:62px;display:grid;gap:8px;font-size:30px;font-weight:600">
          <p>ruben.svanerud@gmail.com</p><p>@rubens.cut</p></div>
      </div>"""),
    'instagram-post': (1080, 1350, False, f"""
      <div style="position:relative;width:1080px;height:1350px;overflow:hidden;background:{C['forest']}">
        <img src="{IMG('dive-reef', 2072)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:52% 50%">
        <div style="position:absolute;inset:0;background:linear-gradient(to top, rgba(10,28,20,.6), rgba(10,28,20,0) 45%)"></div>
        <div style="position:absolute;left:50%;top:26%;transform:translate(-50%,-50%);width:280px">{inline('symbol', C['cream'])}</div>
        <div style="position:absolute;left:64px;right:64px;bottom:64px;display:flex;justify-content:space-between;align-items:end">
          <p style="color:{C['cream']};font-size:64px;font-weight:700;letter-spacing:-.04em;line-height:1">A Different<br>Planet</p>
          <div style="width:330px">{inline('handle', C['cream'])}</div>
        </div></div>"""),
}


def page_html(body, bg='transparent'):
    return f'<!doctype html><html><head><style>{BASE_CSS} body{{background:{bg}}}</style></head><body>{body}</body></html>'


TMP = '/tmp/_rs_brand_render.html'

if __name__ == '__main__':
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=os.environ.get('CHROME') or None, args=['--no-sandbox'])
        pg = br.new_page(device_scale_factor=1)
        # logo PNGs (transparent), long side 2000 px
        for f in sorted(glob.glob(os.path.join(LOGOS, '*.svg'))):
            svg = open(f).read()
            m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
            w, h = float(m.group(1)), float(m.group(2))
            scale = 2000 / max(w, h)
            W, H = round(w * scale), round(h * scale)
            svg2 = re.sub(r'\swidth="[^"]*"\sheight="[^"]*"', f' width="{W}" height="{H}"', svg, count=1)
            pg.set_viewport_size({'width': W, 'height': H})
            open(TMP, 'w').write(page_html(svg2))
            pg.goto('file://' + TMP)
            pg.screenshot(path=os.path.join(LOGOS, 'png', os.path.basename(f)[:-4] + '.png'), omit_background=True)
        # applications
        for name, (w, h, transparent, body) in APPLICATIONS.items():
            pg.set_viewport_size({'width': w, 'height': h})
            open(TMP, 'w').write(page_html(body))
            pg.goto('file://' + TMP, wait_until='load')
            pg.evaluate('document.fonts.ready')
            pg.wait_for_timeout(200)
            pg.screenshot(path=os.path.join(APPS, name + '.png'), omit_background=transparent)
        br.close()
    # zip
    zpath = os.path.join(ROOT, 'brand', 'ruben-svanerud-brand-kit.zip')
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(glob.glob(os.path.join(LOGOS, '*.svg')) + glob.glob(os.path.join(LOGOS, 'png', '*.png'))
                        + glob.glob(os.path.join(APPS, '*.png'))):
            z.write(f, os.path.join('ruben-svanerud-brand-kit', os.path.relpath(f, os.path.join(ROOT, 'brand'))))
        for f in glob.glob(os.path.join(ROOT, 'assets', 'shapes', '*.svg')):
            z.write(f, os.path.join('ruben-svanerud-brand-kit', 'shapes', os.path.basename(f)))
        z.writestr('ruben-svanerud-brand-kit/README.txt', open(os.path.join(HERE, 'KIT_README.txt')).read())
    print('logos:', len(glob.glob(os.path.join(LOGOS, 'png', '*.png'))), 'applications:', len(APPLICATIONS), 'zip:', os.path.getsize(zpath) // 1024, 'KB')
