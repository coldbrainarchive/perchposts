#!/usr/bin/env python3
"""Patch v268 -> v269: fix DM thread height — content wrapper uses overflow:hidden in thread view."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v268.js'
dst = '_deploy/assets/index-DUcNPOLc-v269.js'

content = open(src, encoding='utf-8').read()
errors = []

# The content wrapper div (after tabs) has flex:1,overflowY:auto
# When DM thread is open it should be overflow:hidden + flex column so the thread fills it
OLD_WRAPPER = 'style:{flex:1,overflowY:`auto`},onTouchStart'
NEW_WRAPPER = 'style:{flex:1,overflow:c===`inbox`&&_dmThread?`hidden`:`auto`,display:`flex`,flexDirection:`column`},onTouchStart'

if OLD_WRAPPER in content:
    content = content.replace(OLD_WRAPPER, NEW_WRAPPER, 1)
    print('OK: content wrapper uses overflow:hidden in thread view')
else:
    errors.append('FAIL: content wrapper not found')

# Also ensure notifications + account content sections fill properly when not in thread
# The notifications div needs overflowY:auto when it's the active content
OLD_NOTIF_DIV = 'c===`notifications`&&(0,L.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`},'
NEW_NOTIF_DIV = 'c===`notifications`&&(0,L.jsx)(`div`,{style:{display:`flex`,flexDirection:`column`,flex:1,overflowY:`auto`},'
if OLD_NOTIF_DIV in content:
    content = content.replace(OLD_NOTIF_DIV, NEW_NOTIF_DIV, 1)
    print('OK: notifications scrolls itself')
else:
    print('NOTE: notifications div not patched (may be fine)')

# Account section too
OLD_ACCT = 'c===`account`&&(0,L.jsxs)(`div`,{style:{padding:20,display:`flex`,flexDirection:`column`,gap:14},'
NEW_ACCT = 'c===`account`&&(0,L.jsxs)(`div`,{style:{padding:20,display:`flex`,flexDirection:`column`,gap:14,flex:1,overflowY:`auto`},'
if OLD_ACCT in content:
    content = content.replace(OLD_ACCT, NEW_ACCT, 1)
    print('OK: account section scrolls itself')
else:
    print('NOTE: account div not patched')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
