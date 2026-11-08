#!/usr/bin/env python3
"""Patch v298 -> v299: everything inside the bubble.
Move quote-bar, message text, reactions, and action buttons all inside
the chat-bubble div so the whole interaction is one cohesive card."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v298.js'
dst = '_deploy/assets/index-DUcNPOLc-v299.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Restructure opening: quote-bar + bubble jsx → bubble jsxs wrapping both
# Also wraps _msg.content in a padded span since bubble now has padding:0
OLD_OPEN = (
    '_msg.reply_to&&(0,L.jsxs)(`div`,{className:`chat-quote-bar`,children:['
    '(0,L.jsx)(`span`,{className:`chat-quote-name`,children:_msg.reply_to.from_username}),'
    '(0,L.jsx)(`p`,{className:`chat-quote-text`,children:_msg.reply_to.content})]}),'
    '(0,L.jsx)(`div`,{className:`chat-bubble${_mine?` chat-bubble--mine`:``}`,'
    'onClick:()=>_setDmPickerId(_showActions?null:_msg.id),children:_msg.content})'
)
NEW_OPEN = (
    '(0,L.jsxs)(`div`,{className:`chat-bubble${_mine?` chat-bubble--mine`:``}`,'
    'onClick:()=>_setDmPickerId(_showActions?null:_msg.id),children:['
    '_msg.reply_to&&(0,L.jsxs)(`div`,{className:`chat-quote-bar`,children:['
    '(0,L.jsx)(`span`,{className:`chat-quote-name`,children:_msg.reply_to.from_username}),'
    '(0,L.jsx)(`p`,{className:`chat-quote-text`,children:_msg.reply_to.content})]}),'
    '(0,L.jsx)(`span`,{style:{display:`block`,padding:`8px 12px`},children:_msg.content})'
)
if OLD_OPEN in content:
    content = content.replace(OLD_OPEN, NEW_OPEN, 1)
    print('OK: bubble now opens as jsxs with quote-bar as first child')
else:
    errors.append('FAIL: opening sequence not found')

# ── 2. Remove ts from between content and reactions (will be added outside bubble)
OLD_TS = (
    ',(0,L.jsx)(`span`,{className:`chat-ts`,children:Un(_msg.created_at)}),_rxEntries.length>0'
)
NEW_TS = ',_rxEntries.length>0'
if OLD_TS in content:
    content = content.replace(OLD_TS, NEW_TS, 1)
    print('OK: ts removed from inside content sequence')
else:
    errors.append('FAIL: ts-before-reactions sequence not found')

# ── 3. Close bubble + add ts outside, before body closes
# OLD: body-children `]` + body-props `}` + body-jsxs `)` + chat-msg-children `]` + chat-msg `},_mi)`
# NEW: bubble-children+props+jsxs `]})` + ts span + body `]})` + chat-msg `]},_mi)`
OLD_CLOSE = ']})]},_mi)'
NEW_CLOSE = (
    ']}),'
    '(0,L.jsx)(`span`,{className:`chat-ts`,children:Un(_msg.created_at)})'
    ']})]},_mi)'
)
if OLD_CLOSE in content:
    content = content.replace(OLD_CLOSE, NEW_CLOSE, 1)
    print('OK: bubble closed before ts; ts placed outside bubble before body close')
else:
    errors.append('FAIL: closing bracket sequence not found')

# ── 4. CSS: bubble is now a column flex container (padding moved to inner text span)
OLD_BUBBLE_CSS = (
    '.chat-bubble {\n        background: #252836;\n        color: #e2e8f0;\n'
    '        border-radius: 18px 18px 18px 4px;\n        padding: 8px 12px;\n'
    '        font-size: 13px;\n        line-height: 1.4;\n        cursor: pointer;\n'
    '        word-break: break-word;\n        transition: opacity 0.15s;\n'
    '        display: inline-block;\n        max-width: 100%;\n      }'
)
NEW_BUBBLE_CSS = (
    '.chat-bubble {\n        background: #252836;\n        color: #e2e8f0;\n'
    '        border-radius: 18px 18px 18px 4px;\n        padding: 0;\n'
    '        font-size: 13px;\n        line-height: 1.4;\n        cursor: pointer;\n'
    '        word-break: break-word;\n        transition: opacity 0.15s;\n'
    '        display: flex;\n        flex-direction: column;\n'
    '        overflow: hidden;\n        max-width: 100%;\n      }'
)
if OLD_BUBBLE_CSS in content:
    content = content.replace(OLD_BUBBLE_CSS, NEW_BUBBLE_CSS, 1)
    print('OK: .chat-bubble → flex column container')
else:
    errors.append('FAIL: .chat-bubble CSS not found')

# ── 5. CSS: reactions inside bubble — add horizontal padding
OLD_REACTIONS_CSS = (
    '.chat-reactions {\n        display: flex;\n        flex-wrap: wrap;\n        gap: 4px;\n'
    '        padding: 0;\n        margin-top: 4px;\n      }'
)
NEW_REACTIONS_CSS = (
    '.chat-reactions {\n        display: flex;\n        flex-wrap: wrap;\n        gap: 4px;\n'
    '        padding: 4px 10px 6px;\n      }'
)
if OLD_REACTIONS_CSS in content:
    content = content.replace(OLD_REACTIONS_CSS, NEW_REACTIONS_CSS, 1)
    print('OK: .chat-reactions padded for inside-bubble use')
else:
    errors.append('FAIL: .chat-reactions CSS not found')

# ── 6. CSS: action sheet inside bubble — border-top separator, padded
OLD_ACTION_CSS = (
    '.chat-action-sheet {\n        display: flex;\n        gap: 5px;\n        flex-wrap: wrap;\n'
    '        padding: 5px 0 0;\n      }'
)
NEW_ACTION_CSS = (
    '.chat-action-sheet {\n        display: flex;\n        gap: 5px;\n        flex-wrap: wrap;\n'
    '        padding: 6px 10px 8px;\n        border-top: 1px solid rgba(148,163,184,0.12);\n      }'
)
if OLD_ACTION_CSS in content:
    content = content.replace(OLD_ACTION_CSS, NEW_ACTION_CSS, 1)
    print('OK: .chat-action-sheet padded + separator for inside-bubble use')
else:
    errors.append('FAIL: .chat-action-sheet CSS not found')

# ── 7. CSS: quote bar — no bottom margin (bubble padding handles spacing)
OLD_QUOTE_CSS = (
    '.chat-quote-bar {\n        border-left: 2px solid #c084fc;\n'
    '        padding: 4px 8px;\n        margin-bottom: 4px;\n        border-radius: 4px 10px 10px 4px;\n'
    '        background: rgba(192,132,252,0.08);\n        max-width: 100%;\n      }'
)
NEW_QUOTE_CSS = (
    '.chat-quote-bar {\n        border-left: 2px solid #c084fc;\n'
    '        padding: 6px 12px;\n        margin-bottom: 0;\n        border-radius: 0;\n'
    '        background: rgba(192,132,252,0.1);\n        border-bottom: 1px solid rgba(192,132,252,0.15);\n      }'
)
if OLD_QUOTE_CSS in content:
    content = content.replace(OLD_QUOTE_CSS, NEW_QUOTE_CSS, 1)
    print('OK: .chat-quote-bar updated for inside-bubble use')
else:
    errors.append('FAIL: .chat-quote-bar CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
