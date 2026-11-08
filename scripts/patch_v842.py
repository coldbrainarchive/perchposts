#!/usr/bin/env python3
"""Patch v841 -> v842: tapping the Mod tools title opens and closes the row. It starts closed, and the
choice is remembered on that device. Reading storage can fail in private windows, so that's guarded.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v841.js'
dst = '_deploy/assets/index-DUcNPOLc-v842.js'

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

patch(t('[_ldO,_setLdO]=(0,_.useState)(!1);'),
      t('[_ldO,_setLdO]=(0,_.useState)(!1),[_mt,_setMt]=(0,_.useState)(()=>{try{return localStorage.getItem(`mod_tools_open`)===`1`}catch{return!1}});'), 'open state')
patch(t('(0,L.jsx)(`span`,{className:`mod-tools-label`,children:`🛡️ Mod tools`}),(0,L.jsxs)(`div`,{className:`mod-tools-row`,children:['),
      t('(0,L.jsxs)(`button`,{type:`button`,className:`mod-tools-label`,"aria-expanded":_mt,onClick:()=>_setMt(_v=>{try{localStorage.setItem(`mod_tools_open`,_v?`0`:`1`)}catch{}return!_v}),children:[`🛡️ Mod tools `,(0,L.jsx)(`span`,{className:`mod-tools-arrow`,children:_mt?`▾`:`▸`})]}),_mt&&(0,L.jsxs)(`div`,{className:`mod-tools-row`,children:['), 'title opens and closes')
patch('.mod-tools-label{display:block;font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#d97706;margin-bottom:7px}'
      '.mod-tools-row{display:flex;flex-wrap:wrap;gap:6px}',
      '.mod-tools-label{display:block;background:none;border:none;padding:4px 0;font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#d97706;cursor:pointer}'
      '.mod-tools-arrow{font-size:11px}'
      '.mod-tools-row{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}', 'styles')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
