#!/usr/bin/env python3
"""Patch v674 -> v675:
1. Postcard: grid -> stacked (only loads front photo, stack shadow cards behind)
2. Post detail: add multi-photo stacked view (uses _tAtts)
3. Cap photo upload at 9 (change slice(0,10) -> slice(0,9))
4. Remove overall delete-all X for images type (keep per-image X only)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v674.js'
dst = '_deploy/assets/index-DUcNPOLc-v675.js'

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

# ── Extract lightbox code from grid item (replace _pAtts, ci=_i) ──────────────
raw = open(src, encoding='utf-8').read()
lb_inner_start = raw.find('_ev.stopPropagation();let _ci=_i;', raw.find('_pAtts.map('))
lb_inner_end   = raw.find('document.body.appendChild(_ov);},key:_i', lb_inner_start) + len('document.body.appendChild(_ov);')
lb_for_postcard = raw[lb_inner_start:lb_inner_end].replace('let _ci=_i;', 'let _ci=0;')

# ── Build stacked view helper ─────────────────────────────────────────────────
def make_stacked(atts_var, lb_code):
    q = chr(0x60)
    return (
        '(0,L.jsxs)(' + q + 'div' + q + ',{style:{position:' + q + 'relative' + q + ',marginTop:6},children:['
        + atts_var + '.length>2&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
        + ',bottom:-6,left:6,right:6,height:' + q + '100%' + q + ',borderRadius:10,background:' + q + '#252836' + q + ',zIndex:0}}),'
        + atts_var + '.length>1&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
        + ',bottom:-3,left:3,right:3,height:' + q + '100%' + q + ',borderRadius:10,background:' + q + '#1e2130' + q + ',zIndex:0}}),'
        + '(0,L.jsx)(' + q + 'img' + q + ',{src:' + atts_var + '[0].url,'
        + 'style:{width:' + q + '100%' + q + ',height:320,objectFit:' + q + 'cover' + q
        + ',borderRadius:10,display:' + q + 'block' + q + ',cursor:' + q + 'zoom-in' + q
        + ',position:' + q + 'relative' + q + ',zIndex:1},'
        + 'onClick:_ev=>{' + lb_code + '}}),'
        + atts_var + '.length>1&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
        + ',bottom:10,right:10,background:' + q + 'rgba(0,0,0,0.6)' + q
        + ',color:' + q + 'white' + q + ',borderRadius:20,padding:' + q + '3px 10px' + q
        + ',fontSize:13,fontWeight:600,zIndex:2,pointerEvents:' + q + 'none' + q + '},children:' + q + '📷 ' + q + '+' + atts_var + '.length})'
        + ']})'
    )

stacked_postcard = make_stacked('_pAtts', lb_for_postcard)

# lb for post detail - same but _pAtts -> _tAtts
lb_for_detail = lb_for_postcard.replace('_pAtts', '_tAtts')
stacked_detail = make_stacked('_tAtts', lb_for_detail)

# ── 1. Postcard: grid -> stacked ──────────────────────────────────────────────
title_link = (
    '(0,L.jsx)(I,{to:' + q + '/post/${e.id}' + q
    + ',style:{textDecoration:' + q + 'none' + q + ',display:' + q + 'block' + q
    + ',marginTop:10,marginBottom:8,color:' + q + '#f1f5f9' + q
    + ',fontWeight:700,fontSize:16,lineHeight:1.35,textAlign:' + q + 'left' + q
    + '},children:e.title})'
)

# Old block is the title link + grid
old_grid_block = raw[raw.find(title_link + ',(0,L.jsxs)(' + q + 'div' + q + ',{style:{display:' + q + 'grid'):
                     raw.find('key:_i}))}'  , raw.find(title_link + ',(0,L.jsxs)')) + len('key:_i}))}')]

# Build old block string more reliably
old_grid_start = raw.find(title_link + ',(0,L.jsxs)(' + q + 'div' + q + ',{style:{display:' + q + 'grid')
old_grid_end   = raw.find('key:_i}))}'  , old_grid_start) + len('key:_i}))})' )  # +1 includes grid div jsx close )
old_grid_block = raw[old_grid_start:old_grid_end]
new_grid_block = title_link + ',' + stacked_postcard  # stacked_postcard already ends with )

patch(old_grid_block, new_grid_block, 'postcard: grid -> stacked')

# ── 2. Post detail: add multi-photo support ────────────────────────────────────
patch(
    'let{text:_rawE,attachment:t}=Mr(c.content);',
    'let{text:_rawE,attachment:t,attachments:_tAtts}=Mr(c.content);',
    'post detail: extract _tAtts from Mr'
)

patch(
    't&&(0,L.jsx)(' + q + 'div' + q + ',{style:{marginBottom:10},children:(0,L.jsx)(Fr,{attachment:t})})',
    ('(_tAtts||t)&&(0,L.jsx)(' + q + 'div' + q + ',{style:{marginBottom:10},'
     + 'children:_tAtts?' + stacked_detail + ':(0,L.jsx)(Fr,{attachment:t})})'),
    'post detail: render stacked for _tAtts, Fr for single'
)

# ── 3. Cap at 9 photos (both post form + comment have same string) ─────────────
_slice_old = '.filter(_f=>_f.type.startsWith(' + q + 'image' + q + ')).slice(0,10)'
_slice_new = '.filter(_f=>_f.type.startsWith(' + q + 'image' + q + ')).slice(0,9)'
content = content.replace(_slice_old, _slice_new)
print('OK: cap upload at 9 (all occurrences)')

# ── 4. Remove overall delete-all X for images type ────────────────────────────
# Post form: make overall X conditional on T.type !== 'images'
patch(
    '(0,L.jsx)(' + q + 'button' + q + ',{type:' + q + 'button' + q + ',onClick:()=>E(null),style:{position:' + q + 'absolute' + q + ',top:6,right:6,',
    'T.type!==' + q + 'images' + q + '&&(0,L.jsx)(' + q + 'button' + q + ',{type:' + q + 'button' + q + ',onClick:()=>E(null),style:{position:' + q + 'absolute' + q + ',top:6,right:6,',
    'post form: hide overall X when images type'
)

# Comment: make overall X conditional on _cA.type !== 'images'
patch(
    '(0,L.jsx)(' + q + 'button' + q + ',{type:' + q + 'button' + q + ',onClick:()=>_setCA(null),style:{position:' + q + 'absolute' + q + ',top:2,right:2,',
    '_cA.type!==' + q + 'images' + q + '&&(0,L.jsx)(' + q + 'button' + q + ',{type:' + q + 'button' + q + ',onClick:()=>_setCA(null),style:{position:' + q + 'absolute' + q + ',top:2,right:2,',
    'comment: hide overall X when images type'
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
