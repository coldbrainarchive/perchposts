#!/usr/bin/env python3
"""Patch v177 -> v178: anchor admin PNG to bottom so bird body centres in pill."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v177.js'
dst = '_deploy/assets/index-DUcNPOLc-v178.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Pill badge: anchor image bottom so bird fills pill, hat overflows up ───
# Hat ≈ 40% of PNG, bird ≈ 60%. height:1.85em fills badge container with bird.
OLD_PILL_IMG = (
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{'
    'width:`1.6em`,height:`1.6em`,objectFit:`contain`,display:`block`,margin:`auto`}})'
)
NEW_PILL_IMG = (
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{'
    'position:`absolute`,height:`1.85em`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`,'
    'pointerEvents:`none`}})'
)
if OLD_PILL_IMG in content:
    content = content.replace(OLD_PILL_IMG, NEW_PILL_IMG, 1)
    print('OK: pill badge img anchored to bottom')
else:
    errors.append('FAIL: pill badge img not found')

# ── 2. Header bird: wrap in fixed-height box, anchor img to bottom ────────────
OLD_HDR_IMG = (
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{'
    'width:`72px`,height:`72px`,objectFit:`contain`,display:`block`}})'
)
NEW_HDR_IMG = (
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,'
    'width:`64px`,height:`64px`,overflow:`visible`},children:['
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{'
    'position:`absolute`,height:`110px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})'
    ']})'
)
if OLD_HDR_IMG in content:
    content = content.replace(OLD_HDR_IMG, NEW_HDR_IMG, 1)
    print('OK: header bird img anchored to bottom')
else:
    errors.append('FAIL: header bird img not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
