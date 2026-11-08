#!/usr/bin/env python3
"""Patch v362 -> v363: send auth headers with get-post fetch so backend identifies user from JWT."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v362.js'
dst = '_deploy/assets/index-DUcNPOLc-v363.js'

content = open(src, encoding='utf-8').read()
errors = []

OLD = (
    'const _bid2=Gn(),_un2=localStorage.getItem(`_myUsername`)||null;'
    'let _gpUrl=`${R}/get-post?id=${r}&req_browser_id=${encodeURIComponent(_bid2)}`;'
    'if(_un2)_gpUrl+=`&req_username=${encodeURIComponent(_un2)}`;'
    'let e=await fetch(_gpUrl);'
)
NEW = (
    'const _bid2=Gn(),_un2=localStorage.getItem(`_myUsername`)||null;'
    'let _gpUrl=`${R}/get-post?id=${r}&req_browser_id=${encodeURIComponent(_bid2)}`;'
    'if(_un2)_gpUrl+=`&req_username=${encodeURIComponent(_un2)}`;'
    'let e=await fetch(_gpUrl,{headers:er()});'
)
if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('OK: get-post fetch now sends auth headers')
else:
    errors.append('FAIL: get-post fetch not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
