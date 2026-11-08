#!/usr/bin/env python3
"""Patch v323 -> v324: fix like button flicker (0→2→0).
Root cause: background Dr() vote refresh overwrites the just-voted state with
stale D1 data. Fix:
1. Use a module-level _lastVoteTs to track when a vote was cast
2. Skip the ie() update from background Dr if < 3s since last vote
3. Add optimistic update so UI responds instantly"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v323.js'
dst = '_deploy/assets/index-DUcNPOLc-v324.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add module-level timestamp before the Tr function ─────────────────────
OLD_TR = 'async function Tr(e,t){'
NEW_TR = 'let _lastVoteTs=0;async function Tr(e,t){'
if OLD_TR in content:
    content = content.replace(OLD_TR, NEW_TR, 1)
    print('OK: _lastVoteTs module variable added')
else:
    errors.append('FAIL: Tr function not found')

# ── 2. Optimistic update + stamp vote time in onClick ─────────────────────────
OLD_CLICK = (
    't.preventDefault();let n=await Tr(c.id,re.myVote===1?0:1);'
    'n.success&&ie({score:n.score,myVote:n.myVo'
)
NEW_CLICK = (
    't.preventDefault();'
    'const _nv=re.myVote===1?0:1;'
    'const _os=re.score+_nv-(re.myVote||0);'
    'ie({score:_os,myVote:_nv});'   # optimistic immediately
    '_lastVoteTs=Date.now();'        # stamp so background skip works
    'let n=await Tr(c.id,_nv);'
    'if(n.success)ie({score:n.score,myVote:n.myVo'  # confirm with server
)
if OLD_CLICK in content:
    content = content.replace(OLD_CLICK, NEW_CLICK, 1)
    print('OK: optimistic update + vote timestamp added to onClick')
else:
    errors.append('FAIL: vote onClick not found')

# ── 3. Skip background Dr update within 3s of a vote ─────────────────────────
OLD_REFRESH = 't?.id&&ie(u[t.id]||{score:0,myVote:0})'
NEW_REFRESH = 't?.id&&(Date.now()-_lastVoteTs>3000)&&ie(u[t.id]||{score:0,myVote:0})'
if OLD_REFRESH in content:
    content = content.replace(OLD_REFRESH, NEW_REFRESH, 1)
    print('OK: background Dr refresh skipped for 3s after vote')
else:
    errors.append('FAIL: background refresh ie() not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
