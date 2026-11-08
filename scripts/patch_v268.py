#!/usr/bin/env python3
"""Patch v266 -> v268: fix DM thread — remove comments-panel, use flex:1 to fill panel."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v266.js'
dst = '_deploy/assets/index-DUcNPOLc-v268.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = 'className:`content-card comments-panel`,style:{padding:0,overflow:`clip`,display:`flex`,flexDirection:`column`,height:`min(600px, 80dvh)`},'
NEW = 'style:{display:`flex`,flexDirection:`column`,flex:1,minHeight:0,overflow:`hidden`},'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: comments-panel removed, thread uses flex:1')
else:
    errors.append('FAIL: target not found')
    print('Content around panel:', repr(content[content.find('content-card comments-panel')-10:content.find('content-card comments-panel')+200]))

if errors:
    for e in errors: print(e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
