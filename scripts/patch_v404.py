#!/usr/bin/env python3
"""Patch v403 -> v404: reduce left padding on like button pill to tighten left dead space"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v403.js'
dst = '_deploy/assets/index-DUcNPOLc-v404.js'

content = open(src, encoding='utf-8').read()
errors = []

# Postcard (Ir) like button
OLD1 = 'style:r===1&&i?{borderColor:`#c084fc`,background:`rgba(192,132,252,0.15)`}:{}'
NEW1 = 'style:r===1&&i?{borderColor:`#c084fc`,background:`rgba(192,132,252,0.15)`,paddingLeft:5}:{paddingLeft:5}'
if OLD1 in content:
    content = content.replace(OLD1, NEW1, 1)
    print('OK: Ir like button left padding reduced')
else:
    errors.append('FAIL: Ir like style not found')

# Post page (Wr) like button
OLD2 = 'style:re.myVote===1?{borderColor:`#c084fc`,background:`rgba(192,132,252,0.15)`}:{}'
NEW2 = 'style:re.myVote===1?{borderColor:`#c084fc`,background:`rgba(192,132,252,0.15)`,paddingLeft:5}:{paddingLeft:5}'
if OLD2 in content:
    content = content.replace(OLD2, NEW2, 1)
    print('OK: Wr like button left padding reduced')
else:
    errors.append('FAIL: Wr like style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
