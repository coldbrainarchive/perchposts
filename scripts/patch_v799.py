#!/usr/bin/env python3
"""Patch v798 -> v799:
Notifications:
1. Back from a notification returns to the post. The link's ?highlight stayed in history, so back
   landed on it and replayed the jump; opening the chat now cleans that entry first.
2. A chat notification for the post you're already on opens the chat and finds the comment.
Desktop:
3. The chat header shows the huddle name or headline, and uses the same colours as the phone screen.
   The chat stays inline: no preview, nothing to open.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v798.js'
dst = '_deploy/assets/index-DUcNPOLc-v799.js'

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

patch('_cfR=(0,_.useRef)(!1),_cyR=(0,_.useRef)(0);',
      '_cfR=(0,_.useRef)(!1),_cyR=(0,_.useRef)(0),_ckR=(0,_.useRef)(null);',
      'remember which link opened the chat')
patch(t('_cyR.current=window.scrollY;history.pushState(history.state,``,location.href);'),
      t('_cyR.current=window.scrollY;if(a||_nc||_sy)history.replaceState(history.state,``,location.pathname);history.pushState(history.state,``,location.href);'),
      'clean the notification link out of history')
patch('(0,_.useEffect)(()=>{_cfR.current=!1;_setCF(!1)},[r]);',
      '(0,_.useEffect)(()=>{_cfR.current=!1;_ckR.current=null;_setCF(!1)},[r]);',
      'reset per post')
patch('(0,_.useEffect)(()=>{if(!c||_cfR.current)return;_cfR.current=!0;if(window.innerWidth<768&&(c.is_huddle||a||_nc||_sy||te.current))_openC()},[c]);',
      t('(0,_.useEffect)(()=>{if(!c)return;let _k=[r,a,_nc,_sy].join(`|`);if(_ckR.current===_k)return;_ckR.current=_k;let _first=!_cfR.current;_cfR.current=!0;'
        'if(window.innerWidth<768&&(a||_nc||_sy||_first&&(c.is_huddle||te.current)))_openC()},[c,a,_nc,_sy]);'),
      'open for notifications on the same post')
patch(t('setTimeout(()=>o(`/post/${r}`,{replace:!0}),1800)},[u,a])'),
      t('setTimeout(()=>o(`/post/${r}`,{replace:!0}),1800)},[u,a,_nc,_sy])'),
      'find the comment straight away')

patch(t('onClick:_cf?_closeC:void 0,children:_cf?[_ct]:[u.filter(_c=>_c.username!==`__system__`).length,` Chirps`]})'),
      'onClick:_cf?_closeC:void 0,children:[_ct]})',
      'header shows the name on desktop too')
patch('.chat-full .chat-panel-header>div:first-child{min-width:0;flex:1}',
      '.comments-shell .chat-panel-header>div:first-child{min-width:0;flex:1}',
      'long titles: desktop')
patch('.chat-full .comments-panel-title{display:block;min-width:0;font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
      '.comments-shell .comments-panel-title{display:block;min-width:0;font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
      'title style: desktop')
patch('.chat-full .chat-compose{background:#14161c}.chat-full .chat-panel-header{background:#16171d;border-top:env(safe-area-inset-top) solid #16171d}',
      '.comments-shell .chat-compose{background:#14161c}.comments-shell .chat-panel-header{background:#16171d}.chat-full .chat-panel-header{border-top:env(safe-area-inset-top) solid #16171d}',
      'colours: desktop')

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
