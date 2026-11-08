#!/usr/bin/env python3
"""Patch v307 -> v308: restore original compose CSS for post comments.
All the DM-specific compose tweaks (dark bg, no border-top, bigger pill,
gray send btn) must be scoped to .dm-thread-view so comments are unaffected."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v307.js'
dst = '_deploy/assets/index-DUcNPOLc-v308.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Restore .chat-compose to original + add DM-scoped override ─────────────
OLD_COMPOSE = (
    '.chat-compose {\n        border-top: none;\n'
    '        padding: 10px 12px 14px;\n        display: flex;\n        flex-direction: column;\n'
    '        gap: 5px;\n        background: #13151c;\n        position: sticky;\n        bottom: 0;\n        z-index: 10;\n      }'
)
NEW_COMPOSE = (
    # Original for comments
    '.chat-compose {\n        border-top: 1px solid rgba(148, 163, 184, 0.1);\n'
    '        padding: 10px 12px 10px;\n        display: flex;\n        flex-direction: column;\n'
    '        gap: 6px;\n        background: #1b1d24;\n        position: sticky;\n        bottom: 0;\n        z-index: 10;\n      }\n\n'
    # DM-scoped overrides
    '      .dm-thread-view ~ .chat-compose,\n'
    '      .dm-thread-view + .chat-compose,\n'
    '      .chat-window.dm-thread-view ~ .chat-compose {\n'
    '        border-top: none;\n        padding: 10px 12px 14px;\n'
    '        gap: 5px;\n        background: #13151c;\n      }'
)
if OLD_COMPOSE in content:
    content = content.replace(OLD_COMPOSE, NEW_COMPOSE, 1)
    print('OK: .chat-compose restored for comments; DM override scoped')
else:
    errors.append('FAIL: .chat-compose CSS not found')

# ── 2. Restore .chat-input-bubble to original + DM scoped version ─────────────
OLD_BUBBLE_INPUT = (
    '.chat-input-bubble {\n        flex: 1;\n        background: #0d0f14;\n'
    '        border: 1px solid rgba(255,255,255,0.07);\n        border-radius: 28px;\n'
    '        display: flex;\n        flex-direction: column;\n        transition: border-color 0.15s;\n      }'
)
NEW_BUBBLE_INPUT = (
    # Original
    '.chat-input-bubble {\n        flex: 1;\n        background: #0f1117;\n'
    '        border: 1px solid #2e303a;\n        border-radius: 20px;\n'
    '        display: flex;\n        flex-direction: column;\n        transition: border-color 0.15s;\n      }\n\n'
    # DM scoped
    '      .dm-thread-view ~ .chat-compose .chat-input-bubble,\n'
    '      .chat-window.dm-thread-view ~ .chat-compose .chat-input-bubble {\n'
    '        background: #0d0f14;\n        border: 1px solid rgba(255,255,255,0.07);\n'
    '        border-radius: 28px;\n      }'
)
if OLD_BUBBLE_INPUT in content:
    content = content.replace(OLD_BUBBLE_INPUT, NEW_BUBBLE_INPUT, 1)
    print('OK: .chat-input-bubble restored; DM version scoped')
else:
    errors.append('FAIL: .chat-input-bubble CSS not found')

# ── 3. Restore .chat-send-btn to original purple + DM scoped gray ─────────────
OLD_SEND = (
    '.chat-send-btn {\n        width: 40px;\n        height: 40px;\n        border-radius: 999px;\n'
    '        border: none;\n        background: #2d2f3a;\n        color: #94a3b8;\n'
    '        font-size: 18px;\n        font-weight: 700;\n        cursor: pointer;\n'
    '        flex-shrink: 0;\n        display: flex;\n        align-items: center;\n'
    '        justify-content: center;\n        transition: background 0.15s;\n      }'
)
NEW_SEND = (
    # Original purple for comments
    '.chat-send-btn {\n        width: 36px;\n        height: 36px;\n        border-radius: 999px;\n'
    '        border: none;\n        background: #7c3aed;\n        color: #fff;\n'
    '        font-size: 16px;\n        font-weight: 700;\n        cursor: pointer;\n'
    '        flex-shrink: 0;\n        display: flex;\n        align-items: center;\n'
    '        justify-content: center;\n        transition: background 0.15s;\n      }\n\n'
    # DM scoped gray (turns purple when active via :not(:disabled))
    '      .dm-thread-view ~ .chat-compose .chat-send-btn,\n'
    '      .chat-window.dm-thread-view ~ .chat-compose .chat-send-btn {\n'
    '        width: 40px;\n        height: 40px;\n        background: #2d2f3a;\n'
    '        color: #94a3b8;\n        font-size: 18px;\n      }'
)
if OLD_SEND in content:
    content = content.replace(OLD_SEND, NEW_SEND, 1)
    print('OK: .chat-send-btn restored to purple for comments; DM gray scoped')
else:
    errors.append('FAIL: .chat-send-btn CSS not found')

# ── 4. Scope the :not(:disabled) active state to DM too ──────────────────────
OLD_ACTIVE = (
    '.chat-send-btn:not(:disabled) {\n        background: #7c3aed;\n        color: #fff;\n      }'
)
NEW_ACTIVE = (
    '.dm-thread-view ~ .chat-compose .chat-send-btn:not(:disabled),\n'
    '      .chat-window.dm-thread-view ~ .chat-compose .chat-send-btn:not(:disabled) {\n'
    '        background: #7c3aed;\n        color: #fff;\n      }'
)
if OLD_ACTIVE in content:
    content = content.replace(OLD_ACTIVE, NEW_ACTIVE, 1)
    print('OK: send btn :not(:disabled) scoped to DM context')
else:
    errors.append('FAIL: .chat-send-btn:not(:disabled) not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
