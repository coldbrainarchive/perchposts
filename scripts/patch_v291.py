#!/usr/bin/env python3
"""Patch v290 -> v291: time filter column — center labels above their inputs,
tightly stacked vertically. Wrap each label+input pair in its own centered sub-div."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v290.js'
dst = '_deploy/assets/index-DUcNPOLc-v291.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── Fix the time column container: centered column layout ─────────────────────
OLD_COL_STYLE = (
    'style:{borderLeft:`1px solid #374151`,'
    'minWidth:0,overflow:`hidden`,gridColumn:C?`auto`:`1 / -1`,'
    'flexDirection:`column`,alignItems:`stretch`,gap:4}'
)
NEW_COL_STYLE = (
    'style:{borderLeft:`1px solid #374151`,'
    'minWidth:0,overflow:`hidden`,gridColumn:C?`auto`:`1 / -1`,'
    'flexDirection:`column`,alignItems:`center`,gap:12,padding:`8px 0`}'
)
if OLD_COL_STYLE in content:
    content = content.replace(OLD_COL_STYLE, NEW_COL_STYLE, 1)
    print('OK: time column centered')
else:
    errors.append('FAIL: time column style not found')

# ── Remove side margins from Hour input wrapper ───────────────────────────────
OLD_HOUR_WRAPPER = (
    'style:{height:`32px`,overflow:`hidden`,borderRadius:6,'
    'border:`1px solid rgba(148,163,184,0.2)`,background:`#1e2130`,'
    'margin:`0 10px 8px`,boxSizing:`border-box`,display:`flex`,'
    'alignItems:`center`,justifyContent:`center`},'
    'children:(0,L.jsxs)(`select`'
)
NEW_HOUR_WRAPPER = (
    'style:{height:`32px`,overflow:`hidden`,borderRadius:6,'
    'border:`1px solid rgba(148,163,184,0.2)`,background:`#1e2130`,'
    'width:`calc(100% - 28px)`,boxSizing:`border-box`,display:`flex`,'
    'alignItems:`center`,justifyContent:`center`},'
    'children:(0,L.jsxs)(`select`'
)
if OLD_HOUR_WRAPPER in content:
    content = content.replace(OLD_HOUR_WRAPPER, NEW_HOUR_WRAPPER, 1)
    print('OK: hour wrapper margin removed, width set')
else:
    errors.append('FAIL: hour wrapper not found')

# ── Remove side margins from Day input wrapper ────────────────────────────────
OLD_DAY_WRAPPER = (
    'style:{height:`32px`,overflow:`hidden`,borderRadius:6,'
    'border:`1px solid rgba(148,163,184,0.2)`,background:`#1e2130`,'
    'margin:`0 10px 8px`,boxSizing:`border-box`,display:`flex`,'
    'alignItems:`center`,justifyContent:`center`},'
    'children:(0,L.jsx)(`input`,{type:`date`'
)
NEW_DAY_WRAPPER = (
    'style:{height:`32px`,overflow:`hidden`,borderRadius:6,'
    'border:`1px solid rgba(148,163,184,0.2)`,background:`#1e2130`,'
    'width:`calc(100% - 28px)`,boxSizing:`border-box`,display:`flex`,'
    'alignItems:`center`,justifyContent:`center`},'
    'children:(0,L.jsx)(`input`,{type:`date`'
)
if OLD_DAY_WRAPPER in content:
    content = content.replace(OLD_DAY_WRAPPER, NEW_DAY_WRAPPER, 1)
    print('OK: day wrapper margin removed, width set')
else:
    errors.append('FAIL: day wrapper not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
