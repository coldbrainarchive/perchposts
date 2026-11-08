#!/usr/bin/env python3
"""Patch v261 -> v262: DM thread adopts comment card structure (chat-msg CSS classes)."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v261.js'
dst = '_deploy/assets/index-DUcNPOLc-v262.js'

content = open(src, encoding='utf-8').read()

# Replace just the messages container div (stop before reply preview)
CONTAINER_START = '(0,L.jsx)(`div`,{style:{flex:1,overflowY:`auto`,display:`flex`,flexDirection:`column`,gap:2,padding:`8px 0`},children:_dmMsgs.length===0'
END_MARKER = '_dmReplyTo&&(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:8,padding:`6px 14px 0`'

idx = content.find(CONTAINER_START)
end = content.find(END_MARKER, idx)

if idx == -1 or end == -1:
    print('FAIL: bounds not found')
    sys.exit(1)

old_section = content[idx:end]
print(f'OLD: parens={old_section.count("(")-old_section.count(")")}, braces={old_section.count("{")-old_section.count("}")}')
print('OLD end:', repr(old_section[-40:]))

SEND_REFRESH = (
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);'
)

EMOJI_BTNS = ''.join([
    f'(0,L.jsx)(`button`,{{type:`button`,className:`chat-action-btn`,'
    f'onClick:async()=>{{'
    f'await fetch(`${{R}}/dm-react`,{{method:`POST`,headers:{{"Content-Type":`application/json`,...er()}},'
    f'body:JSON.stringify({{message_id:_msg.id,emoji:`{e}`}})}});'
    f'{SEND_REFRESH}'
    f'_setDmPickerId(null);}},'
    f'children:`{e}`}}),'
    for e in ['❤️','😂','😮','😢','👍','🔥']
])

NEW_BLOCK = (
    '(0,L.jsx)(`div`,{className:`comments-list`,style:{overflowY:`auto`,flex:1,padding:`8px 0`},'
    'children:_dmMsgs.length===0?(0,L.jsx)(`div`,{style:{padding:32,color:`#64748b`,'
    'textAlign:`center`,fontSize:13},children:`No messages yet`}):'
    '_dmMsgs.map((_msg,_mi)=>{'
    'const _mine=_msg.from_username===(Qn()?.username||``);'
    'const _rxs=_msg.reactions||[];'
    'const _mbd=Jn({username:_msg.from_username,browser_id:null});'
    'const _mclr=Hn(null,_msg.from_username);'
    'const _showActions=_dmPickerId===_msg.id;'
    'return(0,L.jsxs)(`div`,{'
    'className:`chat-msg${_mine?` chat-msg--mine`:``}`,'
    '"data-comment-id":_msg.id,'
    'children:[(0,L.jsxs)(`div`,{className:`chat-msg-body`,'
    'children:['
    '(0,L.jsxs)(`div`,{className:`chat-msg-meta`,style:{background:_mclr},'
    'children:['
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,'
    'fontSize:17,lineHeight:1,flexShrink:0},'
    'children:[(0,L.jsx)(`span`,{style:{filter:_mbd&&_mbd.f?_mbd.f:``,display:`block`},'
    'children:_mbd&&_mbd.e?_mbd.e:`\U0001f424`}),...(_mbd&&_mbd.s?_spEls(_mbd.s,17):[])]}),'
    '(0,L.jsx)(`span`,{style:{fontWeight:700,fontSize:11,color:`#0a0a0a`,flex:1,'
    'minWidth:0,whiteSpace:`nowrap`,overflow:`hidden`,textOverflow:`ellipsis`},'
    'children:_msg.from_username}),'
    '(0,L.jsxs)(`span`,{style:{fontSize:11,color:`rgba(0,0,0,0.45)`,fontWeight:400,'
    'flexShrink:0,whiteSpace:`nowrap`},children:[`· `,Un(_msg.created_at)]})]}),'
    '_msg.reply_to&&(0,L.jsx)(`div`,{style:{background:`rgba(148,163,184,0.08)`,'
    'borderLeft:`2px solid rgba(148,163,184,0.4)`,padding:`4px 10px`,'
    'fontSize:11,color:`#64748b`,whiteSpace:`nowrap`,overflow:`hidden`,textOverflow:`ellipsis`},'
    'children:[_msg.reply_to.from_username,`: `,_msg.reply_to.content]}),'
    '(0,L.jsx)(`div`,{className:`chat-bubble`,'
    'onClick:()=>_setDmPickerId(_showActions?null:_msg.id),'
    'children:_msg.content}),'
    '_showActions&&(0,L.jsxs)(`div`,{className:`chat-action-sheet`,'
    'children:['
    '(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:()=>{_setDmReplyTo(_msg);_setDmPickerId(null);},children:`↩ Reply`}),'
    + EMOJI_BTNS +
    '(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:()=>_setDmPickerId(null),children:`✕`})]}),'
    '_rxs.length>0&&(0,L.jsx)(`div`,{className:`chat-reactions`,'
    'children:Object.entries(_rxs.reduce((_a,_r)=>{'
    '_a[_r.emoji]=(_a[_r.emoji]||[]);_a[_r.emoji].push(_r.from_username);return _a;'
    '},{})).map(([_em,_us])=>'
    '(0,L.jsx)(`span`,{className:`chat-reaction-pill`,'
    'children:[_em,` `,_us.length]},_em)'
    ')})]})]}},_mi);'
    '})'
    '}),'
)

new_section = NEW_BLOCK
print(f'NEW: parens={new_section.count("(")-new_section.count(")")}, braces={new_section.count("{")-new_section.count("}")}')

content = content[:idx] + new_section + content[end:]

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'File: parens={p_diff}, braces={b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
