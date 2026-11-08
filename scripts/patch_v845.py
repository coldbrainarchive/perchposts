#!/usr/bin/env python3
"""Patch v844 -> v845: mods no longer see Delete or Pin on an admin's chirps. The server refuses both."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v844.js'
dst = '_deploy/assets/index-DUcNPOLc-v845.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n != 1:
        errors.append('FAIL (' + label + '): found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

OK = '(t===`admin`||!_e.is_admin)'.replace('`', q)
patch('canDelete:N||ae&&n&&_e.username===n,', 'canDelete:N&&' + OK + '||ae&&n&&_e.username===n,', 'delete')
patch('canPin:N||(c.is_huddle&&n&&c.username&&', 'canPin:N&&' + OK + '||(c.is_huddle&&n&&c.username&&', 'pin')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
