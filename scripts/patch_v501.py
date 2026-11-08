#!/usr/bin/env python3
"""Patch v500 -> v501: Allow huddle OP to pin their own chirps."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v500.js'
dst = '_deploy/assets/index-DUcNPOLc-v501.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Expand canPin condition and onPin handler ──────────────────────────────
# canPin was only N (mod/admin). Now also allow huddle OP.
# onPin: mods use zr(/mod-action), OP uses /pin-huddle-comment
OLD = ('canPin:N,onPin:async()=>{await zr({type:`pin_comment`,comment_id:e.id,pinned:!e.pinned}),await P()}')
NEW = ('canPin:N||(c.is_huddle&&n&&c.username&&n.toLowerCase()===c.username.toLowerCase()),'
       'onPin:async()=>{'
       'if(N){await zr({type:`pin_comment`,comment_id:e.id,pinned:!e.pinned})}'
       'else{await fetch(`${R}/pin-huddle-comment`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({post_id:c.id,comment_id:e.id,pinned:!e.pinned,req_username:n})})}'
       ';await P()}')

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: canPin expanded + onPin updated for huddle OP')
else:
    errors.append('FAIL: canPin:N,onPin pattern not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
