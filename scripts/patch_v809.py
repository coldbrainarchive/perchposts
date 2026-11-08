#!/usr/bin/env python3
"""Patch v808 -> v809:
A small flapping bird while the feed, a post or notifications are loading.

It fades in only after 0.4s, so fast loads never show it. The feed had no real loading flag for filtered
views (TagR is null both while loading and after a failed load), so this adds _tgL, _tmL and _hL, and
each one is cleared on failure too, otherwise the bird would flap forever. The 30s refresh doesn't set
them, so the bird never appears on a background refresh.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v808.js'
dst = '_deploy/assets/index-DUcNPOLc-v809.js'

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

BIRD = (
    '<style>'
    '.bird-load{display:flex;justify-content:center;padding:48px 20px;opacity:0;animation:bird-in .25s ease-out .4s forwards}'
    '.bird-load svg{width:60px;height:45px;overflow:visible;animation:bird-bob .9s ease-in-out infinite alternate}'
    '.bird-wing{transform-origin:33px 26px;animation:bird-flap .3s ease-in-out infinite alternate}'
    '@keyframes bird-in{to{opacity:1}}'
    '@keyframes bird-bob{to{transform:translateY(-6px)}}'
    '@keyframes bird-flap{to{transform:scaleY(-.6)}}'
    '@media(prefers-reduced-motion:reduce){.bird-load svg,.bird-wing{animation:none}}'
    '</style>'
    '<svg viewBox="0 0 64 48" aria-hidden="true">'
    '<path fill="#c084fc" d="M18 25 4 21l4 8-3 7 14-4z"/>'
    '<ellipse fill="#c084fc" cx="30" cy="29" rx="15" ry="10"/>'
    '<circle fill="#c084fc" cx="44" cy="23" r="7.5"/>'
    '<path fill="#fbbf24" d="m51 20 7 3-7 3z"/>'
    '<circle fill="#14161c" cx="46" cy="21.5" r="1.4"/>'
    '<path class="bird-wing" fill="#9d5fe0" d="M36 26C32 12 23 6 13 5c2 11 7 20 15 24z"/>'
    '</svg>'
)
assert '`' not in BIRD and '${' not in BIRD

patch(t('\nfunction Vr(){let[e,t]='),
      t('\nfunction _Bd(){return(0,L.jsx)(`div`,{className:`bird-load-wrap`,role:`status`,"aria-label":`Loading`,dangerouslySetInnerHTML:{__html:`<div class="bird-load">' + BIRD + '</div>`}})}\nfunction Vr(){let[e,t]='),
      'bird component')

patch(t('[TagR,setTagR]=(0,_.useState)(null),c=(0,_.useRef)(null),'),
      t('[TagR,setTagR]=(0,_.useState)(null),[_tgL,_setTgL]=(0,_.useState)(!1),[_tmL,_setTmL]=(0,_.useState)(!1),[_hL,_setHL]=(0,_.useState)(!0),c=(0,_.useRef)(null),'),
      'loading flags')

# Home feed: first load only, the 30s refresh calls v() from _pv
patch(t('let e=window.setTimeout(()=>{v()},0),_pv='),
      t('let e=window.setTimeout(()=>{v().finally(()=>_setHL(!1))},0),_pv='),
      'home flag')

# Board, country, continent and user views
patch(t('if(!u&&!d&&!p&&(!f||_cs)){setTagR(null);return}setTagR(null);_setTm(null);let _c=!1,'),
      t('if(!u&&!d&&!p&&(!f||_cs)){setTagR(null);_setTgL(!1);return}setTagR(null);_setTm(null);_setTgL(!0);let _c=!1,'),
      'tag flag on')
patch(t('if(_c)return;_setTm(d2.next_before??null);setTagR(Sr(d2.posts||[]))}).catch(()=>{_c||setTagR(null)});return()=>{_c=!0}}'),
      t('if(_c)return;_setTm(d2.next_before??null);setTagR(Sr(d2.posts||[]));_setTgL(!1)}).catch(()=>{if(!_c){setTagR(null);_setTgL(!1)}});return()=>{_c=!0}}'),
      'tag flag off')

# Time searches
patch(t('if(!qT){setTR(null);return}let since,until;'),
      t('if(!qT){setTR(null);_setTmL(!1);return}let since,until;'),
      'time flag clear')
patch(t('else{setTR(null);return}let turl='),
      t('else{setTR(null);_setTmL(!1);return}_setTmL(!0);let turl='),
      'time flag on')
patch(t('(!e2.pinned||e2.pinned_global)})))}).catch(()=>setTR(null))},[qT])'),
      t('(!e2.pinned||e2.pinned_global)})));_setTmL(!1)}).catch(()=>{setTR(null);_setTmL(!1)})},[qT])'),
      'time flag off')

# Feed: after whatever posts are already showing, so an empty list shows it at the top
patch(t('voteCount:n.voteCount??t[e]?.voteCount??0}}))}:void 0},e.id)),m&&!SRLoading&&SR!==null&&b.length===0&&'),
      t('voteCount:n.voteCount??t[e]?.voteCount??0}}))}:void 0},e.id)),(m?SRLoading:qT?_tmL:(u||d||f||p)?_tgL:_hL)&&(0,L.jsx)(_Bd,{}),m&&!SRLoading&&SR!==null&&b.length===0&&'),
      'bird in feed')

patch(t('if(!c)return(0,L.jsx)(`div`,{children:`Loading...`});'),
      t('if(!c)return(0,L.jsx)(_Bd,{});'),
      'bird on post page')
patch(t('g?(0,L.jsx)(`div`,{style:{padding:32,color:`#64748b`,textAlign:`center`,fontSize:14},children:`Loading…`}):j.length===0'),
      t('g?(0,L.jsx)(_Bd,{}):j.length===0'),
      'bird in notifications')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
