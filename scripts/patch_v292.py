#!/usr/bin/env python3
"""Patch v291 -> v292: restructure time column — wrap each label+input in a centered
sub-div so HOUR sits directly above its dropdown and DAY directly above its date picker."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v291.js'
dst = '_deploy/assets/index-DUcNPOLc-v292.js'

content = open(src, encoding='utf-8').read()
errors = []

# Replace the 4 flat children of the time column with 2 wrapped sub-divs
# OLD: [Hour-label, hour-wrapper, Day-label, day-wrapper]
# NEW: [div{col,center}[Hour-label, hour-wrapper], div{col,center}[Day-label, day-wrapper]]

OLD_HOUR_LABEL = (
    '(0,L.jsx)(`div`,{className:`search-section-label`,children:`Hour`}),'
    '(0,L.jsx)(`div`,{style:{height:`32px`,overflow:`hidden`,borderRadius:6,'
    'border:`1px solid rgba(148,163,184,0.2)`,background:`#1e2130`,'
    'width:`calc(100% - 28px)`,boxSizing:`border-box`,display:`flex`,'
    'alignItems:`center`,justifyContent:`center`},'
    'children:(0,L.jsxs)(`select`'
)
NEW_HOUR_LABEL = (
    '(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,alignItems:`center`,gap:6,width:`100%`},children:['
    '(0,L.jsx)(`div`,{className:`search-section-label`,style:{flexBasis:`auto`,padding:`0 0 2px`},children:`Hour`}),'
    '(0,L.jsx)(`div`,{style:{height:`32px`,overflow:`hidden`,borderRadius:6,'
    'border:`1px solid rgba(148,163,184,0.2)`,background:`#1e2130`,'
    'width:`calc(100% - 28px)`,boxSizing:`border-box`,display:`flex`,'
    'alignItems:`center`,justifyContent:`center`},'
    'children:(0,L.jsxs)(`select`'
)
if OLD_HOUR_LABEL in content:
    content = content.replace(OLD_HOUR_LABEL, NEW_HOUR_LABEL, 1)
    print('OK: Hour section wrapped in sub-div')
else:
    errors.append('FAIL: Hour label+wrapper anchor not found')

# Close the Hour sub-div — it ends just before Day label
# Find the pattern: ...})}), then Day label starts
# The hour select ends with: ...i+1))]})} then , then Day label
OLD_HOUR_CLOSE = (
    'h ago`},i+1))]})})'
    ',(0,L.jsx)(`div`,{className:`search-section-label`,children:`Day`})'
)
NEW_HOUR_CLOSE = (
    'h ago`},i+1))]})})'
    ']})'  # close Hour sub-div children + div
    ',(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,alignItems:`center`,gap:6,width:`100%`},children:['
    '(0,L.jsx)(`div`,{className:`search-section-label`,style:{flexBasis:`auto`,padding:`0 0 2px`},children:`Day`})'
)
if OLD_HOUR_CLOSE in content:
    content = content.replace(OLD_HOUR_CLOSE, NEW_HOUR_CLOSE, 1)
    print('OK: Hour sub-div closed; Day sub-div opened')
else:
    errors.append('FAIL: Hour close / Day open not found')

# Close the Day sub-div — after the date input, close [children, sub-div]
OLD_DAY_CLOSE = (
    'colorScheme:`dark`,boxSizing:`border-box`,textAlign:`center`}})})]})]})'
)
NEW_DAY_CLOSE = (
    'colorScheme:`dark`,boxSizing:`border-box`,textAlign:`center`}})})]})' # date input + wrapper close
    ']})'   # Day sub-div children + div
    ']})'   # time column children + div (existing outer close)
)
if OLD_DAY_CLOSE in content:
    content = content.replace(OLD_DAY_CLOSE, NEW_DAY_CLOSE, 1)
    print('OK: Day sub-div closed')
else:
    errors.append('FAIL: Day close not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
