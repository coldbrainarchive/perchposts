#!/usr/bin/env python3
"""Patch v229 -> v230: own comments appear on the right side (iMessage style)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v229.js'
dst = '_deploy/assets/index-DUcNPOLc-v230.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add chat-msg--mine CSS rule after .chat-msg ──────────────────────────
OLD_CSS = (
    '.chat-msg {\n        display: block;\n        align-self: flex-start;\n'
    '        max-width: min(80%, 480px);\n        margin-bottom: 10px;\n      }'
)
NEW_CSS = (
    '.chat-msg {\n        display: block;\n        align-self: flex-start;\n'
    '        max-width: min(80%, 480px);\n        margin-bottom: 10px;\n      }\n\n'
    '      .chat-msg--mine {\n        align-self: flex-end;\n      }\n\n'
    '      .chat-msg--mine .chat-bubble {\n        background: #3b1f6e;\n        color: #f3e8ff;\n      }'
)
if OLD_CSS in content:
    content = content.replace(OLD_CSS, NEW_CSS, 1)
    print('OK: chat-msg--mine CSS added')
else:
    errors.append('FAIL: .chat-msg CSS not found')

# ── 2. Apply chat-msg--mine class when g (isMine) is true ───────────────────
OLD_JSX = 'className:`chat-msg`,"data-comment-id":e.id'
NEW_JSX = 'className:`chat-msg${g?` chat-msg--mine`:``}`,"data-comment-id":e.id'
if OLD_JSX in content:
    content = content.replace(OLD_JSX, NEW_JSX, 1)
    print('OK: chat-msg--mine class applied conditionally')
else:
    errors.append('FAIL: chat-msg className not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
