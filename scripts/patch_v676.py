#!/usr/bin/env python3
"""Patch v675 -> v676:
1. Lightbox UI: clean header bar (counter left, X right, gradient bg)
   instead of overlapping absolute-positioned elements on photo
2. Comment display: grid -> stacked card (same style as postcard, height:240)
3. Postcard stacked: no height change (already good at 320)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v675.js'
dst = '_deploy/assets/index-DUcNPOLc-v676.js'

q = chr(0x60)
raw = open(src, encoding='utf-8').read()
content = raw
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

# ── 1. Lightbox header bar ────────────────────────────────────────────────────

# 1a. Counter: remove absolute positioning (it goes inside header flex)
content = content.replace(
    '_ctr.style.cssText=' + q + 'position:absolute;top:16px;right:60px;color:white;font-size:13px;background:rgba(0,0,0,0.5);padding:3px 10px;border-radius:20px;' + q,
    '_ctr.style.cssText=' + q + 'color:white;font-size:14px;font-weight:600;letter-spacing:0.02em;' + q
)
print('OK: lightbox counter style -> inline (all occurrences)')

# 1b. Close button: make it inline for header
content = content.replace(
    '_cb.style.cssText=' + q + 'position:absolute;top:16px;right:16px;background:rgba(0,0,0,0.55);color:white;border:none;border-radius:50%;width:36px;height:36px;font-size:16px;cursor:pointer;' + q,
    '_cb.style.cssText=' + q + 'background:none;color:white;border:none;font-size:24px;cursor:pointer;padding:4px 8px;line-height:1;' + q
)
print('OK: lightbox close style -> inline (all occurrences)')

# 1c. Restructure append sequence for each lightbox variant
hdr_setup = (
    'const _hdr=document.createElement(' + q + 'div' + q + ');'
    + '_hdr.style.cssText=' + q + 'position:absolute;top:0;left:0;right:0;height:56px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;background:linear-gradient(rgba(0,0,0,0.55),transparent);z-index:10;' + q + ';'
    + '_hdr.appendChild(_ctr);_hdr.appendChild(_cb);'
)

for atts in ['_pAtts', '_cAtts', '_tAtts']:
    old_ap = ('_ov.appendChild(_im);if(' + atts + '.length>1){'
              + '_ov.appendChild(_dots);_ov.appendChild(_ctr);_ov.appendChild(_lz);_ov.appendChild(_rz);}'
              + '_ov.appendChild(_cb);')
    new_ap = (hdr_setup
              + '_ov.appendChild(_im);_ov.appendChild(_hdr);'
              + 'if(' + atts + '.length>1){_ov.appendChild(_dots);_ov.appendChild(_lz);_ov.appendChild(_rz);}')
    patch(old_ap, new_ap, 'lightbox header append: ' + atts)

# ── 2. Comment display: grid -> stacked card ─────────────────────────────────
# Extract lightbox code from the comment grid item
i_grid   = content.find('display:' + q + 'grid' + q + ',gridTemplateColumns:' + q + 'repeat(${Math.min(_cAtts')
lb_start = content.find('onClick:_ev2=>{_ev2.stopPropagation();let _ci=_i2;', i_grid)
lb_end   = content.find('document.body.appendChild(_ov);},key:_i2', lb_start) + len('document.body.appendChild(_ov);')
comment_lb = content[lb_start:lb_end]  # full onClick:_ev2=>{...}

# Rebuild as lightbox with _ci=0 for the front image click
comment_lb_ci0 = comment_lb.replace('let _ci=_i2;', 'let _ci=0;')

# Build stacked comment block
def make_stacked_comment(lb_code):
    q = chr(0x60)
    return (
        '_cAtts?(0,L.jsxs)(' + q + 'div' + q + ',{style:{position:' + q + 'relative' + q + ',marginBottom:_ct?8:0},'
        + 'onClick:_ev=>_ev.stopPropagation(),children:['
        + '_cAtts.length>2&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
        + ',bottom:-6,left:6,right:6,height:' + q + '100%' + q + ',borderRadius:8,background:' + q + '#252836' + q + ',zIndex:0}}),'
        + '_cAtts.length>1&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
        + ',bottom:-3,left:3,right:3,height:' + q + '100%' + q + ',borderRadius:8,background:' + q + '#1e2130' + q + ',zIndex:0}}),'
        + '(0,L.jsx)(' + q + 'img' + q + ',{src:_cAtts[0].url,'
        + 'style:{width:' + q + '100%' + q + ',height:240,objectFit:' + q + 'cover' + q
        + ',borderRadius:8,display:' + q + 'block' + q + ',cursor:' + q + 'zoom-in' + q + ',position:' + q + 'relative' + q + ',zIndex:1},'
        + lb_code + '}}),'  # } closes onClick body, } closes img props, ) closes img jsx
        + '_cAtts.length>1&&(0,L.jsx)(' + q + 'div' + q + ',{style:{position:' + q + 'absolute' + q
        + ',bottom:8,right:8,background:' + q + 'rgba(0,0,0,0.6)' + q
        + ',color:' + q + 'white' + q + ',borderRadius:20,padding:' + q + '3px 10px' + q
        + ',fontSize:12,fontWeight:600,zIndex:2,pointerEvents:' + q + 'none' + q + '},children:' + q + '📷 ' + q + '+_cAtts.length})'
        + ']})'
    )

# Find the full comment grid block
grid_start = content.find('_cAtts?(0,L.jsx)(' + q + 'div' + q + ',{style:{display:' + q + 'grid')
grid_end   = content.find('key:_i2}))}'  , grid_start) + len('key:_i2}))})') # +1 for grid div jsx close )
old_grid   = content[grid_start:grid_end]
new_stacked = make_stacked_comment(comment_lb_ci0)

patch(old_grid, new_stacked, 'comment display: grid -> stacked card')

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
