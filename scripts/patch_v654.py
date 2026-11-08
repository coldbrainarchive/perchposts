#!/usr/bin/env python3
"""Patch v653 -> v654:
Replace v._exitingFs as the one-shot guard in _onFsExit with a session-local
let _fsCalled=false. _exitingFs is a property on the video DOM node and can
get stuck true across sessions if a timeout fails. A local variable in the
button onClick closure is guaranteed fresh every session.
Also explicitly reset v._exitingFs=false at fullscreen entry so onPause
suppression is never stuck from a previous session.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v653.js'
dst = '_deploy/assets/index-DUcNPOLc-v654.js'

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
    'if(v._fsCln)v._fsCln();const _onFsExit=()=>{if(v._exitingFs)return;if(v._fsCln)v._fsCln();v._exitingFs=!0;',
    'v._exitingFs=!1;if(v._fsCln)v._fsCln();let _fsCalled=!1;const _onFsExit=()=>{if(_fsCalled)return;_fsCalled=!0;if(v._fsCln)v._fsCln();v._exitingFs=!0;',
    'session-local _fsCalled guard + reset _exitingFs on entry'
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
