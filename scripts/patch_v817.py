#!/usr/bin/env python3
"""Patch v816 -> v817: country pill results list Flock posts first (posts by people, and articles with
chirps), newest first within each group. They were sorted in with the news, so a tagged post could sit
at position 87 of 90. Global pins still come first. The worker makes sure these posts are in the results.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v816.js'
dst = '_deploy/assets/index-DUcNPOLc-v817.js'

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

patch(t('let y=u===`activity`,_y=y||u===`feedback`,_bl0='),
      t('let y=u===`activity`,_fk=x=>!fr.includes(x.username)||(n[x.id]||0)>0,_y=y||u===`feedback`,_bl0='),
      'flock check')
patch(t('.sort((e,t)=>{let n=(t.pinned_global?1:0)-(e.pinned_global?1:0);return n===0?_y?'),
      t('.sort((e,t)=>{let n=(t.pinned_global?1:0)-(e.pinned_global?1:0);if(n===0&&_cs)n=_fk(t)-_fk(e);return n===0?_y?'),
      'flock first on country pills')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
