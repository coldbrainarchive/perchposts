#!/usr/bin/env python3
"""Patch v297 -> v298: DM UI polish.
- Remove bird avatar from left of received messages
- Reactions: float as pills below bubble (no dark background card)
- Action sheet: float as pill buttons (no dark background card)
- Quote bar: compact, rounded, matches bubble style
- Compose: smaller font (14px), better padding, cleaner look"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v297.js'
dst = '_deploy/assets/index-DUcNPOLc-v298.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove dm-avatar from JS rendering ────────────────────────────────────
OLD_AVATAR_JS = (
    '!_mine&&(0,L.jsx)(`span`,{className:`dm-avatar`,children:_mbd&&_mbd.hat?'
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{height:`22px`,width:`auto`}})'
    ':(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,fontSize:22,lineHeight:1},'
    'children:[(0,L.jsx)(`span`,{style:{filter:_mbd&&_mbd.f?_mbd.f:``,display:`block`},'
    'children:_mbd&&_mbd.e?_mbd.e:`🐤`}),...(_mbd&&_mbd.s?_spEls(_mbd.s,22):[])]})}),(0,L.jsxs)(`div`,{className:`chat-msg-body`'
)
NEW_AVATAR_JS = (
    '(0,L.jsxs)(`div`,{className:`chat-msg-body`'
)
if OLD_AVATAR_JS in content:
    content = content.replace(OLD_AVATAR_JS, NEW_AVATAR_JS, 1)
    print('OK: dm-avatar removed from message rendering')
else:
    errors.append('FAIL: dm-avatar JS not found')

# ── 2. Remove .dm-avatar CSS ─────────────────────────────────────────────────
OLD_DM_AVATAR_CSS = (
    '.dm-avatar {\n        flex-shrink: 0;\n        width: 26px;\n        display: flex;\n'
    '        align-items: center;\n        justify-content: center;\n      }\n\n\n\n'
)
NEW_DM_AVATAR_CSS = '\n\n'
if OLD_DM_AVATAR_CSS in content:
    content = content.replace(OLD_DM_AVATAR_CSS, NEW_DM_AVATAR_CSS, 1)
    print('OK: .dm-avatar CSS removed')
else:
    errors.append('FAIL: .dm-avatar CSS not found')

# ── 3. Fix .chat-reactions — remove dark card bg, float below bubble ─────────
OLD_REACTIONS_CSS = (
    '.chat-reactions {\n        display: flex;\n        flex-wrap: wrap;\n        gap: 4px;\n'
    '        padding: 0 14px 8px;\n        background: #1e2530;\n      }'
)
NEW_REACTIONS_CSS = (
    '.chat-reactions {\n        display: flex;\n        flex-wrap: wrap;\n        gap: 4px;\n'
    '        padding: 0;\n        margin-top: 4px;\n      }'
)
if OLD_REACTIONS_CSS in content:
    content = content.replace(OLD_REACTIONS_CSS, NEW_REACTIONS_CSS, 1)
    print('OK: .chat-reactions CSS updated — floating pills')
else:
    errors.append('FAIL: .chat-reactions CSS not found')

# ── 4. Fix .chat-action-sheet — remove dark card bg, float as pill row ───────
OLD_ACTION_CSS = (
    '.chat-action-sheet {\n        display: flex;\n        gap: 6px;\n        flex-wrap: wrap;\n'
    '        padding: 8px 14px;\n        background: #1e2530;\n        border-top: 1px solid rgba(148,163,184,0.1);\n      }'
)
NEW_ACTION_CSS = (
    '.chat-action-sheet {\n        display: flex;\n        gap: 5px;\n        flex-wrap: wrap;\n'
    '        padding: 5px 0 0;\n      }'
)
if OLD_ACTION_CSS in content:
    content = content.replace(OLD_ACTION_CSS, NEW_ACTION_CSS, 1)
    print('OK: .chat-action-sheet CSS updated — floating pill buttons')
else:
    errors.append('FAIL: .chat-action-sheet CSS not found')

# ── 5. Fix .chat-quote-bar — compact and rounded to match bubble style ────────
OLD_QUOTE_CSS = (
    '.chat-quote-bar {\n        border-left: 3px solid rgba(192,132,252,0.5);\n'
    '        padding: 4px 8px;\n        margin-bottom: 6px;\n        border-radius: 0 6px 6px 0;\n'
    '        background: rgba(148,163,184,0.07);\n      }'
)
NEW_QUOTE_CSS = (
    '.chat-quote-bar {\n        border-left: 2px solid #c084fc;\n'
    '        padding: 4px 8px;\n        margin-bottom: 4px;\n        border-radius: 4px 10px 10px 4px;\n'
    '        background: rgba(192,132,252,0.08);\n        max-width: 100%;\n      }'
)
if OLD_QUOTE_CSS in content:
    content = content.replace(OLD_QUOTE_CSS, NEW_QUOTE_CSS, 1)
    print('OK: .chat-quote-bar CSS updated — compact rounded style')
else:
    errors.append('FAIL: .chat-quote-bar CSS not found')

# ── 6. Compose: reduce font-size and padding ─────────────────────────────────
OLD_INPUT_CSS = (
    '.chat-input {\n        background: transparent;\n        border: none;\n        border-radius: 20px;\n'
    '        color: #f8fafc;\n        font-size: 16px;\n        font-family: inherit;\n'
    '        padding: 9px 14px;\n        resize: none;\n        max-height: 120px;\n        overflow-y: auto;\n'
    '        line-height: '
)
NEW_INPUT_CSS = (
    '.chat-input {\n        background: transparent;\n        border: none;\n        border-radius: 20px;\n'
    '        color: #f8fafc;\n        font-size: 14px;\n        font-family: inherit;\n'
    '        padding: 8px 12px;\n        resize: none;\n        max-height: 100px;\n        overflow-y: auto;\n'
    '        line-height: '
)
if OLD_INPUT_CSS in content:
    content = content.replace(OLD_INPUT_CSS, NEW_INPUT_CSS, 1)
    print('OK: compose input font-size/padding reduced')
else:
    errors.append('FAIL: .chat-input CSS not found')

# ── 7. Compose container: tighten padding ────────────────────────────────────
OLD_COMPOSE_CSS = (
    '.chat-compose {\n        border-top: 1px solid rgba(148, 163, 184, 0.1);\n'
    '        padding: 10px 12px 10px;\n        display: flex;\n        flex-direction: column;\n'
    '        gap: 6px;\n        background: #1b1d24;\n        position: sticky;\n        bottom: 0;\n        z-index: 10;\n      }'
)
NEW_COMPOSE_CSS = (
    '.chat-compose {\n        border-top: 1px solid rgba(148, 163, 184, 0.08);\n'
    '        padding: 8px 10px;\n        display: flex;\n        flex-direction: column;\n'
    '        gap: 5px;\n        background: #13151c;\n        position: sticky;\n        bottom: 0;\n        z-index: 10;\n      }'
)
if OLD_COMPOSE_CSS in content:
    content = content.replace(OLD_COMPOSE_CSS, NEW_COMPOSE_CSS, 1)
    print('OK: compose container padding/background updated')
else:
    errors.append('FAIL: .chat-compose CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
