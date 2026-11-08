#!/usr/bin/env python3
"""Patch v422 -> v423:
Huddle postcard + post page: replace "Huddle with: name, name" text
with actual user pill tags, excluding the OP (shown at top as poster).
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v422.js'
dst = '_deploy/assets/index-DUcNPOLc-v423.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Feed: also capture parsed _fHm while computing f ──────────────────────
OLD_F = 'const f=(e.is_huddle||e.community_id===`feedback`)?(()=>{try{const _hm=JSON.parse(e.huddle_members||`[]`);return`Huddle with: ${[e.username,..._hm].filter(Boolean).join(`, `)}`;}catch(_){return _rawF;}})():_rawF'
NEW_F = 'let _fHm=null;const f=(e.is_huddle||e.community_id===`feedback`)?(()=>{try{const _hm=JSON.parse(e.huddle_members||`[]`);_fHm=_hm.filter(Boolean);return`Huddle with: ${_fHm.join(`, `)}`;}catch(_){return _rawF;}})():_rawF'
if OLD_F in content:
    content = content.replace(OLD_F, NEW_F, 1)
    print('OK: feed extracts _fHm (members excluding OP)')
else:
    errors.append('FAIL: feed f computation not found')

# ── 2. Feed: pass huddle_members to Pr ────────────────────────────────────────
OLD_PR_CALL = 'text:f||null,image:p?.type===`image`?p.url:null,isHuddle:!!(e.is_huddle||e.community_id===`feedback`)})'
NEW_PR_CALL = 'text:f||null,image:p?.type===`image`?p.url:null,isHuddle:!!(e.is_huddle||e.community_id===`feedback`),huddle_members:_fHm})'
if OLD_PR_CALL in content:
    content = content.replace(OLD_PR_CALL, NEW_PR_CALL, 1)
    print('OK: Pr call passes huddle_members')
else:
    errors.append('FAIL: Pr call site not found')

# ── 3. Pr: accept huddle_members prop ─────────────────────────────────────────
OLD_PR_SIG = 'function Pr({postId:e,title:t,text:n,image:r,isHuddle:_ih})'
NEW_PR_SIG = 'function Pr({postId:e,title:t,text:n,image:r,isHuddle:_ih,huddle_members:_prHm=null})'
if OLD_PR_SIG in content:
    content = content.replace(OLD_PR_SIG, NEW_PR_SIG, 1)
    print('OK: Pr accepts huddle_members prop')
else:
    errors.append('FAIL: Pr signature not found')

# ── 4. Pr: render pills instead of text for huddle postcards ──────────────────
OLD_PR_TEXT = 's&&(0,L.jsx)(`div`,{style:{color:`#64748b`,fontSize:12,marginBottom:8,lineHeight:1.4},children:s})'
NEW_PR_TEXT = (
    '_ih&&_prHm&&_prHm.length>0'
    '?(0,L.jsxs)(`div`,{style:{marginBottom:8},children:['
        '(0,L.jsx)(`div`,{style:{color:`#64748b`,fontSize:11,marginBottom:4},children:`Huddle with:`}),'
        '(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:4},'
            'children:_prHm.map(_u=>(0,L.jsx)(Xn,{record:{username:_u,browser_id:null},name:_u,color:Hn(null,_u)},_u))'
        '})'
    ']})'
    ':s&&(0,L.jsx)(`div`,{style:{color:`#64748b`,fontSize:12,marginBottom:8,lineHeight:1.4},children:s})'
)
if OLD_PR_TEXT in content:
    content = content.replace(OLD_PR_TEXT, NEW_PR_TEXT, 1)
    print('OK: Pr renders member pills for huddles')
else:
    errors.append('FAIL: Pr text render not found')

# ── 5. Post page: parse _hm excluding OP ─────────────────────────────────────
OLD_PP_HM = 'const _hm=JSON.parse(c.huddle_members||`[]`);return`Huddle with: ${[c.username,..._hm].filter(Boolean).join(`, `)}`'
NEW_PP_HM = 'const _hm=JSON.parse(c.huddle_members||`[]`).filter(Boolean);return _hm'
if OLD_PP_HM in content:
    content = content.replace(OLD_PP_HM, NEW_PP_HM, 1)
    print('OK: post page parses _hm excluding OP')
else:
    errors.append('FAIL: post page _hm computation not found')

# ── 6. Post page: render pills instead of <p> text for huddle ─────────────────
OLD_PP_P = 'e&&(0,L.jsx)(`p`,{style:{margin:0,color:`#d4dde7`,fontSize:14,lineHeight:1.55,whiteSpace:`pre-wrap`,overflowWrap:`anywhere`,textAlign:`left`},children:e})'
NEW_PP_P = (
    'c.is_huddle&&Array.isArray(e)&&e.length>0'
    '?(0,L.jsxs)(`div`,{style:{marginTop:c.title?0:4},children:['
        '(0,L.jsx)(`div`,{style:{color:`#94a3b8`,fontSize:12,marginBottom:6},children:`Huddle with:`}),'
        '(0,L.jsx)(`div`,{style:{display:`flex`,flexWrap:`wrap`,gap:4},'
            'children:e.map(_u=>(0,L.jsx)(Xn,{record:{username:_u,browser_id:null},name:_u,color:Hn(null,_u)},_u))'
        '})'
    ']})'
    ':!c.is_huddle&&e&&(0,L.jsx)(`p`,{style:{margin:0,color:`#d4dde7`,fontSize:14,lineHeight:1.55,whiteSpace:`pre-wrap`,overflowWrap:`anywhere`,textAlign:`left`},children:e})'
)
if OLD_PP_P in content:
    content = content.replace(OLD_PP_P, NEW_PP_P, 1)
    print('OK: post page renders member pills for huddles')
else:
    errors.append('FAIL: post page <p> render not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
