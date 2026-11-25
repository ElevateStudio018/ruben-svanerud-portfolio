"""Content for rubensvanerud site. Every fact here comes from Ruben's public
profiles (Instagram @rubens.cut, TikTok @rubens.cut, YouTube @RubensCut) or
the published videos themselves. Nothing invented: missing fields are omitted.
"""

SITE_URL = ''  # set to e.g. 'https://example.com' (no trailing slash) to enable canonical, OG URLs and sitemap
PREVIEW = True  # True = noindex on every page and Disallow in robots.txt. Set False when Ruben has approved and the site goes live.

PERSON = {
    'name': 'Ruben Svanerud',
    'role': 'Film & photo',
    'role_long': 'Filmmaker and photographer',
    'based': 'Uppsala / Stockholm, Sweden',
    'email': 'ruben.svanerud@gmail.com',
    'social': [
        {'name': 'Instagram', 'handle': '@rubens.cut', 'url': 'https://www.instagram.com/rubens.cut/'},
        {'name': 'TikTok', 'handle': '@rubens.cut', 'url': 'https://www.tiktok.com/@rubens.cut'},
        {'name': 'YouTube', 'handle': '@RubensCut', 'url': 'https://www.youtube.com/@RubensCut'},
    ],
}

ALT = {
    'ski-gondola': 'Two cable cars crossing a snow-covered glacier under a clear blue sky',
    'ski-powder': 'Skier in a red jacket turning through powder, snow spraying in the sun',
    'ski-goggles': 'Skier in a red jacket and white helmet looking out over the mountains',
    'ski-trees': 'Skier jumping between snow-covered birch branches',
    'ski-air': 'Skier in mid-air off a jump, skis spread against a blue sky',
    'ski-spin': 'Skier spinning off a jump beside a pine tree',
    'ski-poster': 'Poster for the short film For the Love of Ski, a film by Ruben',
    'pop-street': 'Man in a black cap and t-shirt looking up at a building on a Milan street',
    'pop-milan': 'Cobbled street in Milan with pedestrians in late afternoon light',
    'pop-statue': 'Marble statue of Leonardo da Vinci against a pale sky',
    'pop-night': 'Man lit by a laptop screen in a dark room, holding a bottle of water',
    'pop-orange': 'Close-up of a man in glasses and a cap under orange ceiling light',
    'pop-station': 'Man in a navy cap sitting on a railway platform, talking to camera',
    'pop-bts-street': 'Behind the scenes: a man on the phone outside a shop while a camera operator films him',
    'pop-bts-room': 'Behind the scenes: a camera on a tripod with its monitor, filming a woman by a window in Milan',
    'dive-reef': 'Diver above a coral reef in deep blue water, light falling from the surface',
    'dive-torch': 'Diver with a torch descending into dark blue water',
    'dive-wreck': 'Sunken aircraft resting on the sea floor',
    'dive-coral': 'Black and white close-up of layered plate coral',
    'dive-surface': 'Diver at the water surface with the sun and a coastline behind',
    'dive-turtle': 'Sea turtle feeding among corals',
    'box-win': 'Referee raising the arm of a boxer in blue after a fight, under red stage lights',
    'box-rig': 'Camera rig with a monitor at the corner of a boxing ring, crowd in the background',
    'box-rig-crop': 'Camera rig with a monitor at the corner of a boxing ring, crowd in the background',
    'keb-climb': 'Hiker with a large backpack climbing a steep grassy slope below a misty mountain',
    'keb-hike': 'Two hikers with backpacks crossing a meadow below a pyramid-shaped mountain',
}

