#!/usr/bin/env python3
"""Patch v1152 -> v1153: one shared Worm wallet panel (post wallet + the chirp emoji picker's worm tab, phone and
computer): balance shown big, a number you can type (with − / +), quick picks 1 / 5 / 10 / All, and a full-width
"Give N worms" button. No double-tap zoom (touch-action: manipulation; 18px input). The sheet's colour runs to the
bottom of the screen. The emoji sheet hides its search bar on the worm tab."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1152.js'
dst = '_deploy/assets/index-DUcNPOLc-v1153.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

PANEL = r'''function _wwPanel({kind,id,own,done}){const el=document.createElement(`div`);el.className=`ww`;const MAX=50,signed=!!localStorage.getItem(`auth_token`);
 el.innerHTML=`<div class="ww-hd"><span class="ww-ic">${_ppIco(`WORM`)}</span><div class="ww-tt">Worm wallet</div><div class="ww-bx"><b class="ww-bn">…</b><span>balance</span></div></div>`+(own?`<div class="ww-note">You can't give worms to your own post.</div>`:`<div class="ww-row"><button type="button" class="ww-st" data-d="-1" aria-label="Fewer">−</button><input class="ww-in" type="text" inputmode="numeric" pattern="[0-9]*" autocomplete="off" aria-label="How many worms" value="1"><button type="button" class="ww-st" data-d="1" aria-label="More">+</button></div><div class="ww-q"><button type="button" data-q="1">1</button><button type="button" data-q="5">5</button><button type="button" data-q="10">10</button><button type="button" data-q="all">All</button></div><button type="button" class="ww-give">Give 1 worm</button><div class="ww-msg"></div>`);
 let bal=_ppWorm.bal(),cnt=1;const bn=el.querySelector(`.ww-bn`),inp=el.querySelector(`.ww-in`),gv=el.querySelector(`.ww-give`),msg=el.querySelector(`.ww-msg`);
 const top=()=>Math.max(1,Math.min(MAX,bal==null?MAX:bal));
 const upd=(typing)=>{bn.textContent=!signed?`–`:bal==null?`…`:bal;if(own)return;
  if(!typing){cnt=Math.max(1,Math.min(top(),cnt||1));inp.value=cnt}
  const[mn,pl]=el.querySelectorAll(`.ww-st`);mn.disabled=cnt<=1;pl.disabled=cnt>=top()||bal===0;
  el.querySelectorAll(`.ww-q button`).forEach(b=>{const q=b.dataset.q===`all`?top():+b.dataset.q;b.disabled=bal===0||(bal!=null&&q>bal);b.classList.toggle(`on`,q===cnt&&bal!==0)});
  gv.disabled=!signed?!1:bal===0||!cnt;gv.textContent=!signed?`Sign in to give worms`:bal===0?`No worms to give`:!cnt?`Type a number`:`Give ${cnt} worm${cnt===1?``:`s`}`;
  msg.textContent=!signed?``:bal===0?`You don't have any worms right now.`:bal!=null&&bal>MAX&&cnt>=MAX?`Up to ${MAX} at a time.`:``};
 if(!own){el.querySelectorAll(`.ww-st`).forEach(b=>b.onclick=ev=>{ev.preventDefault();inp.blur();cnt=(cnt||1)+(+b.dataset.d);upd()});
  el.querySelectorAll(`.ww-q button`).forEach(b=>b.onclick=ev=>{ev.preventDefault();inp.blur();cnt=b.dataset.q===`all`?top():+b.dataset.q;upd()});
  inp.addEventListener(`input`,()=>{const v=inp.value.replace(/\D/g,``).slice(0,3);inp.value=v;cnt=v?Math.min(+v,top()):0;if(v&&+v>top())inp.value=cnt;upd(!0)});
  inp.addEventListener(`blur`,()=>upd());const selAll=()=>setTimeout(()=>{try{inp.setSelectionRange(0,inp.value.length)}catch(e){}},0);inp.addEventListener(`focus`,selAll);inp.addEventListener(`mouseup`,selAll);inp.addEventListener(`touchend`,selAll);
  inp.addEventListener(`keydown`,e=>{if(e.key===`Enter`){e.preventDefault();gv.click()}});
  gv.onclick=ev=>{ev.preventDefault();if(!signed){window.dispatchEvent(new CustomEvent(`like-no-auth`));return}upd();if(bal===0||!cnt)return;if(_ppWorm.give(kind,id,cnt))done&&done()}}
 const refresh=()=>{if(signed)_ppWorm.loadBal().then(v=>{bal=v;upd()})};upd();refresh();
 return{el,refresh}}
'''
patch("function _wormWallet(id,own){", PANEL + "function _wormWallet(id,own){", 'shared panel')

# post wallet: use the panel
i = c.index(" sh.innerHTML=`<div class=\"ri-worms ww-worms\">"); j = c.index(" upd();if(localStorage.getItem(`auth_token`))_ppWorm.loadBal().then(v=>{bal=v;upd()});else{bl.textContent=`Sign in to give worms`}}", i)
end = j + len(" upd();if(localStorage.getItem(`auth_token`))_ppWorm.loadBal().then(v=>{bal=v;upd()});else{bl.textContent=`Sign in to give worms`}}")
c = c[:i] + (" let shut=!1;const close=()=>{if(shut)return;shut=!0;document.removeEventListener(`keydown`,esc);ov.classList.remove(`in`);setTimeout(()=>ov.remove(),220)};\n"
             " const esc=e=>{if(e.key===`Escape`)close()};document.addEventListener(`keydown`,esc);\n"
             " const ww=_wwPanel({kind:`p`,id,own,done:close});sh.append(ww.el);\n"
             " ov.append(top,sh);document.body.append(ov);requestAnimationFrame(()=>ov.classList.add(`in`));\n"
             " ov.addEventListener(`click`,e=>{if(e.target===ov||e.target.closest(`.ww-top`))close()})}") + c[end:]
print('OK: post wallet uses the panel')

# phone emoji sheet worm tab
i = c.index("wp.innerHTML=`<div class=\"pp-pick-worm\"><span class=\"pp-ic pp-worm\">${_ppIco(`WORM`)}</span><span class=\"pp-pick-wl\">Worm wallet</span>", c.index("wp.className=`ri-worms`;"))
j = c.index("showW=w=>{", i); k = c.index("}}", j) + 2
c = c[:i] + ("const ww=_wwPanel({kind:wo.kind,id:wo.id,done:()=>close()});wp.append(ww.el);sc.parentNode.insertBefore(wp,sc);\n"
             "  showW=w=>{wp.hidden=!w;sc.style.display=w?`none`:``;const se=ov.querySelector(`.ri-search`);if(se)se.style.display=w?`none`:``;wb.classList.toggle(`on`,w);if(w){nav.querySelectorAll(`.ri-cat:not(.ri-wcat)`).forEach(b=>b.classList.remove(`on`));ww.refresh()}}") + c[k:]
print('OK: phone emoji sheet worm tab')

# computer picker worm tab
i = c.index("let cnt=1,bal=_ppWorm.bal();\n  wp.innerHTML=`<div class=\"pp-pick-worm\">", c.index("wp.className=`rx-pick-worms`;"))
j = c.index("  const show=w=>{", i)
c = c[:i] + "const ww=_wwPanel({kind:wo.kind,id:wo.id,done:()=>close()});wp.append(ww.el);\n" + c[j:]
patch("wp.hidden=!w;host.style.display=kb.style.display=w?`none`:``;if(w)_ppWorm.loadBal().then(v=>{bal=v;upd()})};",
      "wp.hidden=!w;host.style.display=kb.style.display=w?`none`:``;if(w)ww.refresh()};", 'computer picker refresh')
print('OK: computer picker worm tab')

css = ("body .ww{display:flex;flex-direction:column;gap:12px;touch-action:manipulation}body .ww *{touch-action:manipulation}"
       "body .ww-hd{display:flex;align-items:center;gap:10px}body .ww-ic{display:inline-flex}body .ww-ic .ri.wemo{font-size:22px}"
       "body .ww-tt{flex:1;font-size:16px;font-weight:800;color:#fb7185}"
       "body .ww-bx{display:flex;flex-direction:column;align-items:flex-end;line-height:1.1}body .ww-bn{font-size:22px;font-weight:800;color:#fda4af}body .ww-bx span{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#64748b}"
       "body .ww-note{font-size:14px;color:#94a3b8;padding:2px 0 4px}"
       "body .ww-row{display:flex;align-items:center;gap:10px}"
       "body .ww-st{width:48px;height:48px;flex-shrink:0;border-radius:14px;border:1px solid #3a3d48;background:#26282f;color:#f1f5f9;font-size:24px;line-height:1;cursor:pointer;font-family:inherit}body .ww-st:disabled{opacity:.35;cursor:default}"
       "body .ww-in{flex:1;min-width:0;height:48px;box-sizing:border-box;border-radius:14px;border:1px solid #3a3d48;background:#16171d;color:#f8fafc;font:inherit;font-size:22px;font-weight:800;text-align:center;outline:none}"
       "body .ww-in:focus{border-color:#fb7185;box-shadow:0 0 0 3px rgba(251,113,133,.18)}"
       "body .ww-q{display:flex;gap:8px}body .ww-q button{flex:1;height:34px;border-radius:999px;border:1px solid rgba(251,113,133,.3);background:rgba(251,113,133,.06);color:#fda4af;font:inherit;font-size:13.5px;font-weight:700;cursor:pointer}"
       "body .ww-q button.on{background:rgba(251,113,133,.22);border-color:#fb7185;color:#ffe4e6}body .ww-q button:disabled{opacity:.35;cursor:default}"
       "body .ww-give{height:50px;border:0;border-radius:999px;background:#fb7185;color:#1a0b10;font:inherit;font-size:16px;font-weight:800;cursor:pointer}body .ww-give:disabled{background:#3a3d48;color:#94a3b8;cursor:default}"
       "body .ww-msg{font-size:12.5px;color:#94a3b8;text-align:center;min-height:0}body .ww-msg:empty{display:none}"
       "body .ww-ov .ri-sheet,body .ri-ov .ri-sheet{box-shadow:0 -10px 40px rgba(0,0,0,.45),0 300px 0 0 #1f1f21}"
       "body .ww-ov .ww-sheet{padding:18px 18px calc(16px + env(safe-area-inset-bottom))!important;box-sizing:border-box}"
       "body .ri-worms .ww{padding:4px 2px 6px}body .rx-pick-worms .ww{padding:4px 2px}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
