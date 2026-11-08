#!/usr/bin/env python3
"""Patch v478 -> v479: Change ptr-strip background from #0b0f12 to #1a1d27
so the pull-to-refresh area matches the notification panel gray."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v478.js'
dst = '_deploy/assets/index-DUcNPOLc-v479.js'

content = open(src, encoding='utf-8').read()

OLD = 'zIndex:9999,background:`#0b0f12`,pointerEvents:`none`'
NEW = 'zIndex:9999,background:`#1a1d27`,pointerEvents:`none`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: ptr-strip background #0b0f12 → #1a1d27')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