# Gallery rows on project pages: ('full', [img]) · ('half', [a, b]) · ('thirds', [a, b, c]) · ('wn', [wide, narrow])
PROJECTS = [
    {
        'slug': 'for-the-love-of-ski',
        'title': 'For the Love of Ski',
        'kind': 'Short film',
        'cats': ['Film'],
        'year': '2026',
        'runtime': '04:03',
        'iso_duration': 'PT4M3S',
        'credit': 'A film by Ruben',
        'lead': ("A short film cut from a season of skiing with friends. "
                 "It was also Ruben’s entry to Alpingaraget’s video competition Vinter Edit 2026."),
        'meta_desc': ("For the Love of Ski, a short film by Ruben Svanerud from a season of skiing with friends. "
                      "His entry to Alpingaraget's Vinter Edit 2026."),
        'youtube': 'hjpaJWnm0NY',
        'poster': 'ski-gondola',
        'cover': 'ski-spin',
        'thumb': 'ski-air',
        'gallery': [
            ('full', ['ski-trees']),
            ('thirds', ['ski-powder', 'ski-poster', 'ski-goggles']),
            ('full', ['ski-air']),
        ],
        'links': [
            {'label': 'Watch on YouTube', 'url': 'https://www.youtube.com/watch?v=hjpaJWnm0NY'},
            {'label': 'Vertical cut on Instagram', 'url': 'https://www.instagram.com/reel/DfIPBwspRGu/'},
        ],
    },
    {
        'slug': 'betting-everything-on-popcorn',
        'eyebrow': 'EP.01',
        'title': 'Betting Everything on Popcorn',
        'kind': 'YouTube episode',
        'cats': ['Film', 'YouTube'],
        'client': 'Mr. Popcorn',
        'location': 'Milan, Italy',
        'year': '2026',
        'runtime': '11:00',
        'iso_duration': 'PT11M',
        'lead': ("Mr. Popcorn came to Ruben with an idea for a YouTube series. Episode one goes to Italy "
                 "to look at the machine that could start his popcorn company. "
                 "Ruben filmed and edited it in Milan, and calls it his favourite work yet."),
        'meta_desc': ("EP.01 Betting Everything on Popcorn, a YouTube episode for Mr. Popcorn, "
                      "filmed and edited by Ruben Svanerud in Milan."),
        'youtube': 'wZorAZfUz6w',
        'poster': 'pop-station',
        'cover': 'pop-street',
        'thumb': 'pop-street',
        'gallery': [
            ('full', ['pop-milan']),
            ('half', ['pop-statue', 'pop-orange']),
            ('wn', ['pop-bts-room', 'pop-bts-street']),
            ('full', ['pop-night']),
        ],
        'gallery_caption': 'Stills from the episode, and behind the scenes in Milan.',
        'links': [
            {'label': 'Watch on YouTube', 'url': 'https://www.youtube.com/watch?v=wZorAZfUz6w'},
            {'label': 'Behind the scenes on Instagram', 'url': 'https://www.instagram.com/p/DemcnXulyCQ/'},
        ],
    },
    {
        'slug': 'a-different-planet',
        'title': 'A Different Planet',
        'kind': 'Underwater photo & film',
        'cats': ['Photo', 'Film'],
        'year': '2026',
        'lead': ("An underwater series: reefs, a sunken aircraft and a feeding sea turtle, "
                 "published as photographs and short clips."),
        'meta_desc': ("A Different Planet, an underwater photo and film series by Ruben Svanerud: "
                      "reefs, a sunken aircraft and a sea turtle."),
        'primary': {'label': 'View the series on Instagram', 'url': 'https://www.instagram.com/p/De_md_flyqA/'},
        'cover': 'dive-reef',
        'thumb': 'dive-reef',
        'gallery': [
            ('full', ['dive-wreck']),
            ('half', ['dive-torch', 'dive-coral']),
            ('wn', ['dive-surface', 'dive-turtle']),
        ],
        'gallery_caption': 'Right: still from the clip “Turtle munchies”.',
        'links': [
            {'label': 'Photo series on Instagram', 'url': 'https://www.instagram.com/p/De_md_flyqA/'},
            {'label': '“Turtle munchies” on Instagram', 'url': 'https://www.instagram.com/reel/DepFufGpkkO/'},
        ],
    },
    {
        'slug': 'kebnekaise',
        'title': 'Kebnekaise',
        'kind': 'Hiking film & photo',
        'cats': ['Film', 'Photo'],
        'location': 'Kebnekaise, Sweden',
        'year': '2026',
        'lead': ("A summer hike in Kebnekaise with friends, cut into a short film. "
                 "The photograph of the climb is, in Ruben’s words, one of his favourites from the summer."),
        'meta_desc': ("Kebnekaise, a summer hiking film and photograph by Ruben Svanerud, "
                      "shot on a hike with friends in the Swedish mountains."),
        'primary': {'label': 'Watch the film on Instagram', 'url': 'https://www.instagram.com/reel/DgIWM6nN4HL/'},
        'cover': 'keb-climb',
        'thumb': 'keb-climb',
        'gallery': [
            ('wn', ['keb-hike', 'keb-climb']),
        ],
        'gallery_caption': 'Left: still from the film. Right: the photograph of the climb.',
        'links': [
            {'label': 'Film on Instagram', 'url': 'https://www.instagram.com/reel/DgIWM6nN4HL/'},
            {'label': 'Film on TikTok', 'url': 'https://www.tiktok.com/@rubens.cut/video/7711771333570350358'},
            {'label': 'Photograph on Instagram', 'url': 'https://www.instagram.com/p/DfaZlXQJHH9/'},
        ],
    },
    {
        'slug': 'em26-is-next',
        'title': 'EM26 Is Next',
        'subtitle': 'With boxer Erwa',
        'kind': 'Boxing, behind the scenes',
        'cats': ['Film', 'Sport'],
        'location': 'Trädgården',
        'year': '2026',
        'lead': ("Ruben films the boxer Erwa at ringside and backstage, from fight night at Trädgården "
                 "toward the European Championships, EM26. The films are published on Erwa’s and Ruben’s Instagram."),
        'meta_desc': ("EM26 Is Next, behind-the-scenes boxing films with the boxer Erwa, shot by Ruben Svanerud "
                      "at fight night at Trädgården."),
        'primary': {'label': 'Watch on Instagram', 'url': 'https://www.instagram.com/reel/Dc5vxR5pzYn/'},
        'cover_pair': ['box-win', 'box-rig'],
        'thumb': 'box-win',
        'thumb_pos': '50% 30%',
        'gallery': [],
        'links': [
            {'label': '“EM26 is next” on Instagram', 'url': 'https://www.instagram.com/reel/Dc5vxR5pzYn/'},
            {'label': 'Fight night on Erwa’s Instagram', 'url': 'https://www.instagram.com/reel/DdCWilcOnO4/'},
            {'label': 'Ringside and backstage, on Erwa’s Instagram', 'url': 'https://www.instagram.com/reel/DcBQ4YgM9mo/'},
        ],
    },
]

