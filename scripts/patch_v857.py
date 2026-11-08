#!/usr/bin/env python3
"""Patch v856 -> v857: posts open in the same tab, and Back returns to the same spot in the feed.
The feed saves what it had loaded against its history entry when you leave. Going Back lands on that entry and
restores it. The logo makes a new entry, so it gets a fresh feed at the top. The saved copy could show stale
numbers for the post you just visited, so the post page notes its chirp count and the feed refetches its flaps.
Links out to articles still open a new tab, and cmd or ctrl click still opens a post in one.
"""
import re, sys

src = '_deploy/assets/index-DUcNPOLc-v856.js'
dst = '_deploy/assets/index-DUcNPOLc-v857.js'

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

# same tab
content, n = re.subn(r'\(I,\{to:`/post/\$\{(e\.id|e|p)\}`,target:`_blank`,rel:`noopener`,', lambda m: '(I,{to:`/post/${' + m.group(1) + '}`,', content)
print('OK: post links', n)
if n != 6:
    errors.append('FAIL (post links): found ' + str(n))
patch(t('function Ir({post:e,commentCount:t=0,score:n=0,myVote:r=0,onVote:i,showActivity:a=!1}){let[o,s]='), t('function Ir({post:e,commentCount:t=0,score:n=0,myVote:r=0,onVote:i,showActivity:a=!1}){let _nv=nt(),[o,s]='), 'card navigate')
patch(t('{window.open(`/post/${e.id}`,`_blank`);}'), t('{_ce.metaKey||_ce.ctrlKey?window.open(`/post/${e.id}`,`_blank`):_nv(`/post/${e.id}`);}'), 'card click')

# popups push their own history step and lock the page, which never mattered while posts opened in a new tab
patch(t('(0,L.jsx)(I,{to:`/post/${p}`,style:{display:`block`,textAlign:`center`,'), t('(0,L.jsx)(I,{to:`/post/${p}`,replace:!0,onClick:l,style:{display:`block`,textAlign:`center`,'), 'link popup open post')
patch(t('(0,L.jsx)(I,{to:`/post/${e}`,style:{display:`block`,textAlign:`center`,'), t('(0,L.jsx)(I,{to:`/post/${e}`,replace:!0,onClick:l,style:{display:`block`,textAlign:`center`,'), 'post popup open post')
patch(t('(0,_.useEffect)(()=>{if(!i)return;let e=()=>a(!1);return window.addEventListener(`popstate`,e)'), t('(0,_.useEffect)(()=>{if(!i)return;let e=()=>{a(!1);document.body.style.overflow=``};return window.addEventListener(`popstate`,e)'), 'back unlocks the page')
patch(t('let e=()=>{a(!1);document.body.style.overflow=``};return window.addEventListener(`popstate`,e),()=>window.removeEventListener(`popstate`,e)},[i]);'), t('let e=()=>{a(!1);document.body.style.overflow=``};return window.addEventListener(`popstate`,e),()=>{window.removeEventListener(`popstate`,e);document.body.style.overflow=``}},[i]);'), 'popup never leaves the page locked')

# saved feeds
patch(t('\nfunction _Bd(){'), t('\nconst _fsnap=new Map,_fseen=new Map;\nfunction _Bd(){'), 'stores')
patch(t('function Vr(){let[e,t]=(0,_.useState)([]),[n,r]=(0,_.useState)({}),[i,a]=(0,_.useState)({}),[o,s]=(0,_.useState)(10),[_old,_setOld]=(0,_.useState)([]),[_om,_setOm]=(0,_.useState)(void 0),[_tm,_setTm]=(0,_.useState)(null),[_ldg,_setLdg]=(0,_.useState)(!1),_hmR=(0,_.useRef)(null),'),
      t('function Vr(){let _fkR=(0,_.useRef)(null);_fkR.current=history.state?.key||_fkR.current||`first`;let _fk=_fkR.current,_sn=_fsnap.get(_fk)||null,_rsR=(0,_.useRef)(!!_sn),_sr0=(0,_.useRef)(_sn),_snapR=(0,_.useRef)(null),[e,t]=(0,_.useState)(_sn?.e||[]),[n,r]=(0,_.useState)(_sn?.n||{}),[i,a]=(0,_.useState)(_sn?.i||{}),[o,s]=(0,_.useState)(_sn?.o||10),[_old,_setOld]=(0,_.useState)(_sn?.old||[]),[_om,_setOm]=(0,_.useState)(_sn?_sn.om:void 0),[_tm,_setTm]=(0,_.useState)(_sn?.tm??null),[_ldg,_setLdg]=(0,_.useState)(!1),_hmR=(0,_.useRef)(_sn?.hm??null),'), 'restore state')
