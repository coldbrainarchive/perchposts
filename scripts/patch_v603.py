#!/usr/bin/env python3
"""Patch v602 -> v603:
- Link preview cards in comments: tapping opens the URL directly instead of
  triggering the mobile bottom-sheet expand. Remove onClick:u from the <a> branch
  of Nr (LinkPreviewCard) so the browser navigates to the link.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v602.js'
dst = '_deploy/assets/index-DUcNPOLc-v603.js'

content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append(f'FAIL ({label}): not found')
    elif n > 1:
        errors.append(f'FAIL ({label}): {n} matches (not unique)')
    else:
        content = content.replace(old, new)
        print(f'OK: {label}')

# Remove onClick:u from the <a> branch in Nr so tapping opens the link directly
patch(
    'rel:`noopener noreferrer`,style:{textDecoration:`none`,display:`block`,marginTop:10},onClick:u,children:d})',
    'rel:`noopener noreferrer`,style:{textDecoration:`none`,display:`block`,marginTop:10},children:d})',
    'link card taps open URL directly (no bottom-sheet expand)'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print(f'Paren delta: {p_delta}, Brace delta: {b_delta}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
