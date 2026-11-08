#!/usr/bin/env python3
"""Patch v109 -> v110: cage UX on new post form.
- Show cage notice banner on new post page when user is caged
- Hide country pill/selector when caged
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v109.js'
dst = '_deploy/assets/index-DUcNPOLc-v110.js'

content = open(src, encoding='utf-8').read()
errors = []

CAGE_NOTICE = (
    '(0,L.jsx)(`div`,{style:{background:`rgba(251,191,36,0.08)`,border:`1px solid rgba(251,191,36,0.25)`,borderRadius:10,'
    'padding:`8px 12px`,margin:`0 0 10px`,fontSize:12,color:`#fbbf24`,textAlign:`center`},'
    'children:`\U0001fab9 You’ve been caged — you can only post and comment in the Cage tag.`})'
)

# 1. Inject cage notice before feed-post-main div
OLD_MAIN = '(0,L.jsxs)(`div`,{className:`feed-post-main`,style:{paddingBottom:0,borderBottom:`none`},children:[(0,L.jsx)(`div`,{className:`feed-post-author-row`'
NEW_MAIN = f'p&&{CAGE_NOTICE},{OLD_MAIN}'

if OLD_MAIN in content:
    content = content.replace(OLD_MAIN, NEW_MAIN, 1)
    print('OK: cage notice banner injected')
else:
    errors.append('FAIL: feed-post-main insertion point not found')

# 2. Hide country pill when caged (v&&... -> v&&!p&&...)
OLD_COUNTRY = 'v&&(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:4},children:[(0,L.jsx)(kr,{country:v,small:!0})'
NEW_COUNTRY = 'v&&!p&&(0,L.jsxs)(`span`,{style:{display:`inline-flex`,alignItems:`center`,gap:4},children:[(0,L.jsx)(kr,{country:v,small:!0})'

if OLD_COUNTRY in content:
    content = content.replace(OLD_COUNTRY, NEW_COUNTRY, 1)
    print('OK: country pill hidden when caged')
else:
    errors.append('FAIL: country pill pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
