#!/usr/bin/env python3
"""Patch v186 -> v187: new comment card layout — coloured header, bird avatar, globe for mod/admin."""
import sys

src = '_deploy/assets/index-DUcNPOLc-v186.js'
dst = '_deploy/assets/index-DUcNPOLc-v187.js'

content = open(src, encoding='utf-8').read()
errors = []

# ── 1. CSS: .chat-msg — remove flex avatar layout, set max-width on msg itself ──
OLD_MSG_CSS = (
    '.chat-msg {\n'
    '        display: flex;\n'
    '        align-items: flex-start;\n'
    '        gap: 8px;\n'
    '        max-width: 100%;\n'
    '      }'
)
NEW_MSG_CSS = (
    '.chat-msg {\n'
    '        display: block;\n'
    '        max-width: 80%;\n'
    '        margin-bottom: 10px;\n'
    '      }'
)
if OLD_MSG_CSS in content:
    content = content.replace(OLD_MSG_CSS, NEW_MSG_CSS, 1)
    print('OK: .chat-msg CSS')
else:
    errors.append('FAIL: .chat-msg CSS not found')

# ── 2. CSS: .chat-msg-body — becomes card container ──────────────────────────
OLD_BODY_CSS = (
    '.chat-msg-body {\n'
    '        display: flex;\n'
    '        flex-direction: column;\n'
    '        gap: 3px;\n'
    '        max-width: 80%;\n'
    '      }'
)
NEW_BODY_CSS = (
    '.chat-msg-body {\n'
    '        display: flex;\n'
    '        flex-direction: column;\n'
    '        border-radius: 18px;\n'
    '        overflow: hidden;\n'
    '      }'
)
if OLD_BODY_CSS in content:
    content = content.replace(OLD_BODY_CSS, NEW_BODY_CSS, 1)
    print('OK: .chat-msg-body CSS')
else:
    errors.append('FAIL: .chat-msg-body CSS not found')

# ── 3. CSS: .chat-msg-meta — becomes coloured card header ────────────────────
OLD_META_CSS = (
    '.chat-msg-meta {\n'
    '        display: flex;\n'
    '        align-items: center;\n'
    '        gap: 5px;\n'
    '        font-size: 11px;\n'
    '        font-weight: 700;\n'
    '        padding: 0 4px;\n'
    '      }'
)
NEW_META_CSS = (
    '.chat-msg-meta {\n'
    '        display: flex;\n'
    '        align-items: center;\n'
    '        gap: 10px;\n'
    '        padding: 10px 14px;\n'
    '      }'
)
if OLD_META_CSS in content:
    content = content.replace(OLD_META_CSS, NEW_META_CSS, 1)
    print('OK: .chat-msg-meta CSS')
else:
    errors.append('FAIL: .chat-msg-meta CSS not found')

# ── 4. CSS: .chat-bubble — remove custom border-radius (card handles rounding) ─
OLD_BUBBLE_CSS = 'border-radius: 4px 18px 18px 18px;'
NEW_BUBBLE_CSS = 'border-radius: 0;'
if OLD_BUBBLE_CSS in content:
    content = content.replace(OLD_BUBBLE_CSS, NEW_BUBBLE_CSS, 1)
    print('OK: .chat-bubble border-radius CSS')
else:
    errors.append('FAIL: .chat-bubble border-radius CSS not found')

# ── 5. CSS: .chat-reactions — remove margin-top, add padding inside card ─────
OLD_REACT_CSS = (
    '.chat-reactions {\n'
    '        display: flex;\n'
    '        flex-wrap: wrap;\n'
    '        gap: 4px;\n'
    '        margin-top: 5px;\n'
    '      }'
)
NEW_REACT_CSS = (
    '.chat-reactions {\n'
    '        display: flex;\n'
    '        flex-wrap: wrap;\n'
    '        gap: 4px;\n'
    '        padding: 0 14px 8px;\n'
    '        background: #1e2530;\n'
    '      }'
)
if OLD_REACT_CSS in content:
    content = content.replace(OLD_REACT_CSS, NEW_REACT_CSS, 1)
    print('OK: .chat-reactions CSS')
else:
    errors.append('FAIL: .chat-reactions CSS not found')

# ── 6. CSS: .chat-action-sheet — move to bottom of card, add padding/border ──
OLD_ACTION_CSS = (
    '.chat-action-sheet {\n'
    '        display: flex;\n'
    '        gap: 6px;\n'
    '        margin-bottom: 5px;\n'
    '      }'
)
NEW_ACTION_CSS = (
    '.chat-action-sheet {\n'
    '        display: flex;\n'
    '        gap: 6px;\n'
    '        flex-wrap: wrap;\n'
    '        padding: 8px 14px;\n'
    '        background: #1e2530;\n'
    '        border-top: 1px solid rgba(148,163,184,0.1);\n'
    '      }'
)
if OLD_ACTION_CSS in content:
    content = content.replace(OLD_ACTION_CSS, NEW_ACTION_CSS, 1)
    print('OK: .chat-action-sheet CSS')
else:
    errors.append('FAIL: .chat-action-sheet CSS not found')

