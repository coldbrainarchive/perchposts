#!/usr/bin/env python3
"""Patch v398 -> v399: rename postchats -> perchposts everywhere in the bundle"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v398.js'
dst = '_deploy/assets/index-DUcNPOLc-v399.js'

content = open(src, encoding='utf-8').read()

before = content.count('postchats')
content = content.replace('postchats', 'perchposts')
after = content.count('perchposts')
print(f'OK: replaced {before} occurrences of postchats -> perchposts')

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
