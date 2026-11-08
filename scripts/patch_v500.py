#!/usr/bin/env python3
"""Patch v499 -> v500: Add username to delete-my-post fetch so logged-in
users can delete their own posts (worker now accepts username OR browser_id)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v499.js'
dst = '_deploy/assets/index-DUcNPOLc-v500.js'

content = open(src, encoding='utf-8').read()

OLD = ('body:JSON.stringify({post_id:c.id,browser_id:Gn()})});o(`/`)},'
       'children:`Delete`}),N&&')
NEW = ('body:JSON.stringify({post_id:c.id,browser_id:Gn(),'
       'username:localStorage.getItem(`_myUsername`)||null})});o(`/`)},'
       'children:`Delete`}),N&&')

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: username added to delete-my-post request')
else:
    print('FAIL'); sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
