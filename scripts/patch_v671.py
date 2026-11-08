#!/usr/bin/env python3
"""Patch v670 -> v671: Comment stacked thumbnails for multi-photo attachments.
- Update comment rendering destructuring to extract attachments:_cAtts
- If _cAtts: show stacked thumbnail grid (up to 3 visible, tap opens lightbox)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v670.js'
dst = '_deploy/assets/index-DUcNPOLc-v671.js'

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

# Stacked thumbnail lightbox (same logic as postcard but uses _cAtts)
clb = (
    '_ev2.stopPropagation();'
    + 'let _ci=_i2;'
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
    + 'const _upd=()=>{_im.src=_cAtts[_ci].url;_ctr.textContent=(_ci+1)+' + q + ' / ' + q + '+_cAtts.length;_pv.style.opacity=_ci>0?' + q + '1' + q + ':' + q + '0.25' + q + ';_nx.style.opacity=_ci<_cAtts.length-1?' + q + '1' + q + ':' + q + '0.25' + q + '};'
    + '_pv.onclick=_e=>{_e.stopPropagation();if(_ci>0){_ci--;_upd();}};'
    + '_nx.onclick=_e=>{_e.stopPropagation();if(_ci<_cAtts.length-1){_ci++;_upd();}};'
    + 'const _cb=document.createElement(' + q + 'button' + q + ');'
    + '_cb.textContent=' + q + '✕' + q + ';'
    + '_cb.style.cssText=' + q + 'position:absolute;top:16px;right:16px;background:rgba(0,0,0,0.55);color:white;border:none;border-radius:50%;width:36px;height:36px;font-size:16px;cursor:pointer;' + q + ';'
    + '_cb.onclick=_e=>{_e.stopPropagation();_close();};'
    + '_ov.appendChild(_im);'
    + 'if(_cAtts.length>1){_ov.appendChild(_pv);_ov.appendChild(_nx);_ov.appendChild(_ctr);}'
    + '_ov.appendChild(_cb);'
    + '_upd();'
    + 'let _sy=0;'
    + '_ov.addEventListener(' + q + 'touchstart' + q + ',_e=>{_sy=_e.touches[0].clientY;},{passive:!0});'
    + '_ov.addEventListener(' + q + 'touchend' + q + ',_e=>{if(_e.changedTouches[0].clientY-_sy>80)_close();},{passive:!0});'
    + '_ov.onclick=_e=>{if(_e.target===_ov)_close();};'
    + 'document.body.style.overflow=' + q + 'hidden' + q + ';'
    + 'document.body.appendChild(_ov);'
)

# Stacked thumbnails JSX
stacked = (
    '(0,L.jsx)(' + q + 'div' + q + ',{'
    + 'style:{position:' + q + 'relative' + q + ',height:96,marginBottom:_ct?8:0},'
    + 'onClick:_ev=>_ev.stopPropagation(),'
    + 'children:_cAtts.slice(0,3).map((_att2,_i2)=>(0,L.jsx)(' + q + 'img' + q + ',{'
    + 'src:_att2.url,'
    + 'style:{position:' + q + 'absolute' + q
    + ',top:_i2*6,left:_i2*6,width:84,height:84,objectFit:' + q + 'cover' + q
    + ',borderRadius:8,border:' + q + '2px solid #1e2130' + q + ',cursor:' + q + 'zoom-in' + q + '},'
    + 'onClick:_ev2=>{' + clb + '},'
    + 'key:_i2}))'
    + '})'
)

patch(
    '({text:_ct,attachment:_ca})=>(0,L.jsxs)(L.Fragment,{children:[_ca&&(0,L.jsx)(`div`,{style:{marginBottom:_ct?8:0},onClick:_ev=>_ev.stopPropagation(),children:(0,L.jsx)(Fr,{attachment:_ca,maxH:240})}),',
    ('({text:_ct,attachment:_ca,attachments:_cAtts})=>(0,L.jsxs)(L.Fragment,{children:['
     + '_cAtts?' + stacked + ':_ca&&(0,L.jsx)(' + q + 'div' + q + ',{style:{marginBottom:_ct?8:0},onClick:_ev=>_ev.stopPropagation(),children:(0,L.jsx)(Fr,{attachment:_ca,maxH:240})}),'),
    'comment: add _cAtts destructuring + stacked thumbnails'
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
