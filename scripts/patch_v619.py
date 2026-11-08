#!/usr/bin/env python3
"""Patch v618 -> v619:
Feed postcard attachment preview: tapping a photo/video post on mobile
opens a bottom-sheet preview (already built in Pr) showing the full attachment
via Fr, before navigating. Same pattern as link previews.
- Pr signature: add attachment:_att prop
- Pr card: add onClick:u that intercepts mobile tap when attachment exists
- Pr modal: replace static img with Fr(attachment) for photo/video previews
- Ir call site: pass attachment:p to Pr
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v618.js'
dst = '_deploy/assets/index-DUcNPOLc-v619.js'

content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label):
    global content
    n = content.count(old)
    if n == 0:
        errors.append(f'FAIL ({label}): not found')
    elif n > 1:
        errors.append(f'FAIL ({label}): {n} matches (not unique)')
    else:
        content = content.replace(old, new)
        print(f'OK: {label}')

# ── 1. Pr signature: add attachment prop ──
patch(
    'function Pr({postId:e,title:t,text:n,image:r,isHuddle:_ih,huddle_members:_prHm=null,isVideo:_ivid=!1})',
    'function Pr({postId:e,title:t,text:n,image:r,isHuddle:_ih,huddle_members:_prHm=null,isVideo:_ivid=!1,attachment:_att=null})',
    'Pr add attachment prop'
)

# ── 2. Pr card: add u() intercept + onClick on I component ──
# Add u function after the l() close function, and add onClick:u to the I Link
patch(
    'function l(){o(!1)}return',
    'function l(){o(!1)}function u(e){if(i&&_att){e.preventDefault();e.stopPropagation();c();}}return',
    'Pr add u intercept function'
)

patch(
    '(0,L.jsx)(I,{to:`/post/${e}`,style:{textDecoration:`none`,display:`block`,marginTop:10},children:(0,L.jsxs)(`div`,{style',
    '(0,L.jsx)(I,{to:`/post/${e}`,style:{textDecoration:`none`,display:`block`,marginTop:10},onClick:u,children:(0,L.jsxs)(`div`,{style',
    'Pr add onClick:u to card link'
)

# ── 3. Pr modal: replace static img with Fr for attachment previews ──
patch(
    'overflowY:`auto`,padding:`0 20px 36px`},children:[r&&(0,L.jsx)(`img`,{src:r,alt:``,style:{width:`100%`,height:180,objectFit:`cover`,borderRadius:12,marginBottom:14,display:`block`},onError:e=>{e.target.style.display=`none`}}),t&&(0,L.jsx)(`div`,{style:{color:`#f1f5f9`,fontWeight:700,fontSize:17,marginBottom:8,lineHeight:1.3},children:t}),n&&(0,L.jsx)(`div`,{style:{color:`#94a3b8`,fontSize:14,marginBottom:10,lineHeight:1.55},children:n})',
    'overflowY:`auto`,padding:`0 20px 36px`},children:[_att?(0,L.jsx)(Fr,{attachment:_att}):(r&&(0,L.jsx)(`img`,{src:r,alt:``,style:{width:`100%`,height:180,objectFit:`cover`,borderRadius:12,marginBottom:14,display:`block`},onError:e=>{e.target.style.display=`none`}})),t&&(0,L.jsx)(`div`,{style:{color:`#f1f5f9`,fontWeight:700,fontSize:17,marginBottom:8,lineHeight:1.3},children:t}),n&&(0,L.jsx)(`div`,{style:{color:`#94a3b8`,fontSize:14,marginBottom:10,lineHeight:1.55},children:n})',
    'Pr modal uses Fr for attachment preview'
)

# ── 4. Ir call site: pass attachment:p to Pr ──
patch(
    'isHuddle:!!(e.is_huddle||e.community_id===`feedback`),huddle_members:_fHm,isVideo:p?.type===`video`})',
    'isHuddle:!!(e.is_huddle||e.community_id===`feedback`),huddle_members:_fHm,isVideo:p?.type===`video`,attachment:p||null})',
    'Ir passes attachment to Pr'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print(f'Paren delta: {p_delta}, Brace delta: {b_delta}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
