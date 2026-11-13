#!/usr/bin/env python3
"""Patch v1043 -> v1044: custom line icons in the full-screen link view instead of emoji.
Wing (flaps; fills purple when flapped), speech bubble (chat), box-with-arrow (share; becomes a tick when done),
and a matching arrow after the website name. All are inline SVG in one stroke style, coloured by the button text."""
import sys, json
src = '_deploy/assets/index-DUcNPOLc-v1043.js'
dst = '_deploy/assets/index-DUcNPOLc-v1044.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
SV = '<svg class="ri" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
ICONS = {
 'WING': SV + '<g transform="translate(0 2.3)"><path class="fillme" d="M3 10C7 5 14 3.5 21 4c-.6 2-1.8 3.3-3.4 4h2.2c-.9 2-2.5 3.4-4.6 4h1.8c-1.6 2.3-4 3.6-7 3.8C7.6 16 4.8 14 3 10z"/></g></svg>',
 'CHAT': SV + '<path d="M20.5 11.5c0 4.4-3.8 8-8.5 8-1.2 0-2.4-.2-3.4-.7L4 20l1.3-3.6c-1.1-1.4-1.8-3.1-1.8-4.9 0-4.4 3.8-8 8.5-8s8.5 3.6 8.5 8z"/></svg>',
 'SHARE': SV + '<path d="M12 14.5V3.5M8 7.5l4-4 4 4"/><path d="M8.5 10.5H7a2 2 0 0 0-2 2V19a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6.5a2 2 0 0 0-2-2h-1.5"/></svg>',
 'TICK': SV + '<path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
 'ARROW': SV + '<path d="M7 17L17 7M9 7h8v8"/></svg>',
}
c = c.replace('function _reelCollect(){', 'const _RI=' + __import__('json').dumps(ICONS) + ';\nfunction _reelCollect(){', 1)
patch('i.textContent=ic;', 'i.innerHTML=ic;', 'icon slot takes svg')
patch('mk(`reel-flap`,`🪽`,`Flap this post`)', 'mk(`reel-flap`,_RI.WING,`Flap this post`)', 'wing')
patch('mk(`reel-chat`,`💬`,`Open the chat`)', 'mk(`reel-chat`,_RI.CHAT,`Open the chat`)', 'chat')
patch('sh.textContent=`↗ Share`;sh.onclick', 'sh.innerHTML=_RI.SHARE+`<span>Share</span>`;sh.onclick', 'share icon')
patch('sh.textContent=`✓ Shared`;', 'sh.innerHTML=_RI.TICK+`<span>Shared</span>`;', 'tick icon')
patch('setTimeout(()=>{sh.textContent=`↗ Share`;', 'setTimeout(()=>{sh.innerHTML=_RI.SHARE+`<span>Share</span>`;', 'share icon back')
patch('sa.className=`reel-site-ar`;sa.textContent=`↗`;', 'sa.className=`reel-site-ar`;sa.innerHTML=_RI.ARROW;', 'site arrow')
c += r'''
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.reel .ri{width:18px;height:18px;display:block;flex-shrink:0}\n.reel .reel-flap .ri{width:20px;height:20px}
.reel .reel-mini .i{display:inline-flex;margin:0}
.reel .reel-btns .reel-btn.reel-mini{gap:7px}
.reel .reel-share{gap:6px}
.reel .reel-flap .fillme{transition:fill .15s}
.reel .reel-flap.on{color:#c084fc}
.reel .reel-flap.on .fillme{fill:rgba(192,132,252,.35)}
.reel .reel-flap.on .n{color:#f3e8ff}
.reel .reel-flap.pop .ri{transform:scale(1.25) rotate(-10deg)}
.reel .reel-mini .ri{transition:transform .14s}
.reel .reel-share.done .ri{color:#c084fc}
.reel .reel-site-ar .ri{width:13px;height:13px;stroke-width:2.4}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
