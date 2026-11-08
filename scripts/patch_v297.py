#!/usr/bin/env python3
"""Patch v296 -> v297: iMessage-style DM bubbles.
- Remove username+colored header bar from each message
- Received messages: bird avatar on left, dark bubble
- Sent messages: right-aligned, purple bubble, no avatar
- Timestamp shown small below each bubble
- Compose area stays; CSS updated for new layout."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v296.js'
dst = '_deploy/assets/index-DUcNPOLc-v297.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. Replace message rendering ─────────────────────────────────────────────
# Remove chat-msg-meta (bird+name+time header bar), add avatar outside body,
# add chat-ts below bubble, add --mine class to bubble

OLD_MSG = (
    'return(0,L.jsxs)(`div`,{className:`chat-msg${_mine?` chat-msg--mine`:``}`,"data-comment-id":_msg.id,children:[(0,L.jsxs)(`div`,{className:`chat-msg-body`,children:[(0,L.jsxs)(`div`,{className:`chat-msg-meta`,style:{background:_mclr},children:[_mbd&&_mbd.hat?(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{height:`17px`,width:`auto`,flexShrink:0,display:`block`}}):(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,fontSize:17,lineHeight:1,flexShrink:0},children:[(0,L.jsx)(`span`,{style:{filter:_mbd&&_mbd.f?_mbd.f:``,display:`block`},children:_mbd&&_mbd.e?_mbd.e:`🐤`}),...(_mbd&&_mbd.s?_spEls(_mbd.s,17):[])]}),(0,L.jsx)(`span`,{style:{fontWeight:700,fontSize:11,color:`#0a0a0a`,flex:1,minWidth:0,whiteSpace:`nowrap`,overflow:`hidden`,textOverflow:`ellipsis`},children:_msg.from_username}),(0,L.jsxs)(`span`,{style:{fontSize:11,color:`rgba(0,0,0,0.45)`,fontWeight:400,flexShrink:0,whiteSpace:`nowrap`},children:[`· `,Un(_msg.created_at)]})]}),_msg.reply_to&&(0,L.jsxs)(`div`,{className:`chat-quote-bar`,children:[(0,L.jsx)(`span`,{className:`chat-quote-name`,children:_msg.reply_to.from_username}),(0,L.jsx)(`p`,{className:`chat-quote-text`,children:_msg.reply_to.content})]}),(0,L.jsx)(`div`,{className:`chat-bubble`,onClick:()=>_setDmPickerId(_showActions?null:_msg.id),children:_msg.content})'
)
NEW_MSG = (
    'return(0,L.jsxs)(`div`,{className:`chat-msg${_mine?` chat-msg--mine`:``}`,"data-comment-id":_msg.id,children:[!_mine&&(0,L.jsx)(`span`,{className:`dm-avatar`,children:_mbd&&_mbd.hat?(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,style:{height:`22px`,width:`auto`}}):(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,fontSize:22,lineHeight:1},children:[(0,L.jsx)(`span`,{style:{filter:_mbd&&_mbd.f?_mbd.f:``,display:`block`},children:_mbd&&_mbd.e?_mbd.e:`🐤`}),...(_mbd&&_mbd.s?_spEls(_mbd.s,22):[])]})}),(0,L.jsxs)(`div`,{className:`chat-msg-body`,children:[_msg.reply_to&&(0,L.jsxs)(`div`,{className:`chat-quote-bar`,children:[(0,L.jsx)(`span`,{className:`chat-quote-name`,children:_msg.reply_to.from_username}),(0,L.jsx)(`p`,{className:`chat-quote-text`,children:_msg.reply_to.content})]}),(0,L.jsx)(`div`,{className:`chat-bubble${_mine?` chat-bubble--mine`:``}`,onClick:()=>_setDmPickerId(_showActions?null:_msg.id),children:_msg.content}),(0,L.jsx)(`span`,{className:`chat-ts`,children:Un(_msg.created_at)})'
)

if OLD_MSG in content:
    content = content.replace(OLD_MSG, NEW_MSG, 1)
    print('OK: message rendering updated to iMessage style')
else:
    errors.append('FAIL: message rendering not found')

# ── 2. Update CSS: .chat-msg layout ──────────────────────────────────────────
OLD_CSS_MSG = (
    '.chat-msg {\n        display: block;\n        align-self: flex-start;\n        max-width: min(80%, 480px);\n        margin-bottom: 10px;\n      }\n\n      .chat-msg--mine {\n        align-self: flex-end;\n      }'
)
NEW_CSS_MSG = (
    '.chat-msg {\n        display: flex;\n        align-items: flex-end;\n        gap: 8px;\n        max-width: min(82%, 480px);\n        margin-bottom: 4px;\n        align-self: flex-start;\n      }\n\n      .chat-msg--mine {\n        align-self: flex-end;\n        flex-direction: row-reverse;\n      }\n\n      .dm-avatar {\n        flex-shrink: 0;\n        width: 26px;\n        display: flex;\n        align-items: center;\n        justify-content: center;\n      }'
)
if OLD_CSS_MSG in content:
    content = content.replace(OLD_CSS_MSG, NEW_CSS_MSG, 1)
    print('OK: .chat-msg CSS updated for flex iMessage layout')
else:
    errors.append('FAIL: .chat-msg CSS not found')

# ── 3. Update CSS: .chat-msg-body ────────────────────────────────────────────
OLD_CSS_BODY = (
    '.chat-msg-body {\n        display: flex;\n        flex-direction: column;\n        border-radius: 18px;\n        overflow: hidden;\n        width: 100%;\n      }'
)
NEW_CSS_BODY = (
    '.chat-msg-body {\n        display: flex;\n        flex-direction: column;\n        align-items: flex-start;\n        min-width: 0;\n      }\n\n      .chat-msg--mine .chat-msg-body {\n        align-items: flex-end;\n      }'
)
if OLD_CSS_BODY in content:
    content = content.replace(OLD_CSS_BODY, NEW_CSS_BODY, 1)
    print('OK: .chat-msg-body CSS updated')
else:
    errors.append('FAIL: .chat-msg-body CSS not found')

# ── 4. Update CSS: .chat-bubble — received style + add sent + timestamp ───────
OLD_CSS_BUBBLE = (
    '.chat-bubble {\n        background: #1e2530;\n        color: #dbe4ee;\n        border-radius: 0;\n        padding: 6px 10px;\n        font-size: 13px;\n        line-height: 1.4;\n        cursor: pointer;\n        word-break: break-word;\n        transition: opacity 0.15s;\n      }'
)
NEW_CSS_BUBBLE = (
    '.chat-bubble {\n        background: #252836;\n        color: #e2e8f0;\n        border-radius: 18px 18px 18px 4px;\n        padding: 8px 12px;\n        font-size: 13px;\n        line-height: 1.4;\n        cursor: pointer;\n        word-break: break-word;\n        transition: opacity 0.15s;\n        display: inline-block;\n        max-width: 100%;\n      }\n\n      .chat-bubble--mine {\n        background: #7c3aed;\n        color: #ffffff;\n        border-radius: 18px 18px 4px 18px;\n      }\n\n      .chat-ts {\n        font-size: 10px;\n        color: #64748b;\n        padding: 2px 4px;\n        margin-top: 1px;\n      }'
)
if OLD_CSS_BUBBLE in content:
    content = content.replace(OLD_CSS_BUBBLE, NEW_CSS_BUBBLE, 1)
    print('OK: .chat-bubble CSS updated with iMessage bubble shapes + .chat-ts added')
else:
    errors.append('FAIL: .chat-bubble CSS not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

p_diff = content.count('(') - content.count(')')
b_diff = content.count('{') - content.count('}')
print(f'Parens: {p_diff}, Braces: {b_diff}')

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
