#!/usr/bin/env python3
"""Patch v400 -> v401: fix wrong emoji — replace 🪵 (wood, U+1FAB5) with 🪽 (wing, U+1FABD)"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v400.js'
dst = '_deploy/assets/index-DUcNPOLc-v401.js'

content = open(src, encoding='utf-8').read()

before = content.count('\U0001fab5')
content = content.replace('\U0001fab5', '\U0001fabd')
print(f'OK: replaced {before} 🪵 with 🪽')

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
