#!/usr/bin/env python3
"""Patch v433 -> v434:
Chirp/comment bubbles: reduce max-width and padding so they feel proportional
to the rest of the post page rather than taking up most of the screen width.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v433.js'
dst = '_deploy/assets/index-DUcNPOLc-v434.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. .chat-msg: tighter max-width and margin ────────────────────────────────
OLD_MSG = '.chat-msg {\n        display: block;\n        align-self: flex-start;\n        max-width: min(80%, 480px);\n        margin-bottom: 10px;\n      }'
NEW_MSG = '.chat-msg {\n        display: block;\n        align-self: flex-start;\n        max-width: min(70%, 360px);\n        margin-bottom: 8px;\n      }'
if OLD_MSG in content:
    content = content.replace(OLD_MSG, NEW_MSG, 1)
    print('OK: .chat-msg max-width 80%/480px → 70%/360px')
else:
    errors.append('FAIL: .chat-msg not found')

# ── 2. .dm-outer .chat-msg: same proportional reduction ──────────────────────
OLD_DM_MSG = '.dm-outer .chat-msg {\n        display: flex;\n        align-items: flex-end;\n        gap: 8px;\n        max-width: min(82%, 480px);\n        margin-bottom: 4px;\n      }'
NEW_DM_MSG = '.dm-outer .chat-msg {\n        display: flex;\n        align-items: flex-end;\n        gap: 8px;\n        max-width: min(72%, 360px);\n        margin-bottom: 4px;\n      }'
if OLD_DM_MSG in content:
    content = content.replace(OLD_DM_MSG, NEW_DM_MSG, 1)
    print('OK: .dm-outer .chat-msg max-width 82%/480px → 72%/360px')
else:
    errors.append('FAIL: .dm-outer .chat-msg not found')

# ── 3. .dm-outer .chat-bubble: tighter padding and font-size ─────────────────
OLD_BUBBLE = '.dm-outer .chat-bubble {\n        background: #252836;\n        color: #e2e8f0;\n        border-radius: 18px 18px 18px 4px;\n        padding: 8px 12px;\n        font-size: 13px;\n        line-height: 1.4;\n        cursor: pointer;\n        word-break: break-word;\n        transition: opacity 0.15s;\n        display: inline-block;\n        max-width: 100%;\n      }'
NEW_BUBBLE = '.dm-outer .chat-bubble {\n        background: #252836;\n        color: #e2e8f0;\n        border-radius: 14px 14px 14px 4px;\n        padding: 7px 10px;\n        font-size: 13px;\n        line-height: 1.4;\n        cursor: pointer;\n        word-break: break-word;\n        transition: opacity 0.15s;\n        display: inline-block;\n        max-width: 100%;\n      }'
if OLD_BUBBLE in content:
    content = content.replace(OLD_BUBBLE, NEW_BUBBLE, 1)
    print('OK: .dm-outer .chat-bubble padding 8/12 → 7/10, radius 18 → 14')
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
