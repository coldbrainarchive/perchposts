#!/usr/bin/env python3
"""Patch v1168 -> v1169: huddle page tidy-up.
- Members sheet header: Delete (owner only) · Leave · + Invite. The post's Delete pill is gone on huddles.
- The huddle's top card and the chirps section join into one panel.
- The members row is bigger (it's the only thing under the title now) and the huddle age sits on the title row.
- The empty action row (it only held the age pill) is gone on huddles."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1168.js'
dst = '_deploy/assets/index-DUcNPOLc-v1169.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

# page: delete action for the sheet; no Delete pill / action row on huddles
patch("},leave:()=>{const _un3=",
      "},del:()=>{if(!confirm(`Delete this huddle for everyone? This can't be undone.`))return;fetch(`${R}/delete-my-post`,{method:`POST`,headers:{\"Content-Type\":`application/json`,...er()},body:JSON.stringify({post_id:c.id,browser_id:Gn(),username:localStorage.getItem(`_myUsername`)||null})}).then(async _r=>{if(_r.ok){o(`/`);return}const _j=await _r.json().catch(()=>({}));alert(_j.error||`Could not delete the huddle`)}).catch(()=>alert(`Could not delete the huddle`))},leave:()=>{const _un3=",
      'delete action')
patch("ae&&n&&c.username===n&&!c.locked&&!c.frozen&&(0,L.jsxs)(`button`", "!c.is_huddle&&ae&&n&&c.username===n&&!c.locked&&!c.frozen&&(0,L.jsxs)(`button`", 'no Delete pill on huddles')
patch("(0,L.jsxs)(`div`,{className:`feed-post-actions`,children:[!c?.is_huddle",
      "(0,L.jsxs)(`div`,{className:c?.is_huddle?`feed-post-actions hp-noacts`:`feed-post-actions`,children:[!c?.is_huddle", 'hide huddle action row')

# sheet header: Delete · Leave · + Invite
patch("children:[(0,L.jsx)(`button`,{type:`button`,className:`hx-addb hx-lvb`,",
      "children:[me===(post.username||``).toLowerCase()&&!post.locked&&act.del?(0,L.jsx)(`button`,{type:`button`,className:`hx-addb hx-lvb hx-delb`,onClick:()=>{close();setTimeout(()=>act.del(),230)},children:`Delete`}):null,(0,L.jsx)(`button`,{type:`button`,className:`hx-addb hx-lvb`,",
      'delete button')

# members row: bigger + age
patch("(0,L.jsx)(`span`,{className:`hc-dots`,children:all.slice(0,5).map(m=>_hxDot(m,30,!1,!1))}),",
      "(0,L.jsx)(`span`,{className:`hc-dots`,children:all.slice(0,5).map(m=>_hxDot(m,36,!1,!1))}),", 'bigger dots')
# age on the title row
patch("c.title&&(0,L.jsx)(`h2`,{style:{margin:e?`0 0 8px`:`0`,fontSize:18,fontWeight:800,color:`#f8fafc`,lineHeight:1.3,textAlign:`left`},children:c.title})",
      "c.title&&(0,L.jsx)(`h2`,{className:c.is_huddle?`hp-title`:void 0,style:{margin:e?`0 0 8px`:`0`,fontSize:18,fontWeight:800,color:`#f8fafc`,lineHeight:1.3,textAlign:`left`},children:c.is_huddle?[(0,L.jsx)(`span`,{className:`hp-tt`,children:c.title},`t`),c.created_at?(0,L.jsx)(`span`,{className:`hp-age`,children:(()=>{const _a=Un(c.created_at);return _a===`just now`?`New`:_a.replace(/ ago$/,` old`)})()},`a`):null]:c.title})",
      'age on the title row')

css = ("body .hx-sh{flex-wrap:wrap;row-gap:8px}"
       "body .hx-sh .hx-acts .hx-addb{padding:0 12px}"
       "body .feed-post-actions.hp-noacts{display:none!important}"
       # one panel
       "body .hp-card:has(+ .comments-shell.chat-preview){margin-bottom:0!important;border-bottom:0!important;border-bottom-left-radius:0!important;border-bottom-right-radius:0!important;padding-bottom:14px!important}"
       "body .hp-card + .comments-shell.chat-preview{margin-top:0!important;border-top-left-radius:0!important;border-top-right-radius:0!important;border-color:#262a35!important;background:#171a21!important}"
       "body .hp-card + .comments-shell.chat-preview::before{content:'';display:block;height:1px;margin:0 16px;background:#262a35}"
       # bigger members row
       "body .hp-body .hx-row{padding:12px 14px 12px 12px;margin-top:4px;gap:14px;border-radius:16px;background:rgba(148,163,184,.06);border:1px solid #262a35}"
       "body .hp-body .hx-row:active{background:rgba(192,132,252,.1)}"
       "body .hp-body .hx-cnt{font-size:15px}body .hp-body .hx-names{font-size:13px}"
       "body .hp-body h2.hp-title{display:flex;align-items:center;gap:10px}body .hp-tt{flex:1;min-width:0}"
       "body .hp-age{flex-shrink:0;height:24px;display:inline-flex;align-items:center;padding:0 10px;border-radius:999px;border:1px solid #2e3340;color:#94a3b8;font-size:12px;font-weight:700;white-space:nowrap}"
       "body .hp-body .hc-dots .hx-dot+.hx-dot{margin-left:-10px}"
       "body .hp-body .hx-chev{font-size:26px}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