# ── 7. Store Jn(e) result so we can use bird data in the header ───────────────
OLD_JN = 'Jn(e)||m[0]?.toUpperCase();'
NEW_JN = 'let _bd=Jn(e);'
if OLD_JN in content:
    content = content.replace(OLD_JN, NEW_JN, 1)
    print('OK: stored _bd=Jn(e)')
else:
    errors.append('FAIL: Jn(e) expression not found')

# ── 8. Replace the full comment render JSX ────────────────────────────────────
# Old: meta(pill+OP+pin+time), action-sheet, bubble, reactions, emoji-picker
# New: meta(big-bird+username+globe+OP+pin+time), bubble, reactions, action-sheet, emoji-picker
GLOBE_SVG = (
    '(0,L.jsxs)(`svg`,{width:`14`,height:`14`,viewBox:`0 0 100 100`,'
    'xmlns:`http://www.w3.org/2000/svg`,style:{flexShrink:0},'
    'children:['
    '(0,L.jsx)(`circle`,{cx:`50`,cy:`50`,r:`44`,fill:`none`,stroke:`#c084fc`,strokeWidth:`7`}),'
    '(0,L.jsx)(`line`,{x1:`6`,y1:`50`,x2:`94`,y2:`50`,stroke:`#c084fc`,strokeWidth:`6`}),'
    '(0,L.jsx)(`path`,{d:`M 14 28 Q 50 38 86 28`,fill:`none`,stroke:`#c084fc`,strokeWidth:`6`}),'
    '(0,L.jsx)(`path`,{d:`M 14 72 Q 50 62 86 72`,fill:`none`,stroke:`#c084fc`,strokeWidth:`6`}),'
    '(0,L.jsx)(`ellipse`,{cx:`50`,cy:`50`,rx:`16`,ry:`44`,fill:`none`,stroke:`#c084fc`,strokeWidth:`6`,clipPath:`url(#bcc)`}),'
    '(0,L.jsx)(`ellipse`,{cx:`50`,cy:`50`,rx:`32`,ry:`44`,fill:`none`,stroke:`#c084fc`,strokeWidth:`6`,clipPath:`url(#bcc)`}),'
    '(0,L.jsx)(`clipPath`,{id:`bcc`,children:(0,L.jsx)(`circle`,{cx:`50`,cy:`50`,r:`44`})})'
    ']})'
)

OLD_JSX = (
    'return(0,L.jsx)(`div`,{className:`chat-msg`,"data-comment-id":e.id,'
    'children:(0,L.jsxs)(`div`,{className:`chat-msg-body`,children:['
    '(0,L.jsxs)(`div`,{className:`chat-msg-meta`,children:['
    '(0,L.jsx)(Xn,{record:e,name:m,color:h}),'
    'g&&(0,L.jsx)(`span`,{className:`comment-card-op`,children:`OP`}),'
    'e.pinned&&(0,L.jsx)(`span`,{style:{fontSize:10,fontWeight:600,color:`#c084fc`,letterSpacing:`0.03em`},children:`📌 pinned`}),'
    '(0,L.jsxs)(`span`,{className:`chat-msg-time`,children:[`· `,Un(e.created_at)]})]}),'
    'v&&(0,L.jsxs)(`div`,{className:`chat-action-sheet`,children:['
    '(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1),s&&s(e)},children:`Reply`}),'
    '(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:D,children:`React`}),'
    'e.parent_comment_id&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1),d&&d(e.parent_comment_id)},children:`Find`}),'
    'a&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:e=>{e.stopPropagation(),y(!1),o&&o()},children:e.pinned?`Unpin`:`📌 Pin`}),'
    'r&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:e=>{e.stopPropagation(),y(!1),i()},children:`Delete`})]}),'
    '(0,L.jsxs)(`div`,{className:`chat-bubble${p?` pending`:``}`,onClick:()=>!p&&y(e=>!e),'
    'style:e.pinned?{borderLeft:`2px solid rgba(192,132,252,0.5)`,background:`rgba(192,132,252,0.06)`,paddingLeft:10}:void 0,'
    'children:[w&&(0,L.jsxs)(`div`,{className:`chat-quote-bar`,children:['
    '(0,L.jsx)(`span`,{className:`chat-quote-name`,children:T}),'
    '(0,L.jsx)(`p`,{className:`chat-quote-text`,children:w.content})]}),'
    '(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:e.content})]}),'
    'ee.length>0&&(0,L.jsx)(`div`,{className:`chat-reactions`,'
    'children:ee.map(([t,n])=>(0,L.jsxs)(`button`,{type:`button`,'
    'className:`chat-reaction-pill${n.includes(C)?` mine`:``}`,'
    'onClick:()=>c&&c(e.id,t),children:[t,(0,L.jsx)(`span`,{className:`chat-reaction-count`,children:n.length})]},t))}),'
    '(0,L.jsx)(`div`,{className:`chat-emoji-picker-row`,style:{display:b?``:`none`},'
    'children:(0,L.jsx)(`input`,{ref:S,className:`chat-emoji-picker-input`,type:`text`,'
    'inputMode:`emoji`,placeholder:`Pick an emoji...`,onChange:O,onBlur:()=>x(!1)})})'
    ']})})'
)

