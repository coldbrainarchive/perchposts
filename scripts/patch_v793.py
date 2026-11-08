#!/usr/bin/env python3
"""Patch v792 -> v793:
Post and huddle chirps feel steadier on phones.
1. The message box stays enabled and focused while sending, so the keyboard stays up, and you can
   send again straight away.
2. "Am I reading old chirps?" now works: .chat-window is column-reverse, so scrollTop is negative
   when scrolled up, and scrollTop<60 was always true. New chirps no longer yank you to the bottom.
3. The 2s refresh no longer wipes messages that are still sending.
4. A failed send puts your text and attachment back and says so.
5. Return makes a new line on touch screens; Enter still sends on desktop. Neither fires mid-composition.
6. The message box grows with your text, up to its 120px limit.
7. CSS: chat scrolling doesn't chain into the page, and the box clears the iPhone home bar.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v792.js'
dst = '_deploy/assets/index-DUcNPOLc-v793.js'

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

# 1. keyboard stays up
patch(t('placeholder:e?(_lpLoading?`Loading preview…`:`Message...`):`Sign in to comment`,disabled:!e||m,rows:1,'),
      t('placeholder:e?(_lpLoading?`Loading preview…`:`Message...`):`Sign in to comment`,disabled:!e,rows:1,'),
      'message box stays enabled while sending')
patch('let F=async(t,i=null,_att=null)=>{if(!t.trim()&&!_att||c?.locked||m)return;',
      'let F=async(t,i=null,_att=null)=>{if(!t.trim()&&!_att||c?.locked)return;',
      'allow another send while one is in flight')
patch(t('className:`chat-send-btn`,disabled:!e||m||(!f.trim()&&!_cA),onClick:()=>{if(!e||(!f.trim()&&!_cA))return;'),
      t('className:`chat-send-btn`,disabled:!e||(!f.trim()&&!_cA),onMouseDown:_b=>_b.preventDefault(),onClick:()=>{if(!e||(!f.trim()&&!_cA))return;'),
      'send button keeps focus in the box')
patch(t('O.current=!0,F(_txt,t,_ca2)},children:`↑`'),
      t('O.current=!0,F(_txt,t,_ca2),document.querySelector(`.comments-shell .chat-input`)?.focus()},children:`↑`'),
      'refocus box after tapping send')

# 2. scroll position
patch('onScroll:()=>{let e=D.current;e&&(O.current=e.scrollTop<60)}',
      'onScroll:()=>{let e=D.current;e&&(O.current=Math.abs(e.scrollTop)<60)}',
      'detect reading older chirps')

# 3. sending messages survive the refresh
patch('d(s),v([]);let c=s.map(e=>e.id),f=await Er(c);T(f)},[r]);',
      'd(s),v(_q=>_q.filter(_x=>!(_x._sent&&s.some(_y=>_y.content===_x.content))));let c=s.map(e=>e.id),f=await Er(c);T(f)},[r]);',
      'refresh keeps messages still sending')
patch('let a=crypto.randomUUID();try{let o=Gn(),s=Zn(Qn(),n),c=er();',
      'let a=crypto.randomUUID(),_ok=!1;try{let o=Gn(),s=Zn(Qn(),n),c=er();',
      'track whether the server accepted the chirp')
patch(',Error(u.error);e&&n&&fetch(',
      ',Error(u.error);_ok=!0,v(_q=>_q.map(_x=>_x.id===a?{..._x,_sent:!0}:_x));e&&n&&fetch(',
      'mark chirp as accepted')

# 4. failed sends
patch('h(!1),await P()}catch(_ce){v(e=>e.filter(e=>e.id!==a)),h(!1),console.error(_ce)}};',
      t('h(!1),await P(),v(_q=>_q.filter(_x=>_x.id!==a))}catch(_ce){v(e=>e.filter(e=>e.id!==a)),h(!1),'
        '_ok||(p(_x=>_x||t),_att&&_setCA(_x=>_x||_att),_ce instanceof TypeError&&alert(`Couldn’t send. Check your connection and try again.`)),console.error(_ce)}};'),
      'failed send restores text')

# 5. Return key
patch(t('onKeyDown:e=>{if(e.key===`Enter`&&!e.shiftKey){if(e.preventDefault(),!f.trim()&&!_cA)return;let t=f,_ca=_cA||_lpAt,n=S?.id||null;'),
      t('onKeyDown:e=>{if(e.key===`Enter`&&!e.shiftKey&&!e.nativeEvent.isComposing&&!matchMedia(`(pointer:coarse)`).matches){if(e.preventDefault(),!f.trim()&&!_cA)return;let t=f,_ca=_cA||_lpAt,n=S?.id||null;'),
      'Return is a new line on touch screens')

# 6. growing box
patch('},[u.length,g.length]);let F=async',
      t('},[u.length,g.length]);(0,_.useEffect)(()=>{let _t=document.querySelector(`.comments-shell .chat-input`);if(_t){_t.style.boxSizing=`border-box`;_t.style.height=`auto`;_t.style.height=Math.min(_t.scrollHeight,120)+`px`}},[f]);let F=async'),
      'message box grows with text')

# 7. CSS
patch('.chat-window {',
      '.chat-window{overscroll-behavior:contain}.comments-shell .chat-compose:not(:focus-within){padding-bottom:calc(10px + env(safe-area-inset-bottom))} .chat-window {',
      'chat scrolling and home bar spacing')

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
