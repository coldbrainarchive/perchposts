#!/usr/bin/env python3
"""Patch v231 -> v232: fix OP badge broken in v231 — separate isOp (g) from isMine (_isMe)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v231.js'
dst = '_deploy/assets/index-DUcNPOLc-v232.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Revert g back to OP check (post author), add _isMe for viewer's own comments ─
OLD_G = 'let g=e.browser_id===Gn()&&(_myUn?e.username===_myUn:!e.username),'
NEW_G = (
    'let g=e.browser_id===t&&(n?e.username===n:!e.username),'
    '_isMe=e.browser_id===Gn()&&(_myUn?e.username===_myUn:!e.username),'
)
if OLD_G in content:
    content = content.replace(OLD_G, NEW_G, 1)
    print('OK: g restored to OP check, _isMe added for viewer')
else:
    errors.append('FAIL: g calculation not found')

# ── 2. Use _isMe (not g) for the chat-msg--mine class ────────────────────────
OLD_CLASS = 'className:`chat-msg${g?` chat-msg--mine`:``}`'
NEW_CLASS = 'className:`chat-msg${_isMe?` chat-msg--mine`:``}`'
if OLD_CLASS in content:
    content = content.replace(OLD_CLASS, NEW_CLASS, 1)
    print('OK: chat-msg--mine now uses _isMe')
else:
    errors.append('FAIL: chat-msg className not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
