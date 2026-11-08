#!/usr/bin/env python3
"""Patch v399 -> v400: replace 👍 like icon with 🪽 (wing/flap) on all like buttons"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v399.js'
dst = '_deploy/assets/index-DUcNPOLc-v400.js'

content = open(src, encoding='utf-8').read()

before = content.count('\U0001f44d')
content = content.replace('\U0001f44d', '\U0001fab5')
print(f'OK: replaced {before} 👍 with 🪽')

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
