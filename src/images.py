#!/usr/bin/env python3
"""Turn the raw captures in src/raw/ into WebP files at several widths in assets/img/,
and write src/images.json (sizes + placeholder colour) for the templates.

Run:  python3 src/images.py      then  python3 src/build.py

Each entry: output name -> (raw file, crop box or None)
"""
import json, os
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw')
OUT = os.path.join(os.path.dirname(HERE), 'assets', 'img')
os.makedirs(OUT, exist_ok=True)

IMAGES = {
    # For the Love of Ski
    'ski-gondola':   ('ski-148.jpg', None),
    'ski-gondola-tall': ('ski-gondola-portrait.jpg', None),
    'ski-powder':    ('ski-113.jpg', (0, 0, 1000, 1166)),
    'ski-goggles':   ('ski-004.jpg', None),
    'ski-trees':     ('ski-070.jpg', None),
    'ski-air':       ('ski-123.jpg', None),
    'ski-spin':      ('ski-190.jpg', None),
    'ski-poster':    ('ski-poster.jpg', None),
    # Betting Everything on Popcorn
    'pop-street':    ('pop-300.jpg', None),
    'pop-milan':     ('pop-370.jpg', None),
    'pop-statue':    ('pop-354.jpg', None),
    'pop-night':     ('pop-390.jpg', None),
    'pop-orange':    ('pop-048.jpg', None),
    'pop-station':   ('pop-606.jpg', None),
    'pop-bts-street':('milan-street.jpg', None),
    'pop-bts-room':  ('milan-bts.jpg', None),
    # A Different Planet
    'dive-reef':     ('dive-0.jpg', None),
    'dive-torch':    ('dive-2.jpg', None),
    'dive-wreck':    ('dive-9.jpg', None),
    'dive-coral':    ('dive-6.jpg', None),
    'dive-surface':  ('dive-3.jpg', None),
    'dive-turtle':   ('turtle.jpg', None),
    # Erwa
    'box-win':       ('box-win.jpg', None),
    'box-rig':       ('box-bts.jpg', None),
    'box-rig-crop':  ('box-bts.jpg', (0, 600, 820, 1456)),
    # Kebnekaise
    'keb-climb':     ('keb-photo.jpg', None),
    'keb-hike':      ('keb-hike.jpg', None),
}

WIDTHS = [480, 800, 1200, 1600, 2000]
manifest = {}
for name, (src, box) in IMAGES.items():
    im = Image.open(os.path.join(RAW, src)).convert('RGB')
    if box:
        im = im.crop(box)
    w, h = im.size
    sizes = [x for x in WIDTHS if x < w] + [w]
    out = []
    for tw in sizes:
        th = round(h * tw / w)
        r = im if tw == w else im.resize((tw, th), Image.LANCZOS)
        if tw != w:
            r = r.filter(ImageFilter.UnsharpMask(radius=0.6, percent=40, threshold=2))
        fn = f'{name}-{tw}.webp'
        r.save(os.path.join(OUT, fn), 'WEBP', quality=82, method=6)
        out.append(tw)
    # tiny blurred placeholder colour (average) for background while loading
    avg = im.resize((1, 1), Image.BOX).getpixel((0, 0))
    manifest[name] = {'w': w, 'h': h, 'sizes': out, 'bg': '#%02x%02x%02x' % avg}
    print(f'{name:16s} {w}x{h} -> {out}')

with open(os.path.join(HERE, 'images.json'), 'w') as f:
    json.dump(manifest, f, indent=1)
