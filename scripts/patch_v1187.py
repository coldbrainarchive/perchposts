#!/usr/bin/env python3
"""Patch v1186 -> v1187: bird fixes.
- Profile card: the bird / clan come from the profile's own user, not the first post in the list (on the Flaps tab
  that post is someone else's, so borbie showed another bird).
- Big birds (Bird ID cards, notifications panel, Your Nest) draw first instead of waiting behind every tag bird; the
  3x base images warm up a moment after the page loads, and your own big bird is drawn ahead of time.
- While a big bird is still drawing it shows the same bird's small tag image scaled up (or an empty space of the
  right size) instead of a different stand-in emoji bird."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1186.js'
dst = '_deploy/assets/index-DUcNPOLc-v1187.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
# profile card: the right record
patch("record:b[0]||null,onMessage:", "record:b.find(x=>(x.username||``).toLowerCase()===p)||null,onMessage:", 'profile uses its own post')
patch("const _bd=_br?Jn(_br):(_un?Jn({username:_un,browser_id:`_`}):null);",
      "const _bd=_br?Jn(_br):(_un?Jn({username:_un,browser_id:`_`,is_admin:_s.role===`admin`||_adminUsers.has(_un.toLowerCase()),is_mod:_s.role===`mod`}):null);", 'no post: role from stats')
# runtime: big birds first + warm up
patch('cache.set(k, { done: false }); queue.push([n, c, kind === "t" ? "t" : "f"]); pump(); return null;',
      'cache.set(k, { done: false }); (kind === "t" ? queue.push : queue.unshift).call(queue, [n, c, kind === "t" ? "t" : "f"]); pump(); return null;', 'big birds jump the line')
patch('const ready = Promise.all([loadSet(BASE1, ""), loadSet(BASE2, "@2x")]).then(() => { ok = true; pump(); })',
      'const ready = Promise.all([loadSet(BASE1, ""), loadSet(BASE2, "@2x")]).then(() => { ok = true; pump(); setTimeout(() => big(), 1500); })', 'warm the 3x images')
# placeholder while drawing
patch("if(!r||r.fail)return fb!==void 0?fb:c;",
      "if(!r||r.fail){if(!r&&kd===`f`){const tg=_ppKit.get(n,c,`t`);if(tg&&!tg.fail&&tg.t){const w2=z*(1+2*(tg.g||0));return(0,L.jsx)(`img`,{src:tg.t,alt:``,draggable:!1,style:{width:w2,height:w2,margin:-(w2-z)/2,display:`block`,maxWidth:`none`,pointerEvents:`none`,flexShrink:0}})}if(fb===void 0)return(0,L.jsx)(`span`,{\"aria-hidden\":!0,style:{display:`inline-block`,width:z,height:z}})}return fb!==void 0?fb:c}", 'same-bird placeholder')
patch("function _ppB(x,z,k){",
      "setTimeout(()=>{try{const me=Qn()?.username;if(!me)return;const bd=Jn({username:me,browser_id:`_`});if(bd&&bd.u&&bd.e&&!bd.hat)_ppKit.get(bd.u,bd.e,`f`)}catch(e){}},2500);\nfunction _ppB(x,z,k){", 'draw your own big bird early')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
