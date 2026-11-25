#!/usr/bin/env python3
"""Organic shapes for the Ruben Svanerud identity: soft leaf / snow-drift silhouettes with a few deep
notches, drawn as smooth closed Bézier curves. They are used big, cropped and tone-on-tone
(pine on forest, leaf on pine, sage on cream), never as small decorations.

usage: python3 src/brand/shapes.py      -> assets/shapes/shape-1.svg … shape-4.svg (fill="currentColor")
"""
import math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'assets', 'shapes')
os.makedirs(OUT, exist_ok=True)


def catmull_rom(points, tension=0.5):
    """Closed smooth path through points (Catmull-Rom → cubic Bézier)."""
    n = len(points)
    d = f'M{points[0][0]:.1f} {points[0][1]:.1f}'
    for i in range(n):
        p0, p1, p2, p3 = points[i - 1], points[i], points[(i + 1) % n], points[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3, p1[1] + (p2[1] - p0[1]) * tension / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3, p2[1] - (p3[1] - p1[1]) * tension / 3)
        d += f' C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d + ' Z'


def leaf(seed, lobes, notch_depth, stretch=(1.0, 1.0), rot=0.0):
    """A blob with `lobes` soft lobes separated by deep, narrow notches."""
    rnd = random.Random(seed)
    pts = []
    steps = lobes * 6
    for k in range(steps):
        a = 2 * math.pi * k / steps
        phase = (k % 6) / 6.0
        # notch at phase 0: pull radius in sharply, lobes round in between
        if phase == 0:
            r = 1.0 - notch_depth * (0.85 + 0.3 * rnd.random())
        elif phase in (1 / 6, 5 / 6):
            r = 0.92 + 0.05 * rnd.random()
        else:
            r = 1.0 + 0.06 * rnd.random()
        r *= 0.9 + 0.2 * math.sin(a * 2 + seed) * 0.5
        x = math.cos(a + rot) * r * 400 * stretch[0]
        y = math.sin(a + rot) * r * 400 * stretch[1]
        pts.append((500 + x, 500 + y))
    return catmull_rom(pts, 0.55)


SHAPES = {
    'shape-1': leaf(3, 5, 0.42, (1.0, 0.82), 0.3),
    'shape-2': leaf(11, 3, 0.55, (0.9, 1.0), 1.1),
    'shape-3': leaf(21, 4, 0.30, (1.0, 0.7), -0.4),
    'shape-4': leaf(5, 6, 0.36, (0.85, 0.95), 0.0),
}

if __name__ == '__main__':
    for name, d in SHAPES.items():
        with open(os.path.join(OUT, name + '.svg'), 'w') as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" aria-hidden="true">'
                    f'<path fill="currentColor" d="{d}"/></svg>\n')
    print('wrote', len(SHAPES), 'shapes to', OUT)
