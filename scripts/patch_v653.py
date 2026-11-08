#!/usr/bin/env python3
"""Patch v652 -> v653:
Add if(v._exitingFs)return at the very top of _onFsExit so that no matter
how many times it's called (both webkitendfullscreen and fullscreenchange
can fire in the same tick on some iOS versions), only the first invocation
does anything. _exitingFs is already reset to false in the 300ms timeout,
so subsequent fullscreen sessions work correctly.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v652.js'
dst = '_deploy/assets/index-DUcNPOLc-v653.js'

content = open(src, encoding='utf-8').read()
errors = []
q = chr(0x60)

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

patch(
    'const _onFsExit=()=>{if(v._fsCln)v._fsCln();v._exitingFs=!0;',
    'const _onFsExit=()=>{if(v._exitingFs)return;if(v._fsCln)v._fsCln();v._exitingFs=!0;',
    'guard _onFsExit against double-fire with _exitingFs check'
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
