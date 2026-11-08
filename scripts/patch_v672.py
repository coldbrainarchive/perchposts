#!/usr/bin/env python3
"""Patch v671 -> v672:
1. Post form preview: show thumbnail grid when T.type==='images'
2. Comment file input: add multiple:true + multi-image upload handler
3. Comment preview: show thumbnail row when _cA.type==='images'
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v671.js'
dst = '_deploy/assets/index-DUcNPOLc-v672.js'

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

# 1. Post form preview: handle T.type==='images' with thumbnail grid
patch(
    'T&&(0,L.jsxs)(' + q + 'div' + q + ',{style:{marginTop:10,position:' + q + 'relative' + q + '},children:[(0,L.jsx)(Fr,{attachment:T}),',
    ('T&&(0,L.jsxs)(' + q + 'div' + q + ',{style:{marginTop:10,position:' + q + 'relative' + q + '},children:['
     + 'T.type===' + q + 'images' + q
     + '?(0,L.jsx)(' + q + 'div' + q + ',{style:{display:' + q + 'flex' + q + ',flexWrap:' + q + 'wrap' + q + ',gap:4},'
     + 'children:T.urls.map((_u,_i)=>(0,L.jsx)(' + q + 'img' + q + ',{key:_i,src:_u,style:{width:62,height:62,objectFit:' + q + 'cover' + q + ',borderRadius:8}}))})'
     + ':(0,L.jsx)(Fr,{attachment:T}),'),
    'post form preview: thumbnail grid for images type'
)

# 2. Comment file input: add multiple
patch(
    'ref:_cMR,type:' + q + 'file' + q + ',accept:' + q + 'image/*,video/*' + q + ',style:{display:' + q + 'none' + q + '},onChange:_fe=>',
    'ref:_cMR,type:' + q + 'file' + q + ',accept:' + q + 'image/*,video/*' + q + ',multiple:!0,style:{display:' + q + 'none' + q + '},onChange:_fe=>',
    'comment file input: add multiple'
)

# 3. Comment onChange: prepend multi-image handler before existing single-file logic
patch(
    'onChange:_fe=>{let _ff=_fe.target.files[0];if(_ff){',
    ('onChange:_fe=>{'
     + 'if([..._fe.target.files].length>1){'
     + 'const _cims=[..._fe.target.files].filter(_f=>_f.type.startsWith(' + q + 'image' + q + ')).slice(0,10);'
     + '_fe.target.value=' + q + q + ';'
     + 'if(!_cims.length)return;'
     + '_setCUL(!0);'
     + '(async()=>{try{const _us=[];'
     + 'for(const _cf of _cims){'
     + 'const _fd=new FormData;_fd.append(' + q + 'file' + q + ',_cf);'
     + 'const _r=await fetch(' + q + '${R}/upload' + q + ',{method:' + q + 'POST' + q + ',body:_fd});'
     + 'const _j=await _r.json();'
     + 'if(!_r.ok)throw Error(_j.error||' + q + 'Upload failed' + q + ');'
     + '_us.push(_j.url);}'
     + '_setCA({type:' + q + 'images' + q + ',urls:_us});}'
     + 'catch(_ce){alert(' + q + 'Upload failed: ' + q + '+_ce.message);}'
     + 'finally{_setCUL(!1);}})();return;}'
     + 'let _ff=_fe.target.files[0];if(_ff){'),
    'comment onChange: multi-image upload handler'
)

# 4. Comment preview: handle _cA.type==='images' with thumbnail row
patch(
    '_cA.type===' + q + 'image' + q + '?(0,L.jsx)(' + q + 'img' + q + ',{src:_cA.url,alt:' + q + q + ',style:{maxHeight:72,maxWidth:128,borderRadius:8,objectFit:' + q + 'cover' + q + '}}):(0,L.jsx)(' + q + 'video' + q + ',',
    ('_cA.type===' + q + 'images' + q
     + '?(0,L.jsx)(' + q + 'div' + q + ',{style:{display:' + q + 'flex' + q + ',gap:4},'
     + 'children:_cA.urls.slice(0,3).map((_u,_i)=>(0,L.jsx)(' + q + 'img' + q + ',{key:_i,src:_u,style:{width:60,height:60,objectFit:' + q + 'cover' + q + ',borderRadius:7}}))})'
     + ':_cA.type===' + q + 'image' + q + '?(0,L.jsx)(' + q + 'img' + q + ',{src:_cA.url,alt:' + q + q + ',style:{maxHeight:72,maxWidth:128,borderRadius:8,objectFit:' + q + 'cover' + q + '}}):(0,L.jsx)(' + q + 'video' + q + ','),
    'comment preview: thumbnail row for images type'
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
