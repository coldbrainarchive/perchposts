#!/usr/bin/env python3
"""Patch v617 -> v618:
Feed postcards: video attachments now show thumbnail preview like images do.
- Pr component: add isVideo prop, render play-button overlay on thumbnail
- Pr image section: jsx -> jsxs to hold both img + optional play overlay
- Feed postcard call site: route video through Pr (only links use Fr),
  pass poster as image, pass isVideo flag
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v617.js'
dst = '_deploy/assets/index-DUcNPOLc-v618.js'

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

# ── 1. Pr signature: add isVideo prop ──
patch(
    'function Pr({postId:e,title:t,text:n,image:r,isHuddle:_ih,huddle_members:_prHm=null})',
    'function Pr({postId:e,title:t,text:n,image:r,isHuddle:_ih,huddle_members:_prHm=null,isVideo:_ivid=!1})',
    'Pr add isVideo prop'
)

# ── 2. Pr image section: add play icon overlay when isVideo ──
# Need unique context - use the second occurrence (the one in our Pr, not React internals)
old_img = 'r&&(0,L.jsx)(`div`,{style:{width:100,flexShrink:0,position:`relative`,overflow:`hidden`},children:(0,L.jsx)(`img`,{src:r,alt:``,style:{position:`absolute`,inset:0,width:`100%`,height:`100%`,objectFit:`cover`},onError:e=>{e.target.parentElement.style.display=`none`}})})'
new_img = 'r&&(0,L.jsxs)(`div`,{style:{width:100,flexShrink:0,position:`relative`,overflow:`hidden`},children:[(0,L.jsx)(`img`,{src:r,alt:``,style:{position:`absolute`,inset:0,width:`100%`,height:`100%`,objectFit:`cover`},onError:e=>{e.target.parentElement.style.display=`none`}}),_ivid&&(0,L.jsx)(`div`,{style:{position:`absolute`,inset:0,display:`flex`,alignItems:`center`,justifyContent:`center`,background:`rgba(0,0,0,0.35)`},children:(0,L.jsx)(`svg`,{width:22,height:22,viewBox:`0 0 16 16`,fill:`white`,children:(0,L.jsx)(`polygon`,{points:`4,2 14,8 4,14`})})})]})'

# There are 2 matches — use surrounding unique context to patch only Pr's
patch(
    'View Huddle →`:`View Post →`})]}),r&&(0,L.jsx)(`div`,{style:{width:100,flexShrink:0,position:`relative`,overflow:`hidden`},children:(0,L.jsx)(`img`,{src:r,alt:``,style:{position:`absolute`,inset:0,width:`100%`,height:`100%`,objectFit:`cover`},onError:e=>{e.target.parentElement.style.display=`none`}})})',
    'View Huddle →`:`View Post →`})]}),r&&(0,L.jsxs)(`div`,{style:{width:100,flexShrink:0,position:`relative`,overflow:`hidden`},children:[(0,L.jsx)(`img`,{src:r,alt:``,style:{position:`absolute`,inset:0,width:`100%`,height:`100%`,objectFit:`cover`},onError:e=>{e.target.parentElement.style.display=`none`}}),_ivid&&(0,L.jsx)(`div`,{style:{position:`absolute`,inset:0,display:`flex`,alignItems:`center`,justifyContent:`center`,background:`rgba(0,0,0,0.35)`},children:(0,L.jsx)(`svg`,{width:22,height:22,viewBox:`0 0 16 16`,fill:`white`,children:(0,L.jsx)(`polygon`,{points:`4,2 14,8 4,14`})})})]})',
    'Pr image section play overlay'
)

# ── 3. Call site: videos → Pr with poster, only links → Fr ──
patch(
    'p&&p.type!==`image`?(0,L.jsxs)(L.Fragment,{children:[e.title&&(0,L.jsx)(I,{to:`/post/${e.id}`,style:{textDecoration:`none`,display:`block`,marginTop:10,marginBottom:8,color:`#f1f5f9`,fontWeight:700,fontSize:16,lineHeight:1.35,textAlign:`left`},children:e.title}),(0,L.jsx)(Fr,{attachment:p,postId:e.id})]}):(0,L.jsx)(Pr,{postId:e.id,title:e.title||null,text:f||null,image:p?.type===`image`?p.url:null,isHuddle:!!(e.is_huddle||e.community_id===`feedback`),huddle_members:_fHm})',
    'p&&p.type===`link`?(0,L.jsxs)(L.Fragment,{children:[e.title&&(0,L.jsx)(I,{to:`/post/${e.id}`,style:{textDecoration:`none`,display:`block`,marginTop:10,marginBottom:8,color:`#f1f5f9`,fontWeight:700,fontSize:16,lineHeight:1.35,textAlign:`left`},children:e.title}),(0,L.jsx)(Fr,{attachment:p,postId:e.id})]}):(0,L.jsx)(Pr,{postId:e.id,title:e.title||null,text:f||null,image:p?.type===`image`?p.url:p?.type===`video`?p.poster||null:null,isHuddle:!!(e.is_huddle||e.community_id===`feedback`),huddle_members:_fHm,isVideo:p?.type===`video`})',
    'route videos through Pr with poster thumbnail'
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
