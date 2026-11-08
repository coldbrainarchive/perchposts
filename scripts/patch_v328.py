#!/usr/bin/env python3
"""Patch v327 -> v328:
- Fix emoji input width (was stretching full row)
- Prevent iOS zoom (font-size must be 16px on <input>)
- Add a close button (x) next to the emoji input
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v327.js'
dst = '_deploy/assets/index-DUcNPOLc-v328.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Row CSS: flex row so input + close button sit side by side ─────────────
OLD_ROW = '.chat-emoji-picker-row {\n        padding: 6px 10px 8px;\n      }'
NEW_ROW = (
    '.chat-emoji-picker-row {\n'
    '        display: flex;\n'
    '        align-items: center;\n'
    '        gap: 6px;\n'
    '        padding: 6px 10px 8px;\n'
    '      }'
)
if OLD_ROW in content:
    content = content.replace(OLD_ROW, NEW_ROW, 1)
    print('OK: emoji picker row flex layout')
else:
    errors.append('FAIL: .chat-emoji-picker-row CSS not found')

# ── 2. Input CSS: 16px font prevents iOS zoom; visual size from height ─────────
OLD_INPUT = (
    '.chat-emoji-picker-input {\n'
    '        height: 20px;\n'
    '        padding: 0 7px;\n'
    '        border-radius: 999px;\n'
    '        border: 1px solid rgba(148,163,184,0.2);\n'
    '        background: transparent;\n'
    '        color: #94a3b8;\n'
    '        font-size: 11px;\n'
    '        font-weight: 700;\n'
    '        outline: none;\n'
    '        width: auto;\n'
    '      }'
)
NEW_INPUT = (
    '.chat-emoji-picker-input {\n'
    '        height: 20px;\n'
    '        padding: 0 7px;\n'
    '        border-radius: 999px;\n'
    '        border: 1px solid rgba(148,163,184,0.2);\n'
    '        background: transparent;\n'
    '        color: #94a3b8;\n'
    '        font-size: 16px;\n'
    '        outline: none;\n'
    '        width: 120px;\n'
    '        flex-shrink: 0;\n'
    '      }'
)
if OLD_INPUT in content:
    content = content.replace(OLD_INPUT, NEW_INPUT, 1)
    print('OK: emoji input font-size 16px (no iOS zoom), fixed width 120px')
else:
    errors.append('FAIL: .chat-emoji-picker-input CSS not found')

# ── 3. Add close button CSS ────────────────────────────────────────────────────
OLD_EMOJI_PICKER_CSS = '.chat-emoji-picker-input::placeholder {'
NEW_EMOJI_PICKER_CSS = (
    '.chat-emoji-close-btn {\n'
    '        height: 20px;\n'
    '        padding: 0 7px;\n'
    '        border-radius: 999px;\n'
    '        border: 1px solid rgba(148,163,184,0.2);\n'
    '        background: transparent;\n'
    '        color: #94a3b8;\n'
    '        font-size: 11px;\n'
    '        font-weight: 700;\n'
    '        cursor: pointer;\n'
    '        line-height: 1;\n'
    '      }\n\n      .chat-emoji-picker-input::placeholder {'
)
if OLD_EMOJI_PICKER_CSS in content:
    content = content.replace(OLD_EMOJI_PICKER_CSS, NEW_EMOJI_PICKER_CSS, 1)
    print('OK: close button CSS added')
else:
    errors.append('FAIL: .chat-emoji-picker { not found for close button CSS insertion')

# ── 4. JSX: change L.jsx -> L.jsxs on row div, children -> array with close btn
OLD_ROW_JSX = (
    '(0,L.jsx)(`div`,{className:`chat-emoji-picker-row`,'
    'style:{display:b?``:`none`},'
    'children:(0,L.jsx)(`input`,{ref:S,className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
    'onChange:O,onBlur:()=>x(!1)})})'
)
NEW_ROW_JSX = (
    '(0,L.jsxs)(`div`,{className:`chat-emoji-picker-row`,'
    'style:{display:b?``:`none`},'
    'children:[(0,L.jsx)(`input`,{ref:S,className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
    'onChange:O,onBlur:()=>x(!1)}),'
    '(0,L.jsx)(`button`,{className:`chat-emoji-close-btn`,'
    'onMouseDown:(e)=>{e.preventDefault();x(!1);},'
    'children:`✕`})]})'
)
if OLD_ROW_JSX in content:
    content = content.replace(OLD_ROW_JSX, NEW_ROW_JSX, 1)
    print('OK: close button added to emoji picker row JSX')
else:
    errors.append('FAIL: emoji picker row JSX not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
