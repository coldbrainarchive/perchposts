#!/usr/bin/env python3
"""Patch v370 -> v371: fix Leave button to only reload on success, not on error."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v370.js'
dst = '_deploy/assets/index-DUcNPOLc-v371.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    'if(!confirm(`Leave this huddle?`))return;'
    'const _bid=Gn(),_un=localStorage.getItem(`_myUsername`)||null;'
    'fetch(`${R}/leave-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:e.id,browser_id:_bid,username:_un})}).then(()=>window.location.reload());'
)
NEW = (
    'if(!confirm(`Leave this huddle?`))return;'
    'const _bid=Gn(),_un=localStorage.getItem(`_myUsername`)||null;'
    'fetch(`${R}/leave-huddle`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:e.id,browser_id:_bid,username:_un})})'
    '.then(async _r=>{if(_r.ok){window.location.reload();}else{const _j=await _r.json().catch(()=>({}));alert(_j.error||`Could not leave huddle`);}});'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: Leave button only reloads on success')
else:
    errors.append('FAIL: Leave button handler not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
