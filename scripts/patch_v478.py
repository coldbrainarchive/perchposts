#!/usr/bin/env python3
"""Patch v477 -> v478: Make the notification panel full-screen (minHeight:100%)
so its gray background extends behind the iOS status bar area, removing the
black gap at the top. Remove top border-radius since it now fills the screen."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v477.js'
dst = '_deploy/assets/index-DUcNPOLc-v478.js'

content = open(src, encoding='utf-8').read()

OLD = 'position:`relative`,background:`#1a1d27`,borderRadius:`20px 20px 0 0`,maxHeight:`80vh`'
NEW = 'position:`relative`,background:`#1a1d27`,borderRadius:0,minHeight:`100%`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: panel full-screen, no top border-radius')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
