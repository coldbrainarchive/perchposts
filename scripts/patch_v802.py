#!/usr/bin/env python3
"""Patch v801 -> v802:
Chrome on iPhone left a gap under the chat when its bars shrank: the chat kept the height measured
with them showing. With no keyboard up, the chat is now pinned to the bottom of the screen and takes
no measurement at all. The measured height is only used while typing, when the keyboard needs it.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v801.js'
dst = '_deploy/assets/index-DUcNPOLc-v802.js'

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

patch(t('_h.style.setProperty(`--cvt`,(_vv?_vv.offsetTop:0)+`px`);_dg()})}'),
      t('_h.style.setProperty(`--cvt`,(_vv?_vv.offsetTop:0)+`px`);_h.classList.toggle(`chat-kb`,/^(TEXTAREA|INPUT)$/.test(document.activeElement?.tagName||``));_dg()})}'),
      'note when the keyboard is in use')
patch(t('_h.classList.remove(`chat-open`);_h.style.removeProperty(`--cvh`);'),
      t('_h.classList.remove(`chat-open`,`chat-kb`);_h.style.removeProperty(`--cvh`);'),
      'clear it on close')
patch('.chat-back{background:none;border:none;color:#c084fc;font-size:28px;',
      'html:not(.chat-kb) .comments-shell.chat-full{height:auto;bottom:0;transform:none}.chat-back{background:none;border:none;color:#c084fc;font-size:28px;',
      'pin to the bottom with no keyboard')
patch(t('\\nshell ${_s?.top}-${_s?.bottom} box ${_c?.bottom} cvh'),
      t('\\nkb ${_h.classList.contains(`chat-kb`)} shell ${_s?.top}-${_s?.bottom} box ${_c?.bottom} cvh'),
      'readout shows keyboard state')

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
