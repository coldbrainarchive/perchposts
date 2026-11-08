#!/usr/bin/env python3
"""Patch v780 -> v781:
Keep every post reachable without loading them all up front ("Load older posts").
Worker /get-posts now pages with ?before=<cursor> and returns next_before.
1. Filtered views (board / country / continent / user / Flock) fetch 50 posts instead of up to 10000.
2. User filter sends the username as written in the URL (exact match uses the username index).
3. Home feed and filtered views show a "Load older posts" button once everything loaded is shown;
   each click fetches the next 50 older posts from the server cursor.
4. The 30s home poll pauses once older pages are loaded, so they aren't wiped (resets on view change).
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v780.js'
dst = '_deploy/assets/index-DUcNPOLc-v781.js'

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
    # write template literals as `...` in this file; swap for real backticks
    return s.replace('`', q)

# State: older pages, their cursor (undefined = not paging yet), filtered-view cursor, loading flag
patch(t('function Vr(){let[e,t]=(0,_.useState)([]),[n,r]=(0,_.useState)({}),[i,a]=(0,_.useState)({}),[o,s]=(0,_.useState)(10),'),
      t('function Vr(){let[e,t]=(0,_.useState)([]),[n,r]=(0,_.useState)({}),[i,a]=(0,_.useState)({}),[o,s]=(0,_.useState)(10),'
        '[_old,_setOld]=(0,_.useState)([]),[_om,_setOm]=(0,_.useState)(void 0),[_tm,_setTm]=(0,_.useState)(null),[_ldg,_setLdg]=(0,_.useState)(!1),_hmR=(0,_.useRef)(null),_pgR=(0,_.useRef)(!1),'),
      'home state for older pages')

# Home poll: remember the server cursor for the oldest post in the 500
patch('{posts:i}=e.ok?await e.json():{posts:[]};r(wr(n.ok',
      '_gj=e.ok?await e.json():{posts:[]},{posts:i}=_gj;_hmR.current=_gj.next_before??null;r(wr(n.ok',
      'home poll keeps next_before')

# Pause the home poll while reading older pages
patch(t('_pv=()=>{document.hidden||new URLSearchParams(location.search).get(`time`)||v()}'),
      t('_pv=()=>{document.hidden||new URLSearchParams(location.search).get(`time`)||_pgR.current||v()}'),
      'pause home poll while paging')

# Reset older pages when the view changes
patch('(0,_.useEffect)(()=>{s(10);window.scrollTo(0,0)},[u,d,f,p,m,qT])',
      '(0,_.useEffect)(()=>{s(10);_setOld([]);_setOm(void 0);window.scrollTo(0,0)},[u,d,f,p,m,qT])',
      'reset older pages on view change')

# Filtered views: one page instead of 10000 posts
patch(t('let turl=u===`activity`?`${R}/get-posts?activity=1&sort=activity`:`${R}/get-posts?limit=10000`;'),
      t('let turl=u===`activity`?`${R}/get-posts?activity=1&sort=activity&limit=50`:`${R}/get-posts?limit=50`;'),
      'filtered views fetch 50')
patch(t('if(p)turl+=`&username=${encodeURIComponent(p)}`;'),
      t('if(p)turl+=`&username=${encodeURIComponent(l.get(`user`)||p)}`;'),
      'user filter sends original case')
patch('.then(d2=>{setTagR(Sr(d2.posts||[]))})',
      '.then(d2=>{_setTm(d2.next_before??null);setTagR(Sr(d2.posts||[]))})',
      'filtered views keep next_before')

# Displayed list = current view + older pages
patch(t('_bl=m&&SR!==null?SR:qT&&TR!==null?TR:(u||d||f||p||_bot)&&TagR!==null?TagR:e,b=_bl.filter('),
      t('_bl0=m&&SR!==null?SR:qT&&TR!==null?TR:(u||d||f||p||_bot)&&TagR!==null?TagR:e,'
        '_bl=(_pgR.current=_om!==void 0,_old.length?_bl0.concat(_old.filter(x=>!_bl0.some(y=>y.id===x.id))):_bl0),b=_bl.filter('),
      'append older pages to list')

# Load older: next 50 from the server cursor
patch(t('new Date(t.created_at)-new Date(e.created_at):n});return(0,L.jsxs)(`div`,{className:`home-shell`,children:[(0,L.jsx)(Lr,{}),p&&'),
      t('new Date(t.created_at)-new Date(e.created_at):n});'
        'let _tag=!!(u||d||f||p),_cur=_om!==void 0?_om:_tag?(TagR!==null?_tm:null):_hmR.current,'
        '_canMore=!(u===`feedback`||u===`huddles`)&&!m&&!qT&&_cur!=null,'
        '_loadOlder=async()=>{if(_ldg||_cur==null)return;let _act=u===`activity`,'
        '_url=_act?`${R}/get-posts?activity=1&sort=activity&limit=50`:`${R}/get-posts?limit=50`;'
        'if(u&&!_act)_url+=`&board=${encodeURIComponent(u)}`;'
        'if(d)_url+=`&continent=${encodeURIComponent(d)}`;'
        'if(f)_url+=`&country=${encodeURIComponent(f)}`;'
        'if(p)_url+=`&username=${encodeURIComponent(l.get(`user`)||p)}`;'
        '_url+=`&before=${encodeURIComponent(_cur)}`;_setLdg(!0);'
        'try{let _r=await fetch(_url);if(!_r.ok)return;let _j=await _r.json(),'
        '_ps=Sr((_j.posts||[]).filter(x=>{if(_tag)return!0;let t2=cr(x);return t2!==`The Cage`&&t2!==`Jail`&&(!x.pinned||x.pinned_global)}));'
        '_setOld(x=>x.concat(_ps));_setOm(_j.next_before??null);'
        'if(_ps.length){let _vv=await Dr(_ps.map(x=>x.id));a(x=>({...x,..._vv}))}}catch{}finally{_setLdg(!1)}};'
        'return(0,L.jsxs)(`div`,{className:`home-shell`,children:[(0,L.jsx)(Lr,{}),p&&'),
      'load older handler')

patch(t('o<b.length&&(0,L.jsx)(`div`,{ref:c,style:{height:1}})]})]})}function Hr('),
      t('o<b.length&&(0,L.jsx)(`div`,{ref:c,style:{height:1}}),'
        '_canMore&&o>=b.length&&(0,L.jsx)(`button`,{onClick:_loadOlder,disabled:_ldg,'
        'style:{display:`block`,margin:`16px auto 28px`,padding:`10px 18px`,borderRadius:10,border:`1px solid #2e303a`,'
        'background:`transparent`,color:`#94a3b8`,fontWeight:600,fontSize:14,cursor:_ldg?`default`:`pointer`},'
        'children:_ldg?`Loading…`:`Load older posts`})]})]})}function Hr('),
      'load older button')

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
