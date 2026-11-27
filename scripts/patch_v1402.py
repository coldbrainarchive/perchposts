#!/usr/bin/env python3
"""Patch v1396 -> v1402 (spine = cover leather, no shadow/logo pops, whole-book shake; left strip shows what's turned; v1397 + passport fixes: spine, turning behind the spine, closed cover over the spine, no see-through turns): the passport replaces the Bird ID card (your account tab and every other bird's card).
- The passport code (scripts/passport_v1402.js) goes in just before _BC; both _BC calls become _PPass.
- Opens on the ID page; tap right = next page, left = back (on the ID page that closes the cover; tap it to open).
- Notifications: the STAMP badge gets a rubber-stamp icon; "/?passport=<stamp>" links open your account tab on the
  passport page with that stamp."""
import sys, re
src = '_deploy/assets/index-DUcNPOLc-v1396.js'
dst = '_deploy/assets/index-DUcNPOLc-v1402.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    k = c.count(old)
    if k != n: print('FAIL', label, k); sys.exit(1)
    c = c.replace(old, new); print('OK', label)

code = open('scripts/passport_v1402.js', encoding='utf-8').read()
patch("function _BC({col,role,pad,face,badge,title,sub,desc,stats,btn,nest,rc,rtop}){", code + "\nfunction _BC({col,role,pad,face,badge,title,sub,desc,stats,btn,nest,rc,rtop}){", 'passport code')

# another bird's card
i = c.find("return _BC({col:_resolvedCol"); j = c.find("btn:_om&&_me&&_me!==_un?", i)
if i < 0 or j < 0: print('FAIL user card'); sys.exit(1)
c = c[:i] + "return (0,L.jsx)(_PPass,{u:_un,hat:!!(_bd&&_bd.hat),flaps:_s.flaps||0,worms:_wc,rank:_rk?_rk.n:null,clan:_clan?_clan.n:null,issued:_s.joined_at,pad:_om?`10px 0 16px`:`10px 14px`," + c[j:]; print('OK user card')

# your own account tab
i = c.find("e?_BC({col:t===`admin`?`#ffffff`:t===`mod`?`#c084fc`:A,pad:`0`,nest:!0,")
j = c.find("`Worms`,_wc]]}):null", i)
if i < 0 or j < 0: print('FAIL own card'); sys.exit(1)
c = c[:i] + "e&&te?(0,L.jsx)(_PPass,{u:te,own:!0,hat:!!(_bird&&_bird.hat),flaps:_flc,worms:_wc,rank:_rank?_rank.n:null,clan:_clanN?_clanN.n:null}):null" + c[j + len("`Worms`,_wc]]}):null"):]; print('OK own card')

# stamp notifications: the badge, and opening your passport on that stamp's page
patch("e.icon===`GLOBE`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,style:{color:`#60a5fa`},dangerouslySetInnerHTML:{__html:_ppIco(`GLOBE`)}}):e.icon}):null]});",
      "e.icon===`GLOBE`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,style:{color:`#60a5fa`},dangerouslySetInnerHTML:{__html:_ppIco(`GLOBE`)}}):e.icon===`STAMP`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,style:{color:`#c084fc`},dangerouslySetInnerHTML:{__html:`<svg class=\"ri\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M9.5 3h5l-.8 7h-3.4z\"/><path d=\"M7 10h10l1.2 4H5.8z\"/><path d=\"M5 14h14v3H5z\"/><path d=\"M6 20.5h12\"/></svg>`}}):e.icon}):null]});",
      'stamp badge')
patch("onClick:_ev=>{if(e.link&&/^\\/globe\\//.test(e.link)){",
      "onClick:_ev=>{if(e.link&&e.link.startsWith(`/?passport=`)){_ev.preventDefault();_nMark(e);window._ppPassGo=decodeURIComponent(e.link.slice(11));l(`account`);return}if(e.link&&/^\\/globe\\//.test(e.link)){",
      'stamp notification opens the passport')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
