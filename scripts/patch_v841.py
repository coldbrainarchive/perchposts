#!/usr/bin/env python3
"""Patch v840 -> v841: one Mod tools row on the post page. Pin to Board, Pin to Forum, Lock, Archive and the
mod Delete sit together in amber pills, so they read differently from the buttons members get. A filled
pill means that setting is on. The author's own Delete stays with the normal buttons.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v840.js'
dst = '_deploy/assets/index-DUcNPOLc-v841.js'

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

# out of the normal row
patch(t('N&&(0,L.jsxs)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:async()=>{if(!confirm(`Are you sure?`))return;await zr({type:`delete_post`,post_id:c.id});o(`/`)},children:`Delete`}),N&&!c.frozen&&!(c.is_admin&&t!==`admin`)&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:async()=>{if(!confirm(`Archive this post? It stays on the site but freezes: no new chirps, wings or reactions, and its author can\'t delete it.`))return;await zr({type:`archive_post`,post_id:c.id});await P()},children:`Archive`}),N&&c.frozen&&(0,L.jsx)(`button`,{type:`button`,className:`feed-post-action-pill`,onClick:async()=>{await zr({type:`unarchive_post`,post_id:c.id}),P()},children:`Unarchive`}),'),
      '', 'remove from normal row')

BTN = lambda cls, click, label: '(0,L.jsx)(`button`,{type:`button`,className:' + cls + ',onClick:' + click + ',children:' + label + '})'
ROW = ('N&&(0,L.jsxs)(`div`,{className:`mod-tools`,children:[(0,L.jsx)(`span`,{className:`mod-tools-label`,children:`🛡️ Mod tools`}),(0,L.jsxs)(`div`,{className:`mod-tools-row`,children:['
       + 'c.pinned?' + BTN('`mod-tool on`', 'async()=>{await zr({type:`pin_post`,post_id:c.id,pinned:!1,pinned_global:!1}),P()}', '`📌 Unpin`')
       + ':(0,L.jsxs)(L.Fragment,{children:[' + BTN('`mod-tool`', 'async()=>{await zr({type:`pin_post`,post_id:c.id,pinned:!0,pinned_global:!1}),P()}', '`📌 Pin to Board`') + ','
       + BTN('`mod-tool`', 'async()=>{await zr({type:`pin_post`,post_id:c.id,pinned:!0,pinned_global:!0}),P()}', '`📍 Pin to Forum`') + ']}),'
       + BTN('c.locked?`mod-tool on`:`mod-tool`', 'async()=>{await zr({type:`lock_post`,post_id:c.id,locked:!c.locked}),P()}', 'c.locked?`🔓 Unlock`:`🔒 Lock`') + ','
       + '!c.frozen&&!(c.is_admin&&t!==`admin`)&&' + BTN('`mod-tool`', 'async()=>{if(!confirm(`Archive this post? It stays on the site but freezes: no new chirps, wings or reactions, and its author can\'t delete it.`))return;await zr({type:`archive_post`,post_id:c.id});await P()}', '`📦 Archive`') + ','
       + 'c.frozen&&' + BTN('`mod-tool on`', 'async()=>{await zr({type:`unarchive_post`,post_id:c.id}),P()}', '`📦 Unarchive`') + ','
       + '!(c.is_admin&&t!==`admin`)&&' + BTN('`mod-tool danger`', 'async()=>{if(!confirm(`Are you sure?`))return;await zr({type:`delete_post`,post_id:c.id});o(`/`)}', '`🗑️ Delete`')
       + ']})]})')

a = t('N&&(0,L.jsxs)(`div`,{style:{marginTop:14,marginBottom:10},children:[c.pinned?')
b = t('children:c.locked?`Unlock`:`Lock`})]})')
if content.count(a) != 1 or content.count(b) != 1:
    errors.append('FAIL (old row markers)')
else:
    i = content.index(a); j = content.index(b) + len(b)
    content = content[:i] + t(ROW) + content[j:]
    print('OK: mod tools row')

patch(t('_pv&&(0,L.jsx)(`button`,{type:`button`,className:`chat-view-all`,'), t('_pv&&(_cn||!(c.locked||c.frozen))&&(0,L.jsx)(`button`,{type:`button`,className:`chat-view-all`,'), 'no first chirp on frozen posts')

old = '.chat-section-title{display:flex;'
patch(old, '.mod-tools{margin-top:12px;padding-top:10px;border-top:1px solid rgba(251,191,36,.2)}'
      '.mod-tools-label{display:block;font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#d97706;margin-bottom:7px}'
      '.mod-tools-row{display:flex;flex-wrap:wrap;gap:6px}'
      '.mod-tool{display:inline-flex;align-items:center;height:26px;padding:0 10px;border-radius:999px;border:1px solid rgba(251,191,36,.4);background:rgba(251,191,36,.08);color:#fbbf24;font-size:11px;font-weight:700;cursor:pointer;white-space:nowrap}'
      '.mod-tool.on{background:#fbbf24;border-color:#fbbf24;color:#1c1400}'
      '.mod-tool.danger{border-color:rgba(248,113,113,.45);background:rgba(248,113,113,.08);color:#f87171}'
      + old, 'styles')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
