#!/usr/bin/env python3
"""Patch v673 -> v674:
1. Postcard: replace swipe carousel with 3-col grid (like comments)
2. New post form preview: show ALL thumbnails with individual X buttons
3. Comment upload preview: show ALL thumbnails with individual X buttons
4. Comment grid: already shows 9, keep as is but ensure lightbox works
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v673.js'
dst = '_deploy/assets/index-DUcNPOLc-v674.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
raw = content  # keep original for block extraction
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

# ── 1. Postcard carousel → grid ──────────────────────────────────────────────
# Extract lightbox onClick from the carousel image (reuse it in grid)
lb_start = raw.find('onClick:_ev=>{_ev.stopPropagation();let _ci=_i;const _ov=document.createElement(`div`);_ov.style.cssText=`position:fixed;inset:0;background:rgba(0,0,0,0.93)')
lb_end   = raw.find('document.body.appendChild(_ov);},key:_i', lb_start) + len('document.body.appendChild(_ov);')
lb_code  = raw[lb_start:lb_end]  # full onClick:_ev=>{...} up to closing ;

# Old carousel block start (up to the map's children: keyword)
old_carousel_prefix = (
    'position:' + q + 'relative' + q + ',marginTop:6},children:['
    + '(0,L.jsx)(' + q + 'div' + q + ',{style:{display:' + q + 'flex' + q
    + ',overflowX:' + q + 'auto' + q + ',scrollSnapType:' + q + 'x mandatory' + q
    + ',borderRadius:10,scrollbarWidth:' + q + 'none' + q + ',touchAction:' + q + 'pan-x' + q
    + '},onScroll:e=>{const _c=e.currentTarget;const _idx=Math.round(_c.scrollLeft/_c.clientWidth);'
    + 'const _ds=_c.nextElementSibling?.children;if(_ds)for(let _di=0;_di<_ds.length;_di++){'
    + '_ds[_di].style.background=_di===_idx?' + q + '#a855f7' + q + ':' + q + 'rgba(255,255,255,0.28)' + q + ';}},children:'
)
new_carousel_prefix = (
    'display:' + q + 'grid' + q
    + ',gridTemplateColumns:' + q + 'repeat(${Math.min(_pAtts.length,3)},1fr)' + q
    + ',gap:3,borderRadius:10,overflow:' + q + 'hidden' + q + ',marginTop:6},children:'
)
patch(old_carousel_prefix, new_carousel_prefix, 'postcard: carousel prefix → grid')

# Old carousel image style
old_img_style = (
    'style:{minWidth:' + q + '100%' + q + ',flexShrink:0,scrollSnapAlign:' + q + 'start' + q
    + ',height:320,objectFit:' + q + 'cover' + q + ',borderRadius:10,cursor:' + q + 'zoom-in' + q
    + ',display:' + q + 'block' + q + '},'
)
new_img_style = (
    'style:{width:' + q + '100%' + q + ',aspectRatio:' + q + '1' + q
    + ',objectFit:' + q + 'cover' + q + ',cursor:' + q + 'zoom-in' + q
    + ',display:' + q + 'block' + q + '},'
)
patch(old_img_style, new_img_style, 'postcard: carousel img style → grid img style')

# Old carousel suffix (close scroll div + dots + close outer jsxs)
old_carousel_suffix = (
    '}),_pAtts.length>1&&(0,L.jsx)(' + q + 'div' + q
    + ',{style:{display:' + q + 'flex' + q + ',justifyContent:' + q + 'center' + q
    + ',gap:6,marginTop:8},children:_pAtts.map((_,_i)=>(0,L.jsx)(' + q + 'div' + q
    + ',{key:_i,style:{width:7,height:7,borderRadius:' + q + '50%' + q
    + ',background:_i===0?' + q + '#a855f7' + q + ':' + q + 'rgba(255,255,255,0.28)' + q
    + ',transition:' + q + 'background 0.2s' + q + '}}))})]})'
)
new_carousel_suffix = '})'
patch(old_carousel_suffix, new_carousel_suffix, 'postcard: remove dots + fix closing brackets')

# ── 2. New post form: all thumbnails with individual X buttons ────────────────
patch(
    ('T.type===' + q + 'images' + q
     + '?(0,L.jsx)(' + q + 'div' + q + ',{style:{display:' + q + 'flex' + q + ',flexWrap:' + q + 'wrap' + q + ',gap:4},'
     + 'children:T.urls.map((_u,_i)=>(0,L.jsx)(' + q + 'img' + q
     + ',{key:_i,src:_u,style:{width:62,height:62,objectFit:' + q + 'cover' + q + ',borderRadius:8}}))})'),
    ('T.type===' + q + 'images' + q
     + '?(0,L.jsx)(' + q + 'div' + q + ',{style:{display:' + q + 'flex' + q + ',flexWrap:' + q + 'wrap' + q + ',gap:4},'
     + 'children:T.urls.map((_u,_i)=>(0,L.jsxs)(' + q + 'div' + q + ',{key:_i,style:{position:' + q + 'relative' + q + '},'
     + 'children:[(0,L.jsx)(' + q + 'img' + q + ',{src:_u,style:{width:62,height:62,objectFit:' + q + 'cover' + q + ',borderRadius:8,display:' + q + 'block' + q + '}}),'
     + '(0,L.jsx)(' + q + 'button' + q + ',{type:' + q + 'button' + q
     + ',onClick:()=>{const _nu=T.urls.filter((_,_j)=>_j!==_i);_nu.length?E({type:' + q + 'images' + q + ',urls:_nu}):E(null);},'
     + 'style:{position:' + q + 'absolute' + q + ',top:2,right:2,background:' + q + 'rgba(0,0,0,0.65)' + q
     + ',border:' + q + 'none' + q + ',color:' + q + '#fff' + q + ',borderRadius:999,width:18,height:18,cursor:' + q + 'pointer' + q
     + ',fontSize:10,display:' + q + 'flex' + q + ',alignItems:' + q + 'center' + q + ',justifyContent:' + q + 'center' + q + '},'
     + 'children:' + q + '✕' + q + '})]}))})'),
    'post form: all thumbs + per-image X'
)

# ── 3. Comment upload preview: all thumbnails with individual X buttons ───────
patch(
    ('_cA.type===' + q + 'images' + q
     + '?(0,L.jsx)(' + q + 'div' + q + ',{style:{display:' + q + 'flex' + q + ',gap:4},'
     + 'children:_cA.urls.slice(0,3).map((_u,_i)=>(0,L.jsx)(' + q + 'img' + q
     + ',{key:_i,src:_u,style:{width:60,height:60,objectFit:' + q + 'cover' + q + ',borderRadius:7}}))})'),
    ('_cA.type===' + q + 'images' + q
     + '?(0,L.jsx)(' + q + 'div' + q + ',{style:{display:' + q + 'flex' + q + ',flexWrap:' + q + 'wrap' + q + ',gap:4},'
     + 'children:_cA.urls.map((_u,_i)=>(0,L.jsxs)(' + q + 'div' + q + ',{key:_i,style:{position:' + q + 'relative' + q + '},'
     + 'children:[(0,L.jsx)(' + q + 'img' + q + ',{src:_u,style:{width:60,height:60,objectFit:' + q + 'cover' + q + ',borderRadius:7,display:' + q + 'block' + q + '}}),'
     + '(0,L.jsx)(' + q + 'button' + q + ',{type:' + q + 'button' + q
     + ',onClick:_e=>{_e.stopPropagation();const _nu=_cA.urls.filter((_,_j)=>_j!==_i);_nu.length?_setCA({type:' + q + 'images' + q + ',urls:_nu}):_setCA(null);},'
     + 'style:{position:' + q + 'absolute' + q + ',top:2,right:2,background:' + q + 'rgba(0,0,0,0.65)' + q
     + ',border:' + q + 'none' + q + ',color:' + q + '#fff' + q + ',borderRadius:999,width:18,height:18,cursor:' + q + 'pointer' + q
     + ',fontSize:10,display:' + q + 'flex' + q + ',alignItems:' + q + 'center' + q + ',justifyContent:' + q + 'center' + q + '},'
     + 'children:' + q + '✕' + q + '})]}))})'),
    'comment upload preview: all thumbs + per-image X'
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
