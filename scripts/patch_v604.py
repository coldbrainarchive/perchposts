#!/usr/bin/env python3
"""Patch v603 -> v604:
Fix scroll-to-bottom jumping on post open.
- Add _isd (initialScrollDone) ref
- On first load: scroll immediately + 400ms + 1200ms (catches late image loads)
- On subsequent comment changes (polling): only scroll if O.current (user just sent)
- This prevents dragging the user back to bottom while they're reading older comments
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v603.js'
dst = '_deploy/assets/index-DUcNPOLc-v604.js'

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

# ── 1. Add _isd ref after existing refs ──
patch(
    '_lpTimer=(0,_.useRef)(null),_lpUrl=(0,_.useRef)(null)',
    '_lpTimer=(0,_.useRef)(null),_lpUrl=(0,_.useRef)(null),_isd=(0,_.useRef)(!1)',
    'add initialScrollDone ref'
)

# ── 2. Replace scroll effect with smarter version ──
patch(
    '(0,_.useEffect)(()=>{let e=D.current;if(!e)return;e.scrollTop=e.scrollHeight;setTimeout(()=>{const _e=D.current;_e&&(_e.scrollTop=_e.scrollHeight)},400)},[u.length,g.length])',
    '(0,_.useEffect)(()=>{let e=D.current;if(!e||!u.length)return;if(!_isd.current){_isd.current=!0;e.scrollTop=e.scrollHeight;setTimeout(()=>{const _e=D.current;_e&&(_e.scrollTop=_e.scrollHeight)},400);setTimeout(()=>{const _e=D.current;_e&&(_e.scrollTop=_e.scrollHeight)},1200);return;}if(O.current){e.scrollTop=e.scrollHeight;}},[u.length,g.length])',
    'scroll only on initial load or after user sends comment'
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
