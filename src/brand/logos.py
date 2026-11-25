#!/usr/bin/env python3
"""Ruben Svanerud logo suite, generated as clean SVG.

- Type set in Figtree (OFL) via HarfBuzz shaping, converted to outlines (no font needed to display).
- The symbol ("the frame") is four hand-shaped corner strokes: a viewfinder that also reads as a
  four-leaf/snow-crystal mark. Built numerically so widths swell at the ends like a brush stroke.
- "rubens.cut" gets a literal cut: a thin diagonal slice through "cut", top half nudged right.

usage: python3 src/brand/logos.py        -> brand/logos/*.svg (+ currentColor copies in assets/logo/ for inline use)
"""
import math, os, sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'brand', 'logos')
INLINE = os.path.join(ROOT, 'assets', 'logo')
os.makedirs(OUT, exist_ok=True)

PALETTE = {
    'forest': '#12392a', 'pine': '#1f6b47', 'leaf': '#9fcb6b', 'sage': '#c6dcc0',
    'cream': '#f2ebdd', 'ink': '#0e1a14', 'signal': '#e5432d',
}

# ---------------------------------------------------------------- type → outlines
_fonts = {}
def font(weight):
    if weight not in _fonts:
        path = os.path.join(HERE, 'fonts', f'figtree-{weight}.ttf')
        blob = hb.Blob.from_file_path(path)
        face = hb.Face(blob)
        hbf = hb.Font(face)
        tt = TTFont(path)
        _fonts[weight] = (hbf, tt, tt['head'].unitsPerEm)
    return _fonts[weight]


def text_path(text, weight=700, size=100, tracking=0.0, x=0.0, y=0.0):
    """Return (svg path d, advance width) for text at baseline y, in px at `size`."""
    hbf, tt, upm = font(weight)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbf, buf, {'kern': True, 'liga': True})
    gs = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    scale = size / upm
    pen = SVGPathPen(gs)
    cx = 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        t = TransformPen(pen, (scale, 0, 0, -scale, x + (cx + pos.x_offset) * scale, y - pos.y_offset * scale))
        gs[name].draw(t)
        cx += pos.x_advance + tracking * upm
    width = (cx - tracking * upm) * scale
    return pen.getCommands(), width


def metrics(weight=700, size=100):
    _, tt, upm = font(weight)
    os2 = tt['OS/2']
    return {'cap': os2.sCapHeight * size / upm, 'x': os2.sxHeight * size / upm,
            'asc': tt['hhea'].ascent * size / upm, 'desc': -tt['hhea'].descent * size / upm}

# ---------------------------------------------------------------- the frame symbol
def _corner_outline(seed=0):
    """Top-left corner stroke as a closed polygon in a 0..100 box.
    Centerline: short vertical arm -> wide rounded bend -> short horizontal arm.
    Thin at the bend, swelling to soft round lobes at both ends (brush / petal feel)."""
    R, L = 14.0, 2.0                 # bend radius, straight arm length
    C = 22.0 + R                      # bend centre (C, C)
    def centre(t):
        A = math.pi / 2 * R
        total = L + A + L
        s = t * total
        if s < L:
            return (22.0, C + L - s), (0.0, -1.0)
        s -= L
        if s < A:
            a = math.pi + s / R
            return (C + R * math.cos(a), C + R * math.sin(a)), (-math.sin(a), math.cos(a))
        s -= A
        return (C + s, 22.0), (1.0, 0.0)
    def width(t):
        return 12.0 + 3.2 * (abs(2 * t - 1) ** 3) + 0.5 * math.sin(6 * t + seed) + 0.3 * math.sin(15 * t + 2 * seed)
    N = 120
    left, right = [], []
    for i in range(N + 1):
        t = i / N
        (px, py), (tx, ty) = centre(t)
        nx, ny = -ty, tx
        w = width(t)
        left.append((px + nx * w / 2, py + ny * w / 2))
        right.append((px - nx * w / 2, py - ny * w / 2))
    def cap(p_end, tangent, w, outward):
        cx_, cy_ = p_end
        tx, ty = tangent
        base = math.atan2(ty, tx) + (0 if outward else math.pi)
        return [(cx_ + w / 2 * math.cos(base + a), cy_ + w / 2 * math.sin(base + a))
                for a in [math.pi / 2 - k * math.pi / 16 for k in range(17)]]
    (p0, t0), (p1, t1) = centre(0), centre(1)
    poly = left + cap(p1, t1, width(1), True)[1:-1] + right[::-1] + cap(p0, t0, width(0), False)[1:-1]
    return poly


