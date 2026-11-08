#!/usr/bin/env python3
"""Patch v308 -> v309: cleanly scope all DM CSS under dm-outer wrapper.
Add 'dm-outer' class to the outer DM thread container div (content-card comments-panel).
This lets us use .dm-outer .chat-* selectors to scope DM styles, completely
isolating comments from any DM CSS changes."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v308.js'
dst = '_deploy/assets/index-DUcNPOLc-v309.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add dm-outer class to the DM thread wrapper ───────────────────────────
OLD_WRAPPER = 'className:`content-card comments-panel`,style:{padding:0,overflow:`clip`,display:`flex`,flexDirection:`column`,flex:1,height:0}'
NEW_WRAPPER = 'className:`content-card comments-panel dm-outer`,style:{padding:0,overflow:`clip`,display:`flex`,flexDirection:`column`,flex:1,height:0}'
if OLD_WRAPPER in content:
    content = content.replace(OLD_WRAPPER, NEW_WRAPPER, 1)
    print('OK: dm-outer class added to DM thread wrapper')
else:
    errors.append('FAIL: DM thread wrapper not found')

# ── 2. Replace the sibling-selector overrides with proper .dm-outer selectors ─
# chat-compose overrides
OLD_COMPOSE_SCOPE = (
    '      .dm-thread-view ~ .chat-compose,\n'
    '      .dm-thread-view + .chat-compose,\n'
    '      .chat-window.dm-thread-view ~ .chat-compose {\n'
    '        border-top: none;\n        padding: 10px 12px 14px;\n'
    '        gap: 5px;\n        background: #13151c;\n      }'
)
NEW_COMPOSE_SCOPE = (
    '      .dm-outer .chat-compose {\n'
    '        border-top: none;\n        padding: 10px 12px 14px;\n'
    '        gap: 5px;\n        background: #13151c;\n      }'
)
if OLD_COMPOSE_SCOPE in content:
    content = content.replace(OLD_COMPOSE_SCOPE, NEW_COMPOSE_SCOPE, 1)
    print('OK: .chat-compose scoped under .dm-outer')
else:
    errors.append('FAIL: chat-compose sibling selector not found')

# chat-input-bubble overrides
OLD_INPUT_SCOPE = (
    '      .dm-thread-view ~ .chat-compose .chat-input-bubble,\n'
    '      .chat-window.dm-thread-view ~ .chat-compose .chat-input-bubble {\n'
    '        background: #0d0f14;\n        border: 1px solid rgba(255,255,255,0.07);\n'
    '        border-radius: 28px;\n      }'
)
NEW_INPUT_SCOPE = (
    '      .dm-outer .chat-compose .chat-input-bubble {\n'
    '        background: #0d0f14;\n        border: 1px solid rgba(255,255,255,0.07);\n'
    '        border-radius: 28px;\n      }'
)
if OLD_INPUT_SCOPE in content:
    content = content.replace(OLD_INPUT_SCOPE, NEW_INPUT_SCOPE, 1)
    print('OK: .chat-input-bubble scoped under .dm-outer')
else:
    errors.append('FAIL: chat-input-bubble sibling selector not found')

# chat-send-btn override
OLD_SEND_SCOPE = (
    '      .dm-thread-view ~ .chat-compose .chat-send-btn,\n'
    '      .chat-window.dm-thread-view ~ .chat-compose .chat-send-btn {\n'
    '        width: 40px;\n        height: 40px;\n        background: #2d2f3a;\n'
    '        color: #94a3b8;\n        font-size: 18px;\n      }'
)
NEW_SEND_SCOPE = (
    '      .dm-outer .chat-compose .chat-send-btn {\n'
    '        width: 40px;\n        height: 40px;\n        background: #2d2f3a;\n'
    '        color: #94a3b8;\n        font-size: 18px;\n      }'
)
if OLD_SEND_SCOPE in content:
    content = content.replace(OLD_SEND_SCOPE, NEW_SEND_SCOPE, 1)
    print('OK: .chat-send-btn scoped under .dm-outer')
else:
    errors.append('FAIL: chat-send-btn sibling selector not found')

# active send btn
OLD_ACTIVE_SCOPE = (
    '      .dm-thread-view ~ .chat-compose .chat-send-btn:not(:disabled),\n'
    '      .chat-window.dm-thread-view ~ .chat-compose .chat-send-btn:not(:disabled) {\n'
    '        background: #7c3aed;\n        color: #fff;\n      }'
)
NEW_ACTIVE_SCOPE = (
    '      .dm-outer .chat-compose .chat-send-btn:not(:disabled) {\n'
    '        background: #7c3aed;\n        color: #fff;\n      }'
)
if OLD_ACTIVE_SCOPE in content:
    content = content.replace(OLD_ACTIVE_SCOPE, NEW_ACTIVE_SCOPE, 1)
    print('OK: active send btn scoped under .dm-outer')
else:
    errors.append('FAIL: active send btn sibling selector not found')

# chat-msg DM overrides
OLD_MSG_SCOPE = (
    '      .dm-thread-view .chat-msg {\n        display: flex;\n        align-items: flex-end;\n        gap: 8px;\n'
    '        max-width: min(82%, 480px);\n        margin-bottom: 4px;\n      }\n\n'
    '      .dm-thread-view .chat-msg--mine {\n        flex-direction: row-reverse;\n      }'
)
NEW_MSG_SCOPE = (
    '      .dm-outer .chat-msg {\n        display: flex;\n        align-items: flex-end;\n        gap: 8px;\n'
    '        max-width: min(82%, 480px);\n        margin-bottom: 4px;\n      }\n\n'
    '      .dm-outer .chat-msg--mine {\n        flex-direction: row-reverse;\n      }'
)
if OLD_MSG_SCOPE in content:
    content = content.replace(OLD_MSG_SCOPE, NEW_MSG_SCOPE, 1)
    print('OK: .chat-msg scoped under .dm-outer')
else:
    errors.append('FAIL: chat-msg DM scope not found')

# chat-msg-body DM overrides
OLD_BODY_SCOPE = (
    '      .dm-thread-view .chat-msg-body {\n        display: flex;\n        flex-direction: column;\n'
    '        align-items: flex-start;\n        min-width: 0;\n        border-radius: 0;\n        overflow: visible;\n        width: auto;\n      }\n\n'
    '      .dm-thread-view .chat-msg--mine .chat-msg-body {\n        align-items: flex-end;\n      }'
)
NEW_BODY_SCOPE = (
    '      .dm-outer .chat-msg-body {\n        display: flex;\n        flex-direction: column;\n'
    '        align-items: flex-start;\n        min-width: 0;\n        border-radius: 0;\n        overflow: visible;\n        width: auto;\n      }\n\n'
    '      .dm-outer .chat-msg--mine .chat-msg-body {\n        align-items: flex-end;\n      }'
)
if OLD_BODY_SCOPE in content:
    content = content.replace(OLD_BODY_SCOPE, NEW_BODY_SCOPE, 1)
    print('OK: .chat-msg-body scoped under .dm-outer')
else:
    errors.append('FAIL: chat-msg-body DM scope not found')

# chat-bubble DM override
OLD_BUBBLE_SCOPE = (
    '      .dm-thread-view .chat-bubble {\n        background: #252836;\n        color: #e2e8f0;\n'
    '        border-radius: 18px 18px 18px 4px;\n        padding: 8px 12px;\n'
    '        font-size: 13px;\n        line-height: 1.4;\n        cursor: pointer;\n'
    '        word-break: break-word;\n        transition: opacity 0.15s;\n'
    '        display: inline-block;\n        max-width: 100%;\n      }'
)
NEW_BUBBLE_SCOPE = (
    '      .dm-outer .chat-bubble {\n        background: #252836;\n        color: #e2e8f0;\n'
    '        border-radius: 18px 18px 18px 4px;\n        padding: 8px 12px;\n'
    '        font-size: 13px;\n        line-height: 1.4;\n        cursor: pointer;\n'
    '        word-break: break-word;\n        transition: opacity 0.15s;\n'
    '        display: inline-block;\n        max-width: 100%;\n      }'
)
if OLD_BUBBLE_SCOPE in content:
    content = content.replace(OLD_BUBBLE_SCOPE, NEW_BUBBLE_SCOPE, 1)
    print('OK: .chat-bubble scoped under .dm-outer')
else:
    errors.append('FAIL: chat-bubble DM scope not found')

# chat-bubble--mine
OLD_MINE = '.dm-thread-view .chat-bubble--mine {'
NEW_MINE = '.dm-outer .chat-bubble--mine {'
if OLD_MINE in content:
    content = content.replace(OLD_MINE, NEW_MINE, 1)
    print('OK: .chat-bubble--mine scoped under .dm-outer')
else:
    errors.append('FAIL: .chat-bubble--mine not found')

# chat-ts
OLD_TS = '.dm-thread-view .chat-ts {'
NEW_TS = '.dm-outer .chat-ts {'
if OLD_TS in content:
    content = content.replace(OLD_TS, NEW_TS, 1)
    print('OK: .chat-ts scoped under .dm-outer')
else:
    errors.append('FAIL: .chat-ts not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