# Home hero. focus = where the frame symbol sits, as fractions of the image (the two cable cars).
HERO = {'img': 'ski-gondola', 'focus': (0.5, 0.3)}   # where the mark sits: the calm sky above the cable cars

# Default focal point per image (object-position), so crops keep the subject
FOCUS = {
    'ski-goggles': '82% 42%', 'ski-powder': '8% 50%', 'pop-bts-street': '22% 50%', 'pop-street': '62% 42%',
    'keb-climb': '70% 50%', 'box-win': '50% 36%', 'box-rig': '50% 100%', 'dive-turtle': '42% 50%',
    'pop-milan': '52% 60%', 'dive-surface': '40% 50%',
}

# Stills row on the home page: frames not already used elsewhere on the page
HOME_STILLS = ['ski-trees', 'dive-wreck', 'pop-statue', 'keb-hike', 'dive-torch', 'ski-goggles', 'pop-orange',
               'dive-coral', 'pop-night']

# Inline images in the intro sentence
INTRO = [('ski-air', 'ski films'), ('pop-street', 'YouTube episodes'), ('dive-reef', 'underwater series'),
         ('box-win', 'fight-night films')]

# What Ruben makes, one card per kind of work, each pointing at a real project
MAKE = [
    {'title': 'Short films', 'text': 'Season edits cut into short films, like For the Love of Ski.',
     'img': 'ski-powder', 'slug': 'for-the-love-of-ski', 'tone': 'forest'},
    {'title': 'YouTube episodes', 'text': 'Filmed and edited on location: EP.01 for Mr. Popcorn in Milan.',
     'img': 'pop-station', 'slug': 'betting-everything-on-popcorn', 'tone': 'sage'},
    {'title': 'Sport, behind the scenes', 'text': 'Ringside and backstage with the boxer Erwa.',
     'img': 'box-rig-crop', 'slug': 'em26-is-next', 'tone': 'leaf'},
    {'title': 'Underwater & outdoors', 'text': 'Reefs, a sunken aircraft and Kebnekaise, in photo and film.',
     'img': 'dive-surface', 'slug': 'a-different-planet', 'tone': 'glacier'},
]

