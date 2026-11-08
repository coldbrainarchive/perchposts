#!/usr/bin/env python3
"""Patch v103 -> v104: unban/unjail send all identifiers so the delete actually works."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v103.js'
dst = '_deploy/assets/index-DUcNPOLc-v104.js'

content = open(src, encoding='utf-8').read()
errors = []

# Fix unban: send username + ip_hash too
OLD_UNBAN = 'be(e)?await zr({type:`unban`,browser_id:e.browser_id})'
NEW_UNBAN = 'be(e)?await zr({type:`unban`,browser_id:e.browser_id,username:e.username,ip_hash:e.ip_hash})'
if OLD_UNBAN in content:
    content = content.replace(OLD_UNBAN, NEW_UNBAN, 1)
    print('OK: unban now sends browser_id + username + ip_hash')
else:
    errors.append('FAIL: unban call not found')

# Fix unjail: send username + ip_hash too
OLD_UNJAIL = 'Se(e)?await zr({type:`unjail`,browser_id:e.browser_id})'
NEW_UNJAIL = 'Se(e)?await zr({type:`unjail`,browser_id:e.browser_id,username:e.username,ip_hash:e.ip_hash})'
if OLD_UNJAIL in content:
    content = content.replace(OLD_UNJAIL, NEW_UNJAIL, 1)
    print('OK: unjail now sends browser_id + username + ip_hash')
else:
    errors.append('FAIL: unjail call not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
