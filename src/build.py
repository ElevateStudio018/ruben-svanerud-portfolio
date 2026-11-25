#!/usr/bin/env python3
"""Build the static site into the repository root from src/templates + src/site_data.py.

Run from anywhere:  python3 src/build.py
"""
import json, os, sys
from jinja2 import Environment, FileSystemLoader, StrictUndefined, ChainableUndefined

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import site_data as D

OUT = os.path.dirname(HERE)  # repository root
images = json.load(open(os.path.join(HERE, 'images.json')))
from markupsafe import Markup, escape


def keep(text):
    """Glue the last two words with a no-break space when short, so headings never end on a lone short word."""
    w = str(text).rsplit(' ', 1)
    if len(w) == 2 and len(w[0].split(' ')[-1]) + len(w[1]) <= 9:
        return w[0] + '\u00a0' + w[1]
    return text


env = Environment(loader=FileSystemLoader(os.path.join(HERE, 'templates')), autoescape=True,
                  trim_blocks=False, lstrip_blocks=False, undefined=ChainableUndefined)
env.filters['keep'] = keep

import re as _re
ROOT = os.path.dirname(HERE)


def svg_inline(name, label=None):
    """Inline an SVG from assets/logo (fill=currentColor). Decorative unless a label is given."""
    raw = open(os.path.join(ROOT, 'assets', 'logo', name + '.svg')).read()
    raw = _re.sub(r'<title>.*?</title>', '', raw)
    raw = _re.sub(r'\s(width|height)="[^"]*"', '', raw, count=2)
    if label:
        raw = raw.replace('<svg ', f'<svg focusable="false" ', 1).replace('role="img"', 'role="img"').replace(
            _re.search(r'aria-label="[^"]*"', raw).group(0), f'aria-label="{label}"')
    else:
        raw = raw.replace('role="img"', 'aria-hidden="true" focusable="false"')
        raw = _re.sub(r'\saria-label="[^"]*"', '', raw)
    return Markup(raw)


def shape_inline(n):
    raw = open(os.path.join(ROOT, 'assets', 'shapes', f'shape-{n}.svg')).read()
    return Markup(raw.replace('<svg ', '<svg focusable="false" ', 1))


env.globals['svg'] = svg_inline
env.globals['shape'] = shape_inline

SITE = D.SITE_URL.rstrip('/')
person_ld = {
    '@type': 'Person',
    '@id': (SITE + '/#person') if SITE else '#person',
    'name': D.PERSON['name'],
    'jobTitle': D.PERSON['role_long'],
    'email': 'mailto:' + D.PERSON['email'],
    'workLocation': [{'@type': 'Place', 'name': 'Uppsala, Sweden'}, {'@type': 'Place', 'name': 'Stockholm, Sweden'}],
    'sameAs': [s['url'] for s in D.PERSON['social']],
}
if SITE:
    person_ld['url'] = SITE + '/'


def abs_url(path):
    return f'{SITE}/{path}' if SITE else None


def og_img(name):
    if not SITE:
        return None
    i = images[name]
    w = max(x for x in i['sizes'] if x <= 1600)
    return f'{SITE}/assets/img/{name}-{w}.webp'


cats = []
for _pr in D.PROJECTS:
    for _c in _pr.get('cats', []):
        if _c not in cats:
            cats.append(_c)
common = dict(preview=getattr(D, 'PREVIEW', False), person=D.PERSON, projects=D.PROJECTS, images=images, alt=D.ALT,
              short_form=D.SHORT_FORM, stills=D.STILLS, make=D.MAKE, intro=D.INTRO, hero_d=D.HERO, cats=cats,
              quote_popcorn=D.QUOTE_POPCORN, focus=D.FOCUS, home_stills=D.HOME_STILLS, titles={pr['slug']: pr['title'] for pr in D.PROJECTS})


