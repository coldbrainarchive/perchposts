#!/usr/bin/env python3
"""Patch v669 -> v670: Postcard carousel + lightbox for multi-photo posts.
- Update Ir destructuring to extract attachments:_pAtts from Mr
- If _pAtts: render horizontal scroll carousel with dots indicator
- Tap photo: full-screen lightbox with prev/next nav + counter + swipe to close
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v669.js'
dst = '_deploy/assets/index-DUcNPOLc-v670.js'

content = open(src, encoding='utf-8').read()
errors = []
q = chr(0x60)

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

# 1. Update Ir destructuring to include attachments
patch(
    'text:_rawF,attachment:p}=Mr(e.content);',
    'text:_rawF,attachment:p,attachments:_pAtts}=Mr(e.content);',
    'add _pAtts to Ir Mr destructuring'
)

# 2. Lightbox function inline - built as a string for reuse in the map
lb = (
    '_ev.stopPropagation();'
    + 'let _ci=_i;'
    + 'const _ov=document.createElement(' + q + 'div' + q + ');'
    + '_ov.style.cssText=' + q + 'position:fixed;inset:0;background:rgba(0,0,0,0.93);z-index:9999;display:flex;align-items:center;justify-content:center;' + q + ';'
    + 'const _im=document.createElement(' + q + 'img' + q + ');'
    + '_im.style.cssText=' + q + 'max-width:92vw;max-height:88vh;border-radius:10px;object-fit:contain;' + q + ';'
    + 'const _ctr=document.createElement(' + q + 'div' + q + ');'
    + '_ctr.style.cssText=' + q + 'position:absolute;top:16px;right:60px;color:white;font-size:13px;background:rgba(0,0,0,0.5);padding:3px 10px;border-radius:20px;' + q + ';'
    + 'const _pv=document.createElement(' + q + 'button' + q + ');'
    + '_pv.textContent=' + q + '❮' + q + ';'
    + '_pv.style.cssText=' + q + 'position:absolute;left:12px;top:50%;transform:translateY(-50%);background:rgba(0,0,0,0.55);color:white;border:none;border-radius:50%;width:44px;height:44px;font-size:20px;cursor:pointer;display:flex;align-items:center;justify-content:center;' + q + ';'
    + 'const _nx=document.createElement(' + q + 'button' + q + ');'
    + '_nx.textContent=' + q + '❯' + q + ';'
    + '_nx.style.cssText=' + q + 'position:absolute;right:12px;top:50%;transform:translateY(-50%);background:rgba(0,0,0,0.55);color:white;border:none;border-radius:50%;width:44px;height:44px;font-size:20px;cursor:pointer;display:flex;align-items:center;justify-content:center;' + q + ';'
    + 'const _close=()=>{document.body.removeChild(_ov);document.body.style.overflow=' + q + q + '};'
    + 'const _upd=()=>{_im.src=_pAtts[_ci].url;_ctr.textContent=(_ci+1)+' + q + ' / ' + q + '+_pAtts.length;_pv.style.opacity=_ci>0?' + q + '1' + q + ':' + q + '0.25' + q + ';_nx.style.opacity=_ci<_pAtts.length-1?' + q + '1' + q + ':' + q + '0.25' + q + '};'
    + '_pv.onclick=_e=>{_e.stopPropagation();if(_ci>0){_ci--;_upd();}};'
    + '_nx.onclick=_e=>{_e.stopPropagation();if(_ci<_pAtts.length-1){_ci++;_upd();}};'
    + 'const _cb=document.createElement(' + q + 'button' + q + ');'
    + '_cb.textContent=' + q + '✕' + q + ';'
    + '_cb.style.cssText=' + q + 'position:absolute;top:16px;right:16px;background:rgba(0,0,0,0.55);color:white;border:none;border-radius:50%;width:36px;height:36px;font-size:16px;cursor:pointer;' + q + ';'
    + '_cb.onclick=_e=>{_e.stopPropagation();_close();};'
    + '_ov.appendChild(_im);'
    + 'if(_pAtts.length>1){_ov.appendChild(_pv);_ov.appendChild(_nx);_ov.appendChild(_ctr);}'
    + '_ov.appendChild(_cb);'
    + '_upd();'
    + 'let _sy=0;'
    + '_ov.addEventListener(' + q + 'touchstart' + q + ',_e=>{_sy=_e.touches[0].clientY;},{passive:!0});'
    + '_ov.addEventListener(' + q + 'touchend' + q + ',_e=>{if(_e.changedTouches[0].clientY-_sy>80)_close();},{passive:!0});'
    + '_ov.onclick=_e=>{if(_e.target===_ov)_close();};'
    + 'document.body.style.overflow=' + q + 'hidden' + q + ';'
    + 'document.body.appendChild(_ov);'
)

# Carousel JSX
carousel = (
    '(0,L.jsxs)(' + q + 'div' + q + ',{style:{position:' + q + 'relative' + q + ',marginTop:6},children:['
    + '(0,L.jsx)(' + q + 'div' + q + ',{'
    + 'style:{display:' + q + 'flex' + q + ',overflowX:' + q + 'auto' + q + ',scrollSnapType:' + q + 'x mandatory' + q + ',borderRadius:10,scrollbarWidth:' + q + 'none' + q + '},'
    + 'onScroll:e=>{const _c=e.currentTarget;const _idx=Math.round(_c.scrollLeft/_c.clientWidth);const _ds=_c.nextElementSibling?.children;if(_ds)for(let _di=0;_di<_ds.length;_di++){_ds[_di].style.background=_di===_idx?' + q + '#a855f7' + q + ':' + q + 'rgba(255,255,255,0.28)' + q + ';}},'
    + 'children:_pAtts.map((_att,_i)=>(0,L.jsx)(' + q + 'img' + q + ',{'
    + 'src:_att.url,'
    + 'style:{minWidth:' + q + '100%' + q + ',flexShrink:0,scrollSnapAlign:' + q + 'start' + q + ',height:320,objectFit:' + q + 'cover' + q + ',borderRadius:10,cursor:' + q + 'zoom-in' + q + ',display:' + q + 'block' + q + '},'
    + 'onClick:_ev=>{' + lb + '},'
    + 'key:_i}))'
    + '}),'
    + '_pAtts.length>1&&(0,L.jsx)(' + q + 'div' + q + ',{style:{display:' + q + 'flex' + q + ',justifyContent:' + q + 'center' + q + ',gap:6,marginTop:8},children:_pAtts.map((_,_i)=>(0,L.jsx)(' + q + 'div' + q + ',{key:_i,style:{width:7,height:7,borderRadius:' + q + '50%' + q + ',background:_i===0?' + q + '#a855f7' + q + ':' + q + 'rgba(255,255,255,0.28)' + q + ',transition:' + q + 'background 0.2s' + q + '}}))}'
    + ')]})'
)

# Title link (same as existing)
title_link = (
    'e.title&&(0,L.jsx)(I,{to:' + q + '/post/${e.id}' + q
    + ',style:{textDecoration:' + q + 'none' + q + ',display:' + q + 'block' + q
    + ',marginTop:10,marginBottom:8,color:' + q + '#f1f5f9' + q
    + ',fontWeight:700,fontSize:16,lineHeight:1.35,textAlign:' + q + 'left' + q
    + '},children:e.title})'
)

# Full new rendering: _pAtts carousel OR existing p ternary
new_render = (
    '_pAtts?(0,L.jsxs)(L.Fragment,{children:[' + title_link + ',' + carousel + ']})'
    + ':p?(0,L.jsxs)(L.Fragment,{children:[' + title_link
    + ',(0,L.jsx)(Fr,{attachment:p,postId:e.id})]}):(0,L.jsx)(Pr,{postId:'
)

old_render = (
    'p?(0,L.jsxs)(L.Fragment,{children:[' + title_link
    + ',(0,L.jsx)(Fr,{attachment:p,postId:e.id})]}):(0,L.jsx)(Pr,{postId:'
)

patch(old_render, new_render, 'postcard: carousel for _pAtts, fallback to Fr')

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
