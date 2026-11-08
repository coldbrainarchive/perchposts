#!/usr/bin/env python3
"""Patch v390 -> v391:
- Admin pill background: set to white (#ffffff) in huddle search results
- Main search bar: apply CSS filter so bird matches everywhere
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v390.js'
dst = '_deploy/assets/index-DUcNPOLc-v391.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Admin pill background in huddle search pill wrappers ───────────────────
OLD_BG = 'background:Hn(_u.browser_id||null,_u.username)'
NEW_BG = 'background:_u.role===`admin`?`#ffffff`:Hn(_u.browser_id||null,_u.username)'
count = content.count(OLD_BG)
if count == 4:
    content = content.replace(OLD_BG, NEW_BG)
    print(f'OK: admin pill background white in {count} places')
else:
    errors.append(f'FAIL: expected 4 background occurrences, found {count}')

# ── 2. Main search bar: apply CSS filter to bird emoji ────────────────────────
MAIN_OLD = (
    '(0,L.jsx)(`span`,{children:(Jn({username:_u.username,browser_id:null})||{}).e||`\U0001f426`})'
)
MAIN_NEW = (
    '(()=>{const _jd=Jn({username:_u.username,browser_id:null,is_admin:_u.role===`admin`})||{};'
    'return typeof _jd===`object`&&_jd.hat?'
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:``,style:{height:13,width:13,objectFit:`contain`}}):'
    '(0,L.jsx)(`span`,{style:_jd.f?{filter:_jd.f}:{},children:_jd.e||`\U0001f426`});})() '
)
if MAIN_OLD in content:
    content = content.replace(MAIN_OLD, MAIN_NEW, 1)
    print('OK: main search bar bird has CSS filter')
else:
    errors.append('FAIL: main search bar emoji not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