def _rot(p, deg, c=(50, 50)):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def symbol_path(x=0, y=0, size=100):
    s = size / 100.0
    d = []
    for k, deg in enumerate((0, 90, 180, 270)):
        poly = [_rot(p, deg) for p in _corner_outline(seed=k * 1.7)]
        d.append('M' + ' L'.join(f'{x + px * s:.2f} {y + py * s:.2f}' for px, py in poly) + ' Z')
    return ' '.join(d)

# ---------------------------------------------------------------- svg helpers
def svg(w, h, body, bg=None, title='Ruben Svanerud'):
    rect = f'<rect width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{rect}{body}</svg>\n')


def save(name, content):
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(content)

# ---------------------------------------------------------------- logos
def wordmark(color, bg=None, stacked=False):
    size = 100
    m = metrics(700, size)
    pad = 6
    if not stacked:
        d, w = text_path('Ruben Svanerud', 700, size, tracking=-0.035, x=pad, y=pad + m['asc'] * 0.80)
        H = pad * 2 + m['asc'] * 0.80 + m['desc'] * 0.55
        return svg(w + pad * 2, H, f'<path fill="{color}" d="{d}"/>', bg, 'Ruben Svanerud')
    lh = size * 0.92
    d1, w1 = text_path('Ruben', 700, size, tracking=-0.035, x=pad, y=pad + m['cap'] + 2)
    d2, w2 = text_path('Svanerud', 700, size, tracking=-0.035, x=pad, y=pad + m['cap'] + 2 + lh)
    W = max(w1, w2) + pad * 2
    H = pad * 2 + m['cap'] + 2 + lh + m['desc'] * 0.55
    return svg(W, H, f'<path fill="{color}" d="{d1} {d2}"/>', bg, 'Ruben Svanerud')


def handle(color, bg=None, dot=None):
    """rubens.cut with a diagonal cut through 'cut'."""
    size = 100
    m = metrics(700, size)
    pad = 6
    y = pad + m['asc'] * 0.78
    d1, w1 = text_path('rubens', 700, size, tracking=-0.03, x=pad, y=y)
    # dot as a circle so it can take the signal colour
    r = size * 0.072
    dot_cx = pad + w1 + size * 0.035 + r
    dot_cy = y - r
    xc = dot_cx + r + size * 0.035
    d3, w3 = text_path('cut', 700, size, tracking=-0.03, x=xc, y=y)
    W = xc + w3 + pad + 4
    H = pad * 2 + m['asc'] * 0.78 + m['desc'] * 0.35
    # the cut: a line from bottom-left to top-right across 'cut'
    x0, x1 = xc - 4, xc + w3 + 6
    yb, yt = y + 4, y - m['x'] - 6
    def side(a, b):  # polygon above/below the cut line
        return f'{a}'
    top = f'{x0 - 10},{-10} {x1 + 10},{-10} {x1 + 10},{yt + (yb - yt) * 0.05} {x0 - 10},{yb - (yb - yt) * 0.05}'
    bot = f'{x0 - 10},{yb + 0.3 * (yb-yt)} {x1 + 10},{yt + 0.3*(yb-yt)} {x1 + 10},{H + 10} {x0 - 10},{H + 10}'
    # cut line through the middle: from (x0, y-0.15x) to (x1, y-0.85x)
    ya, yb2 = y - m['x'] * 0.18, y - m['x'] * 0.82
    gap = 2.6
    def line_y(xx, off):
        return ya + (yb2 - ya) * (xx - x0) / (x1 - x0) + off
    top = f'{x0-20},-20 {x1+20},-20 {x1+20},{line_y(x1+20,-gap):.1f} {x0-20},{line_y(x0-20,-gap):.1f}'
    bot = f'{x0-20},{line_y(x0-20,gap):.1f} {x1+20},{line_y(x1+20,gap):.1f} {x1+20},{H+20} {x0-20},{H+20}'
    uid = 'c' + color.strip('#') + (bg or 'x').strip('#')
    body = (f'<defs><clipPath id="t{uid}"><polygon points="{top}"/></clipPath>'
            f'<clipPath id="b{uid}"><polygon points="{bot}"/></clipPath></defs>'
            f'<path fill="{color}" d="{d1}"/>'
            f'<circle cx="{dot_cx:.2f}" cy="{dot_cy:.2f}" r="{r:.2f}" fill="{dot or color}"/>'
            f'<g clip-path="url(#t{uid})"><path fill="{color}" transform="translate(5.5 -1.2)" d="{d3}"/></g>'
            f'<g clip-path="url(#b{uid})"><path fill="{color}" d="{d3}"/></g>')
    return svg(W, H, body, bg, 'rubens.cut')


