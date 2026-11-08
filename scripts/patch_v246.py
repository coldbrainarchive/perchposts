#!/usr/bin/env python3
"""Patch v245 -> v246: fix DM compose outer div — className was wrongly nested inside style:{}."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v245.js'
dst = '_deploy/assets/index-DUcNPOLc-v246.js'

content = open(src, encoding='utf-8').read()
errors = []

# The bug: outer div has {style:{className:`chat-input-row`,style:{padding:...},...}}
# Should be: {className:`chat-input-row`,style:{padding:...},...}
OLD = '(0,L.jsxs)(`div`,{style:{className:`chat-input-row`,style:{padding:`10px 14px`,borderTop:`1px solid #2e303a`},'
NEW = '(0,L.jsxs)(`div`,{className:`chat-input-row`,style:{padding:`10px 14px`,borderTop:`1px solid #2e303a`},'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: DM compose outer div fixed')
else:
    errors.append('FAIL: broken compose div not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
