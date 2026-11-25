"""Content for rubensvanerud site. Every fact here comes from Ruben's public
profiles (Instagram @rubens.cut, TikTok @rubens.cut, YouTube @RubensCut) or
the published videos themselves. Nothing invented: missing fields are omitted.
"""

SITE_URL = ''  # set to e.g. 'https://example.com' (no trailing slash) to enable canonical, OG URLs and sitemap

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
    'ski-gondola-tall': 'Two cable cars crossing a snow-covered glacier under a clear blue sky',
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
    'pop-bts-room': 'Behind the scenes: camera on a tripod with a monitor in a bright room',
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

# Suite block types: wide (edge to edge), pair (two in a row), detail (narrow, offset), inset (within margins)
PROJECTS = [
    {
        'slug': 'for-the-love-of-ski',
        'title': 'For the Love of Ski',
        'kind': 'Short film',
        'year': '2026',
        'runtime': '04:03',
        'iso_duration': 'PT4M3S',
        'credit': 'A film by Ruben',
        'lead': ("A short film cut from a season of skiing with friends. "
                 "It was also Ruben's entry to Alpingaraget's video competition Vinter Edit 2026."),
        'meta_desc': ("For the Love of Ski, a short film by Ruben Svanerud from a season of skiing with friends. "
                      "His entry to Alpingaraget's Vinter Edit 2026."),
        'youtube': 'hjpaJWnm0NY',
        'cover': 'ski-spin',
        'thumb': 'ski-air',
        'suite': [
            {'type': 'wide', 'img': 'ski-trees', 'gap': 'm'},
            {'type': 'pair', 'imgs': ['ski-powder', 'ski-poster'], 'pos': ['8% 50%', None], 'gap': 'm',
             'caption': 'A still from the film, and the film poster.'},
            {'type': 'detail', 'img': 'ski-goggles', 'align': 'right', 'gap': 'l'},
            {'type': 'wide', 'img': 'ski-air', 'gap': 'm'},
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
        'client': 'Mr. Popcorn',
        'location': 'Milan, Italy',
        'year': '2026',
        'runtime': '11:00',
        'iso_duration': 'PT11M',
        'lead': ("Mr. Popcorn came to Ruben with an idea for a YouTube series. Episode one goes to Italy "
                 "to look at the machine that could start his popcorn company. "
                 "Ruben filmed and edited it in Milan, and calls it his favourite work yet."),
        'primary': None,
        'meta_desc': ("EP.01 Betting Everything on Popcorn, a YouTube episode for Mr. Popcorn, "
                      "filmed and edited by Ruben Svanerud in Milan."),
        'youtube': 'wZorAZfUz6w',
        'cover': 'pop-street',
        'thumb': 'pop-street',
        'suite': [
            {'type': 'wide', 'img': 'pop-milan', 'gap': 'm'},
            {'type': 'pair', 'imgs': ['pop-statue', 'pop-orange'], 'gap': 'm'},
            {'type': 'detail', 'img': 'pop-night', 'align': 'left', 'gap': 'l'},
            {'type': 'pair', 'imgs': ['pop-bts-street', 'pop-bts-room'], 'gap': 'xl',
             'caption': 'Behind the scenes in Milan.'},
            {'type': 'wide', 'img': 'pop-station', 'gap': 'm'},
        ],
        'links': [
            {'label': 'Watch on YouTube', 'url': 'https://www.youtube.com/watch?v=wZorAZfUz6w'},
            {'label': 'Behind the scenes on Instagram', 'url': 'https://www.instagram.com/p/DemcnXulyCQ/'},
        ],
    },
    {
        'slug': 'a-different-planet',
        'title': 'A Different Planet',
        'kind': 'Underwater photo & film',
        'year': '2026',
        'lead': ("An underwater series: reefs, a sunken aircraft and a feeding sea turtle, "
                 "published as photographs and short clips."),
        'meta_desc': ("A Different Planet, an underwater photo and film series by Ruben Svanerud: "
                      "reefs, a sunken aircraft and a sea turtle."),
        'primary': {'label': 'View the series on Instagram', 'url': 'https://www.instagram.com/p/De_md_flyqA/'},
        'cover': 'dive-reef',
        'thumb': 'dive-reef',
        'suite': [
            {'type': 'wide', 'img': 'dive-wreck', 'gap': 'm'},
            {'type': 'pair', 'imgs': ['dive-torch', 'dive-coral'], 'gap': 'l'},
            {'type': 'detail', 'img': 'dive-turtle', 'align': 'right', 'gap': 'l',
             'caption': 'Still from the clip “Turtle munchies”.'},
            {'type': 'wide', 'img': 'dive-surface', 'gap': 'm'},
        ],
        'links': [
            {'label': 'Photo series on Instagram', 'url': 'https://www.instagram.com/p/De_md_flyqA/'},
            {'label': '“Turtle munchies” on Instagram', 'url': 'https://www.instagram.com/reel/DepFufGpkkO/'},
        ],
    },
    {
        'slug': 'kebnekaise',
        'title': 'Kebnekaise',
        'kind': 'Hiking film & photo',
        'location': 'Kebnekaise, Sweden',
        'year': '2026',
        'lead': ("A summer hike in Kebnekaise with friends, cut into a short film. "
                 "The photograph of the climb is, in Ruben's words, one of his favourites from the summer."),
        'meta_desc': ("Kebnekaise, a summer hiking film and photograph by Ruben Svanerud, "
                      "shot on a hike with friends in the Swedish mountains."),
        'primary': {'label': 'Watch the film on Instagram', 'url': 'https://www.instagram.com/reel/DgIWM6nN4HL/'},
        'cover': 'keb-climb',
        'thumb': 'keb-climb',
        'suite': [
            {'type': 'detail', 'img': 'keb-hike', 'align': 'left', 'gap': 'm',
             'caption': 'Still from the film.'},
        ],
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
        'location': 'Trädgården',
        'year': '2026',
        'lead': ("Ruben films the boxer Erwa at ringside and backstage, from fight night at Trädgården "
                 "toward the European Championships, EM26. The films are published on Erwa’s and Ruben’s Instagram."),
        'meta_desc': ("EM26 Is Next, behind-the-scenes boxing films with the boxer Erwa, shot by Ruben Svanerud "
                      "at fight night at Trädgården."),
        'primary': {'label': 'Watch on Instagram', 'url': 'https://www.instagram.com/reel/Dc5vxR5pzYn/'},
        'cover_pair': ['box-win', 'box-rig'],
        'cover_pos': ['50% 30%', '50% 100%'],
        'thumb': 'box-win',
        'suite': [],
        'links': [
            {'label': '“EM26 is next” on Instagram', 'url': 'https://www.instagram.com/reel/Dc5vxR5pzYn/'},
            {'label': 'Fight night on Erwa’s Instagram', 'url': 'https://www.instagram.com/reel/DdCWilcOnO4/'},
            {'label': 'Ringside and backstage, on Erwa’s Instagram',
             'url': 'https://www.instagram.com/reel/DcBQ4YgM9mo/'},
        ],
    },
]

SHORT_FORM = [
    {'img': 'ski-poster', 'label': 'For the Love of Ski', 'kind': 'Reel', 'pos': '50% 50%',
     'url': 'https://www.instagram.com/reel/DfIPBwspRGu/'},
    {'img': 'box-win', 'label': 'Fight night, with Erwa', 'kind': 'Reel', 'pos': '50% 60%',
     'url': 'https://www.instagram.com/reel/DdCWilcOnO4/'},
    {'img': 'box-rig', 'label': 'EM26 Is Next', 'kind': 'Reel', 'pos': '50% 85%',
     'url': 'https://www.instagram.com/reel/Dc5vxR5pzYn/'},
]
