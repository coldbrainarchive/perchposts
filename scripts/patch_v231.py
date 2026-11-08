#!/usr/bin/env python3
"""Patch v230 -> v231: fix isMine — use viewer's browser_id (Gn()) not post author's."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v230.js'
dst = '_deploy/assets/index-DUcNPOLc-v231.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add myUsername prop to Rr signature ───────────────────────────────────
OLD_SIG = (
    'function Rr({comment:e,postBrowserId:t,postUsername:n,canDelete:r,'
    'onDelete:i,canPin:a,onPin:o,onReply:s,onReact:c,reactions:l={},'
    'allComments:u=[],onFindParent:d})'
)
NEW_SIG = (
    'function Rr({comment:e,postBrowserId:t,postUsername:n,myUsername:_myUn=null,'
    'canDelete:r,onDelete:i,canPin:a,onPin:o,onReply:s,onReact:c,reactions:l={},'
    'allComments:u=[],onFindParent:d})'
)
if OLD_SIG in content:
    content = content.replace(OLD_SIG, NEW_SIG, 1)
    print('OK: myUsername added to Rr signature')
else:
    errors.append('FAIL: Rr function signature not found')

# ── 2. Change isMine (g) to use viewer's Gn() instead of post author's t ─────
OLD_G = 'let g=e.browser_id===t&&(n?e.username===n:!e.username),'
NEW_G = 'let g=e.browser_id===Gn()&&(_myUn?e.username===_myUn:!e.username),'
if OLD_G in content:
    content = content.replace(OLD_G, NEW_G, 1)
    print('OK: g (isMine) now uses viewer browser_id')
else:
    errors.append('FAIL: g isMine calculation not found')

# ── 3. Pass myUsername:n into Rr call from Wr (n = memberUsername) ───────────
OLD_CALL = 'postBrowserId:c.browser_id,postUsername:c.username||null,'
NEW_CALL = 'postBrowserId:c.browser_id,postUsername:c.username||null,myUsername:n,'
if OLD_CALL in content:
    content = content.replace(OLD_CALL, NEW_CALL, 1)
    print('OK: myUsername:n passed to Rr')
else:
    errors.append('FAIL: Rr call postBrowserId prop not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
