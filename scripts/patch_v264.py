#!/usr/bin/env python3
"""Patch v263 -> v264: DM messages exactly match Rr — admin bird/colour, emoji input, reaction pills."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v263.js'
dst = '_deploy/assets/index-DUcNPOLc-v264.js'

content = open(src, encoding='utf-8').read()

CONTAINER_START = '(0,L.jsx)(`div`,{className:`comments-list`,style:{overflowY:`auto`,flex:1,padding:`8px 0`},'
END_MARKER = '_dmReplyTo&&(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:8,padding:`6px 14px 0`'

idx = content.find(CONTAINER_START)
end = content.find(END_MARKER, idx)

if idx == -1 or end == -1:
    print('FAIL: bounds not found')
    sys.exit(1)

old_section = content[idx:end]
print(f'OLD: parens={old_section.count("(")-old_section.count(")")}, braces={old_section.count("{")-old_section.count("}")}')

SEND_REFRESH = (
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);'
)

NEW_BLOCK = (
    '(0,L.jsx)(`div`,{className:`comments-list`,style:{overflowY:`auto`,flex:1,padding:`8px 0`},'
    'children:_dmMsgs.length===0?(0,L.jsx)(`div`,{style:{padding:32,color:`#64748b`,'
    'textAlign:`center`,fontSize:13},children:`No messages yet`}):'
    '_dmMsgs.map((_msg,_mi)=>{'
    'const _mine=_msg.from_username===(Qn()?.username||``);'
    # Reactions grouped like Rr: {emoji: [usernames]}
    'const _rxMap=(_msg.reactions||[]).reduce((_a,_r)=>{'
    '_a[_r.emoji]=(_a[_r.emoji]||[]);_a[_r.emoji].push(_r.from_username);return _a;'
    '},{});'
    'const _rxEntries=Object.entries(_rxMap);'
    'const _mbd=Jn({username:_msg.from_username,browser_id:null,is_admin:!!_msg.is_admin,is_mod:!!_msg.is_mod});'
    'const _mclr=_msg.is_admin?`#ffffff`:Hn(null,_msg.from_username);'
    'const _showActions=_dmPickerId===_msg.id;'
    'const _myUser=Qn()?.username||``;'
    'return(0,L.jsxs)(`div`,{'
    'className:`chat-msg${_mine?` chat-msg--mine`:``}`,'
    '"data-comment-id":_msg.id,'
    'children:[(0,L.jsxs)(`div`,{className:`chat-msg-body`,'
    'children:['
    # Meta header — exact Rr pattern with admin check
    '(0,L.jsxs)(`div`,{className:`chat-msg-meta`,style:{background:_mclr},'
    'children:['
    '_mbd&&_mbd.hat?'
    '(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,'
    'style:{height:`17px`,width:`auto`,flexShrink:0,display:`block`}}):'
    '(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,'
    'fontSize:17,lineHeight:1,flexShrink:0},'
    'children:[(0,L.jsx)(`span`,{style:{filter:_mbd&&_mbd.f?_mbd.f:``,display:`block`},'
    'children:_mbd&&_mbd.e?_mbd.e:`\U0001f424`}),...(_mbd&&_mbd.s?_spEls(_mbd.s,17):[])]}),'
    '(0,L.jsx)(`span`,{style:{fontWeight:700,fontSize:11,color:`#0a0a0a`,flex:1,'
    'minWidth:0,whiteSpace:`nowrap`,overflow:`hidden`,textOverflow:`ellipsis`},'
    'children:_msg.from_username}),'
    '(0,L.jsxs)(`span`,{style:{fontSize:11,color:`rgba(0,0,0,0.45)`,fontWeight:400,'
    'flexShrink:0,whiteSpace:`nowrap`},children:[`· `,Un(_msg.created_at)]})]}),'
    # Reply-to quote (like Rr parent comment display)
    '_msg.reply_to&&(0,L.jsxs)(`div`,{style:{background:`rgba(148,163,184,0.08)`,'
    'borderLeft:`2px solid rgba(148,163,184,0.4)`,padding:`4px 10px`,'
    'fontSize:11,color:`#64748b`,display:`flex`,gap:4,alignItems:`center`,'
    'overflow:`hidden`},'
    'children:[(0,L.jsx)(`span`,{style:{fontWeight:700,flexShrink:0},'
    'children:_msg.reply_to.from_username}),'
    '(0,L.jsx)(`span`,{style:{overflow:`hidden`,textOverflow:`ellipsis`,whiteSpace:`nowrap`},'
    'children:_msg.reply_to.content})]}),'
    # Bubble — click toggles action sheet (exact Rr pattern)
    '(0,L.jsx)(`div`,{className:`chat-bubble`,'
    'onClick:()=>_setDmPickerId(_showActions?null:_msg.id),'
    'children:_msg.content}),'
    # Reactions (exact Rr pill style with mine class + count)
    '_rxEntries.length>0&&(0,L.jsx)(`div`,{className:`chat-reactions`,'
    'children:_rxEntries.map(([_em,_us])=>'
    '(0,L.jsxs)(`button`,{type:`button`,'
    'className:`chat-reaction-pill${_us.includes(_myUser)?` mine`:``}`,'
    'onClick:async()=>{'
    'await fetch(`${R}/dm-react`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({message_id:_msg.id,emoji:_em})});'
    + SEND_REFRESH +
    '},children:[_em,(0,L.jsx)(`span`,{className:`chat-reaction-count`,children:_us.length})]},_em)'
    ')}),'
    # Action sheet (exact Rr layout: Reply, React, emoji input)
    '_showActions&&(0,L.jsxs)(`div`,{className:`chat-action-sheet`,'
    'children:['
    '(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:()=>{_setDmReplyTo(_msg);_setDmPickerId(null);},'
    'children:`Reply`}),'
    '(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,'
    'onClick:()=>{'
    'let _inp=document.getElementById(`dm-emoji-${_msg.id}`);'
    'if(_inp){_inp.value=``;_inp.style.display=_inp.style.display===`none`?``:``; _inp.focus();}'
    '},children:`React`}),'
    '(0,L.jsx)(`input`,{id:`dm-emoji-${_msg.id}`,'
    'className:`chat-emoji-picker-input`,type:`text`,inputMode:`emoji`,'
    'placeholder:`Pick an emoji...`,'
    'onChange:async _ev=>{'
    'const _ch=[..._ev.target.value].find(_c=>/\\p{Emoji}/u.test(_c)&&_c!==`‍`);'
    'if(!_ch)return;'
    '_ev.target.value=``;'
    'await fetch(`${R}/dm-react`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({message_id:_msg.id,emoji:_ch})});'
    + SEND_REFRESH +
    '_setDmPickerId(null);}})]})'
    ']})]}},_mi);'
    '})'
    '}),\n'
)

new_section = NEW_BLOCK
print(f'NEW: parens={new_section.count("(")-new_section.count(")")}, braces={new_section.count("{")-new_section.count("}")}')

content = content[:idx] + new_section + content[end:]

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'File: parens={p_diff}, braces={b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
