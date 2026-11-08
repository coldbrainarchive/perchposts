#!/usr/bin/env python3
"""Patch v486 -> v487: Use true #000000 so the change is actually visible."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v486.js'
dst = '_deploy/assets/index-DUcNPOLc-v487.js'

content = open(src, encoding='utf-8').read()

# Panels → true black
content = content.replace(
    'background:`#0b0f12`,borderRadius:`20px 20px 0 0`',
    'background:`#000000`,borderRadius:`20px 20px 0 0`'
)

# User info card → true black
content = content.replace(
    'background:`#0b0f12`,borderRadius:0,border:`none`',
    'background:`#000000`,borderRadius:0,border:`none`',
    1
)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