patch(t('[SR,setSR]=(0,_.useState)(null),[SRLoading,setSRLoading]=(0,_.useState)(!1),[TR,setTR]=(0,_.useState)(null),[TagR,setTagR]=(0,_.useState)(null),[_tgL,_setTgL]=(0,_.useState)(!1),[_tmL,_setTmL]=(0,_.useState)(!1),[_hL,_setHL]=(0,_.useState)(!0),c=(0,_.useRef)(null),'),
      t('[SR,setSR]=(0,_.useState)(_sn?.sr??null),[SRLoading,setSRLoading]=(0,_.useState)(!1),[TR,setTR]=(0,_.useState)(_sn?.tr??null),[TagR,setTagR]=(0,_.useState)(_sn?.tag??null),[_tgL,_setTgL]=(0,_.useState)(!1),[_tmL,_setTmL]=(0,_.useState)(!1),[_hL,_setHL]=(0,_.useState)(!_sn),c=(0,_.useRef)(null),'), 'restore results')

# scroll: the old restore only knew the home feed and ran on every visit, including the logo
patch(t('h.current=!0;let t=sessionStorage.getItem(g);t&&requestAnimationFrame(()=>requestAnimationFrame(()=>window.scrollTo(0,parseInt(t,10))))},[e]);let v='),
      t('h.current=!0},[e]);_snapR.current={k:_fk,e,n,i,o,old:_old,om:_om,tm:_tm,hm:_hmR.current,sr:SR,tr:TR,tag:TagR};(0,_.useLayoutEffect)(()=>{let _s=_sr0.current,_tm2=[];if(_s){let _go=()=>window.scrollTo(0,_s.y),_st=()=>_tm2.forEach(clearTimeout);_go();_tm2=[60,250,600].map(_x=>setTimeout(_go,_x));window.addEventListener(`touchstart`,_st,{once:!0,passive:!0});window.addEventListener(`wheel`,_st,{once:!0,passive:!0});if(_fseen.size)Dr([..._fseen.keys()]).then(_v=>a(_x=>({..._x,..._v})))}return()=>{_tm2.forEach(clearTimeout);let _c=_snapR.current;_fsnap.set(_c.k,{..._c,y:window.scrollY});if(_fsnap.size>8)_fsnap.delete(_fsnap.keys().next().value)}},[]);let v='), 'save and scroll')

for label, old in (
    ('reset', '(0,_.useEffect)(()=>{s(10);_setOld([]);_setOm(void 0);window.scrollTo(0,0)},[u,d,f,p,m,qT])'),
):
    patch(t(old), t(old.replace('()=>{s(10);', '()=>{if(_rsR.current)return;s(10);')), label)
patch(t('(0,_.useEffect)(()=>{if(!m){setSR(null);setSRLoading(!1);return}'), t('(0,_.useEffect)(()=>{if(_rsR.current)return;if(!m){setSR(null);setSRLoading(!1);return}'), 'search')
patch(t('(0,_.useEffect)(()=>{if(!qT){setTR(null);_setTmL(!1);return}'), t('(0,_.useEffect)(()=>{if(_rsR.current)return;if(!qT){setTR(null);_setTmL(!1);return}'), 'time')
patch(t('(0,_.useEffect)(()=>{if(!u&&!d&&!p&&(!f||_cs)){setTagR(null);_setTgL(!1);return}'), t('(0,_.useEffect)(()=>{if(_rsR.current)return;if(!u&&!d&&!p&&(!f||_cs)){setTagR(null);_setTgL(!1);return}'), 'filters')
patch(t('return()=>{_c=!0}},[u,d,f,p,_cs]),'), t('return()=>{_c=!0}},[u,d,f,p,_cs]),(0,_.useEffect)(()=>{_rsR.current=!1},[]),'), 'restore finished')
patch(t('let e=window.setTimeout(()=>{v().finally(()=>_setHL(!1))},0),_pv='), t('let e=window.setTimeout(()=>{_sr0.current||v().finally(()=>_setHL(!1))},0),_pv='), 'no refetch on restore')
patch('t(o),a(x=>({...x,..._vv}))},[]);(0,_.useEffect)(()=>{let e=window.setTimeout(()=>{_sr0', 't(o),a(x=>({...x,..._vv}));_fseen.clear()},[]);(0,_.useEffect)(()=>{let e=window.setTimeout(()=>{_sr0', 'fresh data clears notes')

# fresh numbers for the post you just left
patch(t('(0,L.jsx)(Ir,{post:e,commentCount:e.comment_count??n[e.id]??0,'), t('(0,L.jsx)(Ir,{post:e,commentCount:_fseen.get(e.id)??e.comment_count??n[e.id]??0,'), 'chirp count on card')
patch(t('if(_fr0!==void 0)_fr.current=_fr0;_hmR.current=!!_hm0;_setTot(_tt??null);'), t('if(_fr0!==void 0)_fr.current=_fr0;_hmR.current=!!_hm0;_setTot(_tt??null);_tt!=null&&_fseen.set(r,_tt);'), 'note chirp count')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
