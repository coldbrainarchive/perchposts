#!/usr/bin/env python3
"""Patch v676 -> v677:
1. Stacked cards: change shadows from bottom-oriented to top-left-oriented
   (peek from upper-left like fanned cards), add marginLeft for space
2. Badge: move from bottom-right to top-right, remove camera emoji, just number
Both postcard and comment stacked cards updated.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v676.js'
dst = '_deploy/assets/index-DUcNPOLc-v677.js'

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

# ── Postcard ──────────────────────────────────────────────────────────────────

# Postcard container + shadows (use _pAtts prefix for uniqueness)
patch(
    'position:' + q + 'relative' + q + ',marginTop:6},children:[_pAtts.length>2&&(0,L.jsx)(' + q + 'div' + q
    + ',{style:{position:' + q + 'absolute' + q + ',bottom:-6,left:6,right:6,height:' + q + '100%' + q
    + ',borderRadius:10,background:' + q + '#252836' + q + ',zIndex:0}}),_pAtts.length>1&&(0,L.jsx)(' + q + 'div' + q
    + ',{style:{position:' + q + 'absolute' + q + ',bottom:-3,left:3,right:3,height:' + q + '100%' + q
    + ',borderRadius:10,background:' + q + '#1e2130' + q + ',zIndex:0}}),',
    'position:' + q + 'relative' + q + ',marginTop:14,marginLeft:10},children:[_pAtts.length>2&&(0,L.jsx)(' + q + 'div' + q
    + ',{style:{position:' + q + 'absolute' + q + ',top:-10,left:-10,right:0,bottom:0'
    + ',borderRadius:10,background:' + q + '#252836' + q + ',zIndex:0}}),_pAtts.length>1&&(0,L.jsx)(' + q + 'div' + q
    + ',{style:{position:' + q + 'absolute' + q + ',top:-5,left:-5,right:0,bottom:0'
    + ',borderRadius:10,background:' + q + '#1e2130' + q + ',zIndex:0}}),',
    'postcard: container margins + top-left shadows'
)

# Badge: move to top-right, remove emoji
patch(
    'bottom:10,right:10,background:' + q + 'rgba(0,0,0,0.6)' + q
    + ',color:' + q + 'white' + q + ',borderRadius:20,padding:' + q + '3px 10px' + q
    + ',fontSize:13,fontWeight:600,zIndex:2,pointerEvents:' + q + 'none' + q
    + '},children:' + q + '📷 ' + q + '+_pAtts.length',
    'top:8,right:8,background:' + q + 'rgba(0,0,0,0.6)' + q
    + ',color:' + q + 'white' + q + ',borderRadius:20,padding:' + q + '3px 10px' + q
    + ',fontSize:13,fontWeight:600,zIndex:2,pointerEvents:' + q + 'none' + q
    + '},children:_pAtts.length',
    'postcard badge: top-right, no emoji'
)

# ── Comment ───────────────────────────────────────────────────────────────────

# Container: add marginLeft
patch(
    'position:' + q + 'relative' + q + ',marginBottom:_ct?8:0},onClick:_ev=>_ev.stopPropagation(),children:['
    + '_cAtts.length>2&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
    + ',bottom:-6,left:6,right:6,height:' + q + '100%' + q + ',borderRadius:8,background:' + q + '#252836' + q + ',zIndex:0}})',
    'position:' + q + 'relative' + q + ',marginBottom:_ct?8:0,marginLeft:10},onClick:_ev=>_ev.stopPropagation(),children:['
    + '_cAtts.length>2&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
    + ',top:-10,left:-10,right:0,bottom:0,borderRadius:8,background:' + q + '#252836' + q + ',zIndex:0}})',
    'comment container+shadow2: top-left, add marginLeft'
)

# Comment shadow 1
patch(
    'bottom:-3,left:3,right:3,height:' + q + '100%' + q + ',borderRadius:8,background:' + q + '#1e2130' + q + ',zIndex:0',
    'top:-5,left:-5,right:0,bottom:0,borderRadius:8,background:' + q + '#1e2130' + q + ',zIndex:0',
    'comment shadow 1: top-left orientation'
)

# Comment badge: top-right, no emoji
patch(
    'bottom:8,right:8,background:' + q + 'rgba(0,0,0,0.6)' + q
    + ',color:' + q + 'white' + q + ',borderRadius:20,padding:' + q + '3px 10px' + q
    + ',fontSize:12,fontWeight:600,zIndex:2,pointerEvents:' + q + 'none' + q
    + '},children:' + q + '📷 ' + q + '+_cAtts.length',
    'top:8,right:8,background:' + q + 'rgba(0,0,0,0.6)' + q
    + ',color:' + q + 'white' + q + ',borderRadius:20,padding:' + q + '3px 10px' + q
    + ',fontSize:12,fontWeight:600,zIndex:2,pointerEvents:' + q + 'none' + q
    + '},children:_cAtts.length',
    'comment badge: top-right, no emoji'
)

# Post detail (uses _tAtts)
patch(
    '_tAtts.length>2&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
    + ',bottom:-6,left:6,right:6,height:' + q + '100%' + q + ',borderRadius:10,background:' + q + '#252836' + q + ',zIndex:0}}),_tAtts.length>1&&(0,L.jsx)(' + q + 'div' + q
    + ',{style:{position:' + q + 'absolute' + q + ',bottom:-3,left:3,right:3,height:' + q + '100%' + q + ',borderRadius:10,background:' + q + '#1e2130' + q + ',zIndex:0}}),',
    '_tAtts.length>2&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
    + ',top:-10,left:-10,right:0,bottom:0,borderRadius:10,background:' + q + '#252836' + q + ',zIndex:0}}),_tAtts.length>1&&(0,L.jsx)(' + q + 'div' + q
    + ',{style:{position:' + q + 'absolute' + q + ',top:-5,left:-5,right:0,bottom:0,borderRadius:10,background:' + q + '#1e2130' + q + ',zIndex:0}}),',
    'post detail shadows: top-left'
)
patch(
    'bottom:10,right:10,background:' + q + 'rgba(0,0,0,0.6)' + q
    + ',color:' + q + 'white' + q + ',borderRadius:20,padding:' + q + '3px 10px' + q
    + ',fontSize:13,fontWeight:600,zIndex:2,pointerEvents:' + q + 'none' + q
    + '},children:' + q + '📷 ' + q + '+_tAtts.length',
    'top:8,right:8,background:' + q + 'rgba(0,0,0,0.6)' + q
    + ',color:' + q + 'white' + q + ',borderRadius:20,padding:' + q + '3px 10px' + q
    + ',fontSize:13,fontWeight:600,zIndex:2,pointerEvents:' + q + 'none' + q
    + '},children:_tAtts.length',
    'post detail badge: top-right, no emoji'
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
