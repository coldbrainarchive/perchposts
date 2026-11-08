#!/usr/bin/env python3
"""Patch v306 -> v307: fix comments broken by DM CSS changes.
Add 'dm-thread-view' class to the DM chat-window so DM-specific styles
are scoped there. Restore original comment-safe CSS for shared classes."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v306.js'
dst = '_deploy/assets/index-DUcNPOLc-v307.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Tag DM chat-window with dm-thread-view class ──────────────────────────
OLD_WIN = 'className:`chat-window`,ref:_dmWRef'
NEW_WIN = 'className:`chat-window dm-thread-view`,ref:_dmWRef'
if OLD_WIN in content:
    content = content.replace(OLD_WIN, NEW_WIN, 1)
    print('OK: dm-thread-view class added to DM chat-window')
else:
    errors.append('FAIL: DM chat-window not found')

# ── 2. Restore .chat-msg to original (comments safe) + add DM scoped version ─
OLD_MSG_CSS = (
    '.chat-msg {\n        display: flex;\n        align-items: flex-end;\n        gap: 8px;\n'
    '        max-width: min(82%, 480px);\n        margin-bottom: 4px;\n        align-self: flex-start;\n      }\n\n'
    '      .chat-msg--mine {\n        align-self: flex-end;\n        flex-direction: row-reverse;\n      }'
)
NEW_MSG_CSS = (
    # Original for comments
    '.chat-msg {\n        display: block;\n        align-self: flex-start;\n'
    '        max-width: min(80%, 480px);\n        margin-bottom: 10px;\n      }\n\n'
    '      .chat-msg--mine {\n        align-self: flex-end;\n      }\n\n'
    # DM-scoped iMessage layout
    '      .dm-thread-view .chat-msg {\n        display: flex;\n        align-items: flex-end;\n        gap: 8px;\n'
    '        max-width: min(82%, 480px);\n        margin-bottom: 4px;\n      }\n\n'
    '      .dm-thread-view .chat-msg--mine {\n        flex-direction: row-reverse;\n      }'
)
if OLD_MSG_CSS in content:
    content = content.replace(OLD_MSG_CSS, NEW_MSG_CSS, 1)
    print('OK: .chat-msg restored for comments; DM scoped version added')
else:
    errors.append('FAIL: .chat-msg CSS block not found')

# ── 3. Restore .chat-msg-body to original + add DM scoped version ─────────────
OLD_BODY_CSS = (
    '.chat-msg-body {\n        display: flex;\n        flex-direction: column;\n'
    '        align-items: flex-start;\n        min-width: 0;\n      }\n\n'
    '      .chat-msg--mine .chat-msg-body {\n        align-items: flex-end;\n      }'
)
NEW_BODY_CSS = (
    # Original for comments
    '.chat-msg-body {\n        display: flex;\n        flex-direction: column;\n'
    '        border-radius: 18px;\n        overflow: hidden;\n        width: 100%;\n      }\n\n'
    # DM-scoped
    '      .dm-thread-view .chat-msg-body {\n        display: flex;\n        flex-direction: column;\n'
    '        align-items: flex-start;\n        min-width: 0;\n        border-radius: 0;\n        overflow: visible;\n        width: auto;\n      }\n\n'
    '      .dm-thread-view .chat-msg--mine .chat-msg-body {\n        align-items: flex-end;\n      }'
)
if OLD_BODY_CSS in content:
    content = content.replace(OLD_BODY_CSS, NEW_BODY_CSS, 1)
    print('OK: .chat-msg-body restored for comments; DM scoped version added')
else:
    errors.append('FAIL: .chat-msg-body CSS block not found')

# ── 4. Restore .chat-bubble to original + add DM scoped version ───────────────
OLD_BUBBLE_CSS = (
    '.chat-bubble {\n        background: #252836;\n        color: #e2e8f0;\n'
    '        border-radius: 18px 18px 18px 4px;\n        padding: 0;\n'
    '        font-size: 13px;\n        line-height: 1.4;\n        cursor: pointer;\n'
    '        word-break: break-word;\n        transition: opacity 0.15s;\n'
    '        display: flex;\n        flex-direction: column;\n        overflow: hid'
)
# Get the full block
idx_bub = content.find('.chat-bubble {\n        background: #252836;')
end_bub = content.find('\n\n      .chat-bubble--mine {', idx_bub)
old_bubble_full = content[idx_bub:end_bub]

new_bubble_full = (
    # Original for comments
    '.chat-bubble {\n        background: #1e2530;\n        color: #dbe4ee;\n'
    '        border-radius: 0;\n        padding: 6px 10px;\n'
    '        font-size: 13px;\n        line-height: 1.4;\n        cursor: pointer;\n'
    '        word-break: break-word;\n        transition: opacity 0.15s;\n      }\n\n'
    # DM-scoped bubble
    '      .dm-thread-view .chat-bubble {\n        background: #252836;\n        color: #e2e8f0;\n'
    '        border-radius: 18px 18px 18px 4px;\n        padding: 8px 12px;\n'
    '        font-size: 13px;\n        line-height: 1.4;\n        cursor: pointer;\n'
    '        word-break: break-word;\n        transition: opacity 0.15s;\n'
    '        display: inline-block;\n        max-width: 100%;\n      }'
)

if old_bubble_full:
    content = content.replace(old_bubble_full, new_bubble_full, 1)
    print('OK: .chat-bubble restored for comments; DM scoped version added')
else:
    errors.append('FAIL: .chat-bubble full block not found')

# ── 5. Scope .chat-bubble--mine and .chat-ts to dm-thread-view ───────────────
OLD_MINE = '.chat-bubble--mine {\n        background: #7c3aed;\n        color: #ffffff;\n        border-radius: 18px 18px 4px 18px;\n      }'
NEW_MINE = '.dm-thread-view .chat-bubble--mine {\n        background: #7c3aed;\n        color: #ffffff;\n        border-radius: 18px 18px 4px 18px;\n      }'
if OLD_MINE in content:
    content = content.replace(OLD_MINE, NEW_MINE, 1)
    print('OK: .chat-bubble--mine scoped to dm-thread-view')
else:
    errors.append('FAIL: .chat-bubble--mine not found')

OLD_TS = '.chat-ts {'
NEW_TS = '.dm-thread-view .chat-ts {'
if OLD_TS in content:
    content = content.replace(OLD_TS, NEW_TS, 1)
    print('OK: .chat-ts scoped to dm-thread-view')
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
