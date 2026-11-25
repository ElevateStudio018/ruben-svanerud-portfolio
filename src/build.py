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


common = dict(preview=getattr(D, 'PREVIEW', False), person=D.PERSON, projects=D.PROJECTS, images=images, alt=D.ALT, short_form=D.SHORT_FORM)


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
    render('project.html', f"projects/{pr['slug']}.html", p='../', section='projects', hero=False,
           pr=pr, nxt=nxt, num=n + 1, total=total, og_type='article',
           title=f"{pr['title']} — Ruben Svanerud", description=pr['meta_desc'],
           canonical=abs_url(f"projects/{pr['slug']}.html"), og_image=og_img(cover), jsonld=ld(work))

# robots, sitemap, llms.txt
robots = 'User-agent: *\n' + ('Disallow: /\n' if getattr(D, 'PREVIEW', False) else 'Allow: /\n')
if SITE:
    urls = ['', 'about.html', 'projects.html'] + [f"projects/{pr['slug']}.html" for pr in D.PROJECTS]
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
