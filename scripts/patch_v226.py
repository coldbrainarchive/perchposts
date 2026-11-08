#!/usr/bin/env python3
"""Rebuild from v219: apply only the two Flock fixes (Hr user-posts fix + Flock server fetch)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v219.js'
dst = '_deploy/assets/index-DUcNPOLc-v226.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── Fix 1: Hr board view — only gate bot posts, user posts always show ────────
# Old: ALL posts on activity board need engagement
# New: only bot posts need engagement
OLD_HR = '.filter(e=>(r[e.id]||0)>0||(a[e.id]?.voteCount??0)>0).filter(e=>!e.pinned||e.pinned_global)'
NEW_HR = '.filter(e=>!fr.includes(e.username)||(r[e.id]||0)>0||(a[e.id]?.voteCount??0)>0).filter(e=>!e.pinned||e.pinned_global)'
if OLD_HR in content:
    content = content.replace(OLD_HR, NEW_HR, 1)
    print('OK: Hr Flock — user posts always show')
else:
    errors.append('FAIL: Hr activity filter not found')

# ── Fix 2: Vr TagR — Flock fetches its own server list sorted by activity ─────
# Old: activity board skips TagR and falls back to cached 500-post list
# New: Flock fetches up to 1000 posts sorted by last_activity from server
OLD_TAGR = 'if(!u&&!d&&!f&&!p){setTagR(null);return}let turl=u===`activity`?`${R}/get-posts?limit=1000&sort=activity`:`${R}/get-posts?limit=500`;if(u&&u!==`activity`)turl+=`&board=${encodeURIComponent(u)}`;'
NEW_TAGR = 'if(!u&&!d&&!f&&!p){setTagR(null);return}let turl=u===`activity`?`${R}/get-posts?limit=2000&sort=activity`:`${R}/get-posts?limit=500`;if(u&&u!==`activity`)turl+=`&board=${encodeURIComponent(u)}`;'

# Check if this was already applied (v222 state)
if OLD_TAGR in content:
    content = content.replace(OLD_TAGR, NEW_TAGR, 1)
    print('OK: Flock TagR fetch limit raised to 2000')
elif 'limit=1000&sort=activity' in content:
    # Already at 1000, just bump to 2000
    content = content.replace('limit=1000&sort=activity', 'limit=2000&sort=activity', 1)
    print('OK: Flock TagR fetch raised to 2000')
else:
    # v219 has the early return for activity — remove it and add dedicated fetch
    OLD_TAGR_V219 = 'if((!u&&!d&&!f&&!p)||u===`activity`){setTagR(null);return}let turl=`${R}/get-posts?limit=500`;if(u)turl+=`&board=${encodeURIComponent(u)}`;'
    NEW_TAGR_V219 = 'if(!u&&!d&&!f&&!p){setTagR(null);return}let turl=u===`activity`?`${R}/get-posts?limit=2000&sort=activity`:`${R}/get-posts?limit=500`;if(u&&u!==`activity`)turl+=`&board=${encodeURIComponent(u)}`;'
    if OLD_TAGR_V219 in content:
        content = content.replace(OLD_TAGR_V219, NEW_TAGR_V219, 1)
        print('OK: Flock TagR fetch added (2000 posts by activity)')
    else:
        errors.append('FAIL: TagR effect not found in any expected form')

# ── Fix 3: _bl — remove !y guard so Flock uses TagR ─────────────────────────
OLD_BL = '(u||d||f||p||_bot)&&!y&&TagR!==null?TagR:e'
NEW_BL = '(u||d||f||p||_bot)&&TagR!==null?TagR:e'
if OLD_BL in content:
    content = content.replace(OLD_BL, NEW_BL, 1)
    print('OK: _bl uses TagR for Flock board')
elif '(u||d||f||p||_bot)&&TagR!==null?TagR:e' in content:
    print('OK: _bl already correct')
else:
    errors.append('FAIL: _bl condition not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
