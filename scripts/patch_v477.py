#!/usr/bin/env python3
"""Patch v476 -> v477: Raise notification panel z-index from 9999 to 10000
so it sits above the ptr-strip (also 9999), covering its black background."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v476.js'
dst = '_deploy/assets/index-DUcNPOLc-v477.js'

content = open(src, encoding='utf-8').read()

OLD = 'position:`fixed`,inset:0,zIndex:9999,display:`flex`,flexDirection:`column`,justifyContent:`flex-end`'
NEW = 'position:`fixed`,inset:0,zIndex:10000,display:`flex`,flexDirection:`column`,justifyContent:`flex-end`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: notification panel zIndex 9999 → 10000')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
