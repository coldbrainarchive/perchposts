#!/usr/bin/env python3
"""Patch v273 -> v274: fix DM thread race condition — conversations were mixing when
switching threads because a slow fetch from thread A could overwrite thread B's messages.
Fix: use AbortController so cleanup cancels the in-flight fetch when _dmThread changes."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v273.js'
dst = '_deploy/assets/index-DUcNPOLc-v274.js'

content = open(src, encoding='utf-8').read()
errors = []

# Replace the dm-thread useEffect with an AbortController version.
# Old: no cleanup — if user switches threads while a fetch is in flight, the old
# fetch resolves later and overwrites the new thread's messages.
# New: AbortController returned as cleanup aborts the stale fetch.
OLD_EFFECT = (
    '(0,_.useEffect)(()=>{if(!_dmThread||!e)return;'
    '(async()=>{let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[])})()},[_dmThread,e])'
)
NEW_EFFECT = (
    '(0,_.useEffect)(()=>{'
    'if(!_dmThread||!e)return;'
    'let _ac=new AbortController();'
    '(async()=>{'
    'try{'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er(),signal:_ac.signal});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);'
    '}catch(_e){}'  # AbortError is caught silently
    '})();'
    'return()=>_ac.abort();'
    '},[_dmThread,e])'
)

if OLD_EFFECT in content:
    content = content.replace(OLD_EFFECT, NEW_EFFECT, 1)
    print('OK: dm-thread useEffect uses AbortController to prevent stale fetch overwrite')
else:
    errors.append('FAIL: dm-thread useEffect not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
