#!/usr/bin/env python3
"""Patch v474 -> v489: Add black background to the notification panel header
(bird + username section above the Notifications/Your Nest tab line)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v474.js'
dst = '_deploy/assets/index-DUcNPOLc-v489.js'

content = open(src, encoding='utf-8').read()

OLD = 'padding:`20px 18px 16px`,borderBottom:e?`1px solid #2e303a`:`none`,position:`relative`}'
NEW = 'padding:`20px 18px 16px`,borderBottom:e?`1px solid #2e303a`:`none`,position:`relative`,background:`#000000`}'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: notification panel header → black')
else:
    print('FAIL'); sys.exit(1)

print(f'Parens: {content.count("(")-content.count(")")}, Braces: {content.count("{")-content.count("}")}')
open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
