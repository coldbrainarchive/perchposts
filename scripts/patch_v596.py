#!/usr/bin/env python3
"""Patch v595 -> v596: Fix mobile layout cutoff — revert image from fixed height to maxHeight.
Fixed height was causing the chat window to miscalculate scroll bounds on mobile,
pushing the compose area below the panel viewport."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v595.js'
dst = '_deploy/assets/index-DUcNPOLc-v596.js'

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

# Revert fixed height back to maxHeight — keeps objectFit:cover crop but is layout-safe
patch(
    'style:{width:`100%`,borderRadius:10,display:`block`,height:_mh,objectFit:`cover`,cursor:`zoom-in`}',
    'style:{width:`100%`,borderRadius:10,display:`block`,maxHeight:_mh,objectFit:`cover`,cursor:`zoom-in`}',
    'revert image height to maxHeight for layout safety'
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
