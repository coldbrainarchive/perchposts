#!/usr/bin/env python3
"""Patch v204 -> v205: fix JSX syntax error; wrap link row + loading in Fragment."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v204.js'
dst = '_deploy/assets/index-DUcNPOLc-v205.js'

content = open(src, encoding='utf-8').read()
errors = []

# Revert the broken v204 change and replace with a proper Fragment wrapper
OLD = (
    'ee===`link`&&(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8,marginTop:10},'
    'children:[(0,L.jsx)(`input`,{value:O,onChange:e=>k(e.target.value),'
    'onKeyDown:e=>e.key===`Enter`&&N(),placeholder:`Paste a URL...`,autoFocus:!0,'
    'style:{flex:1,minWidth:0,padding:`6px 12px`,borderRadius:8,border:`1px solid #3f4756`,'
    'background:`#0f1117`,color:`#f8fafc`,fontSize:16,outline:`none`}}),'
    '(0,L.jsx)(`button`,{type:`button`,onClick:N,disabled:A,'
    'style:{flexShrink:0,padding:`6px 12px`,borderRadius:8,border:`none`,'
    'background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:13,cursor:`pointer`},'
    'children:A?`…`:`Add`})]),A&&(0,L.jsx)(`div`,{style:{textAlign:`center`,'
    'padding:`10px 0 2px`,color:`#94a3b8`,fontSize:13},children:`Fetching link preview…`})'
    ']}),'
)
NEW = (
    'ee===`link`&&(0,L.jsxs)(L.Fragment,{children:['
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:8,marginTop:10},'
    'children:[(0,L.jsx)(`input`,{value:O,onChange:e=>k(e.target.value),'
    'onKeyDown:e=>e.key===`Enter`&&N(),placeholder:`Paste a URL...`,autoFocus:!0,'
    'style:{flex:1,minWidth:0,padding:`6px 12px`,borderRadius:8,border:`1px solid #3f4756`,'
    'background:`#0f1117`,color:`#f8fafc`,fontSize:16,outline:`none`}}),'
    '(0,L.jsx)(`button`,{type:`button`,onClick:N,disabled:A,'
    'style:{flexShrink:0,padding:`6px 12px`,borderRadius:8,border:`none`,'
    'background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:13,cursor:`pointer`},'
    'children:A?`…`:`Add`})]}),'
    'A&&(0,L.jsx)(`div`,{style:{textAlign:`center`,padding:`8px 0 2px`,'
    'color:`#94a3b8`,fontSize:13},children:`Fetching link preview…`})'
    ']}),'
)

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: link row + loading wrapped in Fragment')
else:
    errors.append('FAIL: broken link section not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
