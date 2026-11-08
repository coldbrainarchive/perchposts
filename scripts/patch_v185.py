#!/usr/bin/env python3
"""Patch v184 -> v185: remove bird/pencil emoji from empty-state placeholders."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v184.js'
dst = '_deploy/assets/index-DUcNPOLc-v185.js'

content = open(src, encoding='utf-8').read()
errors = []

# Remove bird emoji div from "No notifications yet"
OLD_NOTIF = '(0,L.jsx)(`div`,{style:{fontSize:36,marginBottom:12},children:`🐦`}),(0,L.jsx)(`div`,{style:{fontSize:14,fontWeight:600},children:`No notifications yet`})'
NEW_NOTIF = '(0,L.jsx)(`div`,{style:{fontSize:14,fontWeight:600},children:`No notifications yet`})'
if OLD_NOTIF in content:
    content = content.replace(OLD_NOTIF, NEW_NOTIF, 1)
    print('OK: removed bird from no-notifications placeholder')
else:
    errors.append('FAIL: no-notifications bird not found')

# Remove pencil emoji div from "No posts yet"
OLD_POSTS = '(0,L.jsx)(`div`,{style:{fontSize:32,marginBottom:10},children:`📝`}),(0,L.jsx)(`div`,{style:{fontSize:14,fontWeight:600},children:`No posts yet`})'
NEW_POSTS = '(0,L.jsx)(`div`,{style:{fontSize:14,fontWeight:600},children:`No posts yet`})'
if OLD_POSTS in content:
    content = content.replace(OLD_POSTS, NEW_POSTS, 1)
    print('OK: removed pencil from no-posts placeholder')
else:
    errors.append('FAIL: no-posts pencil not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