# Stills row (home) and Stills page: (image, project slug, caption)
STILLS = [
    ('ski-trees', 'for-the-love-of-ski', 'Through the birches'),
    ('pop-milan', 'betting-everything-on-popcorn', 'Milan, late afternoon'),
    ('dive-wreck', 'a-different-planet', 'The sunken aircraft'),
    ('keb-climb', 'kebnekaise', 'The climb'),
    ('ski-air', 'for-the-love-of-ski', 'Off the kicker'),
    ('pop-statue', 'betting-everything-on-popcorn', 'Leonardo, Milan'),
    ('dive-torch', 'a-different-planet', 'Going down'),
    ('ski-goggles', 'for-the-love-of-ski', 'Looking out'),
    ('keb-hike', 'kebnekaise', 'Toward the peak'),
    ('pop-orange', 'betting-everything-on-popcorn', 'Day one'),
    ('dive-coral', 'a-different-planet', 'Plate coral'),
    ('ski-gondola', 'for-the-love-of-ski', 'The cable cars'),
    ('dive-surface', 'a-different-planet', 'At the surface'),
    ('pop-night', 'betting-everything-on-popcorn', 'Late night'),
    ('ski-spin', 'for-the-love-of-ski', 'Spin by the pine'),
    ('pop-station', 'betting-everything-on-popcorn', 'On the platform'),
    ('dive-turtle', 'a-different-planet', 'Turtle munchies'),
    ('box-win', 'em26-is-next', 'Fight night'),
    ('ski-powder', 'for-the-love-of-ski', 'Powder turn'),
    ('box-rig', 'em26-is-next', 'At the corner'),
    ('dive-reef', 'a-different-planet', 'Above the reef'),
    ('pop-bts-room', 'betting-everything-on-popcorn', 'Behind the scenes'),
]

# Ruben's own words, from his captions
QUOTE_POPCORN = 'This is my favourite work yet and only the start of something bigger.'

SHORT_FORM = [
    {'img': 'ski-poster', 'label': 'For the Love of Ski', 'kind': 'Reel', 'pos': '50% 50%',
     'url': 'https://www.instagram.com/reel/DfIPBwspRGu/'},
    {'img': 'box-win', 'label': 'Fight night, with Erwa', 'kind': 'Reel', 'pos': '50% 50%',
     'url': 'https://www.instagram.com/reel/DdCWilcOnO4/'},
    {'img': 'box-rig', 'label': 'EM26 Is Next', 'kind': 'Reel', 'pos': '50% 100%',
     'url': 'https://www.instagram.com/reel/Dc5vxR5pzYn/'},
    {'img': 'dive-turtle', 'label': 'Turtle munchies', 'kind': 'Reel', 'pos': '40% 50%',
     'url': 'https://www.instagram.com/reel/DepFufGpkkO/'},
    {'img': 'keb-hike', 'label': 'Hiking in Kebnekaise', 'kind': 'Reel', 'pos': '42% 50%',
     'url': 'https://www.instagram.com/reel/DgIWM6nN4HL/'},
]
