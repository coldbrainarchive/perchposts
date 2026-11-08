#!/usr/bin/env python3
"""Patch v324 -> v325: native emoji picker feel.
Make the emoji input invisible (opacity:0, zero-height container) so tapping React
opens the native emoji keyboard without showing a visible text field.
Also fix focus timing with setTimeout so the keyboard actually appears."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v324.js'
dst = '_deploy/assets/index-DUcNPOLc-v325.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. CSS: emoji picker row — zero height, no margin ────────────────────────
OLD_ROW_CSS = '.chat-emoji-picker-row {\n        margin-top: 5px;\n      }'
NEW_ROW_CSS = (
    '.chat-emoji-picker-row {\n'
    '        position: relative;\n'
    '        height: 0;\n'
    '        overflow: visible;\n'
    '      }'
)
if OLD_ROW_CSS in content:
    content = content.replace(OLD_ROW_CSS, NEW_ROW_CSS, 1)
    print('OK: emoji picker row CSS — zero height, overflow visible')
else:
    errors.append('FAIL: .chat-emoji-picker-row CSS not found')

# ── 2. CSS: emoji input — invisible but focusable ─────────────────────────────
OLD_INPUT_CSS = (
    '.chat-emoji-picker-input {\n        height: 30px;\n        padding: 0 12px;\n'
    '        border-radius: 999px;\n        border: 1px solid rgba(148,163,184,0.25);\n'
    '        background: #0f1117;\n        color: #f'
)
NEW_INPUT_CSS = (
    '.chat-emoji-picker-input {\n'
    '        position: absolute;\n'
    '        bottom: 0;\n'
    '        left: 0;\n'
    '        width: 100%;\n'
    '        height: 44px;\n'
    '        opacity: 0;\n'
    '        font-size: 16px;\n'
    '        pointer-events: none;\n'
    '        border: none;\n'
    '        background: transparent;\n'
    '        color: transparent;\n'
    '        -webkit-user-select: text;\n'
    '        color: #f'  # continue rest of original (will be incomplete but next replace handles)
)
# Actually do a simpler CSS replacement for the full block
idx_css = content.find('.chat-emoji-picker-input {')
end_css = content.find('\n      }', idx_css) + 8
old_full_css = content[idx_css:end_css]
new_full_css = (
    '.chat-emoji-picker-input {\n'
    '        position: absolute;\n'
    '        bottom: 0;\n'
    '        left: 0;\n'
    '        width: 100%;\n'
    '        height: 44px;\n'
    '        opacity: 0;\n'
    '        font-size: 16px;\n'
    '        pointer-events: none;\n'
    '        border: none;\n'
    '        background: transparent;\n'
    '        -webkit-user-select: text;\n'
    '      }'
)
if old_full_css in content:
    content = content.replace(old_full_css, new_full_css, 1)
    print('OK: emoji input CSS — invisible, positioned, focusable')
else:
    errors.append('FAIL: .chat-emoji-picker-input full block not found')

# ── 3. JS: fix focus timing with setTimeout ───────────────────────────────────
OLD_D = 'function D(){y(!1),x(!0),S.current&&(S.current.value=``,S.current.focus())}'
NEW_D = 'function D(){y(!1),x(!0),setTimeout(()=>{S.current&&(S.current.value=``,S.current.focus())},20)}'
if OLD_D in content:
    content = content.replace(OLD_D, NEW_D, 1)
    print('OK: emoji focus delayed 20ms so React renders input before focus()')
else:
    errors.append('FAIL: D() function not found')

# ── 4. JS: remove display:none from emoji picker row (always in DOM) ──────────
OLD_DISPLAY = (
    'className:`chat-emoji-picker-row`,style:{display:b?``:`none`},'
    'children:(0,L.jsx)(`input`,{ref:S,className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:`Pick an emoji...`,'
)
NEW_DISPLAY = (
    'className:`chat-emoji-picker-row`,'
    'children:(0,L.jsx)(`input`,{ref:S,className:`chat-emoji-picker-input`,'
    'type:`text`,inputMode:`emoji`,placeholder:``,'
)
if OLD_DISPLAY in content:
    content = content.replace(OLD_DISPLAY, NEW_DISPLAY, 1)
    print('OK: emoji picker always in DOM (no display:none), placeholder cleared')
else:
    errors.append('FAIL: emoji picker row inline style not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
