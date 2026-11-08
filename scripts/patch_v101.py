#!/usr/bin/env python3
"""Patch v100 -> v101: always show cage/ban buttons for non-admin members."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v100.js'
dst = '_deploy/assets/index-DUcNPOLc-v101.js'

content = open(src, encoding='utf-8').read()
errors = []

# Change condition from requiring browser_id or ip_hash to just not-admin
OLD_COND = '!d&&(o.browser_id||o.ip_hash)&&(0,L.jsxs)(L.Fragment,{children:['
NEW_COND = '!d&&(0,L.jsxs)(L.Fragment,{children:['
if OLD_COND in content:
    content = content.replace(OLD_COND, NEW_COND, 1)
    print('OK: cage/ban buttons now show for all non-admin members')
else:
    errors.append('FAIL: button condition not found')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'\nWrote {dst}')