def render(tpl, out, **ctx):
    html = env.get_template(tpl).render(**common, **ctx)
    path = os.path.join(OUT, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(html)
    print('wrote', out, len(html))


def ld(obj):
    return json.dumps({'@context': 'https://schema.org', **obj}, ensure_ascii=False)


# Home
render('index.html', 'index.html', p='', section='home', hero=True, dialog=True, body_class='has-hero',
       title='Ruben Svanerud — Filmmaker & photographer, Uppsala / Stockholm',
       description=('Ruben Svanerud is a filmmaker and photographer based in Uppsala and Stockholm. '
                    'Ski films, YouTube productions, underwater series and boxing.'),
       canonical=abs_url(''), og_image=og_img('ski-gondola'),
       jsonld=ld({'@graph': [person_ld, {'@type': 'WebSite', 'name': 'Ruben Svanerud', **({'url': SITE + '/'} if SITE else {})}]}))

# About
render('about.html', 'about.html', p='', section='about', hero=False,
       title='About — Ruben Svanerud',
       description=('About Ruben Svanerud, filmmaker and photographer in Uppsala and Stockholm. '
                    'He shoots and edits his own work and is open to working with brands and people.'),
       canonical=abs_url('about.html'), og_image=og_img('box-rig-crop'),
       jsonld=ld({'@type': 'ProfilePage', 'mainEntity': person_ld}))

# Projects index
items = [{'@type': 'ListItem', 'position': n + 1, 'name': pr['title'],
          **({'url': f"{SITE}/projects/{pr['slug']}.html"} if SITE else {})} for n, pr in enumerate(D.PROJECTS)]
render('projects.html', 'projects.html', p='', section='projects', hero=False,
       title='Projects — Ruben Svanerud',
       description=('Film and photo projects by Ruben Svanerud: For the Love of Ski, Betting Everything on Popcorn, '
                    'A Different Planet, Kebnekaise and EM26 Is Next.'),
       canonical=abs_url('projects.html'), og_image=og_img('ski-air'),
       jsonld=ld({'@type': 'CollectionPage', 'name': 'Projects', 'mainEntity': {'@type': 'ItemList', 'itemListElement': items}}))

# Stills
render('stills.html', 'stills.html', p='', section='stills', hero=False, lightbox=True,
       title='Stills — Ruben Svanerud',
       description=('Stills and photographs by Ruben Svanerud: skiing, Milan, underwater, Kebnekaise and fight night.'),
       canonical=abs_url('stills.html'), og_image=og_img('dive-wreck'),
       jsonld=ld({'@type': 'CollectionPage', 'name': 'Stills', 'author': {'@type': 'Person', 'name': D.PERSON['name']}}))

# Project pages
total = len(D.PROJECTS)
for n, pr in enumerate(D.PROJECTS):
    nxt = D.PROJECTS[(n + 1) % total]
    work = {'@type': 'CreativeWork', 'name': pr['title'], 'genre': pr['kind'], 'dateCreated': pr['year'],
            'creator': {'@type': 'Person', 'name': D.PERSON['name']}, 'description': pr['lead']}
    if pr.get('location'):
        work['locationCreated'] = {'@type': 'Place', 'name': pr['location']}
    if pr.get('youtube'):
        work['video'] = {'@type': 'VideoObject', 'name': pr['title'], 'description': pr['meta_desc'],
                         'embedUrl': f"https://www.youtube-nocookie.com/embed/{pr['youtube']}",
                         'duration': pr['iso_duration']}
    if SITE:
        work['url'] = f"{SITE}/projects/{pr['slug']}.html"
    cover = pr.get('cover') or pr['thumb']
    render('project.html', f"projects/{pr['slug']}.html", p='../', section='projects', hero=False, lightbox=bool(pr.get('gallery')),
           dialog=False,
           pr=pr, nxt=nxt, num=n + 1, total=total, og_type='article',
           title=f"{pr['title']} — Ruben Svanerud", description=pr['meta_desc'],
           canonical=abs_url(f"projects/{pr['slug']}.html"), og_image=og_img(cover), jsonld=ld(work))

# Brand kit page
PALETTE = [
    ('Forest', '#12392A', '18 57 42', 'Main dark: backgrounds, text on light, the logo on cream', 'tone-forest'),
    ('Pine', '#1F6B47', '31 107 71', 'Second green: shapes on forest, cards', 'tone-pine'),
    ('Leaf', '#9FCB6B', '159 203 107', 'Bright green: big colour blocks', 'tone-leaf'),
    ('Sage', '#C6DCC0', '198 220 192', 'Soft green: panels', 'tone-sage'),
    ('Cream', '#F2EBDD', '242 235 221', 'Paper, and the logo on dark and on photos', 'tone-cream2'),
    ('Glacier', '#BCD5E4', '188 213 228', 'Sky and glacier blue from his ski footage: calm colour blocks', 'tone-glacier bk-sw--glacier'),
    ('Ink', '#0E1A14', '14 26 20', 'Body text on cream', 'bk-sw--ink'),
    ('Signal', '#E5432D', '229 67 45', 'Only the play dot and small calls to action', 'bk-sw--signal'),
]
APPS = [('youtube-banner', 'YouTube banner, 2560 × 1440', 'bk-app--w'), ('video-end-card', 'Video end card, 1920 × 1080', 'bk-app--w'),
        ('instagram-post', 'Instagram post, 1080 × 1350', 'bk-app--s'), ('instagram-avatar', 'Profile picture, 1080 × 1080', 'bk-app--s'),
        ('watermark', 'Watermark, transparent PNG (shown on a still)', 'bk-app--s'),
        ('business-card-front', 'Business card, front', 'bk-app--w'), ('business-card-back', 'Business card, back', 'bk-app--w'),
        ('lower-third', 'Lower third for video, transparent PNG (shown on a still)', 'bk-app--f')]
render('brand.html', 'brand/index.html', p='../', section='brand', hero=True, body_class='has-hero',
       palette=PALETTE, apps=APPS,
       title='Brand kit — Ruben Svanerud',
       description='Brand kit for Ruben Svanerud: logo, colour, type, shapes, photography and templates.',
       canonical=abs_url('brand/'), og_image=og_img('ski-gondola'),
       jsonld=ld({'@type': 'WebPage', 'name': 'Ruben Svanerud brand kit'}))

# robots, sitemap, llms.txt
robots = 'User-agent: *\n' + ('Disallow: /\n' if getattr(D, 'PREVIEW', False) else 'Allow: /\n')
if SITE:
    urls = ['', 'about.html', 'projects.html', 'stills.html'] + [f"projects/{pr['slug']}.html" for pr in D.PROJECTS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += ''.join(f'  <url><loc>{SITE}/{u}</loc></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)
    robots += f'Sitemap: {SITE}/sitemap.xml\n'
open(os.path.join(OUT, 'robots.txt'), 'w').write(robots)

llms = [f"# {D.PERSON['name']}", '',
        f"> {D.PERSON['role_long']} based in Uppsala and Stockholm, Sweden. Shoots and edits his own work: "
        'ski films, YouTube productions, underwater series and boxing.', '',
        '## Projects', '']
for pr in D.PROJECTS:
    bits = [pr['kind'], pr.get('location'), pr['year'], pr.get('runtime')]
    llms.append(f"- [{pr['title']}](projects/{pr['slug']}.html): {', '.join(b for b in bits if b)}. {pr['lead']}")
llms += ['', '## Contact', '', f"- Email: {D.PERSON['email']}"]
llms += [f"- {s['name']}: {s['url']}" for s in D.PERSON['social']]
open(os.path.join(OUT, 'llms.txt'), 'w').write('\n'.join(llms) + '\n')
print('done')
