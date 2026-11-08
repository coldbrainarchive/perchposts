#!/usr/bin/env python3
"""Patch v162 -> v163: update rank emojis."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v162.js'
dst = '_deploy/assets/index-DUcNPOLc-v163.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD_RANKS = (
    'var _RANKS=['
    '{min:-1/0,max:-1,e:`\U0001f9a6`,n:`Endangered`,d:`At this rate, extinction isn’t far off.`},'
    '{min:0,max:9,e:`\U0001f424`,n:`Hatchling`,d:`Fresh out of the egg. Everything is new, and worms are still a mystery.`},'
    '{min:10,max:24,e:`\U0001f423`,n:`Nestling`,d:`Safe in the nest, chirping loudly and getting the hang of things.`},'
    '{min:25,max:49,e:`\U0001f425`,n:`Fledgling`,d:`Wings are working (mostly). Small hops, big ambitions.`},'
    '{min:50,max:99,e:`\U0001f426`,n:`Forager`,d:`Starting to find worms on your own with mixed success.`},'
    '{min:100,max:199,e:`\U0001f985`,n:`Bird of Prey`,d:`Highly skilled at hunting and locating food. Sharp instincts and precise execution.`},'
    '{min:200,max:299,e:`\U0001f54a️`,n:`Mixed-Flock Attendant`,d:`Moves between groups effortlessly, thriving in shared ecosystems and cooperative flocks.`},'
    '{min:300,max:499,e:`\U0001f9a2`,n:`Seasoned Migrant`,d:`Experienced, far-traveled, and resourceful. You adapt wherever the flock moves.`},'
    '{min:500,max:699,e:`\U0001f30d`,n:`Continental Migrant`,d:`You’ve gone beyond familiar skies. Wide-ranging, observant, and globally aware.`},'
    '{min:700,max:899,e:`\U0001f99c`,n:`Peak Plumage`,d:`Feathers flawless, presence undeniable. A standout across all flocks.`},'
    '{min:900,max:1499,e:`\U0001f9a9`,n:`Master Layer`,d:`Thriving and prolific—your legacy is well underway.`},'
    '{min:1500,max:1/0,e:`\U0001f99a`,n:`Legendary Brood`,d:`The pinnacle. Thriving, dominant, and the envy of the flock.`}'
    '];'
)
NEW_RANKS = (
    'var _RANKS=['
    '{min:-1/0,max:-1,e:`\U0001f9a4`,n:`Endangered`,d:`At this rate, extinction isn’t far off.`},'
    '{min:0,max:9,e:`\U0001f423`,n:`Hatchling`,d:`Fresh out of the egg. Everything is new, and worms are still a mystery.`},'
    '{min:10,max:24,e:`\U0001f425`,n:`Nestling`,d:`Safe in the nest, chirping loudly and getting the hang of things.`},'
    '{min:25,max:49,e:`\U0001f424`,n:`Fledgling`,d:`Wings are working (mostly). Small hops, big ambitions.`},'
    '{min:50,max:99,e:`\U0001f426‍⬛`,n:`Forager`,d:`Starting to find worms on your own with mixed success.`},'
    '{min:100,max:199,e:`\U0001f985`,n:`Bird of Prey`,d:`Highly skilled at hunting and locating food. Sharp instincts and precise execution.`},'
    '{min:200,max:299,e:`\U0001f54a️`,n:`Mixed-Flock Attendant`,d:`Moves between groups effortlessly, thriving in shared ecosystems and cooperative flocks.`},'
    '{min:300,max:499,e:`\U0001f986`,n:`Seasoned Migrant`,d:`Experienced, far-traveled, and resourceful. You adapt wherever the flock moves.`},'
    '{min:500,max:699,e:`\U0001f30d`,n:`Continental Migrant`,d:`You’ve gone beyond familiar skies. Wide-ranging, observant, and globally aware.`},'
    '{min:700,max:899,e:`\U0001f99c`,n:`Peak Plumage`,d:`Feathers flawless, presence undeniable. A standout across all flocks.`},'
    '{min:900,max:1499,e:`\U0001fabf`,n:`Master Layer`,d:`Thriving and prolific—your legacy is well underway.`},'
    '{min:1500,max:1/0,e:`\U0001f426‍\U0001f525`,n:`Legendary Brood`,d:`The pinnacle. Thriving, dominant, and the envy of the flock.`}'
    '];'
)

if OLD_RANKS in content:
    content = content.replace(OLD_RANKS, NEW_RANKS, 1)
    print('OK: rank emojis updated')
else:
    errors.append('FAIL: RANKS constant not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
