#!/usr/bin/env python3
"""Patch v221 -> v222: Flock fetches its own server list sorted by last_activity."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v221.js'
dst = '_deploy/assets/index-DUcNPOLc-v222.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. TagR effect: let Flock fetch its own list (sort=activity, no board filter) ─
OLD_TAGR = (
    'if((!u&&!d&&!f&&!p)||u===`activity`){setTagR(null);return}'
    'let turl=`${R}/get-posts?limit=500`;'
    'if(u)turl+=`&board=${encodeURIComponent(u)}`;'
)
NEW_TAGR = (
    'if(!u&&!d&&!f&&!p){setTagR(null);return}'
    'let turl=u===`activity`'
    '?`${R}/get-posts?limit=1000&sort=activity`'  # Flock: all posts by last activity
    ':`${R}/get-posts?limit=500`;'
    'if(u&&u!==`activity`)turl+=`&board=${encodeURIComponent(u)}`;'
)
if OLD_TAGR in content:
    content = content.replace(OLD_TAGR, NEW_TAGR, 1)
    print('OK: Flock fetches server list sorted by activity')
else:
    errors.append('FAIL: TagR effect not found')

# ── 2. _bl: remove !y guard so Flock uses TagR too ───────────────────────────
OLD_BL = '(u||d||f||p||_bot)&&!y&&TagR!==null?TagR:e'
NEW_BL = '(u||d||f||p||_bot)&&TagR!==null?TagR:e'
if OLD_BL in content:
    content = content.replace(OLD_BL, NEW_BL, 1)
    print('OK: _bl uses TagR for Flock')
else:
    errors.append('FAIL: _bl condition not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
