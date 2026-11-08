#!/usr/bin/env python3
"""Patch v677 -> v678:
1. Fix comment overlap: marginLeft -> paddingLeft so card stays in bounds
2. More visible/dynamic stack: rotate shadows + stronger colors + bigger offset
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v677.js'
dst = '_deploy/assets/index-DUcNPOLc-v678.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append('FAIL (' + label + '): not found')
    elif n > 1:
        errors.append('FAIL (' + label + '): ' + str(n) + ' matches')
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

# ── Postcard container: marginLeft -> paddingLeft (no overflow into siblings) ──
patch(
    'position:' + q + 'relative' + q + ',marginTop:14,marginLeft:10},',
    'position:' + q + 'relative' + q + ',marginTop:6,paddingTop:13,paddingLeft:13},',
    'postcard container: marginLeft -> paddingLeft'
)

# ── Comment container: same fix ───────────────────────────────────────────────
patch(
    'marginBottom:_ct?8:0,marginLeft:10},',
    'marginBottom:_ct?8:0,paddingTop:13,paddingLeft:13},',
    'comment container: marginLeft -> paddingLeft'
)

# ── Postcard shadows (identified by _pAtts context) ──────────────────────────
patch(
    'top:-10,left:-10,right:0,bottom:0,borderRadius:10,background:' + q + '#252836' + q + ',zIndex:0}}),_pAtts.length>1',
    'top:-13,left:-13,right:0,bottom:0,borderRadius:10,background:' + q + '#3a3d4e' + q + ',zIndex:0,transform:' + q + 'rotate(-5deg)' + q + '}}),_pAtts.length>1',
    'postcard shadow 2: bigger + rotated + brighter'
)
patch(
    'top:-5,left:-5,right:0,bottom:0,borderRadius:10,background:' + q + '#1e2130' + q + ',zIndex:0}}),(0,L.jsx)(' + q + 'img' + q + ',{src:_pAtts[0].url',
    'top:-7,left:-7,right:0,bottom:0,borderRadius:10,background:' + q + '#2e3140' + q + ',zIndex:0,transform:' + q + 'rotate(-2.5deg)' + q + '}}),(0,L.jsx)(' + q + 'img' + q + ',{src:_pAtts[0].url',
    'postcard shadow 1: bigger + rotated + brighter'
)

# ── Comment shadows (borderRadius:8, already patched above) ───────────────────
# (handled above with borderRadius:8)

# ── Post detail shadows (identified by _tAtts context) ────────────────────────
patch(
    'top:-10,left:-10,right:0,bottom:0,borderRadius:10,background:' + q + '#252836' + q + ',zIndex:0}}),_tAtts.length>1',
    'top:-13,left:-13,right:0,bottom:0,borderRadius:10,background:' + q + '#3a3d4e' + q + ',zIndex:0,transform:' + q + 'rotate(-5deg)' + q + '}}),_tAtts.length>1',
    'post detail shadow 2: bigger + rotated'
)
patch(
    'top:-5,left:-5,right:0,bottom:0,borderRadius:10,background:' + q + '#1e2130' + q + ',zIndex:0}}),(0,L.jsx)(' + q + 'img' + q + ',{src:_tAtts[0].url',
    'top:-7,left:-7,right:0,bottom:0,borderRadius:10,background:' + q + '#2e3140' + q + ',zIndex:0,transform:' + q + 'rotate(-2.5deg)' + q + '}}),(0,L.jsx)(' + q + 'img' + q + ',{src:_tAtts[0].url',
    'post detail shadow 1: bigger + rotated'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print('Paren delta: ' + str(p_delta) + ', Brace delta: ' + str(b_delta))

open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
