#!/usr/bin/env python3
"""Patch v427 -> v428:
- Postcard (Pr): reduce top padding when huddle has no title so body starts near top
- Post page: same — no top gap when huddle has no title
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v427.js'
dst = '_deploy/assets/index-DUcNPOLc-v428.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Pr postcard: conditional top padding ────────────────────────────────────
OLD_PR_PAD = 'flex:1,padding:`16px 14px`,minWidth:0,display:`flex`,flexDirection:`column`,justifyContent:`flex-start`,textAlign:`left`'
NEW_PR_PAD = 'flex:1,padding:t?`16px 14px`:`10px 14px`,minWidth:0,display:`flex`,flexDirection:`column`,justifyContent:`flex-start`,textAlign:`left`'
if OLD_PR_PAD in content:
    content = content.replace(OLD_PR_PAD, NEW_PR_PAD, 1)
    print('OK: Pr postcard top padding reduced when no title')
else:
    errors.append('FAIL: Pr inner div padding not found')

# ── 2. Post page: remove tiny marginTop gap when no title ─────────────────────
OLD_PP_MT = 'style:{marginTop:c.title?0:4}'
NEW_PP_MT = 'style:{marginTop:0}'
if OLD_PP_MT in content:
    content = content.replace(OLD_PP_MT, NEW_PP_MT, 1)
    print('OK: post page members marginTop normalised to 0')
else:
    errors.append('FAIL: post page marginTop not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
