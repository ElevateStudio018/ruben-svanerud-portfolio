#!/usr/bin/env python3
"""Ruben Svanerud logo suite, generated as clean SVG.

- Type set in Figtree (OFL) via HarfBuzz shaping, converted to outlines (no font needed to display).
- The symbol is a rune that hides a camera on a tripod seen from the front (painted strokes, shapely geometry).
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

# ---------------------------------------------------------------- the symbol: a camera rune
# At first glance a petroglyph / branding-iron rune (a figure with its arms up). Decoded, it is a camera on a
# tripod seen from the front: two brackets make the LENS, the dot is the GLASS, the short stroke on top is the
# VIEWFINDER, the arms are the rig's HANDLES, and the brackets step down into a TRIPOD with the middle stroke.
import random
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import unary_union
from shapely.geometry.polygon import orient


def _cubic(p0, c1, c2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n; mt = 1 - t
        out.append((mt**3 * p0[0] + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t**3 * p3[0],
                    mt**3 * p0[1] + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t**3 * p3[1]))
    return out


def _chain(*segs):
    pts = list(segs[0])
    for sg in segs[1:]:
        pts += list(sg)[1:]
    return pts


def _mirror(pts):
    return [(100 - x, y) for x, y in pts]


def _brush(pts, w, seed=0, swell=0.10, ends=0.12):
    """Painted stroke: hulls of consecutive discs whose radius breathes along the stroke."""
    rnd = random.Random(seed)
    ph1, ph2 = rnd.random() * 6.28, rnd.random() * 6.28
    n = len(pts)
    discs = []
    for i, (x, y) in enumerate(pts):
        t = i / (n - 1)
        r = w / 2 * (1 + swell * 0.7 * math.sin(t * 7 + ph1) + swell * 0.5 * math.sin(t * 17 + ph2) + ends * (abs(2 * t - 1) ** 6))
        discs.append(Point(x, y).buffer(r, quad_segs=10))
    return unary_union([unary_union([discs[i], discs[i + 1]]).convex_hull for i in range(n - 1)])


def _grain(geom, amp=0.42, seed=1):
    """Dry-brush edge, like a hand-painted or branded mark."""
    rnd = random.Random(seed)
    def ring(coords):
        pts = list(LineString(coords).segmentize(0.6).coords)[:-1]
        n = len(pts); ph = [rnd.random() * 6.28 for _ in range(3)]
        out = []
        for i, (x, y) in enumerate(pts):
            (px, py), (qx, qy) = pts[i - 1], pts[(i + 1) % n]
            tx, ty = qx - px, qy - py; L = math.hypot(tx, ty) or 1
            k = amp * (0.65 * math.sin(i * 0.6 * 0.45 + ph[0]) + 0.35 * math.sin(i * 0.6 * 1.25 + ph[1]))
            out.append((x + ty / L * k, y - tx / L * k))
        return out
    polys = [geom] if geom.geom_type == 'Polygon' else list(geom.geoms)
    return unary_union([Polygon(ring(p.exterior.coords), [ring(i.coords) for i in p.interiors]).buffer(0) for p in polys])


def _rune_parts(w=8.0, seed=2):
    arm = _cubic((73, 9), (70, 16), (64, 22), (57.5, 25.5))
    arc = _cubic((57.5, 25.5), (72, 30), (72, 54), (58, 60.5))
    leg = _cubic((58, 60.5), (64, 70), (72, 81), (79, 94))
    return {
        'handles': unary_union([_brush(arm, w, seed), _brush(_mirror(arm), w, seed + 11)]),
        'lens': unary_union([_brush(arc, w, seed + 1), _brush(_mirror(arc), w, seed + 12)]),
        'glass': Point(50, 43).buffer(w * 0.62, quad_segs=16),
        'viewfinder': _brush(_cubic((50, 5), (50, 10), (50, 15), (50, 21)), w * 0.95, seed + 5),
        'tripod': unary_union([_brush(leg, w, seed + 2), _brush(_mirror(leg), w, seed + 13),
                               _brush(_cubic((50, 62), (50, 72), (50.5, 84), (50, 95)), w, seed + 3)]),
    }


_PARTS = _rune_parts()
_RUNE = _grain(unary_union(list(_PARTS.values())), 0.5, 2)


def _geom_path(geom, x, y, s):
    geoms = [geom] if geom.geom_type == 'Polygon' else [g for g in geom.geoms if g.geom_type == 'Polygon']
    d = []
    for g in geoms:
        g = orient(g, 1.0)              # holes wind the other way, so the default nonzero fill rule works everywhere
        for ring in [g.exterior] + list(g.interiors):
            pts = list(ring.coords)[:-1]
            d.append('M' + ' L'.join(f'{x + px * s:.2f} {y + py * s:.2f}' for px, py in pts) + ' Z')
    return ' '.join(d)


def symbol_path(x=0, y=0, size=100):
    return _geom_path(_RUNE, x, y, size / 100.0)


def symbol_parts_svg():
    """The rune split into its camera parts (classes p-lens, p-glass, p-viewfinder, p-handles, p-tripod)."""
    body = ''.join(f'<path class="p-{k}" fill="currentColor" d="{_geom_path(_grain(g, 0.5, 2), 0, 0, 1.0)}"/>'
                   for k, g in _PARTS.items())
    return svg(100, 100, body, None, 'The Ruben Svanerud mark, split into the parts of a camera')


# ---------------------------------------------------------------- svg helpers
def svg(w, h, body, bg=None, title='Ruben Svanerud'):
    rect = f'<rect width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{rect}{body}</svg>\n')


def save(name, content):
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(content)

# ---------------------------------------------------------------- the cut through R
_cut_n = [0]
def cut_first_glyph(text, weight, size, tracking, x, y, color):
    """Draw `text` with a diagonal slice through its first glyph (top part nudged right), same move as rubens.cut."""
    first, rest = text[0], text[1:]
    m = metrics(weight, size)
    d0, w0 = text_path(first, weight, size, tracking=0, x=x, y=y)
    # advance of first glyph incl. kerning with the next: measure pair
    _, wpair = text_path(text[:2], weight, size, tracking=tracking, x=0, y=0)
    _, wsecond = text_path(text[1], weight, size, tracking=0, x=0, y=0)
    adv = wpair - wsecond
    d1, w1 = text_path(rest, weight, size, tracking=tracking, x=x + adv, y=y)
    x0, x1 = x - 6, x + w0 + 6
    ya, yb = y - m['cap'] * 0.30, y - m['cap'] * 0.62          # the slice rises left → right through the bowl/leg
    gap = size * 0.034
    ly = lambda xx, off: ya + (yb - ya) * (xx - x0) / (x1 - x0) + off
    top = f'{x0-20},{y-size*2} {x1+20},{y-size*2} {x1+20},{ly(x1+20,-gap):.1f} {x0-20},{ly(x0-20,-gap):.1f}'
    bot = f'{x0-20},{ly(x0-20,gap):.1f} {x1+20},{ly(x1+20,gap):.1f} {x1+20},{y+size} {x0-20},{y+size}'
    _cut_n[0] += 1
    uid = f'r{_cut_n[0]}'
    body = (f'<defs><clipPath id="t{uid}"><polygon points="{top}"/></clipPath>'
            f'<clipPath id="b{uid}"><polygon points="{bot}"/></clipPath></defs>'
            f'<g clip-path="url(#t{uid})"><path fill="{color}" transform="translate({size*0.038:.2f} {-size*0.01:.2f})" d="{d0}"/></g>'
            f'<g clip-path="url(#b{uid})"><path fill="{color}" d="{d0}"/></g>'
            f'<path fill="{color}" d="{d1}"/>')
    return body, adv + w1

# ---------------------------------------------------------------- logos
def wordmark(color, bg=None, stacked=False):
    size = 100
    m = metrics(700, size)
    pad = 6
    if not stacked:
        body, w = cut_first_glyph('Ruben Svanerud', 700, size, -0.035, pad, pad + m['asc'] * 0.80, color)
        H = pad * 2 + m['asc'] * 0.80 + m['desc'] * 0.55
        return svg(w + pad * 2 + size * 0.04, H, body, bg, 'Ruben Svanerud')
    lh = size * 0.92
    b1, w1 = cut_first_glyph('Ruben', 700, size, -0.035, pad, pad + m['cap'] + 2, color)
    d2, w2 = text_path('Svanerud', 700, size, tracking=-0.035, x=pad, y=pad + m['cap'] + 2 + lh)
    W = max(w1, w2) + pad * 2
    H = pad * 2 + m['cap'] + 2 + lh + m['desc'] * 0.55
    return svg(W, H, b1 + f'<path fill="{color}" d="{d2}"/>', bg, 'Ruben Svanerud')


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
    ya, yb2 = y - m['x'] * 0.22, y - m['x'] * 0.78
    gap = 4.2
    def line_y(xx, off):
        return ya + (yb2 - ya) * (xx - x0) / (x1 - x0) + off
    top = f'{x0-20},-20 {x1+20},-20 {x1+20},{line_y(x1+20,-gap):.1f} {x0-20},{line_y(x0-20,-gap):.1f}'
    bot = f'{x0-20},{line_y(x0-20,gap):.1f} {x1+20},{line_y(x1+20,gap):.1f} {x1+20},{H+20} {x0-20},{H+20}'
    _cut_n[0] += 1
    uid = f'h{_cut_n[0]}'
    body = (f'<defs><clipPath id="t{uid}"><polygon points="{top}"/></clipPath>'
            f'<clipPath id="b{uid}"><polygon points="{bot}"/></clipPath></defs>'
            f'<path fill="{color}" d="{d1}"/>'
            f'<circle cx="{dot_cx:.2f}" cy="{dot_cy:.2f}" r="{r:.2f}" fill="{dot or color}"/>'
            f'<g clip-path="url(#t{uid})"><path fill="{color}" transform="translate(7.5 -2)" d="{d3}"/></g>'
            f'<g clip-path="url(#b{uid})"><path fill="{color}" d="{d3}"/></g>')
    return svg(W, H, body, bg, 'rubens.cut')


def symbol(color, bg=None, size=100, pad=0):
    S = size + pad * 2
    return svg(S, S, f'<path fill="{color}" d="{symbol_path(pad, pad, size)}"/>', bg, 'Ruben Svanerud symbol')


def lockup(color, bg=None):
    size = 100
    m = metrics(700, size)
    sym = size * 1.18
    gap = size * 0.2
    pad = 6
    tb, w = cut_first_glyph('Ruben Svanerud', 700, size, -0.035, pad + sym + gap, pad + sym / 2 + m['cap'] / 2, color)
    W = pad * 2 + sym + gap + w
    H = pad * 2 + sym
    body = f'<path fill="{color}" d="{symbol_path(pad - sym * 0.1, pad, sym)}"/>' + tb
    return svg(W, H, body, bg, 'Ruben Svanerud')


def lockup_stacked(color, bg=None):
    size = 100
    m = metrics(700, size)
    pad = 6
    lh = size * 0.92
    d1, w1 = text_path('Ruben', 700, size, tracking=-0.035, x=0, y=0)
    d2, w2 = text_path('Svanerud', 700, size, tracking=-0.035, x=0, y=0)
    W = max(w1, w2) + pad * 2
    sym = W * 0.4
    top = pad
    ty = top + sym + size * 0.3 + m['cap']
    b1, _ = cut_first_glyph('Ruben', 700, size, -0.035, pad + (W - 2 * pad - w1) / 2, ty, color)
    d2, _ = text_path('Svanerud', 700, size, tracking=-0.035, x=pad + (W - 2 * pad - w2) / 2, y=ty + lh)
    H = ty + lh + m['desc'] * 0.5 + pad
    body = (f'<path fill="{color}" d="{symbol_path((W - sym) / 2, top, sym)}"/>' + b1 +
            f'<path fill="{color}" d="{d2}"/>')
    return svg(W, H, body, bg, 'Ruben Svanerud')


def avatar(fg, bg, size=1080):
    s = size * 0.62
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
    for name, content in {'symbol': symbol('currentColor'),  'symbol-parts': symbol_parts_svg(), 'lockup': lockup('currentColor'),
                          'wordmark': wordmark('currentColor'), 'wordmark-stacked': wordmark('currentColor', stacked=True),
                          'handle': handle('currentColor', dot='var(--signal, #e5432d)')}.items():
        with open(os.path.join(INLINE, name + '.svg'), 'w') as f:
            f.write(content)
    print('wrote', len(os.listdir(OUT)), 'files to', OUT, '+ inline set in', INLINE)
