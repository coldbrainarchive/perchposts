#!/usr/bin/env python3
"""Patch v220 -> v221:
  - Restore bot engagement filter in Vr (revert v220 mistake)
  - Fix Hr board view: user posts always show on Flock; only bot posts need engagement
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v220.js'
dst = '_deploy/assets/index-DUcNPOLc-v221.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Restore Vr bot filter (undo v220) ─────────────────────────────────────
# v220 removed the bot engagement check, leaving just !0 for all activity posts.
OLD_VR = (
    'b=_bl.filter(e=>u?y?!0:'
    'cr(e)===(sr(u)?.name||u):!0)'
)
NEW_VR = (
    'b=_bl.filter(e=>u?y?fr.includes(e.username)?'
    '(n[e.id]||0)>0||(i[e.id]?.voteCount??0)>0:!0:'
    'cr(e)===(sr(u)?.name||u):!0)'
)
if OLD_VR in content:
    content = content.replace(OLD_VR, NEW_VR, 1)
    print('OK: Vr bot filter restored')
else:
    errors.append('FAIL: Vr activity filter not found')

# ── 2. Fix Hr board view: only gate bots, not real users ─────────────────────
# Old: all posts need (comments>0 OR votes>0)
# New: bot posts need engagement; user posts always show
OLD_HR = '.filter(e=>(r[e.id]||0)>0||(a[e.id]?.voteCount??0)>0).filter(e=>!e.pinned||e.pinned_global)'
NEW_HR = '.filter(e=>!fr.includes(e.username)||(r[e.id]||0)>0||(a[e.id]?.voteCount??0)>0).filter(e=>!e.pinned||e.pinned_global)'
if OLD_HR in content:
    content = content.replace(OLD_HR, NEW_HR, 1)
    print('OK: Hr Flock filter fixed — user posts always show')
else:
    errors.append('FAIL: Hr activity engagement filter not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
