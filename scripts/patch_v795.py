#!/usr/bin/env python3
"""Patch v794 -> v795:
1. Phone preview loses its "N Chirps" header; the View all button already says it.
2. The chat screen's header shows the huddle name or a short headline, not "N Chirps".
3. Safari: the chat screen is one solid colour. The pull-to-refresh strip left a dark band across
   the top, and the page colour showed around the browser's address pill above the keyboard.
4. Chrome on iPhone: the site's pull to refresh stands down. It cancels touch scrolling when it
   thinks the page is at the top, and Chrome's collapsing toolbar can make that true too early.
   Chrome on iPhone has its own pull to refresh.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v794.js'
dst = '_deploy/assets/index-DUcNPOLc-v795.js'

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

patch(t('_ct=Mr(c.content).attachment?.title||c.title||``;'),
      t('_cm=Mr(c.content),_ct=c.title||_cm.attachment?.title||(_cm.text||``).trim().slice(0,70)||`Chirps`;'),
      'chat title falls back to post text')
patch(t('className:`comments-panel-title`,children:[u.filter(_c=>_c.username!==`__system__`).length,` Chirps`]})'),
      t('className:`comments-panel-title`,children:_cf?[_ct]:[u.filter(_c=>_c.username!==`__system__`).length,` Chirps`]})'),
      'chat header shows the name')
patch(t('_cf&&_ct&&(0,L.jsx)(`div`,{className:`chat-post-line`,children:_ct}),'),
      '',
      'remove the separate title line')

patch(t('_h.classList.add(`chat-open`);'),
      t('let _tc=document.querySelector(`meta[name="theme-color"]`),_tv=_tc?.content;_tc&&(_tc.content=`#14161c`);_h.classList.add(`chat-open`);'),
      'browser colour matches the chat')
patch(t('_h.classList.remove(`chat-open`);'),
      t('_tc&&(_tc.content=_tv);_h.classList.remove(`chat-open`);'),
      'browser colour restored on close')

patch(t('t=e=>{if(x.current.insideScroller||document.documentElement.classList.contains(`chat-open`)||!e.touches||!e.touches[0])return;'),
      t('t=e=>{if(/CriOS/.test(navigator.userAgent)||x.current.insideScroller||document.documentElement.classList.contains(`chat-open`)||!e.touches||!e.touches[0])return;'),
      'Chrome on iPhone keeps native scrolling')

patch('.chat-post-line{padding:0 16px 8px;color:#94a3b8;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;border-bottom:1px solid rgba(148,163,184,.1)}',
      '.chat-preview .chat-panel-header{display:none!important}'
      '.chat-full .chat-panel-header>div:first-child{min-width:0;flex:1}'
      '.chat-full .comments-panel-title{display:block;min-width:0;font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
      'html.chat-open,html.chat-open body{background:#14161c}'
      'html.chat-open .ptr-strip{display:none!important}'
      '.chat-full .chat-panel-header,.chat-full .chat-compose{background:#14161c}',
      'chat screen colours and title')

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
