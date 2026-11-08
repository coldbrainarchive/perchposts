#!/usr/bin/env python3
"""Patch v207 -> v208: more saturated board colours; better country colour."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v207.js'
dst = '_deploy/assets/index-DUcNPOLc-v208.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Board chips — richer, saturated colours ────────────────────────────────
OLD_COLORS = (
    'let _bc={'
    'activity:`#a5f3fc`,'
    'general:`#93c5fd`,'
    'sports:`#86efac`,'
    '"science-nature":`#f9a8d4`,'
    'random:`#fda4af`,'
    'announcements:`#fde68a`,'
    'feedback:`#6ee7b7`,'
    'cage:`#fb923c`'
    '}[n.slug]||`#e2e8f0`;'
)
NEW_COLORS = (
    'let _bc={'
    'activity:`#22d3ee`,'    # cyan
    'general:`#60a5fa`,'     # blue
    'sports:`#4ade80`,'      # green
    '"science-nature":`#818cf8`,'  # indigo
    'random:`#f87171`,'      # red
    'announcements:`#facc15`,'  # yellow
    'feedback:`#2dd4bf`,'    # teal
    'cage:`#f43f5e`'         # rose/red
    '}[n.slug]||`#e2e8f0`;'
)
if OLD_COLORS in content:
    content = content.replace(OLD_COLORS, NEW_COLORS, 1)
    print('OK: board colours saturated')
else:
    errors.append('FAIL: board colour map not found')

# ── 2. Country/continent chip — warm amber/gold ───────────────────────────────
OLD_COUNTRY = "background:`#fde68a`"
NEW_COUNTRY = "background:`#f59e0b`"
if OLD_COUNTRY in content:
    content = content.replace(OLD_COUNTRY, NEW_COUNTRY, 1)
    print('OK: country chip → amber-500')
else:
    errors.append('FAIL: country chip colour not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
