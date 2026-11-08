#!/usr/bin/env python3
"""Patch v822 -> v823: the preview always shows the Latest title, and the Pinned pill is the same grey."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v822.js'
dst = '_deploy/assets/index-DUcNPOLc-v823.js'

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

patch(t('if(_np){if(_i===_nl-1)_st(`🕒 Latest`,``,_e.created_at);if(_i===_rev.length-1)_st(`📌 Pinned`,` pinned`,_e.created_at)}'),
      t('if(_pv){if(_i===_nl-1)_st(`🕒 Latest`,_e.created_at);if(_np&&_i===_rev.length-1)_st(`📌 Pinned`,_e.created_at)}'),
      'titles')
patch(t('_st=(_x,_c,_d)=>{'), t('_st=(_x,_d)=>{'), 'title args')
patch(t('className:`chat-section-pill`+_c,'), t('className:`chat-section-pill`,'), 'pill class')
patch('.chat-section-pill.pinned{border-color:rgba(192,132,252,0.5);background:rgba(192,132,252,0.14);color:#c084fc}', '', 'pinned colour')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
