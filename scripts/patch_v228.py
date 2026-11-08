#!/usr/bin/env python3
"""Patch v227 -> v228: delete post asks 'Are you sure?', then navigates to feed after deletion."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v227.js'
dst = '_deploy/assets/index-DUcNPOLc-v228.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Mod delete in post view: async, await zr(), then navigate to feed ──────
OLD_MOD = (
    'onClick:()=>{confirm(`Delete this post?`)&&zr({type:`delete_post`,post_id:c.id})}'
)
NEW_MOD = (
    'onClick:async()=>{if(!confirm(`Are you sure?`))return;'
    'await zr({type:`delete_post`,post_id:c.id});o(`/`)}'
)
count = content.count(OLD_MOD)
if count > 0:
    content = content.replace(OLD_MOD, NEW_MOD)
    print(f'OK: mod delete updated ({count} occurrence(s))')
else:
    errors.append('FAIL: mod delete handler not found')

# ── 2. User delete in post view: navigate to feed instead of going back ────────
OLD_USER = (
    'onClick:async()=>{confirm(`Delete your post?`)&&'
    '(await fetch(`${R}/delete-my-post`,{method:`POST`,'
    'headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:c.id,browser_id:Gn()})}),o(-1))}'
)
NEW_USER = (
    'onClick:async()=>{if(!confirm(`Are you sure?`))return;'
    'await fetch(`${R}/delete-my-post`,{method:`POST`,'
    'headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({post_id:c.id,browser_id:Gn()})});o(`/`)}'
)
count2 = content.count(OLD_USER)
if count2 > 0:
    content = content.replace(OLD_USER, NEW_USER)
    print(f'OK: user delete updated ({count2} occurrence(s))')
else:
    errors.append('FAIL: user delete handler not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
