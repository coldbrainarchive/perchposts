#!/usr/bin/env python3
"""Patch v474 -> v488: Black only from top of panel to the Notifications/Nest
tab line. Panel stays #1a1d27 for tab content. Top header + user info → black."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v474.js'
dst = '_deploy/assets/index-DUcNPOLc-v488.js'

content = open(src, encoding='utf-8').read()
errors = []

# 1. Drag handle header → add black background
OLD_HDR = '{display:`flex`,alignItems:`center`,justifyContent:`center`,padding:`14px 20px 8px`,flexShrink:0}'
NEW_HDR = '{display:`flex`,alignItems:`center`,justifyContent:`center`,padding:`14px 20px 8px`,flexShrink:0,background:`#000000`}'
if OLD_HDR in content:
    content = content.replace(OLD_HDR, NEW_HDR, 1)
    print('OK: header → black')
else:
    errors.append('FAIL: header')

# 2. User info card → black, no border/radius
OLD_CARD = 'background:`#161920`,borderRadius:14,border:`1px solid #2e303a`,overflow:`hidden`'
NEW_CARD = 'background:`#000000`,borderRadius:0,border:`none`,overflow:`hidden`'
if OLD_CARD in content:
    content = content.replace(OLD_CARD, NEW_CARD, 1)
    print('OK: user info card → black')
else:
    errors.append('FAIL: card')

if errors:
    print('\nERRORS:'); [print(' ',e) for e in errors]; sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