def symbol(color, bg=None, size=100, pad=0):
    S = size + pad * 2
    return svg(S, S, f'<path fill="{color}" d="{symbol_path(pad, pad, size)}"/>', bg, 'Ruben Svanerud symbol')


def lockup(color, bg=None):
    size = 100
    m = metrics(700, size)
    sym = size * 1.28
    gap = size * 0.34
    pad = 6
    d, w = text_path('Ruben Svanerud', 700, size, tracking=-0.035, x=pad + sym + gap, y=pad + sym / 2 + m['cap'] / 2)
    W = pad * 2 + sym + gap + w
    H = pad * 2 + sym
    body = f'<path fill="{color}" d="{symbol_path(pad, pad, sym)}"/><path fill="{color}" d="{d}"/>'
    return svg(W, H, body, bg, 'Ruben Svanerud')


def lockup_stacked(color, bg=None):
    size = 100
    m = metrics(700, size)
    pad = 6
    lh = size * 0.92
    d1, w1 = text_path('Ruben', 700, size, tracking=-0.035, x=0, y=0)
    d2, w2 = text_path('Svanerud', 700, size, tracking=-0.035, x=0, y=0)
    W = max(w1, w2) + pad * 2
    sym = W * 0.42
    top = pad
    ty = top + sym + size * 0.42 + m['cap']
    d1, _ = text_path('Ruben', 700, size, tracking=-0.035, x=pad + (W - 2 * pad - w1) / 2, y=ty)
    d2, _ = text_path('Svanerud', 700, size, tracking=-0.035, x=pad + (W - 2 * pad - w2) / 2, y=ty + lh)
    H = ty + lh + m['desc'] * 0.5 + pad
    body = (f'<path fill="{color}" d="{symbol_path((W - sym) / 2, top, sym)}"/>'
            f'<path fill="{color}" d="{d1} {d2}"/>')
    return svg(W, H, body, bg, 'Ruben Svanerud')


def avatar(fg, bg, size=1080):
    s = size * 0.56
    return svg(size, size, f'<path fill="{fg}" d="{symbol_path((size - s) / 2, (size - s) / 2, s)}"/>', bg, 'Ruben Svanerud')


if __name__ == '__main__':
    P = PALETTE
    variants = {'forest': P['forest'], 'cream': P['cream'], 'ink': P['ink'], 'leaf': P['leaf']}
    for vname, col in variants.items():
        save(f'ruben-svanerud-lockup-{vname}.svg', lockup(col))
        save(f'ruben-svanerud-lockup-stacked-{vname}.svg', lockup_stacked(col))
        save(f'ruben-svanerud-wordmark-{vname}.svg', wordmark(col))
        save(f'ruben-svanerud-wordmark-stacked-{vname}.svg', wordmark(col, stacked=True))
        save(f'rubens-cut-{vname}.svg', handle(col))
        save(f'symbol-{vname}.svg', symbol(col))
    save('rubens-cut-cream-signal.svg', handle(P['cream'], dot=P['signal']))
    save('rubens-cut-forest-signal.svg', handle(P['forest'], dot=P['signal']))
    save('avatar-forest.svg', avatar(P['cream'], P['forest']))
    save('avatar-leaf.svg', avatar(P['forest'], P['leaf']))
    save('avatar-cream.svg', avatar(P['forest'], P['cream']))
    # currentColor copies for inlining in the site
    os.makedirs(INLINE, exist_ok=True)
    for name, content in {'symbol': symbol('currentColor'), 'lockup': lockup('currentColor'),
                          'wordmark': wordmark('currentColor'), 'wordmark-stacked': wordmark('currentColor', stacked=True),
                          'handle': handle('currentColor', dot='var(--signal, #e5432d)')}.items():
        with open(os.path.join(INLINE, name + '.svg'), 'w') as f:
            f.write(content)
    print('wrote', len(os.listdir(OUT)), 'files to', OUT, '+ inline set in', INLINE)
