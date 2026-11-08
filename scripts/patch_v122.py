#!/usr/bin/env python3
"""Patch v121 -> v122: styled ban/cage modals with big icons, swap alert() back."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v121.js'
dst = '_deploy/assets/index-DUcNPOLc-v122.js'

content = open(src, encoding='utf-8').read()
errors = []

# 1. Update _showBlock: red ✕ for banned, 🪹 for caged
OLD_BLOCK = (
    'function _showBlock(msg,type){'
    'var o=document.createElement("div");'
    'o.style.cssText="position:fixed;inset:0;background:rgba(0,0,0,0.75);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:pointer;";'
    'var icon=type==="caged"?"\U0001fab9":"🚫";'
    'o.innerHTML="<div style=\\"background:#1a1d27;border:1px solid #2e303a;border-radius:16px;padding:32px 28px;max-width:320px;width:90%;text-align:center;\\">"'
    '+"<div style=\\"font-size:44px;margin-bottom:14px;\\">"+icon+"</div>"'
    '+"<div style=\\"color:#f8fafc;font-size:17px;font-weight:700;margin-bottom:6px;\\">"+msg+"</div>"'
    '+"<div style=\\"color:#64748b;font-size:12px;\\">Tap anywhere to dismiss</div></div>";'
    'o.onclick=function(){o.remove()};document.body.appendChild(o)'
    '}'
)
NEW_BLOCK = (
    'function _showBlock(msg,type){'
    'var o=document.createElement("div");'
    'o.style.cssText="position:fixed;inset:0;background:rgba(0,0,0,0.75);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:pointer;";'
    'var icon=type==="caged"'
    '?"<span style=\\"font-size:56px;display:block;margin-bottom:14px;\\">\U0001fab9</span>"'
    ':"<span style=\\"font-size:64px;font-weight:900;color:#ef4444;display:block;margin-bottom:14px;line-height:1;\\">✕</span>";'
    'o.innerHTML="<div style=\\"background:#1a1d27;border:1px solid #2e303a;border-radius:16px;padding:32px 28px;max-width:320px;width:90%;text-align:center;\\">"'
    '+icon'
    '+"<div style=\\"color:#f8fafc;font-size:17px;font-weight:700;margin-bottom:6px;\\">"+msg+"</div>"'
    '+"<div style=\\"color:#64748b;font-size:12px;\\">Tap anywhere to dismiss</div></div>";'
    'o.onclick=function(){o.remove()};document.body.appendChild(o)'
    '}'
)
if OLD_BLOCK in content:
    content = content.replace(OLD_BLOCK, NEW_BLOCK, 1)
    print('OK: _showBlock updated with styled icons')
else:
    errors.append('FAIL: _showBlock not found')

BAN_ALERT  = 'alert("You are banned from postchats.")'
CAGE_ALERT = 'alert("You’re Caged! You can only post and comment in \U0001fab9 The Cage")'
BAN_BLOCK  = '_showBlock("You are banned from postchats.")'
CAGE_BLOCK = '_showBlock("You’re Caged! You can only post and comment in \U0001fab9 The Cage","caged")'

# 2. Swap ban alerts -> _showBlock
count = content.count(BAN_ALERT)
if count:
    content = content.replace(BAN_ALERT, BAN_BLOCK)
    print(f'OK: swapped {count} ban alert(s) to _showBlock')
else:
    errors.append('FAIL: ban alert not found')

# 3. Swap cage alerts -> _showBlock
count = content.count(CAGE_ALERT)
if count:
    content = content.replace(CAGE_ALERT, CAGE_BLOCK)
    print(f'OK: swapped {count} cage alert(s) to _showBlock')
else:
    errors.append('FAIL: cage alert not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
