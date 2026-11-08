#!/usr/bin/env python3
"""Patch v838 -> v839: permanently deleting posts is admin only, so mods lose Delete and Delete All in the
Deleted and Archived lists. Mods can't archive admin posts. Admin checks in the Mod Panel use the signed in
account's role, because the user_role setting isn't always there.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v838.js'
dst = '_deploy/assets/index-DUcNPOLc-v839.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label, count=1):
    global content
    n = content.count(old)
    if n != count:
        errors.append('FAIL (' + label + '): expected ' + str(count) + ' matches, found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

def t(s):
    return s.replace('`', q)

patch(t('function Gr(){let e=localStorage.getItem(`user_role`)===`admin`,'), t('function Gr(){let e=localStorage.getItem(`user_role`)===`admin`,_adm=e||Qn()?.role===`admin`,'), 'real admin check')
patch(t('e&&!d&&(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Delete ${i||`this flock member`}?'), t('_adm&&!d&&(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Delete ${i||`this flock member`}?'), 'member delete')
patch(t('p&&d.length>0&&(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Permanently delete all'), t('_adm&&p&&d.length>0&&(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Permanently delete all'), 'delete all')
patch(t('(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Permanently delete this post?`))return;'), t('_adm&&(0,L.jsx)(`button`,{onClick:async()=>{if(!confirm(`Permanently delete this post?`))return;'), 'single delete', 2)
patch(t('N&&!c.archived&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:async()=>{if(!confirm(`Archive this post?'),
      t('N&&!c.archived&&!(c.is_admin&&t!==`admin`)&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:async()=>{if(!confirm(`Archive this post?'), 'archive button')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
