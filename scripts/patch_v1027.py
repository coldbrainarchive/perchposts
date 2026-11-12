#!/usr/bin/env python3
"""Patch v1026 -> v1027: login lockout in the mod panel and on the login screen.
- Mod panel members: a locked account shows "🔒 Locked · 12m" beside the name with an Unlock button
  (mods and admins); accounts with some wrong passwords (not yet locked) show "⚠️ 3 wrong passwords".
- Login screen: when an account is locked the message says so (and for how long) instead of
  "Invalid username or password"."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1026.js'
dst = '_deploy/assets/index-DUcNPOLc-v1027.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('(0,L.jsx)(Xn,{record:{is_admin:d,is_mod:u&&!d,username:i||`—`,browser_id:n.id},name:i||`—`,color:Hn(n.id,i)}),',
      '(0,L.jsx)(Xn,{record:{is_admin:d,is_mod:u&&!d,username:i||`—`,browser_id:n.id},name:i||`—`,color:Hn(n.id,i)}),(0,L.jsx)(_LockBadge,{m:n,refresh:_e}),',
      'lock beside the name')
patch('return _wr?` · ${_wr.e} ${_wr.n} · 🪱 ${_wc}`:``;})(),',
      'return _wr?` · ${_wr.e} ${_wr.n} · 🪱 ${_wc}`:``;})(),n.failed_logins&&!(n.locked_until&&new Date(n.locked_until)>Date.now())?` · ⚠️ ${n.failed_logins} wrong password${n.failed_logins===1?``:`s`}`:``,',
      'wrong-password note')
patch('if(E(!1),!e.ok){alert(`Invalid username or password`);return}', 'if(E(!1),!e.ok){alert(e.status===423&&t.error?t.error:`Invalid username or password`);return}', 'login screen lock message')
c += r'''
function _LockBadge({m,refresh}){const [busy,setBusy]=(0,_.useState)(!1),[,tick]=(0,_.useReducer)(x=>x+1,0);
 (0,_.useEffect)(()=>{if(!m.locked_until)return;const t=setInterval(tick,30000);return()=>clearInterval(t)},[m.locked_until]);
 if(!m.locked_until)return null;const left=Math.ceil((new Date(m.locked_until)-Date.now())/60000);if(left<=0)return null;
 const stop=e=>e.stopPropagation();
 const unlock=async e=>{e.stopPropagation();if(busy)return;setBusy(!0);try{const r=await fetch(`${R}/unlock-member`,{method:`POST`,headers:{"Content-Type":`application/json`,...er()},body:JSON.stringify({user_id:m.id})});if(!r.ok)throw 0;try{_hxToast(`${m.user_metadata?.username||`Account`} is unlocked`)}catch(_){}refresh&&refresh()}catch(_){alert(`Could not unlock the account`)}setBusy(!1)};
 return(0,L.jsxs)(`span`,{className:`lk-badge`,onClick:stop,title:`Locked after ${10} wrong passwords`,children:[`🔒 Locked · ${left}m`,(0,L.jsx)(`button`,{type:`button`,className:`lk-unlock`,disabled:busy,onClick:unlock,children:busy?`…`:`Unlock`})]})}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.lk-badge{display:inline-flex;align-items:center;gap:6px;font-size:10px;font-weight:700;color:#fca5a5;background:rgba(248,113,113,.12);padding:1px 2px 1px 7px;border-radius:999px;white-space:nowrap}
.lk-unlock{height:18px;padding:0 8px;border-radius:999px;border:none;background:#f87171;color:#1a0505;font-size:10px;font-weight:800;cursor:pointer;font-family:inherit}
.lk-unlock:disabled{opacity:.6}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
