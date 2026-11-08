#!/usr/bin/env python3
"""Patch v621 -> v622:
1. Taller postcard thumbnail minHeight 120->160
2. Tap thumbnail -> fullscreen lightbox (image or video), tap to close
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v621.js'
dst = '_deploy/assets/index-DUcNPOLc-v622.js'

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

# 1. Pr signature: add attachment prop
patch(
    'function Pr({postId:e,title:t,text:n,image:r,isHuddle:_ih,huddle_members:_prHm=null,isVideo:_ivid=!1})',
    'function Pr({postId:e,title:t,text:n,image:r,isHuddle:_ih,huddle_members:_prHm=null,isVideo:_ivid=!1,attachment:_att=null})',
    'Pr add attachment prop'
)

# 2. Add lightbox state
patch(
    ',[a,o]=(0,_.useState)(!1),s=n&&n.length>160',
    ',[a,o]=(0,_.useState)(!1),[_lb,_setLb]=(0,_.useState)(!1),s=n&&n.length>160',
    'Pr add lightbox state'
)

# 3. Thumbnail: taller + onClick
old3 = ('minHeight:120},children:[(0,L.jsx)(' + q + 'img' + q + ',{src:r,alt:' + q + q
        + ',style:{position:' + q + 'absolute' + q + ',inset:0,width:' + q + '100%' + q
        + ',height:' + q + '100%' + q + ',objectFit:' + q + 'cover' + q + '}')
new3 = ('minHeight:160,cursor:_att?' + q + 'pointer' + q + ':undefined},'
        + 'onClick:_att?e=>{e.stopPropagation();_setLb(!0);}:undefined,'
        + 'children:[(0,L.jsx)(' + q + 'img' + q + ',{src:r,alt:' + q + q
        + ',style:{position:' + q + 'absolute' + q + ',inset:0,width:' + q + '100%' + q
        + ',height:' + q + '100%' + q + ',objectFit:' + q + 'cover' + q + '}')
patch(old3, new3, 'thumbnail taller + lightbox onClick')

# 4. Fragment end: insert lightbox before Fragment close
# Extract exact end string from source (position verified unique)
src_content = open(src, encoding='utf-8').read()
old4 = src_content[292280:292300]  # 'Post`})]})]})]})]`})}'
assert src_content.count(old4) == 1, 'old4 not unique!'

# Fragment close is last 4 chars of old4: ] } ) }
# We insert lightbox before Fragment close (before last ]}) keeping final }
# old4 = ...overlay_close ]}) }   <- last 4 chars = Fragment ]}) + Pr }
# new4 = ...overlay_close ,lightbox ]}) }
split_at = len(old4) - 4  # position of Fragment's ] in old4
before = old4[:split_at]   # everything up to Fragment close
frag_close_and_pr = old4[split_at:]  # last 4 chars: ]`})}

lightbox = (
    '_lb&&(0,L.jsxs)(' + q + 'div' + q + ',{style:{position:' + q + 'fixed' + q
    + ',inset:0,zIndex:9999,background:' + q + 'rgba(0,0,0,0.92)' + q
    + ',display:' + q + 'flex' + q + ',alignItems:' + q + 'center' + q
    + ',justifyContent:' + q + 'center' + q + '},onClick:()=>_setLb(!1),children:['
    + '_att?.type===' + q + 'video' + q + '?'
    + '(0,L.jsx)(' + q + 'video' + q + ',{src:_att.url,controls:!0,autoPlay:!0,'
    + 'playsInline:!0,style:{maxWidth:' + q + '100%' + q + ',maxHeight:' + q + '90vh' + q
    + ',borderRadius:10},onClick:e=>e.stopPropagation()})'
    + ':(0,L.jsx)(' + q + 'img' + q + ',{src:_att?.url||r,alt:' + q + q
    + ',style:{maxWidth:' + q + '100%' + q + ',maxHeight:' + q + '90vh' + q
    + ',borderRadius:10,objectFit:' + q + 'contain' + q + '},onClick:e=>e.stopPropagation()})'
    + ']})'
)
new4 = before + ',' + lightbox + frag_close_and_pr
patch(old4, new4, 'add lightbox overlay to Fragment')

# 5. Ir call site: pass attachment:p
patch(
    'isHuddle:!!(e.is_huddle||e.community_id===' + q + 'feedback' + q + '),huddle_members:_fHm,isVideo:p?.type===' + q + 'video' + q + '})',
    'isHuddle:!!(e.is_huddle||e.community_id===' + q + 'feedback' + q + '),huddle_members:_fHm,isVideo:p?.type===' + q + 'video' + q + ',attachment:p||null})',
    'Ir passes attachment to Pr'
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
