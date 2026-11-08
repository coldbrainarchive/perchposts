#!/usr/bin/env python3
"""Patch v845 -> v846: on a locked post nobody gets Delete on their own chirp, and reactions stay on. On an
archived post nothing can be changed: the Mod tools row only offers Unarchive, and chirps lose Delete and Pin.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v845.js'
dst = '_deploy/assets/index-DUcNPOLc-v846.js'

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

def t(s):
    return s.replace('`', q)

patch(t('canDelete:N&&(t===`admin`||!_e.is_admin)||ae&&n&&_e.username===n,'),
      t('canDelete:!c.frozen&&(N&&(t===`admin`||!_e.is_admin)||ae&&!c.locked&&n&&_e.username===n),'), 'chirp delete')
patch(t('canPin:N&&(t===`admin`||!_e.is_admin)||(c.is_huddle&&n&&c.username&&n.toLowerCase()===c.username.toLowerCase()&&_e.username&&_e.username.toLowerCase()===n.toLowerCase()),'),
      t('canPin:!c.frozen&&(N&&(t===`admin`||!_e.is_admin)||(c.is_huddle&&n&&c.username&&n.toLowerCase()===c.username.toLowerCase()&&_e.username&&_e.username.toLowerCase()===n.toLowerCase())),'), 'chirp pin')
patch(t('className:`mod-tools-row`,children:[c.pinned?'), t('className:`mod-tools-row`,children:[c.frozen?null:c.pinned?'), 'no pinning')
patch(t('(0,L.jsx)(`button`,{type:`button`,className:c.locked?`mod-tool on`:`mod-tool`,'), t('!c.frozen&&(0,L.jsx)(`button`,{type:`button`,className:c.locked?`mod-tool on`:`mod-tool`,'), 'no locking')
patch(t('!(c.is_admin&&t!==`admin`)&&(0,L.jsx)(`button`,{type:`button`,className:`mod-tool danger`,'), t('!c.frozen&&!(c.is_admin&&t!==`admin`)&&(0,L.jsx)(`button`,{type:`button`,className:`mod-tool danger`,'), 'no mod delete')
patch(t('c?.is_huddle&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,style:_wpInvOpen?'), t('c?.is_huddle&&!c.frozen&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,style:_wpInvOpen?'), 'no invites')
patch(t('return c?.is_huddle&&(_rIsOp||_rIsAdm||_rIsMod)?'), t('return c?.is_huddle&&!c.frozen&&(_rIsOp||_rIsAdm||_rIsMod)?'), 'no removing')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
