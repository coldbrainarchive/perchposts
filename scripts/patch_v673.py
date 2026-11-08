#!/usr/bin/env python3
"""Patch v672 -> v673:
1. Carousel: add touchAction:pan-x for reliable iOS swiping
2. Lightbox (postcard + comment): remove arrow buttons, add swipe left/right
   to navigate, dots indicator at bottom, desktop click-zone navigation
3. Comment thumbnails: change stacked layout to grid (fills comment bubble)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v672.js'
dst = '_deploy/assets/index-DUcNPOLc-v673.js'

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

# 1. Carousel: add touchAction:pan-x
patch(
    'display:' + q + 'flex' + q + ',overflowX:' + q + 'auto' + q + ',scrollSnapType:' + q + 'x mandatory' + q + ',borderRadius:10,scrollbarWidth:' + q + 'none' + q + '}',
    'display:' + q + 'flex' + q + ',overflowX:' + q + 'auto' + q + ',scrollSnapType:' + q + 'x mandatory' + q + ',borderRadius:10,scrollbarWidth:' + q + 'none' + q + ',touchAction:' + q + 'pan-x' + q + '}',
    'carousel: add touchAction pan-x'
)

# Helper: build new lightbox internals (swipe navigation + dots)
def make_lb_new(atts_var):
    q = chr(0x60)
    return (
        'const _close=()=>{document.body.removeChild(_ov);document.body.style.overflow=' + q + q + '};'
        + 'const _dots=document.createElement(' + q + 'div' + q + ');'
        + '_dots.style.cssText=' + q + 'position:absolute;bottom:28px;left:50%;transform:translateX(-50%);display:flex;gap:8px;pointer-events:none;' + q + ';'
        + 'const _mkDots=()=>{_dots.innerHTML=' + q + q + ';' + atts_var + '.forEach((_,_di)=>{const _d=document.createElement(' + q + 'div' + q + ');_d.style.cssText=(_di===_ci?' + q + 'width:8px;height:8px;border-radius:50%;background:white;' + q + ':' + q + 'width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,0.35);' + q + ');_dots.appendChild(_d);});};'
        + 'const _upd=()=>{_im.src=' + atts_var + '[_ci].url;_ctr.textContent=(_ci+1)+' + q + ' / ' + q + '+' + atts_var + '.length;_mkDots();};'
        + 'const _cb=document.createElement(' + q + 'button' + q + ');'
        + '_cb.textContent=' + q + '✕' + q + ';'
        + '_cb.style.cssText=' + q + 'position:absolute;top:16px;right:16px;background:rgba(0,0,0,0.55);color:white;border:none;border-radius:50%;width:36px;height:36px;font-size:16px;cursor:pointer;' + q + ';'
        + '_cb.onclick=_e=>{_e.stopPropagation();_close();};'
        + 'const _lz=document.createElement(' + q + 'div' + q + ');'
        + '_lz.style.cssText=' + q + 'position:absolute;left:0;top:0;width:40%;height:100%;cursor:w-resize;' + q + ';'
        + '_lz.onclick=_e=>{_e.stopPropagation();if(_ci>0){_ci--;_upd();}};'
        + 'const _rz=document.createElement(' + q + 'div' + q + ');'
        + '_rz.style.cssText=' + q + 'position:absolute;right:0;top:0;width:40%;height:100%;cursor:e-resize;' + q + ';'
        + '_rz.onclick=_e=>{_e.stopPropagation();if(_ci<' + atts_var + '.length-1){_ci++;_upd();}};'
        + '_ov.appendChild(_im);'
        + 'if(' + atts_var + '.length>1){_ov.appendChild(_dots);_ov.appendChild(_ctr);_ov.appendChild(_lz);_ov.appendChild(_rz);}'
        + '_ov.appendChild(_cb);'
        + '_upd();'
        + 'let _sx=0,_sy=0;'
        + '_ov.addEventListener(' + q + 'touchstart' + q + ',_e=>{_sx=_e.touches[0].clientX;_sy=_e.touches[0].clientY;},{passive:!0});'
        + '_ov.addEventListener(' + q + 'touchend' + q + ',_e=>{const _dx=_e.changedTouches[0].clientX-_sx;const _dy=_e.changedTouches[0].clientY-_sy;if(Math.abs(_dy)>80&&Math.abs(_dy)>Math.abs(_dx)){_close();return;}if(Math.abs(_dx)>50){if(_dx<0&&_ci<' + atts_var + '.length-1){_ci++;_upd();}else if(_dx>0&&_ci>0){_ci--;_upd();}}},{passive:!0});'
        + '_ov.onclick=_e=>{if(_e.target===_ov)_close();};'
    )

# 2. Postcard lightbox - replace button nav with swipe nav
raw = open(src, encoding='utf-8').read()
i_p = raw.find('_im.src=_pAtts[_ci].url')
s_p = raw.rfind('const _pv=document.createElement', 0, i_p)
e_p = raw.find('document.body.style.overflow=`hidden`', i_p)
old_p = raw[s_p:e_p]
new_p = make_lb_new('_pAtts')
patch(old_p, new_p, 'postcard lightbox: swipe nav + dots')

# 3. Comment lightbox - replace button nav with swipe nav
i_c = raw.find('_im.src=_cAtts[_ci].url')
s_c = raw.rfind('const _pv=document.createElement', 0, i_c)
e_c = raw.find('document.body.style.overflow=`hidden`', i_c)
old_c = raw[s_c:e_c]
new_c = make_lb_new('_cAtts')
patch(old_c, new_c, 'comment lightbox: swipe nav + dots')

# 4. Comment thumbnails: replace stacked layout with responsive grid
patch(
    ('_cAtts?(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'relative' + q + ',height:96,marginBottom:_ct?8:0},'
     + 'onClick:_ev=>_ev.stopPropagation(),'
     + 'children:_cAtts.slice(0,3).map((_att2,_i2)=>(0,L.jsx)(' + q + 'img' + q + ',{'
     + 'src:_att2.url,style:{position:' + q + 'absolute' + q + ',top:_i2*6,left:_i2*6,width:84,height:84,objectFit:' + q + 'cover' + q + ',borderRadius:8,border:' + q + '2px solid #1e2130' + q + ',cursor:' + q + 'zoom-in' + q + '},'),
    ('_cAtts?(0,L.jsx)(' + q + 'div' + q + ',{style:{display:' + q + 'grid' + q
     + ',gridTemplateColumns:' + q + 'repeat('+chr(36)+'{Math.min(_cAtts.length,3)},1fr)' + q
     + ',gap:3,borderRadius:10,overflow:' + q + 'hidden' + q + ',marginBottom:_ct?8:0},'
     + 'onClick:_ev=>_ev.stopPropagation(),'
     + 'children:_cAtts.slice(0,9).map((_att2,_i2)=>(0,L.jsx)(' + q + 'img' + q + ',{'
     + 'src:_att2.url,style:{width:' + q + '100%' + q + ',aspectRatio:' + q + '1' + q + ',objectFit:' + q + 'cover' + q + ',cursor:' + q + 'zoom-in' + q + ',display:' + q + 'block' + q + '},'),
    'comment thumbnails: stacked -> responsive grid'
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
