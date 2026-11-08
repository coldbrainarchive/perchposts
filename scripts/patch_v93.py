#!/usr/bin/env python3
"""Patch v92 -> v93:
- Move 'tap to shuffle' + copy button to the right of the username pill (same row)
- Change placeholder text to 'tap to generate username'
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v92.js'
dst = '_deploy/assets/index-DUcNPOLc-v93.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Outer wrapper: column → row ────────────────────────────────────────────
OLD_OUTER = (
    'display:`flex`,flexDirection:`column`,gap:8},'
    'children:[(0,L.jsxs)(`span`,{onClick:function(){_su('
)
NEW_OUTER = (
    'display:`flex`,alignItems:`center`,gap:8},'
    'children:[(0,L.jsxs)(`span`,{onClick:function(){_su('
)
if OLD_OUTER in content:
    content = content.replace(OLD_OUTER, NEW_OUTER, 1)
    print('OK: outer wrapper changed to row')
else:
    errors.append('FAIL: outer wrapper not found')

# ── 2. Remove alignSelf from pill (not needed in row layout) ──────────────────
OLD_ALIGN = (
    'flexShrink:0,boxSizing:`border-box`,alignSelf:`flex-start`},'
    'children:[(0,L.jsx)(`span`,{style:{fontSize:15},children:`\U0001f424`})'
)
NEW_ALIGN = (
    'flexShrink:0,boxSizing:`border-box`},'
    'children:[(0,L.jsx)(`span`,{style:{fontSize:15},children:`\U0001f424`})'
)
if OLD_ALIGN in content:
    content = content.replace(OLD_ALIGN, NEW_ALIGN, 1)
    print('OK: removed alignSelf from pill')
else:
    errors.append('FAIL: alignSelf pattern not found')

# ── 3. Placeholder text ───────────────────────────────────────────────────────
OLD_TEXT = 'children:_gu||`tap to generate`'
NEW_TEXT = 'children:_gu||`tap to generate username`'
if OLD_TEXT in content:
    content = content.replace(OLD_TEXT, NEW_TEXT, 1)
    print('OK: placeholder text updated')
else:
    errors.append('FAIL: placeholder text not found')

# ── 4. Unwrap inner div — make span + button direct siblings of outer row ──────
OLD_INNER = (
    '_gu?(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:8},children:['
    '(0,L.jsx)(`span`,{style:{fontSize:11,color:`#64748b`},children:`tap to shuffle`}),'
    '(0,L.jsx)(`button`,{onClick:function(ev){try{navigator.clipboard.writeText(_gu);'
    'var b=ev.currentTarget;b.textContent="✓";b.style.color="#22c55e";'
    'setTimeout(function(){b.textContent="\U0001f4cb";b.style.color="#64748b"},1500)'
    '}catch(err){}},style:{background:`transparent`,border:`none`,cursor:`pointer`,'
    'color:`#64748b`,fontSize:14,padding:`0 2px`,lineHeight:1,flexShrink:0},'
    'children:`\U0001f4cb`})'
    ']}):null'
)
NEW_INNER = (
    '_gu?(0,L.jsx)(`span`,{style:{fontSize:11,color:`#64748b`},children:`tap to shuffle`}):null,'
    '_gu?(0,L.jsx)(`button`,{onClick:function(ev){try{navigator.clipboard.writeText(_gu);'
    'var b=ev.currentTarget;b.textContent="✓";b.style.color="#22c55e";'
    'setTimeout(function(){b.textContent="\U0001f4cb";b.style.color="#64748b"},1500)'
    '}catch(err){}},style:{background:`transparent`,border:`none`,cursor:`pointer`,'
    'color:`#64748b`,fontSize:14,padding:`0 2px`,lineHeight:1,flexShrink:0},'
    'children:`\U0001f4cb`}):null'
)
if OLD_INNER in content:
    content = content.replace(OLD_INNER, NEW_INNER, 1)
    print('OK: inner div unwrapped — shuffle + copy are now row siblings')
else:
    errors.append('FAIL: inner div wrapper not found')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'\nWrote {dst}')
