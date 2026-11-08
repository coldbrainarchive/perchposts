#!/usr/bin/env python3
"""Patch v793 -> v794:
Dedicated chirp screen on phones (under 768px). Desktop is unchanged.
1. The post page shows the last 5 chirps and a "View all" button; tapping anywhere there opens chat.
2. The chat opens full height with a back button and the post title. It's the same chat, restyled.
3. Huddles, the chirp button, and comment notifications open straight into it.
4. The screen tracks window.visualViewport, so the message box stays above the keyboard.
5. Back, browser back and edge swipe close it: opening pushes a history entry.
6. Pull to refresh is off while it's open.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v793.js'
dst = '_deploy/assets/index-DUcNPOLc-v794.js'

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

patch('_lpUrl=(0,_.useRef)(null),_isd=(0,_.useRef)(!1);',
      '_lpUrl=(0,_.useRef)(null),_isd=(0,_.useRef)(!1),[_cf,_setCF]=(0,_.useState)(!1),_cfR=(0,_.useRef)(!1),_cyR=(0,_.useRef)(0);',
      'chat screen state')

patch('},[f]);let F=async',
      t('},[f]);'
        'let _openC=()=>{if(_cf)return;_cyR.current=window.scrollY;history.pushState(history.state,``,location.href);O.current=!0;_setCF(!0)},_closeC=()=>history.back();'
        '(0,_.useEffect)(()=>{_cfR.current=!1;_setCF(!1)},[r]);'
        '(0,_.useEffect)(()=>{let _f=()=>_setCF(!1);window.addEventListener(`popstate`,_f);return()=>window.removeEventListener(`popstate`,_f)},[]);'
        '(0,_.useEffect)(()=>{if(!c||_cfR.current)return;_cfR.current=!0;if(window.innerWidth<768&&(c.is_huddle||a||_nc||_sy||te.current))_openC()},[c]);'
        '(0,_.useEffect)(()=>{if(!_cf)return;let _y=_cyR.current,_b=document.body.style,_h=document.documentElement,_vv=window.visualViewport,_r=0,'
        '_f=()=>{cancelAnimationFrame(_r);_r=requestAnimationFrame(()=>{_h.style.setProperty(`--cvh`,(_vv?_vv.height:window.innerHeight)+`px`);_h.style.setProperty(`--cvt`,(_vv?_vv.offsetTop:0)+`px`)})};'
        '_h.classList.add(`chat-open`);_b.position=`fixed`;_b.top=-_y+`px`;_b.left=`0`;_b.right=`0`;_b.width=`100%`;_f();'
        'if(_vv){_vv.addEventListener(`resize`,_f);_vv.addEventListener(`scroll`,_f)}'
        'requestAnimationFrame(()=>{let _w=D.current;if(_w&&!a&&!_nc&&!_sy)_w.scrollTop=0});'
        'return()=>{cancelAnimationFrame(_r);if(_vv){_vv.removeEventListener(`resize`,_f);_vv.removeEventListener(`scroll`,_f)}'
        '_h.classList.remove(`chat-open`);_h.style.removeProperty(`--cvh`);_h.style.removeProperty(`--cvt`);_b.position=_b.top=_b.left=_b.right=_b.width=``;window.scrollTo(0,_y)}},[_cf]);'
        'let F=async'),
      'open, close, auto-open, keyboard tracking')

patch(t('if(!c)return(0,L.jsx)(`div`,{children:`Loading...`});let ce=cr(c);'),
      t('if(!c)return(0,L.jsx)(`div`,{children:`Loading...`});let _pv=window.innerWidth<768&&!_cf&&!a&&!_nc&&!_sy,'
        '_cn=u.filter(_c=>_c.username!==`__system__`).length,_ct=Mr(c.content).attachment?.title||c.title||``;let ce=cr(c);'),
      'preview mode')

patch(t('(0,L.jsx)(`section`,{className:`comments-shell`,children:'),
      t('(0,L.jsx)(`section`,{className:`comments-shell`+(_cf?` chat-full`:_pv?` chat-preview`:``),'
        'onClickCapture:_pv?_ev=>{_ev.stopPropagation();_ev.preventDefault();_openC()}:void 0,children:'),
      'shell modes')

patch(t('children:[(0,L.jsxs)(`span`,{className:`comments-panel-title`,children:['),
      t('children:[_cf&&(0,L.jsx)(`button`,{type:`button`,className:`chat-back`,"aria-label":`Back to post`,onClick:_closeC,children:`‹`}),(0,L.jsxs)(`span`,{className:`comments-panel-title`,children:['),
      'back button')

patch(t('(0,L.jsx)(`div`,{className:`chat-window`,ref:D,'),
      t('_cf&&_ct&&(0,L.jsx)(`div`,{className:`chat-post-line`,children:_ct}),(0,L.jsx)(`div`,{className:`chat-window`,ref:D,'),
      'post title line')

patch('let _rev=[...de].reverse(),_out=[];',
      'let _rev=[...de].reverse(),_out=[];if(_pv)_rev=_rev.slice(0,5);',
      'last 5 chirps in preview')

patch(t('return _out;})()]}),!c.locked&&(0,L.jsxs)(`div`,{className:`chat-compose`,'),
      t('return _out;})()]}),_pv&&(0,L.jsx)(`button`,{type:`button`,className:`chat-view-all`,children:_cn?`View all ${_cn} chirp${_cn===1?``:`s`}`:`Write the first chirp`}),!c.locked&&(0,L.jsxs)(`div`,{className:`chat-compose`,'),
      'view all button')

patch(t('let e=document.querySelector(`.comments-shell`);e&&e.scrollIntoView({behavior:`smooth`}),setTimeout('),
      t('if(window.innerWidth<768){_openC();return}let e=document.querySelector(`.comments-shell`);e&&e.scrollIntoView({behavior:`smooth`}),setTimeout('),
      'chirp button opens the screen on phones')

patch('t=e=>{if(x.current.insideScroller||!e.touches||!e.touches[0])return;',
      t('t=e=>{if(x.current.insideScroller||document.documentElement.classList.contains(`chat-open`)||!e.touches||!e.touches[0])return;'),
      'no pull to refresh in the chat screen')

patch('.chat-window{overscroll-behavior:contain}',
      '.chat-window{overscroll-behavior:contain}'
      '.comments-shell.chat-preview{position:static;max-height:none}'
      '.chat-preview .chat-window{flex:none;overflow:hidden;padding-bottom:6px}'
      '.chat-preview .chat-compose,.chat-preview .sort-toggle{display:none}'
      '.chat-view-all{display:block;width:calc(100% - 24px);margin:4px 12px 12px;padding:11px;border-radius:12px;border:1px solid #2e303a;background:rgba(192,132,252,.12);color:#c084fc;font-weight:700;font-size:14px;cursor:pointer}'
      '.comments-shell.chat-full{position:fixed;top:0;left:0;right:0;height:var(--cvh,100dvh);max-height:none;margin:0;border:0;border-radius:0;z-index:45;padding-top:env(safe-area-inset-top);box-sizing:border-box;transform:translateY(var(--cvt,0px));background:#14161c}'
      '.chat-back{background:none;border:none;color:#c084fc;font-size:28px;line-height:1;padding:0 10px 2px 0;cursor:pointer}'
      '.chat-post-line{padding:0 16px 8px;color:#94a3b8;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;border-bottom:1px solid rgba(148,163,184,.1)}',
      'chat screen styles')

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
