#!/usr/bin/env python3
"""Patch v932 -> v933:
1. Send buttons (chirp + DM) use your own name-tag colour (--me: admin white, mod purple, else your bird
   colour), not fixed purple.
2. Chirp effects stay on their chirp: the materialize card and the landing glow follow the chirp's position
   every frame (they were fixed at the spot where they started, so if the chat scrolled - e.g. opening a
   chat from a notification - the outline was left somewhere else).
3. Effects are clipped to the chat area, so glows no longer show through the compose box or anything outside
   the chat.
4. Only chirps marked "just now" materialize / count toward "new chirps" (older chirps loading when a chat
   opens from a notification were treated as new). Initial quiet period 2s -> 3s.
"""
import re, sys
src = '_deploy/assets/index-DUcNPOLc-v932.js'
dst = '_deploy/assets/index-DUcNPOLc-v933.js'
c = open(src, encoding='utf-8').read()
errors = []
def patch(old, new, label, count=1):
    global c
    n = c.count(old)
    if n != count: errors.append(f'FAIL ({label}): {n}')
    else: c = c.replace(old, new); print('OK: ' + label)

# 1. send buttons
patch('background:_cA?`#c084fc`', 'background:_cA?`var(--me,#c084fc)`', 'chirp send button colour')
c, n = re.subn(r'(\.chat-send-btn \{\s*width: 36px;\s*height: 36px;\s*border-radius: 999px;\s*border: none;\s*)background: #c084fc;', r'\1background: var(--me, #c084fc);', c); print('dm send base:', n)
patch('.dm-outer .chat-compose .chat-send-btn:not(:disabled) {\n        background: #c084fc;', '.dm-outer .chat-compose .chat-send-btn:not(:disabled) {\n        background: var(--me, #c084fc);', 'dm send active')
# 2+3. materialize card follows + clipped
patch("document.body.appendChild(g);\n g.animate([{transform:'scale(.85)'", "document.body.appendChild(g);window._follow(g,body,w);\n g.animate([{transform:'scale(.85)'", 'materialize follows chirp')
# landing glow: stop the flight animation, pin styles, then follow the chirp
patch("   const keep={left:px(br.left),top:px(br.top),width:px(br.width),height:px(br.height),borderRadius:RR,fontSize:cs.fontSize,padding:cs.padding};",
      "   try{a.cancel()}catch(_){};Object.assign(g.style,{left:px(br.left),top:px(br.top),width:px(br.width),height:px(br.height),borderRadius:RR,fontSize:cs.fontSize,padding:cs.padding});\n"
      "   window._follow(g,nb||body,document.querySelector('.chat-window'));const keep={};", 'landing glow follows chirp')
# 4. only "just now" chirps are live
patch("   if(Date.now()-st.t<2000||idx>2||m.classList.contains('chat-msg--mine'))return;", "   if(Date.now()-st.t<3000||idx>2||m.classList.contains('chat-msg--mine'))return;\n   if(!/just now/.test((m.querySelector('.chat-msg-meta')||{}).textContent||''))return;", 'only just-now chirps animate')

JS = r'''
;window._follow=function(g,el,w){const tick=()=>{if(!g.isConnected)return;if(!el||!el.isConnected){g.remove();return}
 const r=el.getBoundingClientRect();g.style.left=r.left+'px';g.style.top=r.top+'px';g.style.width=r.width+'px';g.style.height=r.height+'px';
 if(w&&w.isConnected){const q=w.getBoundingClientRect();g.style.clipPath='inset('+(q.top-r.top)+'px '+(r.right-q.right)+'px '+(r.bottom-q.bottom)+'px '+(q.left-r.left)+'px)'}
 requestAnimationFrame(tick)};tick()};
;(()=>{try{const setMe=()=>{try{const u=JSON.parse(localStorage.getItem('auth_user')||'null');if(!u||!u.username){document.documentElement.style.removeProperty('--me');return}
 const col=u.role==='admin'?'#ffffff':u.role==='mod'?'#c084fc':Hn(Gn(),u.username);document.documentElement.style.setProperty('--me',col)}catch(e){}};
 setMe();setInterval(setMe,3000);addEventListener('storage',setMe)}catch(e){}})();
'''
if errors: print('\n'.join(errors)); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(c + JS); print('Wrote ' + dst)
