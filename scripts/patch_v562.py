#!/usr/bin/env python3
"""Patch v559 -> v562: Comment attachments (photo/video via R2).
Patches applied to index-DUcNPOLc (the live bundle).
- Adds _cA/_setCA/_cUL/_setCUL/_cMR state to PostPage (Wr)
- Modifies F (submitComment) to accept + encode attachment via jr (ATTACH_MARKER)
- Fixes early-return guards to allow attachment-only sends
- Adds file <input>, attachment preview, 📎 button to chat-compose
- Updates ChatMessage bubble to parse (Mr) + render (Fr) attachments
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v559.js'
dst = '_deploy/assets/index-DUcNPOLc-v562.js'

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

# ── 1. Add comment attachment state + ref to PostPage state block ──
patch(
    'te=(0,_.useRef)(!!s.state?.scrollToComments);(0,_.useEffect)(()=>{window.scrollTo(0,0)},[r])',
    'te=(0,_.useRef)(!!s.state?.scrollToComments),[_cA,_setCA]=(0,_.useState)(null),[_cUL,_setCUL]=(0,_.useState)(!1),_cMR=(0,_.useRef)(null);(0,_.useEffect)(()=>{window.scrollTo(0,0)},[r])',
    'add comment attachment state + ref'
)

# ── 2. Modify F (submitComment) signature + compute _fc ──
patch(
    'let F=async(t,i=null)=>{if(!t.trim()||c?.locked||m)return;',
    'let F=async(t,i=null,_att=null)=>{if(!t.trim()&&!_att||c?.locked||m)return;let _fc=_att?t+jr+JSON.stringify(_att)+`]`:t;',
    'modify F signature'
)

# ── 3. Optimistic comment uses _fc ──
patch(
    '{id:a,content:t,created_at:new Date().toISOString(),browser_id:o,parent_comment_id:i,username:s.username,is_mod:s.is_mod,isPending:!0}',
    '{id:a,content:_fc,created_at:new Date().toISOString(),browser_id:o,parent_comment_id:i,username:s.username,is_mod:s.is_mod,isPending:!0}',
    'optimistic comment uses _fc'
)

# ── 4. Fetch body uses _fc ──
patch(
    'body:JSON.stringify({content:t,post_id:r,parent_comment_id:i,browser_id:o,...s})',
    'body:JSON.stringify({content:_fc,post_id:r,parent_comment_id:i,browser_id:o,...s})',
    'fetch body uses _fc'
)

# ── 5. onKeyDown: fix early-return guard + pass attachment ──
patch(
    'if(e.preventDefault(),!f.trim())return;let t=f,n=S?.id||null;p(``),C(null),O.current=!0,F(t,n)',
    'if(e.preventDefault(),!f.trim()&&!_cA)return;let t=f,_ca=_cA,n=S?.id||null;p(``),C(null),_setCA(null),O.current=!0,F(t,n,_ca)',
    'onKeyDown guard + attachment pass'
)

# ── 6. onClick: fix early-return guard + pass attachment ──
patch(
    'onClick:()=>{if(!e||!f.trim())return;let _txt=f,t=S?.id||null;p(``),C(null),O.current=!0,F(_txt,t)}',
    'onClick:()=>{if(!e||(!f.trim()&&!_cA))return;let _txt=f,_ca2=_cA,t=S?.id||null;p(``),C(null),_setCA(null),O.current=!0,F(_txt,t,_ca2)}',
    'onClick guard + attachment pass'
)

# ── 7. Send button disabled when no text AND no attachment ──
patch(
    'disabled:!e||m||!f.trim(),',
    'disabled:!e||m||(!f.trim()&&!_cA),',
    'send button disabled state'
)

# ── 8a. File input injected at start of chat-compose children ──
patch(
    'children:[S&&(0,L.jsxs)(`div`,{className:`chat-reply-preview`,',
    'children:[(0,L.jsx)(`input`,{ref:_cMR,type:`file`,accept:`image/*,video/*`,style:{display:`none`},onChange:_fe=>{let _ff=_fe.target.files[0];if(_ff){_setCUL(!0);let _fd=new FormData();_fd.append(`file`,_ff);fetch(`${R}/upload`,{method:`POST`,body:_fd}).then(_fr=>_fr.json()).then(_fj=>{if(!_fj.url)throw Error(_fj.error||`Upload failed`);_setCA({type:_ff.type.startsWith(`image/`)?`image`:`video`,url:_fj.url})}).catch(_fErr=>alert(`Upload failed: `+_fErr.message)).finally(()=>_setCUL(!1));}_fe.target.value=``}}),S&&(0,L.jsxs)(`div`,{className:`chat-reply-preview`,',
    'inject file input into chat-compose'
)

# ── 8b. Fix reply preview to strip attachment marker from quoted text ──
patch(
    'children:S.content})]}),(0,L.jsx)(`button`,{type:`button`,className:`chat-reply-dismiss`',
    'children:Mr(S.content).text})]}),(0,L.jsx)(`button`,{type:`button`,className:`chat-reply-dismiss`',
    'reply preview text uses Mr'
)

# ── 8c. Attachment preview injected after reply preview, before chat-input-row ──
patch(
    'children:`✕`})]}),(0,L.jsxs)(`div`,{className:`chat-input-row`,',
    'children:`✕`})]}),_cA&&(0,L.jsx)(`div`,{style:{padding:`6px 12px 0`},children:(0,L.jsxs)(`div`,{style:{position:`relative`,display:`inline-flex`},children:[_cA.type===`image`?(0,L.jsx)(`img`,{src:_cA.url,alt:``,style:{maxHeight:72,maxWidth:128,borderRadius:8,objectFit:`cover`}}):(0,L.jsx)(`video`,{src:_cA.url,style:{maxHeight:72,maxWidth:128,borderRadius:8},muted:!0}),(0,L.jsx)(`button`,{type:`button`,onClick:()=>_setCA(null),style:{position:`absolute`,top:2,right:2,background:`rgba(0,0,0,0.65)`,border:`none`,color:`#fff`,borderRadius:999,width:18,height:18,cursor:`pointer`,fontSize:10,display:`flex`,alignItems:`center`,justifyContent:`center`,padding:0},children:`✕`})]})}),(0,L.jsxs)(`div`,{className:`chat-input-row`,',
    'inject attachment preview before chat-input-row'
)

# ── 8d. Attach button at start of chat-input-row children ──
patch(
    'children:[(0,L.jsx)(`div`,{className:`chat-input-bubble`,onClick:e?void 0:',
    'children:[(0,L.jsx)(`button`,{type:`button`,onClick:()=>_cMR.current?.click(),disabled:_cUL||m,style:{flexShrink:0,background:`none`,border:`none`,color:_cA?`#c084fc`:`#8fa0b6`,fontSize:18,cursor:`pointer`,padding:`0 4px`,lineHeight:1,display:`flex`,alignItems:`center`},title:`Attach photo or video`,children:_cUL?(0,L.jsx)(`span`,{style:{fontSize:12},children:`…`}):`📎`}),(0,L.jsx)(`div`,{className:`chat-input-bubble`,onClick:e?void 0:',
    'inject attach button into chat-input-row'
)

# ── 9. ChatMessage bubble: parse content, render attachment ──
patch(
    '(0,L.jsx)(`p`,{className:`chat-quote-text`,children:w.content})]}),(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:e.content})',
    '(0,L.jsx)(`p`,{className:`chat-quote-text`,children:Mr(w.content).text})]}),(({text:_ct,attachment:_ca})=>(0,L.jsxs)(L.Fragment,{children:[_ct&&(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:_ct}),_ca&&(0,L.jsx)(`div`,{style:{marginTop:_ct?6:0},onClick:_ev=>_ev.stopPropagation(),children:(0,L.jsx)(Fr,{attachment:_ca})})]}))( Mr(e.content))',
    'ChatMessage parses + renders attachment'
)

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

p_base = open(src, encoding='utf-8').read()
p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
p_base_diff = p_base.count('(') - p_base.count(')')
b_base_diff = p_base.count('{') - p_base.count('}')
print(f'Paren delta vs base: {p_diff - p_base_diff} (base={p_base_diff}, new={p_diff})')
print(f'Brace delta vs base: {b_diff - b_base_diff} (base={b_base_diff}, new={b_diff})')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
