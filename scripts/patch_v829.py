#!/usr/bin/env python3
"""Patch v828 -> v829, for scale:
Feeds use the comment_count the server sends with each post instead of downloading every chirp on the
site every 30s. Reactions come with /get-post, because listing chirp ids in a URL fails on long chats.
A poll on an unchanged post gets a tiny "unchanged" reply, so nothing downloads or redraws, and the page
 after a quiet minute polls every 10s
instead of 2s until the next tap, key press or return to the tab. The notification count polls every 30s.
Notifications show an error with a retry instead of looking empty when the request fails.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v828.js'
dst = '_deploy/assets/index-DUcNPOLc-v829.js'

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

# Feed counts
patch(t('let[e,n]=await Promise.all([fetch(`${R}/get-posts?limit=500`),fetch(`${R}/get-comments-index`)]),_gj=e.ok?await e.json():{posts:[]},{posts:i}=_gj;_hmR.current=_gj.next_before??null;r(wr(n.ok?await n.json():[]));'),
      t('let e=await fetch(`${R}/get-posts?limit=500`),_gj=e.ok?await e.json():{posts:[]},{posts:i}=_gj;_hmR.current=_gj.next_before??null;r(Object.fromEntries((i||[]).map(x=>[x.id,x.comment_count||0])));'),
      'home counts')
patch(t('let[e,t]=await Promise.all([fetch(`${R}/get-posts?limit=500`),fetch(`${R}/get-comments-index`)]),{posts:r}=e.ok?await e.json():{posts:[]};i(wr(t.ok?await t.json():[]));'),
      t('let e=await fetch(`${R}/get-posts?limit=500`),{posts:r}=e.ok?await e.json():{posts:[]};i(Object.fromEntries((r||[]).map(x=>[x.id,x.comment_count||0])));'),
      'board page counts')
patch('(0,L.jsx)(Ir,{post:e,commentCount:n[e.id]||0,', '(0,L.jsx)(Ir,{post:e,commentCount:e.comment_count??n[e.id]??0,', 'home card')
patch('(0,L.jsx)(Ir,{post:e,commentCount:r[e.id]||0,', '(0,L.jsx)(Ir,{post:e,commentCount:e.comment_count??r[e.id]??0,', 'board card')
patch('fr.includes(e.username)?(n[e.id]||0)>0||', 'fr.includes(e.username)?(e.comment_count??n[e.id]??0)>0||', 'flock filter')
patch('!fr.includes(e.username)||(r[e.id]||0)>0||', '!fr.includes(e.username)||(e.comment_count??r[e.id]??0)>0||', 'board flock filter')

# Post page
patch(t('let{post:t,comments:n}=await e.json(),_v0='), t('let{post:t,comments:n,reactions:_rx,unchanged:_un0,version:_ver}=await e.json();if(_un0){_qt.current++;let _vu=await Dr([r]);_vu[r]&&(Date.now()-_lastVoteTs>3000)&&ie(_vu[r]);return}let _v0='), 'reactions from get-post')
patch(t('let _gpUrl=`${R}/get-post?id=${r}&req_browser_id=${encodeURIComponent(_bid2)}`;'),
      t('let _gpUrl=`${R}/get-post?id=${r}&req_browser_id=${encodeURIComponent(_bid2)}`;if(_pk.current)_gpUrl+=`&v=${_pk.current}`;'),
      'send version')
patch(t('&&ie(_v0[t.id]);l(Cr(t));let s=n||[];d(s),'),
      t('&&ie(_v0[t.id]);_qt.current=0;_pk.current=_ver||null;l(Cr(t));let s=n||[];d(s),'),
      'skip unchanged')
patch(t('let c=s.map(e=>e.id),f=await Er(c);T(f)},[r]);'),
      t('let f={};(_rx||[]).forEach(({comment_id:_i,browser_id:_b,emoji:_m})=>{f[_i]||(f[_i]={});f[_i][_m]||(f[_i][_m]=[]);f[_i][_m].push(_b)});T(f)},[r]);'),
      'build reactions')
patch(t('_fid=(0,_.useRef)(null);'), t('_fid=(0,_.useRef)(null),_pk=(0,_.useRef)(null),_qt=(0,_.useRef)(0);'), 'poll refs')
patch(t('let e=window.setTimeout(()=>{P()},0),_pv=()=>{document.hidden||P()},t=window.setInterval(_pv,2e3);document.addEventListener(`visibilitychange`,_pv);return()=>{'),
      t('let _tk=0,_wk=()=>{_qt.current=0},e=window.setTimeout(()=>{P()},0),_pv=()=>{_tk++;if(document.hidden||_qt.current>30&&_tk%5)return;P()},t=window.setInterval(_pv,2e3);_qt.current=0;document.addEventListener(`pointerdown`,_wk,!0);document.addEventListener(`keydown`,_wk,!0);document.addEventListener(`visibilitychange`,_wk);document.addEventListener(`visibilitychange`,_pv);return()=>{document.removeEventListener(`pointerdown`,_wk,!0);document.removeEventListener(`keydown`,_wk,!0);document.removeEventListener(`visibilitychange`,_wk);'),
      'quiet polling')

# Notifications
patch(t('setInterval(()=>{document.hidden||e()},1e4)'), t('setInterval(()=>{document.hidden||e()},3e4)'), 'count every 30s')
patch(t('[g,v]=(0,_.useState)(!0),[_showClear,'), t('[g,v]=(0,_.useState)(!0),[_ne,_setNe]=(0,_.useState)(!1),[_nt,_setNt]=(0,_.useState)(0),[_showClear,'), 'error state')
patch(t('i&&t.set(`exclude_username`,i);let n=await fetch(`${R}/notifications?${t}`,{headers:er()});h((n.ok?await n.json():{}).notifs||[]),v(!1)})())},[c,e,r]);'),
      t('i&&t.set(`exclude_username`,i);try{let n=await fetch(`${R}/notifications?${t}`,{headers:er()});if(!n.ok)throw 0;h((await n.json()).notifs||[]);_setNe(!1)}catch{_setNe(!0)}v(!1)})())},[c,e,r,_nt]);'),
      'catch failures')
patch(t('g?(0,L.jsx)(_Bd,{}):j.length===0?'),
      t('g?(0,L.jsx)(_Bd,{}):_ne?(0,L.jsxs)(`div`,{style:{padding:`48px 20px`,color:`#64748b`,textAlign:`center`},children:[(0,L.jsx)(`div`,{style:{fontSize:14,fontWeight:600},children:`Couldn\'t load notifications`}),(0,L.jsx)(`button`,{type:`button`,onClick:()=>_setNt(_x=>_x+1),style:{marginTop:12,padding:`8px 16px`,borderRadius:10,border:`1px solid #2e303a`,background:`transparent`,color:`#c084fc`,fontWeight:600,fontSize:13,cursor:`pointer`},children:`Try again`})]}):j.length===0?'),
      'error message')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
