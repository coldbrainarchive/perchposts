#!/usr/bin/env python3
"""Patch v470 -> v471: Profile pill — remove fontSize scaling, just let the
pill grow to fit the username naturally (no maxWidth constraint)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v470.js'
dst = '_deploy/assets/index-DUcNPOLc-v471.js'

content = open(src, encoding='utf-8').read()

OLD = 'cursor:`default`,fontSize:_un&&_un.length>19?Math.max(7,Math.round(11*19/_un.length)):undefined}'
NEW = 'cursor:`default`}'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: profile pill unconstrained — grows to fit username')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
