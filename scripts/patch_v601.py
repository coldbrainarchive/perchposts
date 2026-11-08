#!/usr/bin/env python3
"""Patch v600 -> v601: Auto link preview in comment compose.
- Detects URLs as user types (800ms debounce)
- Fetches metadata from microlink.io
- Shows LinkPreviewCard (Fr type=link) above compose bubble with X to dismiss
- On send, encodes link as attachment using ATTACH_MARKER (same as posts)
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v600.js'
dst = '_deploy/assets/index-DUcNPOLc-v601.js'

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

# ── 1. Add link preview state + refs ──
patch(
    ',[_cA,_setCA]=(0,_.useState)(null),[_cUL,_setCUL]=(0,_.useState)(!1),_cMR=(0,_.useRef)(null)',
    ',[_cA,_setCA]=(0,_.useState)(null),[_cUL,_setCUL]=(0,_.useState)(!1),_cMR=(0,_.useRef)(null),[_lpAt,_setLpAt]=(0,_.useState)(null),[_lpLoading,_setLpLoading]=(0,_.useState)(!1),_lpTimer=(0,_.useRef)(null),_lpUrl=(0,_.useRef)(null)',
    'add link preview state + refs'
)

# ── 2. Textarea onChange: detect URL and fetch preview ──
patch(
    'onChange:e=>p(e.target.value),placeholder:e?`Message...`:`Sign in to comment`',
    'onChange:_te=>{const _tv=_te.target.value;p(_tv);const _um=_tv.match(/https?:\\/\\/[^\\s]+/);const _tu=_um?_um[0]:null;if(!_tu){if(_lpUrl.current){_setLpAt(null);_lpUrl.current=null;}return;}if(_tu===_lpUrl.current)return;if(_lpTimer.current)clearTimeout(_lpTimer.current);_lpTimer.current=setTimeout(async()=>{_lpUrl.current=_tu;_setLpLoading(!0);try{const _lr=await fetch(`https://api.microlink.io/?url=${encodeURIComponent(_tu)}`);const _ld=await _lr.json();const _ldd=_ld.data||{};_setLpAt({type:`link`,url:_ldd.url||_tu,title:_ldd.title,description:_ldd.description,image:_ldd.image?.url});}catch{_setLpAt({type:`link`,url:_tu});}finally{_setLpLoading(!1);}},800);},placeholder:e?(_lpLoading?`Loading preview…`:`Message...`):`Sign in to comment`',
    'textarea onChange detects URL and fetches preview'
)

# ── 3. onKeyDown: use link preview as attachment if no media attachment ──
patch(
    'let t=f,_ca=_cA,n=S?.id||null;p(``),C(null),_setCA(null),O.current=!0,F(t,n,_ca)',
    'let t=f,_ca=_cA||_lpAt,n=S?.id||null;p(``),C(null),_setCA(null),_setLpAt(null),_lpUrl.current=null,O.current=!0,F(t,n,_ca)',
    'onKeyDown uses link preview as attachment'
)

# ── 4. onClick: same ──
patch(
    'let _txt=f,_ca2=_cA,t=S?.id||null;p(``),C(null),_setCA(null),O.current=!0,F(_txt,t,_ca2)',
    'let _txt=f,_ca2=_cA||_lpAt,t=S?.id||null;p(``),C(null),_setCA(null),_setLpAt(null),_lpUrl.current=null,O.current=!0,F(_txt,t,_ca2)',
    'onClick uses link preview as attachment'
)

# ── 5. Show link preview above compose + loading indicator ──
# Insert after the media attachment preview block
patch(
    '_cA&&(0,L.jsx)(`div`,{style:{padding:`6px 12px 0`},children:',
    '(_lpLoading&&!_cA)&&(0,L.jsx)(`div`,{style:{padding:`6px 12px 0`,fontSize:11,color:`#8fa0b6`},children:`Loading preview…`}),(_lpAt&&!_cA)&&(0,L.jsxs)(`div`,{style:{padding:`6px 12px 0`,position:`relative`},children:[(0,L.jsx)(Fr,{attachment:_lpAt}),(0,L.jsx)(`button`,{type:`button`,onClick:()=>{_setLpAt(null);_lpUrl.current=null;},style:{position:`absolute`,top:8,right:8,background:`rgba(0,0,0,0.6)`,border:`none`,color:`#fff`,borderRadius:999,width:20,height:20,cursor:`pointer`,fontSize:11,display:`flex`,alignItems:`center`,justifyContent:`center`},children:`✕`})]}),_cA&&(0,L.jsx)(`div`,{style:{padding:`6px 12px 0`},children:',
    'show link preview and loading state above compose'
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
