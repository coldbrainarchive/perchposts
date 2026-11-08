#!/usr/bin/env python3
"""Patch v181 -> v182: mod panel clean-up; role-change triggers re-login prompt."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v181.js'
dst = '_deploy/assets/index-DUcNPOLc-v182.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Rename "Account" → "Utilities" in the Gr mod panel ────────────────────
# (Only in Gr — the Kr panel uses a tab label, not this heading)
OLD_ACCT_HDR = (
    'fontSize:16,fontWeight:700},children:`Account`}),(0,L.jsx)(`button`,'
)
NEW_ACCT_HDR = (
    'fontSize:16,fontWeight:700},children:`Utilities`}),(0,L.jsx)(`button`,'
)
if OLD_ACCT_HDR in content:
    content = content.replace(OLD_ACCT_HDR, NEW_ACCT_HDR, 1)
    print('OK: Account → Utilities in mod panel')
else:
    errors.append('FAIL: Account heading in Gr not found')

# ── 2. After role change (→ Mod / Demote), show alert telling user to re-login─
# Currently: fetch(...update-member...), _e()
# New: fetch, then if promoting to mod, alert them
OLD_ROLE_CHANGE = (
    'let e=d?`mod`:u?`user`:`mod`,t=$n();'
    'await fetch(`https://daboysforumip.coldbrainarchive.workers.dev/update-member`,'
    '{method:`POST`,headers:{"Content-Type":`application/json`,...t},'
    'body:JSON.stringify({user_id:n.id,role:e})}),_e()'
)
NEW_ROLE_CHANGE = (
    'let e=d?`mod`:u?`user`:`mod`,t=$n();'
    'await fetch(`https://daboysforumip.coldbrainarchive.workers.dev/update-member`,'
    '{method:`POST`,headers:{"Content-Type":`application/json`,...t},'
    'body:JSON.stringify({user_id:n.id,role:e})});'
    '_e();'
    'if(e===`mod`)alert((n.user_metadata?.username||`User`)+` is now a mod — they’ll see their new role after logging out and back in.`)'
)
if OLD_ROLE_CHANGE in content:
    content = content.replace(OLD_ROLE_CHANGE, NEW_ROLE_CHANGE, 1)
    print('OK: role-change now prompts re-login message')
else:
    errors.append('FAIL: role change code not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
