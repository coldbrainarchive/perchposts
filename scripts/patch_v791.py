#!/usr/bin/env python3
"""Patch v790 -> v791:
Comments flash with the same glow as the Sign In button (around the bubble, 1.5s, fades in and
out) instead of blinking a purple fill inside it. Covers notification taps and the huddle
invite/remove messages. The glow goes on .chat-msg-body, the rounded card: it hides overflow, so a
shadow on the .chat-bubble inside it would never show.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v790.js'
dst = '_deploy/assets/index-DUcNPOLc-v791.js'

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

patch('let _lastVoteTs=0;',
      t('let _lastVoteTs=0;function _glow(e){e=e.closest(`.chat-msg-body`)||e;e.style.transition=`box-shadow 0.3s`;'
        'e.style.boxShadow=`0 0 0 4px rgba(192,132,252,0.6),0 0 20px rgba(192,132,252,0.8)`;'
        'setTimeout(()=>{e.style.boxShadow=``;setTimeout(()=>{e.style.transition=``},350)},1500)}'),
      'shared glow')

patch(t('if(_b){let _bn=0;const _bl=()=>{_b.style.background=`rgba(192,132,252,0.35)`;setTimeout(()=>{_b.style.background=``;_bn++;if(_bn<3)setTimeout(_bl,130);},350);};_bl();}'),
      'if(_b)_glow(_b);',
      'notification tap glows')
patch(t('if(_fb){let _fbn=0;const _fbl=()=>{_fb.style.background=`rgba(192,132,252,0.35)`;setTimeout(()=>{_fb.style.background=``;_fbn++;if(_fbn<3)setTimeout(_fbl,130);},350)};_fbl();}'),
      'if(_fb)_glow(_fb);',
      'huddle invite/remove glows', count=2)

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