NEW_JSX = (
    'return(0,L.jsx)(`div`,{className:`chat-msg`,"data-comment-id":e.id,'
    'children:(0,L.jsxs)(`div`,{className:`chat-msg-body`,children:['
    # ── new header ──────────────────────────────────────────────────────────────
    '(0,L.jsxs)(`div`,{className:`chat-msg-meta`,'
    'style:{background:e.is_admin===true?`#ffffff`:h},'
    'children:['
    # bird emoji (hat = admin PNG, else custom bird with spots)
    '_bd&&_bd.hat'
    '?(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,width:`32px`,height:`32px`,overflow:`visible`,flexShrink:0},'
    'children:[(0,L.jsx)(`img`,{src:`/admin-bird.png`,alt:`admin`,'
    'style:{position:`absolute`,height:`52px`,width:`auto`,bottom:0,left:`50%`,transform:`translateX(-50%)`}})]})'
    ':(0,L.jsxs)(`span`,{style:{position:`relative`,display:`inline-block`,fontSize:32,lineHeight:1,flexShrink:0},'
    'children:[(0,L.jsx)(`span`,{style:{filter:_bd&&_bd.f?_bd.f:``,display:`block`},'
    'children:_bd&&_bd.e?_bd.e:`🐤`}),...(_bd&&_bd.s?_spEls(_bd.s,32):[])]}),'
    # username bold
    '(0,L.jsx)(`span`,{style:{fontWeight:700,fontSize:15,color:`#0a0a0a`,flex:1,minWidth:0},children:m}),'
    # globe for mod/admin
    f'f&&{GLOBE_SVG},'
    # OP badge
    'g&&(0,L.jsx)(`span`,{className:`comment-card-op`,children:`OP`}),'
    # pin icon
    'e.pinned&&(0,L.jsx)(`span`,{style:{fontSize:11,color:`#c084fc`,flexShrink:0},children:`📌`}),'
    # time
    '(0,L.jsxs)(`span`,{style:{fontSize:11,color:`rgba(0,0,0,0.45)`,fontWeight:400,flexShrink:0,whiteSpace:`nowrap`},'
    'children:[`· `,Un(e.created_at)]})'
    ']}),'
    # ── body (bubble, same click-to-toggle) ─────────────────────────────────────
    '(0,L.jsxs)(`div`,{className:`chat-bubble${p?` pending`:``}`,onClick:()=>!p&&y(e=>!e),'
    'style:e.pinned?{borderLeft:`2px solid rgba(192,132,252,0.5)`,background:`rgba(192,132,252,0.06)`,paddingLeft:10}:void 0,'
    'children:[w&&(0,L.jsxs)(`div`,{className:`chat-quote-bar`,children:['
    '(0,L.jsx)(`span`,{className:`chat-quote-name`,children:T}),'
    '(0,L.jsx)(`p`,{className:`chat-quote-text`,children:w.content})]}),'
    '(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:e.content})]}),'
    # ── reactions ───────────────────────────────────────────────────────────────
    'ee.length>0&&(0,L.jsx)(`div`,{className:`chat-reactions`,'
    'children:ee.map(([t,n])=>(0,L.jsxs)(`button`,{type:`button`,'
    'className:`chat-reaction-pill${n.includes(C)?` mine`:``}`,'
    'onClick:()=>c&&c(e.id,t),children:[t,(0,L.jsx)(`span`,{className:`chat-reaction-count`,children:n.length})]},t))}),'
    # ── action sheet at bottom ───────────────────────────────────────────────────
    'v&&(0,L.jsxs)(`div`,{className:`chat-action-sheet`,children:['
    '(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1),s&&s(e)},children:`Reply`}),'
    '(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:D,children:`React`}),'
    'e.parent_comment_id&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:()=>{y(!1),d&&d(e.parent_comment_id)},children:`Find`}),'
    'a&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:e=>{e.stopPropagation(),y(!1),o&&o()},children:e.pinned?`Unpin`:`📌 Pin`}),'
    'r&&(0,L.jsx)(`button`,{type:`button`,className:`chat-action-btn`,onClick:e=>{e.stopPropagation(),y(!1),i()},children:`Delete`})]}),'
    # ── emoji picker ────────────────────────────────────────────────────────────
    '(0,L.jsx)(`div`,{className:`chat-emoji-picker-row`,style:{display:b?``:`none`},'
    'children:(0,L.jsx)(`input`,{ref:S,className:`chat-emoji-picker-input`,type:`text`,'
    'inputMode:`emoji`,placeholder:`Pick an emoji...`,onChange:O,onBlur:()=>x(!1)})})'
    ']})})'
)

if OLD_JSX in content:
    content = content.replace(OLD_JSX, NEW_JSX, 1)
    print('OK: comment card JSX restructured')
else:
    errors.append('FAIL: comment card JSX not found')

if errors:
    print('\nERRORS:')
    for e in errors: print(' ', e)
    sys.exit(1)

open(dst, 'w', encoding='utf-8').write(content)
print(f'Wrote {dst}')
