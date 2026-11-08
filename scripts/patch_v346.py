#!/usr/bin/env python3
"""Patch v345 -> v346: remove Inbox tab and DM panel (keep post comments untouched)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v345.js'
dst = '_deploy/assets/index-DUcNPOLc-v346.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Remove Inbox from the authenticated tabs array ────────────────────────
OLD_TABS = '{id:`notifications`,label:`Notifications`},{id:`inbox`,label:`Inbox`},{id:`account`,label:`Your Nest`}]'
NEW_TABS = '{id:`notifications`,label:`Notifications`},{id:`account`,label:`Your Nest`}]'
if OLD_TABS in content:
    content = content.replace(OLD_TABS, NEW_TABS, 1)
    print('OK: Inbox tab removed from tabs array')
else:
    errors.append('FAIL: tabs array not found')

# ── 2. Remove the mobile DM overlay ──────────────────────────────────────────
OLD_OVERLAY = ',c===`inbox`&&_dmThread&&window.innerWidth<768&&(0,L.jsx)(`div`,{style:{position:`fixed`,inset:0,background:`#13151c`,zIndex:199}})'
if OLD_OVERLAY in content:
    content = content.replace(OLD_OVERLAY, '', 1)
    print('OK: mobile DM overlay removed')
else:
    errors.append('FAIL: mobile DM overlay not found')

# ── 3. Remove the entire inbox panel JSX block ───────────────────────────────
# It starts with: c===`inbox`&&(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,flex:1},
# and ends just before: c===`account`&&(0,L.jsxs)(
# Find the exact boundary
inbox_start = content.find('c===`inbox`&&(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,flex:1}')
account_start = content.find('c===`account`&&(0,L.jsxs)(`div`,')

if inbox_start != -1 and account_start != -1:
    # The separator between them: `]},_ci))})]}),`
    # Find `,c===\`account\`` preceded by the inbox section closing
    # Everything from inbox_start up to (but not including) ,c===`account` should be removed
    # Find the comma right before c===`account`
    sep = content.rfind(',', inbox_start, account_start)
    if sep != -1:
        removed = content[inbox_start:sep]
        content = content[:inbox_start] + content[sep:]
        print(f'OK: inbox panel removed ({len(removed)} chars)')
    else:
        errors.append('FAIL: could not find separator before c===`account`')
else:
    if inbox_start == -1:
        errors.append('FAIL: inbox panel start not found')
    if account_start == -1:
        errors.append('FAIL: account panel not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
