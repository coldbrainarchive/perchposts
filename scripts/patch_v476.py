#!/usr/bin/env python3
"""Patch v475 -> v476: Change the notification panel overlay background from
rgba(0,0,0,0.6) to #1a1d27 so the status bar area matches the panel gray."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v475.js'
dst = '_deploy/assets/index-DUcNPOLc-v476.js'

content = open(src, encoding='utf-8').read()

OLD = 'position:`absolute`,inset:0,background:`rgba(0,0,0,0.6)`'
NEW = 'position:`absolute`,inset:0,background:`#1a1d27`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: overlay rgba(0,0,0,0.6) → #1a1d27')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
