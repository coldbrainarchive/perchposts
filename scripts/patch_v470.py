#!/usr/bin/env python3
"""Patch v469 -> v470:
Profile sidebar username pill: replace hard truncation (maxWidth:150/ellipsis)
with computed fontSize that shrinks the text to fit.
At 11px bold, ~19 chars fit in the pill. Beyond that, scale down proportionally
to a minimum of 7px so long names stay readable instead of being cut off.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v469.js'
dst = '_deploy/assets/index-DUcNPOLc-v470.js'

content = open(src, encoding='utf-8').read()

OLD = 'cursor:`default`,maxWidth:150,overflow:`hidden`,textOverflow:`ellipsis`}'
NEW = 'cursor:`default`,fontSize:_un&&_un.length>19?Math.max(7,Math.round(11*19/_un.length)):undefined}'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: profile pill switches to shrink-to-fit fontSize')
else:
    print('FAIL: profile pill style not found'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
