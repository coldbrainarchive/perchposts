#!/usr/bin/env python3
"""Patch v443 -> v444:
- Revert flex-wrap on chat-msg-meta (wrapping looks ugly)
- Revert marginLeft:auto on timestamp
- Widen chat-msg max-width so long usernames fit on one line
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v443.js'
dst = '_deploy/assets/index-DUcNPOLc-v444.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Revert flex-wrap on chat-msg-meta ──────────────────────────────────────
OLD_META = '.chat-msg-meta {\n        display: flex;\n        align-items: center;\n        flex-wrap: wrap;\n        gap: 4px 6px;\n        padding: 5px 10px;\n      }'
NEW_META = '.chat-msg-meta {\n        display: flex;\n        align-items: center;\n        gap: 6px;\n        padding: 5px 10px;\n      }'
if OLD_META in content:
    content = content.replace(OLD_META, NEW_META, 1)
    print('OK: flex-wrap reverted on chat-msg-meta')
else:
    errors.append('FAIL: chat-msg-meta not found')

# ── 2. Revert marginLeft:auto on timestamp ────────────────────────────────────
OLD_TS = 'style:{fontSize:11,color:`rgba(0,0,0,0.45)`,fontWeight:400,flexShrink:0,whiteSpace:`nowrap`,marginLeft:`auto`}'
NEW_TS = 'style:{fontSize:11,color:`rgba(0,0,0,0.45)`,fontWeight:400,flexShrink:0,whiteSpace:`nowrap`}'
if OLD_TS in content:
    content = content.replace(OLD_TS, NEW_TS, 1)
    print('OK: marginLeft:auto reverted on timestamp')
else:
    errors.append('FAIL: timestamp span not found')

# ── 3. Widen chat-msg so long usernames fit without wrapping ──────────────────
OLD_MSG = '.chat-msg {\n        display: block;\n        align-self: flex-start;\n        max-width: min(70%, 360px);\n        margin-bottom: 8px;\n      }'
NEW_MSG = '.chat-msg {\n        display: block;\n        align-self: flex-start;\n        max-width: min(88%, 480px);\n        margin-bottom: 8px;\n      }'
if OLD_MSG in content:
    content = content.replace(OLD_MSG, NEW_MSG, 1)
    print('OK: chat-msg max-width widened to min(88%, 480px)')
else:
    errors.append('FAIL: .chat-msg not found')

OLD_DM_MSG = '.dm-outer .chat-msg {\n        display: flex;\n        align-items: flex-end;\n        gap: 8px;\n        max-width: min(72%, 360px);\n        margin-bottom: 4px;\n      }'
NEW_DM_MSG = '.dm-outer .chat-msg {\n        display: flex;\n        align-items: flex-end;\n        gap: 8px;\n        max-width: min(88%, 480px);\n        margin-bottom: 4px;\n      }'
if OLD_DM_MSG in content:
    content = content.replace(OLD_DM_MSG, NEW_DM_MSG, 1)
    print('OK: dm-outer chat-msg max-width widened')
else:
    errors.append('FAIL: .dm-outer .chat-msg not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
