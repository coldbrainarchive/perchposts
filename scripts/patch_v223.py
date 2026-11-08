#!/usr/bin/env python3
"""Patch v222 -> v223: universal server-side search — unified v() with all filters + real scroll pagination."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v222.js'
dst = '_deploy/assets/index-DUcNPOLc-v223.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Add _lRef (post-count ref) to Vr state declarations ───────────────────
OLD_REF = 'c=(0,_.useRef)(null),'
NEW_REF = 'c=(0,_.useRef)(null),_lRef=(0,_.useRef)(0),'
if OLD_REF in content:
    content = content.replace(OLD_REF, NEW_REF, 1)
    print('OK: _lRef added')
else:
    errors.append('FAIL: c=useRef not found')

# ── 2. Rewrite v() — server filters all params, offset for pagination ─────────
OLD_V = (
    'let v=(0,_.useCallback)(async()=>{'
    'let[e,n]=await Promise.all([fetch(`${R}/get-posts?limit=500`),fetch(`${R}/get-comments-index`)]),'
    '{posts:i}=e.ok?await e.json():{posts:[]};'
    'r(wr(n.ok?await n.json():[]));'
    'let o=Sr((i||[]).filter(e=>{let t=cr(e);return t!==`The Cage`&&t!==`Jail`&&(!e.pinned||e.pinned_global)}));'
    't(o),a(await Dr(o.map(e=>e.id)))},'
    '[])'
)
NEW_V = (
    'let v=(0,_.useCallback)(async(_ofs)=>{'
    '_ofs=_ofs||0;'
    'let _u=`${R}/get-posts?limit=30&offset=${_ofs}`;'
    'if(u===`activity`)_u+=`&sort=activity`;'
    'else if(u)_u+=`&board=${encodeURIComponent(u)}`;'
    'if(d)_u+=`&continent=${encodeURIComponent(d)}`;'
    'if(f)_u+=`&country=${encodeURIComponent(f)}`;'
    'if(p)_u+=`&username=${encodeURIComponent(p)}`;'
    'if(m)_u+=`&search=${encodeURIComponent(m)}`;'
    'if(qT&&qT.startsWith(`ago_`)){const _h=parseInt(qT.slice(4));_u+=`&since=${encodeURIComponent(new Date(Date.now()-_h*3600000).toISOString())}`}'
    'else if(qT&&qT.includes(`-`)){const _qd=new Date(qT);_u+=`&since=${encodeURIComponent(_qd.toISOString())}&until=${encodeURIComponent(new Date(_qd.getTime()+86400000).toISOString())}`}'
    'let[_r,_cn]=await Promise.all([fetch(_u),_ofs===0?fetch(`${R}/get-comments-index`):Promise.resolve(null)]);'
    'const{posts:_p}=_r.ok?await _r.json():{posts:[]};'
    'if(_cn&&_cn.ok)r(wr(await _cn.json()));'
    'const _f=(_p||[]).filter(_e=>{const _t=cr(_e);return _t!==`The Cage`&&_t!==`Jail`&&(!_e.pinned||_e.pinned_global)});'
    'if(_ofs===0)t(_f);else t(_pr=>[..._pr,..._f]);'
    'a(_pr=>({..._pr,...await Dr(_f.map(_e=>_e.id))}));'
    '_lRef.current=(_ofs===0?0:_lRef.current)+_f.length;'
    '},[u,d,f,p,m,qT])'
)
if OLD_V in content:
    content = content.replace(OLD_V, NEW_V, 1)
    print('OK: v() rewritten with server filters + pagination')
else:
    errors.append('FAIL: v() function not found')

# ── 3. Filter change: clear posts list + reset display ───────────────────────
OLD_RESET = '(0,_.useEffect)(()=>{s(10);window.scrollTo(0,0)},[u,d,f,p,m,qT])'
NEW_RESET = '(0,_.useEffect)(()=>{t([]);_lRef.current=0;s(10);window.scrollTo(0,0)},[u,d,f,p,m,qT])'
if OLD_RESET in content:
    content = content.replace(OLD_RESET, NEW_RESET, 1)
    print('OK: filter reset clears posts list')
else:
    errors.append('FAIL: filter reset effect not found')

# ── 4. Remove SR fetch effect (server search now in v()) ─────────────────────
OLD_SR = (
    '(0,_.useEffect)(()=>{if(!m){setSR(null);setSRLoading(!1);return}'
    'setSRLoading(!0);fetch(`${R}/get-posts?search=${encodeURIComponent(m)}&limit=1000`)'
    '.then(r2=>r2.ok?r2.json():{posts:[]})'
    '.then(d2=>{setSR(Sr((d2.posts||[]).filter(e2=>{const t2=cr(e2);return t2!==`The Cage`&&t2!==`Jail`&&(!e2.pinned||e2.pinned_global)})));setSRLoading(!1)})'
    '.catch(()=>{setSR(null);setSRLoading(!1)})},[m])'
)
NEW_SR = '(0,_.useEffect)(()=>{setSR(null);setSRLoading(!1)},[m])'
if OLD_SR in content:
    content = content.replace(OLD_SR, NEW_SR, 1)
    print('OK: SR effect neutralised')
else:
    errors.append('FAIL: SR effect not found')

# ── 5. Remove TR time-range fetch effect (time params now in v()) ─────────────
OLD_TR = (
    '(0,_.useEffect)(()=>{if(!qT){setTR(null);return}'
    'let since,until;if(qT.includes(`-`)){since=qT+`T00:00:00.000Z`;until=new Date(new Date(qT).getTime()+86400000).toISOString().slice(0,10)+`T00:00:00.000Z`}'
    'else if(qT.startsWith(`ago_`)){const n=parseInt(qT.slice(4));since=new Date(Date.now()-n*3600000).toISOString()}'
    'else{setTR(null);return}'
    'let turl=`${R}/get-posts?limit=500${since?`&since=${encodeURIComponent(since)}`:``}${until?`&until=${encodeURIComponent(until)}`:``}`;'
    'fetch(turl).then(r2=>r2.ok?r2.json():{posts:[]})'
    '.then(d2=>{setTR(Sr((d2.posts||[]).filter(e2=>{const t2=cr(e2);return t2!==`The Cage`&&t2!==`Jail`&&(!e2.pinned||e2.pinned_global)})))})'
    '.catch(()=>setTR(null))},[qT])'
)
NEW_TR = '(0,_.useEffect)(()=>{setTR(null)},[qT])'
if OLD_TR in content:
    content = content.replace(OLD_TR, NEW_TR, 1)
    print('OK: TR effect neutralised')
else:
    errors.append('FAIL: TR effect not found')

# ── 6. Remove TagR board/filter fetch effect (board/user/country now in v()) ──
OLD_TAGR = (
    '(0,_.useEffect)(()=>{if(!u&&!d&&!f&&!p){setTagR(null);return}'
    'let turl=u===`activity`?`${R}/get-posts?limit=1000&sort=activity`:`${R}/get-posts?limit=500`;'
    'if(u&&u!==`activity`)turl+=`&board=${encodeURIComponent(u)}`;'
    'if(d)turl+=`&continent=${encodeURIComponent(d)}`;'
    'if(f)turl+=`&country=${encodeURIComponent(f)}`;'
    'if(p)turl+=`&username=${encodeURIComponent(p)}`;'
    'fetch(turl).then(r2=>r2.ok?r2.json():{posts:[]})'
    '.then(d2=>{setTagR(Sr(d2.posts||[]))})'
    '.catch(()=>setTagR(null))},[u,d,f,p])'
)
NEW_TAGR = '(0,_.useEffect)(()=>{setTagR(null)},[u,d,f,p])'
if OLD_TAGR in content:
    content = content.replace(OLD_TAGR, NEW_TAGR, 1)
    print('OK: TagR effect neutralised')
else:
    errors.append('FAIL: TagR effect not found')

# ── 7. IntersectionObserver: fetch next page when near bottom ─────────────────
OLD_IO = 'e[0].isIntersecting&&s(e=>e+10)'
NEW_IO = 'e[0].isIntersecting&&(_lRef.current>0&&_lRef.current%30===0?v(_lRef.current):s(_n=>_n+20))'
if OLD_IO in content:
    content = content.replace(OLD_IO, NEW_IO, 1)
    print('OK: IntersectionObserver fetches next page')
else:
    errors.append('FAIL: IntersectionObserver not found')

# ── 8. _bl: always use e (SR/TR/TagR are all null now) ───────────────────────
OLD_BL = 'let y=u===`activity`,_bl=m&&SR!==null?SR:qT&&TR!==null?TR:(u||d||f||p||_bot)&&TagR!==null?TagR:e,'
NEW_BL = 'let y=u===`activity`,_bl=e,'
if OLD_BL in content:
    content = content.replace(OLD_BL, NEW_BL, 1)
    print('OK: _bl always uses e')
else:
    errors.append('FAIL: _bl line not found')

# ── 9. b filter: remove server-handled filters, keep only bot + sort ──────────
OLD_B = (
    'b=_bl.filter(e=>u?y?fr.includes(e.username)?(n[e.id]||0)>0||(i[e.id]?.voteCount??0)>0:!0:'
    'cr(e)===(sr(u)?.name||u):!0)'
    '.filter(e=>!_bot||!!(e.browser_id&&String(e.browser_id).startsWith(`bot-`)))'
    '.filter(e=>!d||e.continent===d)'
    '.filter(e=>!f||e.country===f)'
    '.filter(e=>!p||(e.username||``).toLowerCase()===p)'
    '.filter(e=>{if(!m)return!0;let{text:t,attachment:n}=Mr(e.content);return[e.username,e.title,n?.title,n?.description,n?.url,t].filter(Boolean).join(` `).toLowerCase().includes(m)})'
    '.filter(e=>{if(!qT||m||TR!==null)return!0;const now=Date.now(),ca=new Date(e.created_at);if(qT.includes(`-`)){const d=new Date(qT);return ca>=d&&ca<new Date(d.getTime()+86400000)}if(qT.startsWith(`ago_`)){const n=parseInt(qT.slice(4));return(now-ca.getTime())>=n*3600000}return!0})'
)
NEW_B = (
    'b=_bl.filter(e=>!_bot||!!(e.browser_id&&String(e.browser_id).startsWith(`bot-`)))'
)
if OLD_B in content:
    content = content.replace(OLD_B, NEW_B, 1)
    print('OK: b filter simplified to bot-only')
else:
    errors.append('FAIL: b filter chain not found')

# ── 10. render: b.slice(0,o) → b.map (server pagination controls page size) ──
OLD_SLICE = 'b.slice(0,o).map(e=>(0,L.jsx)(Ir,'
NEW_SLICE = 'b.map(e=>(0,L.jsx)(Ir,'
if OLD_SLICE in content:
    content = content.replace(OLD_SLICE, NEW_SLICE, 1)
    print('OK: removed client-side slice, server controls page size')
else:
    errors.append('FAIL: b.slice not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
