#!/usr/bin/env python3
"""Patch v301 -> v302:
1. Full-screen DM only on mobile (window.innerWidth < 768)
2. Add solid bg div behind panel on mobile DM to plug keyboard gap
3. Compose: match screenshot — bigger pill input, dark gray send button"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v301.js'
dst = '_deploy/assets/index-DUcNPOLc-v302.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add solid backdrop div between overlay and panel (plugs keyboard gap) ─
# Also restrict full-screen to mobile (window.innerWidth < 768)
OLD_BACKDROP_TO_PANEL = (
    'backdropFilter:`blur(3px)`}}),(0,L.jsxs)(`div`,{style:{...(c===`inbox`&&_dmThread'
    '?{position:`fixed`,top:0,left:0,right:0,bottom:0,width:`100vw`,height:`100dvh`,'
    'background:`#13151c`,zIndex:200,display:`flex`,flexDirection:`column`}'
)
NEW_BACKDROP_TO_PANEL = (
    'backdropFilter:`blur(3px)`}})'
    # Extra solid bg div — covers entire screen behind DM panel on mobile
    ',c===`inbox`&&_dmThread&&window.innerWidth<768&&(0,L.jsx)(`div`,{style:{position:`fixed`,inset:0,background:`#13151c`,zIndex:199}})'
    ',(0,L.jsxs)(`div`,{style:{...(c===`inbox`&&_dmThread&&window.innerWidth<768'
    '?{position:`fixed`,top:0,left:0,right:0,bottom:0,width:`100vw`,height:`100dvh`,'
    'background:`#13151c`,zIndex:200,display:`flex`,flexDirection:`column`}'
)
if OLD_BACKDROP_TO_PANEL in content:
    content = content.replace(OLD_BACKDROP_TO_PANEL, NEW_BACKDROP_TO_PANEL, 1)
    print('OK: mobile-only full-screen + solid backdrop div added')
else:
    errors.append('FAIL: backdrop-to-panel sequence not found')

# ── 2. Compose: larger pill input to match screenshot ─────────────────────────
OLD_INPUT_BUBBLE = (
    '.chat-input-bubble {\n        flex: 1;\n        background: #0f1117;\n'
    '        border: 1px solid #2e303a;\n        border-radius: 20px;\n'
    '        display: flex;\n        flex-direction: column;\n        transition: border-color 0.15s;\n      }'
)
NEW_INPUT_BUBBLE = (
    '.chat-input-bubble {\n        flex: 1;\n        background: #0d0f14;\n'
    '        border: 1px solid rgba(255,255,255,0.07);\n        border-radius: 28px;\n'
    '        display: flex;\n        flex-direction: column;\n        transition: border-color 0.15s;\n      }'
)
if OLD_INPUT_BUBBLE in content:
    content = content.replace(OLD_INPUT_BUBBLE, NEW_INPUT_BUBBLE, 1)
    print('OK: .chat-input-bubble updated — bigger pill shape')
else:
    errors.append('FAIL: .chat-input-bubble CSS not found')

# ── 3. Compose input: more padding, matches spacious screenshot look ──────────
OLD_INPUT_CSS = (
    '        font-size: 16px;\n        font-family: inherit;\n        padding: 8px 12px;\n'
    '        resize: none;\n        max-height: 100px;'
)
NEW_INPUT_CSS = (
    '        font-size: 16px;\n        font-family: inherit;\n        padding: 12px 16px;\n'
    '        resize: none;\n        max-height: 120px;'
)
if OLD_INPUT_CSS in content:
    content = content.replace(OLD_INPUT_CSS, NEW_INPUT_CSS, 1)
    print('OK: .chat-input padding increased')
else:
    errors.append('FAIL: .chat-input padding not found')

# ── 4. Send button: dark gray (like screenshot), not purple ───────────────────
OLD_SEND = (
    '.chat-send-btn {\n        width: 36px;\n        height: 36px;\n        border-radius: 999px;\n'
    '        border: none;\n        background: #7c3aed;\n        color: #fff;\n'
    '        font-size: 16px;\n        font-weight: 700;\n        cursor: pointer;\n'
    '        flex-shrink: 0;\n        display: flex;\n        align-items: center;\n'
    '        justify-content: center;\n        transition: background 0.15s;\n      }'
)
NEW_SEND = (
    '.chat-send-btn {\n        width: 40px;\n        height: 40px;\n        border-radius: 999px;\n'
    '        border: none;\n        background: #2d2f3a;\n        color: #94a3b8;\n'
    '        font-size: 18px;\n        font-weight: 700;\n        cursor: pointer;\n'
    '        flex-shrink: 0;\n        display: flex;\n        align-items: center;\n'
    '        justify-content: center;\n        transition: background 0.15s;\n      }'
)
if OLD_SEND in content:
    content = content.replace(OLD_SEND, NEW_SEND, 1)
    print('OK: .chat-send-btn changed to dark gray, bigger')
else:
    errors.append('FAIL: .chat-send-btn CSS not found')

# ── 5. Send btn active state: purple when there's text ───────────────────────
# Also update the :disabled state
OLD_SEND_DISABLED = (
    '.chat-send-btn:disabled {\n        background: #2e303a;\n        color: #8fa0b6;\n        cursor: default;\n      }'
)
NEW_SEND_DISABLED = (
    '.chat-send-btn:not(:disabled) {\n        background: #7c3aed;\n        color: #fff;\n      }\n\n'
    '      .chat-send-btn:disabled {\n        background: #2d2f3a;\n        color: #4b5563;\n        cursor: default;\n      }'
)
if OLD_SEND_DISABLED in content:
    content = content.replace(OLD_SEND_DISABLED, NEW_SEND_DISABLED, 1)
    print('OK: send btn turns purple when active, stays gray when empty')
else:
    errors.append('FAIL: .chat-send-btn:disabled not found')

# ── 6. Compose container: remove top border, cleaner padding ─────────────────
OLD_COMPOSE = (
    '.chat-compose {\n        border-top: 1px solid rgba(148, 163, 184, 0.08);\n'
    '        padding: 8px 10px;\n        display: flex;\n        flex-direction: column;\n'
    '        gap: 5px;\n        background: #13151c;\n        position: sticky;\n        bottom: 0;\n        z-index: 10;\n      }'
)
NEW_COMPOSE = (
    '.chat-compose {\n        border-top: none;\n'
    '        padding: 10px 12px 14px;\n        display: flex;\n        flex-direction: column;\n'
    '        gap: 5px;\n        background: #13151c;\n        position: sticky;\n        bottom: 0;\n        z-index: 10;\n      }'
)
if OLD_COMPOSE in content:
    content = content.replace(OLD_COMPOSE, NEW_COMPOSE, 1)
    print('OK: compose container — no top border, extra bottom padding')
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
