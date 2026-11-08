#!/usr/bin/env python3
"""Patch v442 -> v443:
- chat-msg-meta: flex-wrap so timestamp never gets squished
- timestamp span: margin-left:auto so it stays right when wrapped
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v442.js'
dst = '_deploy/assets/index-DUcNPOLc-v443.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. chat-msg-meta CSS: add flex-wrap ───────────────────────────────────────
OLD_META = '.chat-msg-meta {\n        display: flex;\n        align-items: center;\n        gap: 6px;\n        padding: 5px 10px;\n      }'
NEW_META = '.chat-msg-meta {\n        display: flex;\n        align-items: center;\n        flex-wrap: wrap;\n        gap: 4px 6px;\n        padding: 5px 10px;\n      }'
if OLD_META in content:
    content = content.replace(OLD_META, NEW_META, 1)
    print('OK: chat-msg-meta flex-wrap added')
else:
    errors.append('FAIL: .chat-msg-meta CSS not found')

# ── 2. Timestamp span: add marginLeft:auto so it stays right on wrap ──────────
OLD_TS = 'style:{fontSize:11,color:`rgba(0,0,0,0.45)`,fontWeight:400,flexShrink:0,whiteSpace:`nowrap`},children:[`· `,Un(e.created_at)'
NEW_TS = 'style:{fontSize:11,color:`rgba(0,0,0,0.45)`,fontWeight:400,flexShrink:0,whiteSpace:`nowrap`,marginLeft:`auto`},children:[`· `,Un(e.created_at)'
if OLD_TS in content:
    content = content.replace(OLD_TS, NEW_TS, 1)
    print('OK: timestamp marginLeft:auto added')
else:
    errors.append('FAIL: timestamp span not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
