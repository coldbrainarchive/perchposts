#!/usr/bin/env python3
"""Patch v91 -> v92:
- _gu starts empty ("") so signup shows "tap to generate" placeholder
- handleAuth also requires _gu to be set before submitting signup
- Signup username area looks like the actual user-pill tag
"""
import sys, re

src = '_deploy/assets/index-DUcNPOLc-v91.js'
dst = '_deploy/assets/index-DUcNPOLc-v92.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── Extract the BIRD_GEN IIFE (the one in the shuffle button onclick) ─────────
# We'll need it verbatim for the new UI onClick
iife_start = content.find('(function(){var _a=["african"')
iife_end   = content.find('})()', iife_start) + 4
BIRD_GEN   = content[iife_start:iife_end]
print(f'Extracted BIRD_GEN IIFE ({len(BIRD_GEN)} chars)')

# ── 1. Change _gu initial state from BIRD_GEN IIFE to empty string ────────────
# Pattern: [_gu,_su]=(0,_.useState)(<BIG IIFE>),[y,b]=
OLD_STATE_START = '[_gu,_su]=(0,_.useState)((function(){var _a=['
OLD_STATE_END   = ',[y,b]=(0,_.useState)(``)'

idx = content.find(OLD_STATE_START)
if idx == -1:
    errors.append('FAIL: _gu state start not found')
else:
    end_idx = content.find(OLD_STATE_END, idx)
    if end_idx == -1:
        errors.append('FAIL: _gu state end marker not found')
    else:
        old_block = content[idx:end_idx]
        new_block = '[_gu,_su]=(0,_.useState)(``)'
        content = content[:idx] + new_block + content[end_idx:]
        print(f'OK: _gu initial state changed to empty string (removed {len(old_block)} chars)')

# ── 2. Update handleAuth guard: signup also requires _gu ─────────────────────
OLD_GUARD = 'if(!(C?!x:(!y.trim()||!x)))'
NEW_GUARD = 'if(!(C?(!_gu||!x):(!y.trim()||!x)))'
if OLD_GUARD in content:
    content = content.replace(OLD_GUARD, NEW_GUARD, 1)
    print('OK: handleAuth guard now requires _gu for signup')
else:
    errors.append('FAIL: handleAuth guard not found')

# ── 3. Replace signup display with pill-style UI ──────────────────────────────
# Find the full C? block we need to replace
OLD_DISPLAY_START = 'C?(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:8},children:['
OLD_DISPLAY_END   = ':(0,L.jsx)(`input`,{placeholder:`Username`'

idx = content.find(OLD_DISPLAY_START)
if idx == -1:
    errors.append('FAIL: signup display start not found')
else:
    end_idx = content.find(OLD_DISPLAY_END, idx)
    if end_idx == -1:
        errors.append('FAIL: signup display end not found')
    else:
        old_display = content[idx:end_idx]
        # New pill display
        NEW_DISPLAY = (
            'C?'
            # Outer column wrapper
            '(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,gap:8},children:['
              # The pill itself — tap to generate (empty) or tap to shuffle (filled)
              '(0,L.jsxs)(`span`,{'
                'onClick:function(){_su(' + BIRD_GEN + ')},'
                'style:{'
                  'display:`inline-flex`,alignItems:`center`,gap:6,'
                  'padding:`6px 14px 6px 10px`,borderRadius:999,'
                  'border:_gu?`1.5px solid #c084fc55`:`1.5px dashed #3f4756`,'
                  'background:_gu?`#c084fc18`:`transparent`,'
                  'color:_gu?`#c084fc`:`#64748b`,'
                  'fontSize:13,fontWeight:700,lineHeight:1,'
                  'whiteSpace:`nowrap`,cursor:`pointer`,userSelect:`none`,'
                  'flexShrink:0,boxSizing:`border-box`,'
                  'alignSelf:`flex-start`'
                '},'
                'children:['
                  '(0,L.jsx)(`span`,{style:{fontSize:15},children:`\U0001f424`}),'
                  '(0,L.jsx)(`span`,{children:_gu||`tap to generate`})'
                ']'
              '}),'
              # Subtext + copy — only shown once name is generated
              '_gu?(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:8},children:['
                '(0,L.jsx)(`span`,{style:{fontSize:11,color:`#64748b`},children:`tap to shuffle`}),'
                '(0,L.jsx)(`button`,{'
                  'onClick:function(ev){'
                    'try{'
                      'navigator.clipboard.writeText(_gu);'
                      'var b=ev.currentTarget;'
                      'b.textContent="✓";'
                      'b.style.color="#22c55e";'
                      'setTimeout(function(){b.textContent="\U0001f4cb";b.style.color="#64748b"},1500)'
                    '}catch(err){}'
                  '},'
                  'style:{background:`transparent`,border:`none`,cursor:`pointer`,color:`#64748b`,fontSize:14,padding:`0 2px`,lineHeight:1,flexShrink:0},'
                  'children:`\U0001f4cb`'
                '})'
              ']}):null'
            ']})'
        )
        content = content[:idx] + NEW_DISPLAY + content[end_idx:]
        print('OK: signup display replaced with pill UI')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'\nWrote {dst}')
