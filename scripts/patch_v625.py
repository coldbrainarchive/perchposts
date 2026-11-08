#!/usr/bin/env python3
"""Patch v624 -> v625:
1. Photo on feed postcard (postId set): tap navigates to post instead of lightbox
2. Video controls: after clicking play, blur() the video after 1.5s so
   browser hides the native control bar sooner
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v624.js'
dst = '_deploy/assets/index-DUcNPOLc-v625.js'

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

# 1. Photo: if postId (o) is set, navigate to post; else use lightbox
old1 = ('if(t===' + q + 'image' + q + ')return(0,L.jsxs)(' + q + 'div' + q
        + ',{style:{position:' + q + 'relative' + q + ',marginTop:10},children:')
new1 = ('if(t===' + q + 'image' + q + '){if(o)return(0,L.jsx)(I,{to:' + q + '/post/${o}' + q
        + ',style:{display:' + q + 'block' + q + ',marginTop:10,textDecoration:' + q + 'none' + q
        + '},children:(0,L.jsx)(' + q + 'img' + q + ',{src:n,alt:' + q + q
        + ',style:{width:' + q + '100%' + q + ',borderRadius:10,display:' + q + 'block' + q
        + ',maxHeight:_mh,objectFit:' + q + 'cover' + q + '},'
        + 'onError:e=>{e.target.style.display=' + q + 'none' + q + '}})});'
        + 'return(0,L.jsxs)(' + q + 'div' + q
        + ',{style:{position:' + q + 'relative' + q + ',marginTop:10},children:')
patch(old1, new1, 'photo on postcard navigates to post')

# 1b. Close the image if-block before the video section
patch(
    '}})]});if(t===' + q + 'video' + q + ')',
    '}})]});}if(t===' + q + 'video' + q + ')',
    'close image if-block'
)

# 2. Video: blur after 1.5s to hide controls sooner
patch(
    '_pe.currentTarget.previousElementSibling.play()}}',
    'let _vid=_pe.currentTarget.previousElementSibling;_vid.play();setTimeout(()=>{_vid.blur();},1500)}}',
    'blur video after 1.5s to hide controls'
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
