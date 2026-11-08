#!/usr/bin/env python3
"""Patch v175 -> v176: fix hat position (closer to head); admin pill white."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v175.js'
dst = '_deploy/assets/index-DUcNPOLc-v176.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Fix pill badge hat — sit on head, not float above ─────────────────────
# Use bottom:75% so hat brim overlaps ~25% of the bird's top
OLD_PILL_HAT = (
    'style:{position:`absolute`,top:`-55%`,left:`50%`,'
    'transform:`translateX(-50%)`,fontSize:`1em`,lineHeight:1,'
    'pointerEvents:`none`,zIndex:2},children:`\U0001f3a9`}'
)
NEW_PILL_HAT = (
    'style:{position:`absolute`,bottom:`75%`,left:`50%`,'
    'transform:`translateX(-50%)`,fontSize:`1.1em`,lineHeight:1,'
    'pointerEvents:`none`,zIndex:2},children:`\U0001f3a9`}'
)
if OLD_PILL_HAT in content:
    content = content.replace(OLD_PILL_HAT, NEW_PILL_HAT, 1)
    print('OK: pill hat position fixed')
else:
    errors.append('FAIL: pill hat not found')

# ── 2. Fix header bird hat — same treatment at large size ─────────────────────
OLD_HDR_HAT = (
    'style:{position:`absolute`,top:`-55%`,left:`50%`,'
    'transform:`translateX(-50%)`,fontSize:`44px`,lineHeight:1,'
    'pointerEvents:`none`,zIndex:2},children:`\U0001f3a9`}'
)
NEW_HDR_HAT = (
    'style:{position:`absolute`,bottom:`75%`,left:`50%`,'
    'transform:`translateX(-50%)`,fontSize:`46px`,lineHeight:1,'
    'pointerEvents:`none`,zIndex:2},children:`\U0001f3a9`}'
)
if OLD_HDR_HAT in content:
    content = content.replace(OLD_HDR_HAT, NEW_HDR_HAT, 1)
    print('OK: header hat position fixed')
else:
    errors.append('FAIL: header hat not found')

# ── 3. Admin pill in panel header → white background (matches outside panel) ──
OLD_PILL = 'style:{color:`#0a0a0a`,background:A,borderColor:A,cursor:`default`}'
NEW_PILL = 'style:{color:`#0a0a0a`,background:D?`#ffffff`:A,borderColor:D?`#e2e8f0`:A,cursor:`default`}'
if OLD_PILL in content:
    content = content.replace(OLD_PILL, NEW_PILL, 1)
    print('OK: admin pill in header is now white')
else:
    errors.append('FAIL: admin pill style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
