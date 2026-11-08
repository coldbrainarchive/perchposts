#!/usr/bin/env python3
"""Patch v474 -> v484: Make the user info section (bird + username, above the
tabs) use black background on mobile so it blends with the native iOS status
bar instead of showing as a different shade."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v474.js'
dst = '_deploy/assets/index-DUcNPOLc-v484.js'

content = open(src, encoding='utf-8').read()

# The user info card background #161920 → #000000 (black, matches status bar)
OLD = 'background:`#161920`,borderRadius:14,border:`1px solid #2e303a`'
NEW = 'background:`#000000`,borderRadius:14,border:`none`'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: user info card → black, no border')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
