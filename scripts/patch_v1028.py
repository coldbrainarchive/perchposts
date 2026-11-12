#!/usr/bin/env python3
"""Patch v1027 -> v1028: security follow-ups.
- Reactions/votes lookups send your own browser id (?bid=) so the server can scramble everyone else's, and
  reactions send your login so huddle members still see reactions inside their huddles.
- Changing your password asks for your current password (a small box), and keeps this device logged in with
  the fresh login the server returns (other devices are signed out)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1027.js'
dst = '_deploy/assets/index-DUcNPOLc-v1028.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('let t=await fetch(`${R}/get-reactions?comment_ids=${e.join(`,`)}`);',
      'let t=await fetch(`${R}/get-reactions?comment_ids=${e.join(`,`)}&bid=${encodeURIComponent(Gn())}`,{headers:er()});', 'reactions lookup')
patch('let _vu=`${R}/get-votes?post_ids=${e.join(`,`)}`,', 'let _vu=`${R}/get-votes?post_ids=${e.join(`,`)}&bid=${encodeURIComponent(t)}`,', 'votes lookup')
for setter, var in [('fe', 'de'), ('d', 'u')]:
    old = ('let e=await fetch(`${R}/update-password`,{method:`POST`,headers:{"Content-Type":`application/json`,...$n()},body:JSON.stringify({newPassword:' + var + '})}),t=await e.json();if(!e.ok)return alert(t.error||`Failed to update password`);alert(`Password updated 🔑`),' + setter + '(``)')
    new = ('const _cur=await _askCurrentPw();if(!_cur)return;let e=await fetch(`${R}/update-password`,{method:`POST`,headers:{"Content-Type":`application/json`,...$n()},body:JSON.stringify({newPassword:' + var + ',currentPassword:_cur})}),t=await e.json();if(!e.ok)return alert(t.error||`Failed to update password`);'
           't.token&&localStorage.setItem(`auth_token`,t.token);alert(`Password updated 🔑 Any other phones or computers logged in to this account have been signed out.`),' + setter + '(``)')
    patch(old, new, 'password change ' + var)
c += r'''
function _askCurrentPw(){return new Promise(res=>{try{const ov=document.createElement(`div`);ov.className=`cp-ov`;
 ov.innerHTML=`<form class="cp-box"><div class="cp-t">Enter your current password</div><input class="cp-in" type="password" autocomplete="current-password" placeholder="Current password"><div class="cp-row"><button type="button" class="cp-no">Cancel</button><button type="submit" class="cp-yes">Change password</button></div></form>`;
 const done=v=>{ov.remove();res(v)};ov.querySelector(`.cp-no`).onclick=()=>done(null);ov.onclick=e=>{if(e.target===ov)done(null)};
 ov.querySelector(`form`).onsubmit=e=>{e.preventDefault();const v=ov.querySelector(`.cp-in`).value;if(v)done(v)};
 document.body.appendChild(ov);setTimeout(()=>ov.querySelector(`.cp-in`).focus(),50)}catch(e){res(null)}})}
;(()=>{try{const s=document.createElement(`style`);s.textContent=`
.cp-ov{position:fixed;inset:0;z-index:10001;background:rgba(0,0,0,.6);display:flex;align-items:center;justify-content:center;padding:16px}
.cp-box{width:100%;max-width:340px;background:#1a1d27;border:1px solid #2e303a;border-radius:16px;padding:20px;box-shadow:0 20px 60px rgba(0,0,0,.5)}
.cp-t{color:#f1f5f9;font-weight:800;font-size:16px;margin-bottom:12px}
.cp-in{width:100%;box-sizing:border-box;padding:12px 14px;border-radius:12px;border:1px solid #3f4756;background:#0f1117;color:#f8fafc;font-size:16px;outline:none}
.cp-in:focus{border-color:#c084fc}
.cp-row{display:flex;gap:8px;justify-content:flex-end;margin-top:14px}
.cp-row button{height:38px;padding:0 16px;border-radius:999px;border:none;font-weight:800;font-size:14px;cursor:pointer;font-family:inherit}
.cp-no{background:#1f2937;color:#cbd5e1}.cp-yes{background:#c084fc;color:#14081d}
`;document.head.appendChild(s)}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
