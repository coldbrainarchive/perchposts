#!/usr/bin/env python3
"""Patch v843 -> v844: mods get no controls on admin posts. The Mod tools row is gone for them on those
posts, and so are Restore, Unarchive and Hide in the Mod Panel. The server refuses these anyway.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v843.js'
dst = '_deploy/assets/index-DUcNPOLc-v844.js'

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

patch(t('N&&(0,L.jsxs)(`div`,{className:`mod-tools`,'), t('N&&!(c.is_admin&&t!==`admin`)&&(0,L.jsxs)(`div`,{className:`mod-tools`,'), 'no row on admin posts')
for kind in ('restore_post', 'hide_archive', 'unarchive_post'):
    old = '(0,L.jsx)(`button`,{onClick:async()=>{await zr({type:`' + kind + '`,post_id:e.id'
    patch(t(old), t('(_adm||!e.is_admin)&&' + old), 'panel ' + kind)

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
