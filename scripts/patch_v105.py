#!/usr/bin/env python3
"""Patch v104 -> v105: nice modal for banned/caged, server-side cage check."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v104.js'
dst = '_deploy/assets/index-DUcNPOLc-v105.js'

content = open(src, encoding='utf-8').read()
errors = []

CAGE_ICON = '\U0001fab9'
BAN_ICON  = '\U0001f6ab'

HELPER = (
    'function _showBlock(msg,type){'
    'var o=document.createElement("div");'
    'o.style.cssText="position:fixed;inset:0;background:rgba(0,0,0,0.75);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:pointer;";'
    'var icon=type==="caged"?"' + CAGE_ICON + '":"' + BAN_ICON + '";'
    'o.innerHTML="<div style=\\"background:#1a1d27;border:1px solid #2e303a;border-radius:16px;padding:32px 28px;max-width:320px;width:90%;text-align:center;\\">"'
    '+"<div style=\\"font-size:44px;margin-bottom:14px;\\">"+icon+"</div>"'
    '+"<div style=\\"color:#f8fafc;font-size:17px;font-weight:700;margin-bottom:6px;\\">"+msg+"</div>"'
    '+"<div style=\\"color:#64748b;font-size:12px;\\">Tap anywhere to dismiss</div></div>";'
    'o.onclick=function(){o.remove()};'
    'document.body.appendChild(o);'
    'setTimeout(function(){if(o.parentNode)o.remove()},5000)'
    '};'
)

# Inject at the very start of the file
content = HELPER + content
print('OK: injected _showBlock helper at file start')

# Replace banned/caged alert on post submission
OLD_POST = 'g.error===`Banned`?alert(`' + BAN_ICON + ' You are banned from posting`):alert(g.error)'
NEW_POST = (
    'g.error===`Banned`?_showBlock("You are banned from postchats."):'
    'g.error===`Caged`?_showBlock("You are caged — posting is restricted.","caged"):'
    'alert(g.error)'
)
if OLD_POST in content:
    content = content.replace(OLD_POST, NEW_POST, 1)
    print('OK: post banned/caged -> modal')
else:
    errors.append('FAIL: post banned alert not found')

# Replace banned/caged alert on comment submission
OLD_CMT = 'u.error===`Banned`?alert(`' + BAN_ICON + ' You are banned from commenting`):alert(u.error)'
NEW_CMT = (
    'u.error===`Banned`?_showBlock("You are banned from postchats."):'
    'u.error===`Caged`?_showBlock("You are caged — commenting is restricted.","caged"):'
    'alert(u.error)'
)
if OLD_CMT in content:
    content = content.replace(OLD_CMT, NEW_CMT, 1)
    print('OK: comment banned/caged -> modal')
else:
    errors.append('FAIL: comment banned alert not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
