#!/usr/bin/env python3
"""Patch v355 -> v356:
- Huddles board fetch sends auth headers so backend reads username from JWT
- my-username fetch cached earlier (top-level app component)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v355.js'
dst = '_deploy/assets/index-DUcNPOLc-v356.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Send auth headers with huddles board fetch ─────────────────────────────
# The board fetch currently uses: fetch(turl).then(...)
# For huddles board, we need to send auth headers so backend can read username from JWT
OLD_HUDDLE_FETCH = (
    'if(u&&(u===`feedback`||u===`huddles`)){const _bid=Gn();const _un=localStorage.getItem(`_myUsername`)||null;'
    'if(_bid)turl+=`&req_browser_id=${encodeURIComponent(_bid)}`;'
    'if(_un)turl+=`&req_username=${encodeURIComponent(_un)}`;}'
    'fetch(turl).then(r2=>r2.ok?r2.json():{posts:[]}).then(d2=>{setTagR(Sr(d2.posts||[]))})'
)
NEW_HUDDLE_FETCH = (
    'const _isHuddleBoard=u&&(u===`feedback`||u===`huddles`);'
    'if(_isHuddleBoard){const _bid=Gn();const _un=localStorage.getItem(`_myUsername`)||null;'
    'if(_bid)turl+=`&req_browser_id=${encodeURIComponent(_bid)}`;'
    'if(_un)turl+=`&req_username=${encodeURIComponent(_un)}`;}'
    'fetch(turl,_isHuddleBoard?{headers:er()}:{}).then(r2=>r2.ok?r2.json():{posts:[]}).then(d2=>{setTagR(Sr(d2.posts||[]))})'
)
if OLD_HUDDLE_FETCH in content:
    content = content.replace(OLD_HUDDLE_FETCH, NEW_HUDDLE_FETCH, 1)
    print('OK: huddles board fetch sends auth headers')
else:
    errors.append('FAIL: huddles board fetch not found')

# ── 2. Cache username in localStorage from top-level my-username fetch ─────────
# Find all my-username fetches and ensure they cache to localStorage
OLD_MY_UN = 't.ok&&(async()=>{const _u=(await t.json()).username||null;ee(_u);if(_u)localStorage.setItem(`_myUsername`,_u);})()'
if OLD_MY_UN in content:
    print('OK: username already cached in localStorage (v354 change present)')
else:
    # Try the original pattern
    OLD_MY_UN2 = 't.ok&&ee((await t.json()).username||null)'
    if OLD_MY_UN2 in content:
        NEW_MY_UN2 = 't.ok&&(async()=>{const _u=(await t.json()).username||null;ee(_u);if(_u)localStorage.setItem(`_myUsername`,_u);})()'
        content = content.replace(OLD_MY_UN2, NEW_MY_UN2)
        print(f'OK: username caching applied (replaced {content.count(OLD_MY_UN2)} occurrences)')
    else:
        print('NOTE: my-username cache pattern not found - may already be applied')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
