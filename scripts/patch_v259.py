#!/usr/bin/env python3
"""Patch v258 -> v259: DM thread — Xn header, reactions, reply-to support."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v258.js'
dst = '_deploy/assets/index-DUcNPOLc-v259.js'

content = open(src, encoding='utf-8').read()
errors = []

COMMON_EMOJIS = ['❤️','😂','😮','😢','👍','🔥']

# ── 1. Add _dmReplyTo state in Kr ────────────────────────────────────────────
OLD_DM_STATE = '[_dmSending,_setDmSending]=(0,_.useState)(!1),'
NEW_DM_STATE = '[_dmSending,_setDmSending]=(0,_.useState)(!1),[_dmReplyTo,_setDmReplyTo]=(0,_.useState)(null),'
if OLD_DM_STATE in content:
    content = content.replace(OLD_DM_STATE, NEW_DM_STATE, 1)
    print('OK: _dmReplyTo state added')
else:
    errors.append('FAIL: DM state anchor not found')

# ── 2. Replace plain username in thread header with Xn user tag ──────────────
OLD_HDR = '(0,L.jsx)(`span`,{style:{color:`#f8fafc`,fontWeight:700,fontSize:14},children:_dmThread})'
NEW_HDR = '(0,L.jsx)(Xn,{record:{username:_dmThread},name:_dmThread,color:Hn(null,_dmThread)})'
if OLD_HDR in content:
    content = content.replace(OLD_HDR, NEW_HDR, 1)
    print('OK: thread header uses Xn user tag')
else:
    errors.append('FAIL: thread header not found')

# ── 3. Replace message render with reactions + reply support ─────────────────
SEND_LOGIC = (
    '_setDmSending(!0);'
    'await fetch(`${R}/send-dm`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({to_username:_dmThread,content:_dmInput.trim()})});'
    '_setDmInput(``);'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);'
    '_setDmSending(!1);'
)
SEND_LOGIC_NEW = (
    '_setDmSending(!0);'
    'await fetch(`${R}/send-dm`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},'
    'body:JSON.stringify({to_username:_dmThread,content:_dmInput.trim(),'
    'reply_to_id:_dmReplyTo?.id||null})});'
    '_setDmInput(``);_setDmReplyTo(null);'
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);'
    '_setDmSending(!1);'
)

OLD_MSG_MAP = (
    '_dmMsgs.map((_msg,_mi)=>{'
    'const _mine=_msg.from_username===(Qn()?.username||``);'
    'return(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,'
    'alignItems:_mine?`flex-end`:`flex-start`,padding:`2px 14px`},'
    'children:['
    '(0,L.jsx)(`div`,{style:{background:_mine?`#3b1f6e`:`#1e2530`,color:`#dbe4ee`,'
    'borderRadius:14,padding:`7px 12px`,fontSize:13,maxWidth:`78%`,wordBreak:`break-word`},'
    'children:_msg.content}),'
    '(0,L.jsx)(`div`,{style:{color:`#475569`,fontSize:10,marginTop:2},'
    'children:Un(_msg.created_at)})]},_mi)})'
)

EMOJI_PICKER = (
    '(0,L.jsxs)(`div`,{style:{display:`flex`,gap:4,marginTop:4,flexDirection:_mine?`row-reverse`:`row`},'
    'children:[' +
    ','.join([
        f'(0,L.jsx)(`button`,{{onClick:async()=>{{'
        f'await fetch(`${{R}}/dm-react`,{{method:`POST`,headers:{{"Content-Type":`application/json`,...er()}},'
        f'body:JSON.stringify({{message_id:_msg.id,emoji:`{e}`}})}});'
        f'let _r=await fetch(`${{R}}/dm-thread?with=${{encodeURIComponent(_dmThread)}}`,{{headers:er()}});'
        f'_setDmMsgs((_r.ok?await _r.json():{{}}).messages||[]);'
        f'}},style:{{background:`none`,border:`none`,fontSize:14,cursor:`pointer`,padding:`1px 3px`,'
        f'borderRadius:6,opacity:0.6}},children:`{e}`}})'
        for e in COMMON_EMOJIS
    ]) +
    ']})'
)

NEW_MSG_MAP = (
    '_dmMsgs.map((_msg,_mi)=>{'
    'const _mine=_msg.from_username===(Qn()?.username||``);'
    'const _rxs=_msg.reactions||[];'
    'const [_showPicker,_setShowPicker]=(0,_.useState)(!1);'
    'return(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,'
    'alignItems:_mine?`flex-end`:`flex-start`,padding:`2px 14px`,gap:2},'
    'children:['
    # Reply-to quoted context
    '_msg.reply_to&&(0,L.jsx)(`div`,{style:{background:`#0f1117`,borderLeft:`2px solid #4b5563`,'
    'borderRadius:6,padding:`4px 8px`,fontSize:11,color:`#64748b`,'
    'maxWidth:`70%`,overflow:`hidden`,textOverflow:`ellipsis`,whiteSpace:`nowrap`,marginBottom:2},'
    'children:[_msg.reply_to.from_username,`: `,_msg.reply_to.content]}),'
    # Message bubble + reply button
    '(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:6,'
    'flexDirection:_mine?`row-reverse`:`row`},'
    'children:['
    '(0,L.jsx)(`div`,{onClick:()=>_setShowPicker(p=>!p),'
    'style:{background:_mine?`#3b1f6e`:`#1e2530`,color:`#dbe4ee`,'
    'borderRadius:14,padding:`7px 12px`,fontSize:13,maxWidth:`78%`,'
    'wordBreak:`break-word`,cursor:`pointer`},'
    'children:_msg.content}),'
    # Reply button
    '(0,L.jsx)(`button`,{onClick:()=>{_setDmReplyTo(_msg);_setShowPicker(!1);},'
    'style:{background:`none`,border:`none`,color:`#475569`,fontSize:13,'
    'cursor:`pointer`,padding:`2px 4px`,opacity:0.6,flexShrink:0},'
    'children:`↩`})]})'
    ','
    # Emoji picker (shown on tap)
    '_showPicker&&' + EMOJI_PICKER + ','
    # Reactions row
    '_rxs.length>0&&(0,L.jsxs)(`div`,{style:{display:`flex`,gap:4,flexWrap:`wrap`,'
    'flexDirection:_mine?`row-reverse`:`row`},'
    'children:Object.entries(_rxs.reduce((_a,_r)=>{'
    '_a[_r.emoji]=(_a[_r.emoji]||[]);_a[_r.emoji].push(_r.from_username);return _a;'
    '},{})).map(([_em,_us])=>'
    '(0,L.jsx)(`span`,{style:{background:`#1e2530`,borderRadius:999,'
    'padding:`2px 7px`,fontSize:12,cursor:`pointer`,border:`1px solid #2e303a`},'
    'children:[_em,` `,_us.length]},_em))'
    '}),'
    # Timestamp
    '(0,L.jsx)(`div`,{style:{color:`#475569`,fontSize:10},'
    'children:Un(_msg.created_at)})]},_mi)})'
)

if OLD_MSG_MAP in content:
    content = content.replace(OLD_MSG_MAP, NEW_MSG_MAP, 1)
    print('OK: message render updated with reactions + replies')
else:
    errors.append('FAIL: message map not found')

# ── 4. Update send logic to include reply_to_id ──────────────────────────────
if SEND_LOGIC in content:
    content = content.replace(SEND_LOGIC, SEND_LOGIC_NEW)
    print(f'OK: send logic updated with reply_to_id ({content.count(SEND_LOGIC_NEW)} occurrences)')
else:
    errors.append('FAIL: send logic not found')

# ── 5. Add reply-to preview above compose input ───────────────────────────────
OLD_COMPOSE_ROW = 'className:`chat-input-row`,style:{padding:`10px 14px`,borderTop:`1px solid #2e303a`}'
NEW_COMPOSE_ROW = (
    'className:`chat-input-row`,style:{padding:`10px 14px`,borderTop:`1px solid #2e303a`},'
    'onKeyDown:undefined'  # placeholder — actual fix below
)
# Actually insert the reply preview as a sibling before the compose row
OLD_BEFORE_COMPOSE = (
    '(0,L.jsxs)(`div`,{className:`chat-input-row`,style:{padding:`10px 14px`,borderTop:`1px solid #2e303a`},'
)
NEW_BEFORE_COMPOSE = (
    '_dmReplyTo&&(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:8,'
    'padding:`6px 14px 0`,borderTop:`1px solid #2e303a`},'
    'children:[(0,L.jsxs)(`div`,{style:{flex:1,background:`#0f1117`,borderLeft:`2px solid #c084fc`,'
    'borderRadius:6,padding:`4px 8px`,fontSize:11,color:`#94a3b8`,'
    'overflow:`hidden`,textOverflow:`ellipsis`,whiteSpace:`nowrap`},'
    'children:[`Replying to `,_dmReplyTo.from_username,`: `,_dmReplyTo.content]}),'
    '(0,L.jsx)(`button`,{onClick:()=>_setDmReplyTo(null),'
    'style:{background:`none`,border:`none`,color:`#475569`,fontSize:14,cursor:`pointer`},'
    'children:`✕`})]}),'
    '(0,L.jsxs)(`div`,{className:`chat-input-row`,style:{padding:`10px 14px`,'
    'borderTop:_dmReplyTo?`none`:`1px solid #2e303a`},'
)
if OLD_BEFORE_COMPOSE in content:
    content = content.replace(OLD_BEFORE_COMPOSE, NEW_BEFORE_COMPOSE, 1)
    print('OK: reply preview above compose added')
else:
    errors.append('FAIL: compose row anchor not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
