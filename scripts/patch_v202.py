#!/usr/bin/env python3
"""Patch v201 -> v202: rename Log out / Logout → Leave."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v201.js'
dst = '_deploy/assets/index-DUcNPOLc-v202.js'

content = open(src, encoding='utf-8').read()

before = len(content)
content = content.replace('Log out', 'Leave')
content = content.replace('Logout', 'Leave')
print(f'OK: replaced all logout variants with Leave')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
