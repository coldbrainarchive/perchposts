#!/usr/bin/env python3
"""Patch v623 -> v624:
Postcard style for all attachments: title at top, full-width Fr attachment below.
Route all attachment types (image, video, link) through the Fr branch, not Pr.
Previously only links used Fr; images/videos used the small Pr thumbnail.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v623.js'
dst = '_deploy/assets/index-DUcNPOLc-v624.js'

content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append('FAIL (' + label + '): not found')
    elif n > 1:
        errors.append('FAIL (' + label + '): ' + str(n) + ' matches')
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

# Change condition: any attachment -> full-width Fr, no attachment -> Pr
patch(
    'p&&p.type===`link`?(0,L.jsxs)(L.Fragment,',
    'p?(0,L.jsxs)(L.Fragment,',
    'all attachments use full-width Fr'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print('Paren delta: ' + str(p_delta) + ', Brace delta: ' + str(b_delta))

open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
