#!/usr/bin/env python3
"""Patch v188 -> v189: fix card width (align-self), shrink admin bird, fix delete confirm."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v188.js'
dst = '_deploy/assets/index-DUcNPOLc-v189.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Fix card width — align-self:flex-start stops flex stretch ──────────────
# display:inline-block inside a flex column gets blockified and still stretches.
# align-self:flex-start is the correct fix.
OLD_MSG = (
    '.chat-msg {\n'
    '        display: inline-block;\n'
    '        width: fit-content;\n'
    '        max-width: min(80%, 520px);\n'
    '        margin-bottom: 10px;\n'
    '        vertical-align: top;\n'
    '      }'
)
NEW_MSG = (
    '.chat-msg {\n'
    '        display: block;\n'
    '        align-self: flex-start;\n'
    '        max-width: min(80%, 480px);\n'
    '        margin-bottom: 10px;\n'
    '      }'
)
if OLD_MSG in content:
    content = content.replace(OLD_MSG, NEW_MSG, 1)
    print('OK: .chat-msg align-self fix')
else:
    errors.append('FAIL: .chat-msg CSS not found')

# ── 2. Admin bird — much smaller (match emoji font-size 22px) ─────────────────
OLD_ADMIN = (
    'style:{position:`relative`,display:`inline-block`,width:`22px`,height:`22px`,'
    'overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,'
    'alt:`admin`,style:{position:`absolute`,height:`36px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})]}'
)
NEW_ADMIN = (
    'style:{position:`relative`,display:`inline-block`,width:`18px`,height:`18px`,'
    'overflow:`visible`,flexShrink:0},children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,'
    'alt:`admin`,style:{position:`absolute`,height:`28px`,width:`auto`,'
    'bottom:0,left:`50%`,transform:`translateX(-50%)`}})]}'
)
if OLD_ADMIN in content:
    content = content.replace(OLD_ADMIN, NEW_ADMIN, 1)
    print('OK: admin bird much smaller')
else:
    errors.append('FAIL: admin bird not found')

# ── 3. Delete — add confirm() so the action is explicit and visible ───────────
# Also add stopPropagation to Reply/React so action sheet buttons are clean
OLD_DEL = (
    'r&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:e=>{e.stopPropagation(),y(!1),i()},children:`Delete`})'
)
NEW_DEL = (
    'r&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:e=>{e.stopPropagation(),confirm(`Delete this comment?`)&&(y(!1),i())},children:`Delete`})'
)
if OLD_DEL in content:
    content = content.replace(OLD_DEL, NEW_DEL, 1)
    print('OK: delete confirm added')
else:
    errors.append('FAIL: delete button not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
