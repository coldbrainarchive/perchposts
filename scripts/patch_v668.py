#!/usr/bin/env python3
"""Patch v666 -> v668: Data layer for multi-photo attachments.
1. Add _amk marker constant for [ATTACHMENTS:[...]] format
2. Extend Mr parser to handle ATTACHMENTS array (backwards compatible)
3. Update post content encoding to use _amk when attachment type is 'images'
4. Update comment content encoding same way
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v666.js'
dst = '_deploy/assets/index-DUcNPOLc-v668.js'

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

# 1. Add _amk marker after jr
patch(
    'var jr=' + q + '\n\n[ATTACH:' + q + ';',
    'var jr=' + q + '\n\n[ATTACH:' + q + ';var _amk=' + q + '\n\n[ATTACHMENTS:' + q + ';',
    'add _amk marker constant'
)

# 2. Extend Mr parser to handle [ATTACHMENTS:[...]] format
patch(
    ('function Mr(e){if(!e)return{text:e||' + q + q + ',attachment:null};'
     + 'let t=e.indexOf(jr);if(t===-1)return{text:e,attachment:null};'
     + 'let n=e.slice(0,t);try{let r=e.slice(t+10,e.lastIndexOf(' + q + ']' + q + '));'
     + 'return{text:n,attachment:JSON.parse(r)}}catch{return{text:e,attachment:null}}}'),
    ('function Mr(e){if(!e)return{text:e||' + q + q + ',attachment:null,attachments:null};'
     + 'let _ai=e.indexOf(_amk);if(_ai!==-1){let _at=e.slice(0,_ai);'
     + 'try{let _ar=e.slice(_ai+15,e.lastIndexOf(' + q + ']' + q + '));'
     + 'return{text:_at,attachment:null,attachments:JSON.parse(_ar)}}'
     + 'catch{return{text:e,attachment:null,attachments:null}}}'
     + 'let t=e.indexOf(jr);if(t===-1)return{text:e,attachment:null,attachments:null};'
     + 'let n=e.slice(0,t);try{let r=e.slice(t+10,e.lastIndexOf(' + q + ']' + q + '));'
     + 'return{text:n,attachment:JSON.parse(r),attachments:null}}'
     + 'catch{return{text:e,attachment:null,attachments:null}}}'),
    'extend Mr parser for ATTACHMENTS format'
)

# 3. Post submit: encode images array with _amk marker
patch(
    'T?s+jr+JSON.stringify(T)+' + q + ']' + q + ':s',
    ('T?T.type===' + q + 'images' + q
     + '?s+_amk+JSON.stringify(T.urls.map(_u=>({type:' + q + 'image' + q + ',url:_u})))+' + q + ']' + q
     + ':s+jr+JSON.stringify(T)+' + q + ']' + q + ':s'),
    'post submit: encode multi-photo with _amk'
)

# 4. Comment submit: encode images array with _amk marker
patch(
    '_att?t+jr+JSON.stringify(_att)+' + q + ']' + q + ':t',
    ('_att?_att.type===' + q + 'images' + q
     + '?t+_amk+JSON.stringify(_att.urls.map(_u=>({type:' + q + 'image' + q + ',url:_u})))+' + q + ']' + q
     + ':t+jr+JSON.stringify(_att)+' + q + ']' + q + ':t'),
    'comment submit: encode multi-photo with _amk'
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
