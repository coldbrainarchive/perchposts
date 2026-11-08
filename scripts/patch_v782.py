#!/usr/bin/env python3
"""Patch v781 -> v782:
Flap counts must never show a false 0.
1. Dr (vote loader) requests 100 posts but recorded 0 for every post past the 100th; only record what was asked for.
2. Dr retries a failed request once, with a 4s timeout per try so a hung request can't hold up the feed.
3. Home/board polls merge votes instead of replacing them, so a failed poll can't wipe counts.
4. Posts and their votes appear together, so a refresh doesn't flash 0.
5. Home view loads votes for any shown post that has none yet (filtered views, search, deep scroll).
6. Post page ignores a failed vote poll instead of setting 0, and shows post + flaps together.
7. /board/:slug loads votes for all its posts in chunks of 100.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v781.js'
dst = '_deploy/assets/index-DUcNPOLc-v782.js'

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

patch(t('async function Dr(e){if(!e.length)return{};let t=Gn();try{let n=await fetch(`${R}/get-votes?post_ids=${e.slice(0,100).join(`,`)}`);if(!n.ok)return{};'),
      t('async function Dr(e){if(!e.length)return{};e=e.slice(0,100);let t=Gn();try{let _vu=`${R}/get-votes?post_ids=${e.join(`,`)}`,_vo={signal:AbortSignal.timeout(4e3)},n=await fetch(_vu,_vo).catch(()=>null);if(!n||!n.ok)n=await fetch(_vu,{signal:AbortSignal.timeout(4e3)});if(!n.ok)return{};'),
      'Dr: only record requested posts, retry once')

patch('t(o),a(await Dr(o.map(e=>e.id)))},[]);',
      'let _vv=await Dr(o.map(e=>e.id));t(o),a(x=>({...x,..._vv}))},[]);',
      'home: posts and votes together, merge votes')

patch('n(a),o(await Dr(a.map(e=>e.id)))},[]);',
      'let _vv={};for(let _k=0;_k<a.length;_k+=100)Object.assign(_vv,await Dr(a.slice(_k,_k+100).map(e=>e.id)));n(a),o(x=>({...x,..._vv}))},[]);',
      'board page: all votes in chunks, merge')

patch(t('new Date(t.created_at)-new Date(e.created_at):n});let _tag=!!(u||d||f||p),'),
      t('new Date(t.created_at)-new Date(e.created_at):n});'
        '(0,_.useEffect)(()=>{if(!b.slice(0,o).some(x=>!i[x.id]))return;let _c=!1;'
        'Dr(b.filter(x=>!i[x.id]).slice(0,100).map(x=>x.id)).then(v=>{_c||a(x=>({...x,...v}))});'
        'return()=>{_c=!0}},[b.length,o,u,d,f,p,m,qT]);'
        'let _tag=!!(u||d||f||p),'),
      'home: load votes for shown posts missing them')

patch('let{post:t,comments:n}=await e.json();l(Cr(t));',
      'let{post:t,comments:n}=await e.json(),_v0=t?.id?await Dr([t.id]):{};t?.id&&_v0[t.id]&&(Date.now()-_lastVoteTs>3000)&&ie(_v0[t.id]);l(Cr(t));',
      'post page: post and flaps together')
patch('[u,f]=await Promise.all([t?.id?Dr([t.id]):Promise.resolve({}),Er(c)]);t?.id&&(Date.now()-_lastVoteTs>3000)&&ie(u[t.id]||{score:0,myVote:0}),T(f)},[r]);',
      'f=await Er(c);T(f)},[r]);',
      'post page: failed vote poll keeps the count')

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
