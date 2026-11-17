#!/usr/bin/env python3
"""Patch v1138 -> v1139: you can't flap your own post. Tapping the bird on your own post (feed card, post page, or the
preview, which taps the card) shows "You can't flap your own post" instead. The worker refuses it too."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1138.js'
dst = '_deploy/assets/index-DUcNPOLc-v1139.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
OWN = "const _ppOwn=u=>{const m=Qn()?.username;return!!(u&&m&&u.toLowerCase()===m.toLowerCase())},_ppOwnMsg=()=>{try{_hxToast(`You can't flap your own post`)}catch(e){}};\n"
patch("function _PFTabs({u,on}){", OWN + "function _PFTabs({u,on}){", 'helpers')
patch("onClick:t=>{t.preventDefault(),t.stopPropagation();if(e.frozen)return;i?i(e.id,r===1?0:1)",
      "onClick:t=>{t.preventDefault(),t.stopPropagation();if(e.frozen)return;if(_ppOwn(e.username)){_ppOwnMsg();return}i?i(e.id,r===1?0:1)", 'card')
patch("onClick:async t=>{if(c.frozen)return;if(!e){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}t.preventDefault();const _nv=re.myVote===1?0:1;",
      "onClick:async t=>{if(c.frozen)return;if(!e){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}t.preventDefault();if(_ppOwn(c.username)){_ppOwnMsg();return}const _nv=re.myVote===1?0:1;", 'post page')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
