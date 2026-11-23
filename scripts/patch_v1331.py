#!/usr/bin/env python3
"""Patch v1330 -> v1331: birds' posts with a link show the bird's own words.
- Feed card: title, then the bird's text (3 lines max), then the link box; the link's own description is hidden when
  the bird wrote something.
- Post scroller: the bird's title as the headline and their text below it (was the link's title/description); then
  the link as a small line (link title + site), then View post. News posts unchanged."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1330.js'
dst = '_deploy/assets/index-DUcNPOLc-v1331.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
# feed card
patch("e.title&&(0,L.jsx)(I,{to:`/post/${e.id}`,style:{textDecoration:`none`,display:`block`,marginTop:10,marginBottom:8,color:`#f1f5f9`,fontWeight:700,fontSize:16,lineHeight:1.35,textAlign:`left`},children:e.title}),(0,L.jsx)(Fr,{attachment:p,postId:e.id})]})",
      "e.title&&(0,L.jsx)(I,{to:`/post/${e.id}`,style:{textDecoration:`none`,display:`block`,marginTop:10,marginBottom:8,color:`#f1f5f9`,fontWeight:700,fontSize:16,lineHeight:1.35,textAlign:`left`},children:e.title}),_rpOk&&(f||``).trim()?(0,L.jsx)(`div`,{className:`fp-utext`,children:_ppMent((f||``).trim())}):null,(0,L.jsx)(Fr,{attachment:p,postId:e.id,noDesc:_rpOk&&!!(f||``).trim()})]})", 'card: bird text above the link')
patch("function Fr({attachment:e,postId:o,maxH:_mh=480}){", "function Fr({attachment:e,postId:o,maxH:_mh=480,noDesc:_nd}){", 'Fr noDesc prop')
patch("return t===`link`?(0,L.jsx)(Nr,{url:n,title:r,description:i,image:a,postId:o}):null}", "return t===`link`?(0,L.jsx)(Nr,{url:n,title:r,description:_nd?null:i,image:a,postId:o}):null}", 'hide link description')
# scroller: take the bird's title/text from the card
patch("else{try{d=JSON.parse(el.dataset.lp)}catch(e){continue}const cd=el.closest(`.feed-post-card`);d.who=_reelWho(cd&&cd.querySelector(`.feed-post-board-row .user-pill`))}",
      "else{try{d=JSON.parse(el.dataset.lp)}catch(e){continue}const cd=el.closest(`.feed-post-card`);d.who=_reelWho(cd&&cd.querySelector(`.feed-post-board-row .user-pill`));if(cd&&cd.dataset.rp){try{const rp=JSON.parse(cd.dataset.rp);if(rp.title){d.ltitle=d.title;d.title=rp.title;d.desc=(rp.desc||``).trim()||null;d.mine=1}}catch(e){}}}", 'reel: bird title/text')
patch("if(d.kind!==`u`&&d.post){const tt=inner.querySelector(`.reel-title`);if(tt){tt.before(site);site.classList.add(`reel-site-up`)}",
      "if(d.kind!==`u`&&d.post){const tt=inner.querySelector(`.reel-title`);if(d.mine){site.classList.add(`reel-lsite`);if(d.ltitle){const lt=document.createElement(`span`);lt.className=`reel-lt`;lt.textContent=d.ltitle;site.prepend(lt)}}else if(tt){tt.before(site);site.classList.add(`reel-site-up`)}", 'reel: link as a small line')
patch("t.className=`reel-title`;d.kind===`u`?_ppMentDom(t,d.title):t.textContent=d.title;", "t.className=`reel-title`;d.kind===`u`||d.mine?_ppMentDom(t,d.title):t.textContent=d.title;", 'reel: tags in title')
patch("t.className=`reel-desc`;d.kind===`u`?_ppMentDom(t,d.desc):t.textContent=d.desc;", "t.className=`reel-desc`;d.kind===`u`||d.mine?_ppMentDom(t,d.desc):t.textContent=d.desc;", 'reel: tags in text')
patch("body .lb-ic{", "body .fp-utext{color:#cbd5e1;font-size:14px;line-height:1.5;margin:-2px 0 10px;white-space:pre-wrap;overflow-wrap:anywhere;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;text-align:left}body .reel-lsite{display:flex!important;flex-wrap:wrap;align-items:center!important;gap:4px 5px;margin-top:14px}body .reel-lsite .reel-lt{flex-basis:100%;color:#e2e8f0;font-size:14px;font-weight:700;text-transform:none;letter-spacing:0}body .lb-ic{", 'css')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
