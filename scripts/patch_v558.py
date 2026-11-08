#!/usr/bin/env python3
"""Patch v557 -> v558: Version bump to pair with bfcache-fix index.html."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v557.js'
dst = '_deploy/assets/index-DUcNPOLc-v558.js'

content = open(src, encoding='utf-8').read()

# No code changes — just creates a new file so the HTML reference changes too
p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
