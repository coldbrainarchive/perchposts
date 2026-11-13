#!/usr/bin/env python3
"""Patch v1044 -> v1045: flaps icon is a bird in flight that flaps its wings when you flap a post, and the post
cards (feed + post page) use the same custom icons as the full-screen view: bird (flaps), speech bubble (chirps),
box-with-arrow (share). Search filter labels keep their emoji.
- _ppIco(k) is a hoisted function so React components can use it before the bottom of the file runs.
- The bird's wing beat is an SVG <animate> on the path, started with beginElement() — only when flapping, not when
  taking a flap back, and not when signed out."""
import sys, json
src = '_deploy/assets/index-DUcNPOLc-v1044.js'
dst = '_deploy/assets/index-DUcNPOLc-v1045.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
SV = '<svg class="ri" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
REST = 'M2 13.5C4 9.5 8.5 8.5 12 15C15.5 8.5 20 9.5 22 13.5'
UP   = 'M4.5 7C6 5 9.5 6 12 15C14.5 6 18 5 19.5 7'
DOWN = 'M3 18C4.5 14.5 8.5 13 12 15C15.5 13 19.5 14.5 21 18'
vals = ';'.join([REST, UP, REST, DOWN, REST, UP, REST])
ICONS = {
 'BIRD': SV + '<path d="' + REST + '"><animate attributeName="d" dur=".75s" begin="indefinite" fill="remove" calcMode="spline" keyTimes="0;.17;.33;.5;.67;.83;1" keySplines=".4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1" values="' + vals + '"/></path></svg>',
 'CHAT': SV + '<path d="M20.5 11.5c0 4.4-3.8 8-8.5 8-1.2 0-2.4-.2-3.4-.7L4 20l1.3-3.6c-1.1-1.4-1.8-3.1-1.8-4.9 0-4.4 3.8-8 8.5-8s8.5 3.6 8.5 8z"/></svg>',
 'SHARE': SV + '<path d="M12 14.5V3.5M8 7.5l4-4 4 4"/><path d="M8.5 10.5H7a2 2 0 0 0-2 2V19a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6.5a2 2 0 0 0-2-2h-1.5"/></svg>',
}
helper = ('function _ppIco(k){return (' + json.dumps(ICONS) + ')[k]||``}\n'
          'function _ppFlapAnim(root){try{root&&root.querySelectorAll(`.pp-bird animate, .reel-flap animate`).forEach(a=>{try{a.endElement&&a.endElement();a.beginElement()}catch(e){}})}catch(e){}}\n')
patch('function _reelCollect(){', helper + 'function _reelCollect(){', 'icon helpers')
ICON_SPAN = lambda k, cls: '(0,L.jsx)(`span`,{className:`pp-ic ' + cls + '`,dangerouslySetInnerHTML:{__html:_ppIco(`' + k + '`)}})'
WING_SPAN = '(0,L.jsx)(`span`,{style:{fontSize:14,lineHeight:1,display:`inline-flex`,alignItems:`center`,verticalAlign:`middle`,marginRight:-3},children:`🪽`})'
patch(WING_SPAN, ICON_SPAN('BIRD', 'pp-bird'), 'cards: bird', n=2)
patch('(0,L.jsx)(`span`,{children:`💬`}),(0,L.jsx)(`span`,{children:t})', ICON_SPAN('CHAT', 'pp-chat') + ',(0,L.jsx)(`span`,{children:t})', 'feed card: chat')
patch('(0,L.jsx)(`span`,{children:`💬`}),(0,L.jsx)(`span`,{children:_cn})', ICON_SPAN('CHAT', 'pp-chat') + ',(0,L.jsx)(`span`,{children:_cn})', 'post page: chat')
patch('(0,L.jsx)(`span`,{children:`↗`}),(0,L.jsx)(`span`,{children:o})', ICON_SPAN('SHARE', 'pp-share') + ',(0,L.jsx)(`span`,{children:o})', 'feed card: share')
patch('(0,L.jsx)(`span`,{children:`↗`}),(0,L.jsx)(`span`,{children:j})', ICON_SPAN('SHARE', 'pp-share') + ',(0,L.jsx)(`span`,{children:j})', 'post page: share')
# full-screen view uses the same set
patch('for(const b of c.querySelectorAll(`.feed-post-actions button`))if((b.textContent||``).includes(`🪽`))return b;return null}',
      'for(const b of c.querySelectorAll(`.feed-post-actions button`))if(b.querySelector(`.pp-bird`))return b;return null}', 'reel finds card flap button')
patch('mk(`reel-flap`,_RI.WING,`Flap this post`)', 'mk(`reel-flap`,_ppIco(`BIRD`),`Flap this post`)', 'reel bird')
patch('mk(`reel-chat`,_RI.CHAT,`Open the chat`)', 'mk(`reel-chat`,_ppIco(`CHAT`),`Open the chat`)', 'reel chat')
patch('sh.innerHTML=_RI.SHARE+`<span>Share</span>`;sh.onclick', 'sh.innerHTML=_ppIco(`SHARE`)+`<span>Share</span>`;sh.onclick', 'reel share')
patch('setTimeout(()=>{sh.innerHTML=_RI.SHARE+`<span>Share</span>`;', 'setTimeout(()=>{sh.innerHTML=_ppIco(`SHARE`)+`<span>Share</span>`;', 'reel share back')
# reel: wing beat when flapping (not when taking it back)
patch('const flap=(s,id)=>{const b=_reelFlapBtn(id);if(!b)return;let na=!1;',
      'const flap=(s,id)=>{const b=_reelFlapBtn(id);if(!b)return;const fb0=s.querySelector(`.reel-flap`),wasOn=fb0&&fb0.classList.contains(`on`);let na=!1;', 'reel remembers state')
patch('if(na){pendingNoAuth=!0;close();return}const fb=s.querySelector(`.reel-flap`);',
      'if(na){pendingNoAuth=!0;close();return}const fb=s.querySelector(`.reel-flap`);if(!wasOn)_ppFlapAnim(fb);', 'reel wing beat')
c += r'''
;(()=>{try{document.addEventListener(`click`,e=>{try{if(!e.isTrusted)return;const b=e.target.closest&&e.target.closest(`.feed-post-action-pill`);if(!b||!b.querySelector(`.pp-bird`))return;
 if(!localStorage.getItem(`auth_token`))return;if(/192,\s*132,\s*252/.test(b.getAttribute(`style`)||``))return;_ppFlapAnim(b)}catch(er){}},!0)}catch(e){}})();
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.pp-ic{display:inline-flex;align-items:center;justify-content:center;line-height:1;vertical-align:middle}
.pp-ic .ri{width:14px;height:14px;display:block}
.pp-ic.pp-bird .ri{width:16px;height:16px;stroke-width:2.2}
.feed-post-action-pill .pp-ic{margin-right:1px}
.reel .reel-flap .ri{width:22px;height:22px;stroke-width:2.1}
.reel .reel-flap.pop .ri{transform:none}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
