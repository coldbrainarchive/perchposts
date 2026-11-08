#!/usr/bin/env python3
"""Patch v434 -> v435:
- Show full username in comment bubbles (no ellipsis truncation)
- Make bubbles slightly smaller (font 13->12px, padding 7/10->6/8px)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v434.js'
dst = '_deploy/assets/index-DUcNPOLc-v435.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Username span: remove overflow/ellipsis ────────────────────────────────
OLD_NAME = 'style:{fontWeight:700,fontSize:11,color:`#0a0a0a`,flex:1,minWidth:0,whiteSpace:`nowrap`,overflow:`hidden`,textOverflow:`ellipsis`}'
NEW_NAME = 'style:{fontWeight:700,fontSize:11,color:`#0a0a0a`,whiteSpace:`nowrap`}'
if OLD_NAME in content:
    content = content.replace(OLD_NAME, NEW_NAME, 1)
    print('OK: username span no longer truncated')
else:
    errors.append('FAIL: username span style not found')

# ── 2. chat-msg-meta: remove overflow:hidden so username can show fully ───────
OLD_META = '.chat-msg-meta {\n        display: flex;\n        align-items: center;\n        gap: 6px;\n        padding: 5px 10px;\n        overflow: hidden;\n      }'
NEW_META = '.chat-msg-meta {\n        display: flex;\n        align-items: center;\n        gap: 6px;\n        padding: 5px 10px;\n      }'
if OLD_META in content:
    content = content.replace(OLD_META, NEW_META, 1)
    print('OK: chat-msg-meta overflow:hidden removed')
else:
    errors.append('FAIL: .chat-msg-meta not found')

# ── 3. Bubble: slightly smaller font + padding ────────────────────────────────
OLD_BUBBLE = '.dm-outer .chat-bubble {\n        background: #252836;\n        color: #e2e8f0;\n        border-radius: 14px 14px 14px 4px;\n        padding: 7px 10px;\n        font-size: 13px;'
NEW_BUBBLE = '.dm-outer .chat-bubble {\n        background: #252836;\n        color: #e2e8f0;\n        border-radius: 14px 14px 14px 4px;\n        padding: 6px 8px;\n        font-size: 12px;'
if OLD_BUBBLE in content:
    content = content.replace(OLD_BUBBLE, NEW_BUBBLE, 1)
    print('OK: bubble font 13->12px, padding 7/10->6/8px')
else:
    errors.append('FAIL: .dm-outer .chat-bubble not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
