#!/usr/bin/env python3
"""Patch v161 -> v162: new panel header with rank, bird, hatch date, worm count."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v161.js'
dst = '_deploy/assets/index-DUcNPOLc-v162.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Inject RANKS constant before Kr ───────────────────────────────────────
RANKS_JS = (
    'var _RANKS=['
    '{min:-1/0,max:-1,e:`\U0001f9a6`,n:`Endangered`,d:`At this rate, extinction isn’t far off.`},'
    '{min:0,max:9,e:`\U0001f424`,n:`Hatchling`,d:`Fresh out of the egg. Everything is new, and worms are still a mystery.`},'
    '{min:10,max:24,e:`\U0001f423`,n:`Nestling`,d:`Safe in the nest, chirping loudly and getting the hang of things.`},'
    '{min:25,max:49,e:`\U0001f425`,n:`Fledgling`,d:`Wings are working (mostly). Small hops, big ambitions.`},'
    '{min:50,max:99,e:`\U0001f426`,n:`Forager`,d:`Starting to find worms on your own with mixed success.`},'
    '{min:100,max:199,e:`\U0001f985`,n:`Bird of Prey`,d:`Highly skilled at hunting and locating food. Sharp instincts and precise execution.`},'
    '{min:200,max:299,e:`\U0001f54a️`,n:`Mixed-Flock Attendant`,d:`Moves between groups effortlessly, thriving in shared ecosystems and cooperative flocks.`},'
    '{min:300,max:499,e:`\U0001f9a2`,n:`Seasoned Migrant`,d:`Experienced, far-traveled, and resourceful. You adapt wherever the flock moves.`},'
    '{min:500,max:699,e:`\U0001f30d`,n:`Continental Migrant`,d:`You’ve gone beyond familiar skies. Wide-ranging, observant, and globally aware.`},'
    '{min:700,max:899,e:`\U0001f99c`,n:`Peak Plumage`,d:`Feathers flawless, presence undeniable. A standout across all flocks.`},'
    '{min:900,max:1499,e:`\U0001f9a9`,n:`Master Layer`,d:`Thriving and prolific—your legacy is well underway.`},'
    '{min:1500,max:1/0,e:`\U0001f99a`,n:`Legendary Brood`,d:`The pinnacle. Thriving, dominant, and the envy of the flock.`}'
    '];'
)
OLD_KR = 'function Kr({user:e,userRole:t'
if OLD_KR in content:
    content = content.replace(OLD_KR, RANKS_JS + OLD_KR, 1)
    print('OK: RANKS injected before Kr')
else:
    errors.append('FAIL: Kr function not found')

# ── 2. Add wormCount + hatchDate state ───────────────────────────────────────
OLD_STATE = ',[T,E]=(0,_.useState)(!1),ee=(0,_.useRef)'
NEW_STATE = ',[T,E]=(0,_.useState)(!1),[_wc,_swc]=(0,_.useState)(0),[_hd,_shd]=(0,_.useState)(null),ee=(0,_.useRef)'
if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
    print('OK: worm/hatch state added')
else:
    errors.append('FAIL: state init not found')

# ── 3. Add /user-stats fetch effect after existing last effect ────────────────
OLD_LAST_EFFECT = '},[c,e,r]);let re=async'
NEW_LAST_EFFECT = (
    '},[c,e,r]);'
    '(0,_.useEffect)(()=>{'
    '(async()=>{'
    'let t=new URLSearchParams({browser_id:k});'
    'D&&e?t.set(`mod_user_id`,e.id):r&&t.set(`username`,r);'
    'let n=await fetch(`${R}/user-stats?${t}`,{headers:er()});'
    'if(n.ok){let{joined_at:j,worm_count:w}=await n.json();'
    '_swc(w||0);'
    'if(j){let d=new Date(j),'
    'dd=String(d.getDate()).padStart(2,`0`),'
    'mm=String(d.getMonth()+1).padStart(2,`0`),'
    'yy=d.getFullYear();'
    '_shd(`${dd}-${mm}-${yy}`);}}'
    '})();'
    '},[e,r,k]);'
    'let re=async'
)
if OLD_LAST_EFFECT in content:
    content = content.replace(OLD_LAST_EFFECT, NEW_LAST_EFFECT, 1)
    print('OK: user-stats effect added')
else:
    errors.append('FAIL: last effect end not found')

# ── 4. Inject _rank/_bird calc before return ─────────────────────────────────
OLD_RETURN = 'N=M.map(e=>e.id),ae=(0,_.useRef)({startX:0,startY:0});return'
NEW_RETURN = (
    'N=M.map(e=>e.id),ae=(0,_.useRef)({startX:0,startY:0});'
    'let _rank=_RANKS.find(_r=>_wc>=_r.min&&_wc<=_r.max)||_RANKS[1];'
    'let _bird=te?Jn({username:te,browser_id:k,is_admin:t===`admin`,is_mod:t===`mod`}):null;'
    'return'
)
if OLD_RETURN in content:
    content = content.replace(OLD_RETURN, NEW_RETURN, 1)
    print('OK: _rank/_bird calc injected')
else:
    errors.append('FAIL: ae+return not found')

# ── 5. Replace header with 3-column layout ───────────────────────────────────
# Find the header div (starts with padding:e?`14px 18px`)
OLD_HEADER = (
    '(0,L.jsxs)(`div`,{style:{padding:e?`14px 18px`:`6px 18px`,'
    'borderBottom:e?`1px solid #2e303a`:`none`,'
    'display:`flex`,alignItems:`center`,justifyContent:`center`,position:`relative`},'
    'children:[e&&(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,'
    'alignItems:`center`,gap:4},children:['
    '(0,L.jsx)(Xn,{record:{is_admin:t===`admin`,is_mod:t===`mod`,username:te,browser_id:k},'
    'name:te,color:A}),'
    '(0,L.jsx)(`div`,{style:{color:`#64748b`,fontSize:12},children:ne})]}),'
    '(0,L.jsx)(`button`,{onClick:a,style:{position:`absolute`,right:12,'
    'top:e?`50%`:`8px`,transform:e?`translateY(-50%)`:`none`,'
    'width:30,height:30,borderRadius:`50%`,border:`none`,background:`#1f2937`,'
    'color:`#94a3b8`,cursor:`pointer`,fontSize:14,display:`flex`,'
    'alignItems:`center`,justifyContent:`center`},children:`✕`})]}),'
)

BTN = '{padding:`5px 12px`,borderRadius:999,border:`none`,background:`#7c3aed`,color:`#fff`,fontWeight:700,fontSize:11,cursor:`pointer`}'

NEW_HEADER = (
    '(0,L.jsxs)(`div`,{style:{padding:`16px 18px`,borderBottom:`1px solid #2e303a`,position:`relative`},children:['
    'e?(0,L.jsxs)(`div`,{style:{display:`grid`,gridTemplateColumns:`1fr auto 1fr`,gap:10,alignItems:`flex-start`},children:['
    # Left: rank
    '(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,gap:3},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:26,lineHeight:1},children:_rank.e}),'
    '(0,L.jsx)(`div`,{style:{fontWeight:700,fontSize:11,color:`#f1f5f9`,marginTop:4},children:_rank.n}),'
    '(0,L.jsx)(`div`,{style:{fontSize:10,color:`#64748b`,fontStyle:`italic`,lineHeight:1.4,marginTop:2},children:_rank.d})]}),'
    # Center: bird + username + buttons
    '(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,alignItems:`center`,gap:7},children:['
    '(0,L.jsx)(`span`,{style:{fontSize:52,lineHeight:1,filter:_bird&&_bird.f?_bird.f:``,display:`block`},children:_bird&&_bird.e?_bird.e:`\U0001f424`}),'
    '(0,L.jsx)(Xn,{record:{is_admin:t===`admin`,is_mod:t===`mod`,username:te,browser_id:k},name:te,color:A}),'
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:5,marginTop:2},children:['
    '(0,L.jsx)(`button`,{onClick:()=>{o(),a()},style:' + BTN + ',children:`Logout`}),'
    'O&&(0,L.jsx)(`button`,{onClick:()=>l(`account`),style:' + BTN + ',children:`Change password`})'
    ']})]}),'
    # Right: hatch date + worm count
    '(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,gap:10,alignItems:`flex-end`},children:['
    '(0,L.jsxs)(`div`,{style:{textAlign:`right`},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#94a3b8`},children:`\U0001f424 Hatch date`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:12,color:`#f1f5f9`,marginTop:3},children:_hd||`—`})]}),'
    '(0,L.jsxs)(`div`,{style:{textAlign:`right`},children:['
    '(0,L.jsx)(`div`,{style:{fontSize:11,fontWeight:700,color:`#94a3b8`},children:`\U0001fab1 Worm Count`}),'
    '(0,L.jsx)(`div`,{style:{fontSize:20,fontWeight:700,color:`#f1f5f9`,marginTop:3},children:_wc})]})]})]}):'
    'null,'
    '(0,L.jsx)(`button`,{onClick:a,style:{position:`absolute`,right:12,top:12,width:30,height:30,borderRadius:`50%`,border:`none`,background:`#1f2937`,color:`#94a3b8`,cursor:`pointer`,fontSize:14,display:`flex`,alignItems:`center`,justifyContent:`center`},children:`✕`})]}),'
)

if OLD_HEADER in content:
    content = content.replace(OLD_HEADER, NEW_HEADER, 1)
    print('OK: header replaced with 3-column layout')
else:
    errors.append('FAIL: old header not found')
    # Debug
    probe = '(0,L.jsxs)(`div`,{style:{padding:e?`14px 18px`:`6px 18px`'
    idx = content.find(probe)
    print(f'  probe at {idx}:', repr(content[idx:idx+100]) if idx >= 0 else 'not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
