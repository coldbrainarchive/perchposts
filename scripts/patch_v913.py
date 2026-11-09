#!/usr/bin/env python3
"""Patch v912 -> v913: one standard size for the big action buttons, and the profile card lines up with posts.
- Buttons in the link preview sheet (Open Link / Open Post), the bird sheets (Huddle / See Posts), the
  profile card (Huddle), Your Nest (Change password, Leave, Open Mod Panel) and Login: 10px padding, 14px
  text (~37px tall, was ~46px with 15px text), 12px corners. Main action = solid purple; second action =
  purple outline (Open Post was grey). Pairs sit side by side in one row.
- The profile card at the top of a bird's feed (?user=) is as wide as the post cards, with their 18px
  corners (it was inset 14px more with 14px corners). The same card inside the bird sheets is unchanged.
"""
import re, sys
src = '_deploy/assets/index-DUcNPOLc-v912.js'
dst = '_deploy/assets/index-DUcNPOLc-v913.js'
content = open(src, encoding='utf-8').read()
errors = []
def patch(old, new, label, count=1):
    global content
    n = content.count(old)
    if n != count: errors.append(f'FAIL ({label}): found {n}, expected {count}')
    else: content = content.replace(old, new); print('OK: ' + label)

# 1. the 13px / 15px buttons -> standard
content, n = re.subn(r'padding:`13px`,borderRadius:12,([^{}]*?)fontSize:15', r'padding:`10px 12px`,borderRadius:12,lineHeight:`18px`,\1fontSize:14', content)
print('standard size (13px buttons):', n); 
if n != 8: errors.append(f'FAIL (13px buttons): {n}, expected 8')
# 2. login button
patch('padding:`14px 18px`,borderRadius:14,border:`none`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:15,cursor:`pointer`,boxShadow:`0 14px 30px rgba(192, 132, 252, 0.28)`',
      'padding:`10px 18px`,borderRadius:12,lineHeight:`18px`,border:`none`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:14,cursor:`pointer`', 'login button')
# 3. nest buttons 12px -> 10px
content, n = re.subn(r'padding:`12px 0`,borderRadius:12,', 'padding:`10px 0`,borderRadius:12,lineHeight:`18px`,', content)
print('nest buttons:', n)
if n < 5: errors.append(f'FAIL (nest buttons): {n}')
# 4. Open Post: grey -> purple outline
patch('to:`/post/${p}`,replace:!0,onClick:l,style:{display:`block`,textAlign:`center`,padding:`10px 12px`,borderRadius:12,lineHeight:`18px`,background:`#20262f`,color:`#dbe4ee`,',
      'to:`/post/${p}`,replace:!0,onClick:l,style:{display:`block`,flex:1,textAlign:`center`,padding:`10px 12px`,borderRadius:12,lineHeight:`18px`,background:`#1e293b`,color:`#c084fc`,border:`1.5px solid #c084fc`,', 'Open Post outline')
# 5. pairs side by side
patch('(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,gap:10},children:[(0,L.jsx)(`a`,{href:e,target:`_blank`,rel:`noopener noreferrer`,style:{display:`block`,',
      '(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`row`,gap:8},children:[(0,L.jsx)(`a`,{href:e,target:`_blank`,rel:`noopener noreferrer`,style:{display:`block`,flex:1,', 'Open Link | Open Post row')
patch('style:{padding:`0 16px`,marginTop:8,display:`flex`,flexDirection:`column`,gap:8}', 'style:{padding:`0 16px`,marginTop:8,display:`flex`,flexDirection:`row`,gap:8}', 'Huddle | See Posts rows', 2)
patch('href:`/new?huddle=1&invite=${encodeURIComponent(_gpBird)}`,style:{display:`block`,', 'href:`/new?huddle=1&invite=${encodeURIComponent(_gpBird)}`,style:{display:`block`,flex:1,', 'gp Huddle flex')
patch('onClick:()=>_setGpBird(null),style:{display:`block`,', 'onClick:()=>_setGpBird(null),style:{display:`block`,flex:1,', 'gp See Posts flex')
# 6. profile card in the feed lines up with post cards
patch('return(0,L.jsxs)(`div`,{style:{padding:`10px 14px`,maxWidth:480,margin:`0 auto`},children:[(0,L.jsxs)(`div`,{style:{background:`#161920`,borderRadius:14,',
      'return(0,L.jsxs)(`div`,{style:_om?{padding:`10px 0 16px`}:{padding:`10px 14px`,maxWidth:480,margin:`0 auto`},children:[(0,L.jsxs)(`div`,{style:{background:`#161920`,borderRadius:_om?18:14,', 'profile card width')
# solid buttons get a same-colour border so their text lines up with the outline ones
content, n = re.subn(r'lineHeight:`18px`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:14,textDecoration:`none`}', 'lineHeight:`18px`,background:`#c084fc`,color:`#14081d`,fontWeight:700,fontSize:14,textDecoration:`none`,border:`1.5px solid #c084fc`}', content)
print('solid borders:', n)
if n != 4: errors.append(f'FAIL (solid borders): {n}')
# profile card Huddle button sits inside the card
patch('style:{width:`100%`,marginTop:8,padding:`10px 12px`,borderRadius:12,lineHeight:`18px`,', 'style:{width:`calc(100% - 24px)`,margin:`4px 12px 12px`,padding:`10px 12px`,borderRadius:12,lineHeight:`18px`,', 'profile Huddle inset')
if errors: print('\n'.join(errors)); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
