#!/usr/bin/env python3
"""Patch v668 -> v669: File input + multi-upload for new post form.
- Add multiple:true to file input
- onChange: single video → existing M() flow; multiple images → upload each,
  collect URLs, set E({type:'images', urls:[...]})
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v668.js'
dst = '_deploy/assets/index-DUcNPOLc-v669.js'

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

# Add multiple:true to post form file input only (ref:ie, not ref:_cMR)
patch(
    'ref:ie,type:' + q + 'file' + q + ',accept:' + q + 'image/*,video/*' + q + ',style:{display:' + q + 'none' + q + '}',
    'ref:ie,type:' + q + 'file' + q + ',accept:' + q + 'image/*,video/*' + q + ',multiple:!0,style:{display:' + q + 'none' + q + '}',
    'add multiple to post form file input'
)

# Replace onChange to handle single video OR multiple images
patch(
    ('onChange:e=>{if(e.target.files[0]){re(!0);M(e.target.files[0],'
     + 'e.target.files[0].type.startsWith(' + q + 'video' + q + ')?' + q + 'video' + q + ':' + q + 'image' + q + ');}}'),
    ('onChange:e=>{const _fs=[...e.target.files];e.target.value=' + q + q + ';'
     + 'if(!_fs.length)return;'
     + 'if(_fs.length===1&&_fs[0].type.startsWith(' + q + 'video' + q + ')){re(!0);M(_fs[0],' + q + 'video' + q + ');}'
     + 'else{const _ims=_fs.filter(_f=>_f.type.startsWith(' + q + 'image' + q + ')).slice(0,10);'
     + 'if(!_ims.length)return;re(!0);'
     + '(async()=>{try{const _us=[];'
     + 'for(const _f of _ims){'
     + 'const _fd=new FormData;_fd.append(' + q + 'file' + q + ',_f);'
     + 'const _r=await fetch(`${R}/upload`,{method:' + q + 'POST' + q + ',body:_fd});'
     + 'const _j=await _r.json();'
     + 'if(!_r.ok)throw Error(_j.error||' + q + 'Upload failed' + q + ');'
     + '_us.push(_j.url);}'
     + 'E({type:' + q + 'images' + q + ',urls:_us});D(null);}'
     + 'catch(_e){alert(' + q + 'Upload failed: ' + q + '+_e.message);}'
     + 'finally{re(!1);}})();}}'),
    'onChange: multi-image upload flow'
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
