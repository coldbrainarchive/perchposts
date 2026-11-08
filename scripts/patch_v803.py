#!/usr/bin/env python3
"""Patch v802 -> v803:
Temporary diagnostics only, no behaviour change. Chrome on iPhone sometimes leaves a gap under the
chat even when it's pinned to the bottom, so the page's own bottom edge is short of the screen.
?vvdebug=1 now stays on for that browser (so it also covers chats opened from notifications) until
?vvdebug=0, and the readout adds the sizes from before the page was locked and where a bottom-pinned
element actually lands. Remove the readout once the gap is solved.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v802.js'
dst = '_deploy/assets/index-DUcNPOLc-v803.js'

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

patch(t('_vv=window.visualViewport,_r=0,_ts=[],_dg=()=>{if(!/vvdebug/.test(location.search))return;let _e='),
      t('_vv=window.visualViewport,_r=0,_ts=[],_bi=`inner ${window.innerHeight} vv ${_vv?.height} y ${window.scrollY} doc ${_h.scrollHeight}`,'
        '_dg=()=>{let _on=/vvdebug=1/.test(location.search);try{if(_on)localStorage.setItem(`vvd`,`1`);else if(/vvdebug=0/.test(location.search))localStorage.removeItem(`vvd`);else _on=!!localStorage.getItem(`vvd`)}catch{}if(!_on)return;let _e='),
      'readout stays on, keeps the before-lock sizes')
patch(t('_c=document.querySelector(`.chat-compose`)?.getBoundingClientRect();_e.textContent=`vv ${_vv?.height}'),
      t('_c=document.querySelector(`.chat-compose`)?.getBoundingClientRect(),_b0=document.createElement(`div`);_b0.style.cssText=`position:fixed;bottom:0;height:1px;width:1px;visibility:hidden`;document.body.appendChild(_b0);let _fb=_b0.getBoundingClientRect().bottom;_b0.remove();_e.textContent=`v803 before: ${_bi}\\nfixed bottom ${_fb} doc ${_h.scrollHeight} y ${window.scrollY}\\nvv ${_vv?.height}'),
      'readout shows the page bottom')

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
