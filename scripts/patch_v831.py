#!/usr/bin/env python3
"""Patch v830 -> v831: reacting needs an account. Signed out, the React button and existing reaction pills
flash Sign In instead. If the server still refuses, for example an expired login, the next poll fetches
the real reactions so the optimistic one doesn't stick.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v830.js'
dst = '_deploy/assets/index-DUcNPOLc-v831.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label, count=1):
    global content
    n = content.count(old)
    if n != count:
        errors.append('FAIL (' + label + '): expected ' + str(count) + ' matches, found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

def t(s):
    return s.replace('`', q)

GATE = 'if(!localStorage.getItem(`auth_token`)){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}'

patch(t('function ne(e,t){let r=Gn(),i=(w[e]?.[t]||[]).includes(r);'),
      t('function ne(e,t){' + GATE + 'let r=Gn(),i=(w[e]?.[t]||[]).includes(r);'), 'gate reacting')
patch(t('function D(){y(!1),x(!0),S.current&&'),
      t('function D(){y(!1);' + GATE + 'x(!0),S.current&&'), 'gate the picker')
patch(t('action:i?`remove`:`add`,username:a})}).catch(()=>{})}let[re,ie]='),
      t('action:i?`remove`:`add`,username:a})}).then(_r=>{_r.ok||(_pk.current=null)}).catch(()=>{_pk.current=null})}let[re,ie]='),
      'recover from a refusal')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
