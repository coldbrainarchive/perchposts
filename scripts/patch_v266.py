#!/usr/bin/env python3
"""Patch v265 -> v266: DM thread matches post comment panel layout; compose sticks to bottom; no OP."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v265.js'
dst = '_deploy/assets/index-DUcNPOLc-v266.js'

content = open(src, encoding='utf-8').read()
errors = []

SEND_REFRESH = (
    'let _r=await fetch(`${R}/dm-thread?with=${encodeURIComponent(_dmThread)}`,{headers:er()});'
    '_setDmMsgs((_r.ok?await _r.json():{}).messages||[]);'
)

# ── 1. Replace thread container + header with comments-panel style ────────────
OLD_THREAD_HEADER = (
    '(0,L.jsxs)(`div`,{style:{display:`flex`,flexDirection:`column`,flex:1},'
    'children:[(0,L.jsxs)(`div`,{style:{padding:`10px 16px`,borderBottom:`1px solid #2e303a`,'
    'display:`flex`,alignItems:`center`,gap:10},'
    'children:[(0,L.jsx)(`button`,{onClick:()=>{_setDmThread(null);_setDmMsgs([]);},'
    'style:{background:`none`,border:`none`,color:`#94a3b8`,fontSize:18,'
    'cursor:`pointer`,padding:0,lineHeight:1},children:`←`}),'
    '(()=>{const _tc=_dmConvs.find(c=>c.contact===_dmThread)||{};'
    'return(0,L.jsx)(Xn,{record:{username:_dmThread,'
    'is_admin:!!_tc.is_admin,is_mod:!!_tc.is_mod},'
    'name:_dmThread,'
    'color:_tc.is_admin?`#ffffff`:Hn(null,_dmThread)})})()'
    ']})'
)
NEW_THREAD_HEADER = (
    '(0,L.jsxs)(`div`,{className:`content-card comments-panel`,'
    'style:{padding:0,overflow:`clip`,display:`flex`,flexDirection:`column`,flex:1,height:0},'
    'children:[(0,L.jsxs)(`div`,{className:`chat-panel-header`,'
    'style:{display:`flex`,alignItems:`center`,justifyContent:`space-between`},'
    'children:[(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,gap:8},'
    'children:[(0,L.jsx)(`button`,{onClick:()=>{_setDmThread(null);_setDmMsgs([]);},'
    'style:{background:`none`,border:`none`,color:`#94a3b8`,fontSize:18,'
    'cursor:`pointer`,padding:`0 4px`,lineHeight:1},children:`←`}),'
    '(()=>{const _tc=_dmConvs.find(c=>c.contact===_dmThread)||{};'
    'return(0,L.jsx)(Xn,{record:{username:_dmThread,'
    'is_admin:!!_tc.is_admin,is_mod:!!_tc.is_mod},'
    'name:_dmThread,'
    'color:_tc.is_admin?`#ffffff`:Hn(null,_dmThread)});})()'
    ']})]})' # closes header
)
if OLD_THREAD_HEADER in content:
    content = content.replace(OLD_THREAD_HEADER, NEW_THREAD_HEADER, 1)
    print('OK: thread header updated to chat-panel-header')
else:
    errors.append('FAIL: thread header not found')

# ── 2. Change messages container from comments-list to chat-window ────────────
OLD_MSGS = 'className:`comments-list`,style:{overflowY:`auto`,flex:1,padding:`8px 0`},'
NEW_MSGS = 'className:`chat-window`,'
if OLD_MSGS in content:
    content = content.replace(OLD_MSGS, NEW_MSGS, 1)
    print('OK: messages area uses chat-window class')
else:
    errors.append('FAIL: messages container not found')

# ── 3. Replace reply-preview + compose with Wr-style compose ─────────────────
OLD_COMPOSE_AREA = (
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
NEW_COMPOSE_AREA = (
    # Reply dismiss bar (Wr style)
    '_dmReplyTo&&(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,'
    'gap:8,padding:`6px 14px`,borderTop:`1px solid #2e303a`,background:`#0f1117`},'
    'children:[(0,L.jsxs)(`div`,{style:{flex:1,borderLeft:`2px solid #c084fc`,'
    'paddingLeft:8,fontSize:11,color:`#94a3b8`,overflow:`hidden`,'
    'textOverflow:`ellipsis`,whiteSpace:`nowrap`},'
    'children:[_dmReplyTo.from_username,`: `,_dmReplyTo.content]}),'
    '(0,L.jsx)(`button`,{type:`button`,className:`chat-reply-dismiss`,'
    'onClick:()=>_setDmReplyTo(null),children:`✕`})]}),'
    # Compose row — same as Wr
    '(0,L.jsxs)(`div`,{className:`chat-input-row`,'
)
if OLD_COMPOSE_AREA in content:
    content = content.replace(OLD_COMPOSE_AREA, NEW_COMPOSE_AREA, 1)
    print('OK: compose area updated to Wr style')
else:
    errors.append('FAIL: compose area not found')

# ── 4. Update compose children: remove padding/borderTop inline styles ────────
# The chat-input-row in DM still has style attr — remove it to let CSS handle it
OLD_COMPOSE_STYLE = (
    '(0,L.jsxs)(`div`,{className:`chat-input-row`,style:{padding:`10px 14px`,'
    'borderTop:`1px solid #2e303a`},'
)
NEW_COMPOSE_STYLE = '(0,L.jsxs)(`div`,{className:`chat-input-row`,'
if OLD_COMPOSE_STYLE in content:
    content = content.replace(OLD_COMPOSE_STYLE, NEW_COMPOSE_STYLE, 1)
    print('OK: compose inline style removed (uses chat-input-row CSS)')
else:
    print('NOTE: compose style already clean (skipped)')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
