#!/usr/bin/env python3
"""Patch v1262 -> v1263: mods can pin, lock, cage and flag; archive, unarchive, restore, hide-from-members and
ban / unban / ban IP are admin-only (the worker refuses them for mods too). Hides those buttons from mods:
post page Archive / Unarchive, mod panel Restore / Hide from members / Unarchive, Flock Ban / Unban / Ban IP."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1262.js'
dst = '_deploy/assets/index-DUcNPOLc-v1263.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch("!c.frozen&&!(c.is_admin&&t!==`admin`)&&(0,L.jsxs)(`button`,{type:`button`,className:`mod-tool`,onClick:async()=>{if(!confirm(`Archive this post?",
      "t===`admin`&&!c.frozen&&(0,L.jsxs)(`button`,{type:`button`,className:`mod-tool`,onClick:async()=>{if(!confirm(`Archive this post?", 'post Archive: admins')
patch("c.frozen&&(0,L.jsxs)(`button`,{type:`button`,className:`mod-tool on`,onClick:async()=>{await zr({type:`unarchive_post`",
      "t===`admin`&&c.frozen&&(0,L.jsxs)(`button`,{type:`button`,className:`mod-tool on`,onClick:async()=>{await zr({type:`unarchive_post`", 'post Unarchive: admins')
for t in ['restore_post', 'hide_archive', 'unarchive_post']:
    patch("(_adm||!e.is_admin)&&(0,L.jsxs)(`button`,{onClick:async()=>{await zr({type:`%s`" % t,
          "_adm&&(0,L.jsxs)(`button`,{onClick:async()=>{await zr({type:`%s`" % t, 'panel %s: admins' % t)
patch("(0,L.jsxs)(`button`,{onClick:()=>xe(o),className:s?`mod-tool fs`:`mod-tool danger fs`",
      "_adm&&(0,L.jsxs)(`button`,{onClick:()=>xe(o),className:s?`mod-tool fs`:`mod-tool danger fs`", 'Ban/Unban: admins')
patch("!s&&(0,L.jsxs)(`button`,{onClick:()=>_banIp(o)", "_adm&&!s&&(0,L.jsxs)(`button`,{onClick:()=>_banIp(o)", 'Ban IP: admins')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
