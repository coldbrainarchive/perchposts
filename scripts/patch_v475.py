#!/usr/bin/env python3
"""Patch v474 -> v475: User info card background #161920 → #1a1d27 to match
the notifications panel background."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v474.js'
dst = '_deploy/assets/index-DUcNPOLc-v475.js'

content = open(src, encoding='utf-8').read()

OLD = 'background:`#161920`,borderRadius:14,border:`1px solid #2e303a`'
NEW = 'background:`#1a1d27`,borderRadius:14,border:`1px solid #2e303a`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: user info card background #161920 → #1a1d27')
else:
    print('FAIL: card background not found'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
