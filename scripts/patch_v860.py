#!/usr/bin/env python3
"""Patch v859 -> v860: drop the Nest panel's /my-posts request.
The panel fetched the list every time it opened or the account changed, but nothing ever showed it. Since the
accounts-only lockdown it also logged a 401 in the console after leaving, because the request ran signed out.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v859.js'
dst = '_deploy/assets/index-DUcNPOLc-v860.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n != 1:
        errors.append('FAIL (' + label + '): found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

def t(s):
    return s.replace('`', q)

patch(t('(0,_.useEffect)(()=>{(async()=>{let t=new URLSearchParams({browser_id:k});D&&e?t.set(`mod_user_id`,e.id):r&&t.set(`username`,r),i&&t.set(`exclude_username`,i);let n=await fetch(`${R}/my-posts?${t}`,{headers:er()});p((n.ok?await n.json():{}).posts||[])})()},[r,D,O]),'),
      '', 'remove the unused my-posts request')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
