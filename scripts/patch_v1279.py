#!/usr/bin/env python3
"""Patch v1278 -> v1279: @tags.
- Typing @ in a chirp box or the New Post title/body shows matching birds; tap (or Enter/Tab) fills in @name.
- @names in chirps and post bodies are purple; tapping one opens that bird's card (data-gpb).
- Tag notifications (worker: icon "AT") get an @ badge; they open the post or jump to the chirp (?highlight=)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1278.js'
dst = '_deploy/assets/index-DUcNPOLc-v1279.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
AT = '<svg class=\\"ri\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\" aria-hidden=\\"true\\"><circle cx=\\"12\\" cy=\\"12\\" r=\\"4\\"/><path d=\\"M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-3.92 7.94\\"/></svg>'
patch('function _ppIco(k){return ({"FLAG":', 'function _ppIco(k){return ({"AT": "' + AT + '", "FLAG":', 'AT icon')
# @name -> purple, tappable (opens the bird card through the existing [data-gpb] handler)
MENT = ("function _ppMent(s){if(typeof s!==`string`||s.indexOf(`@`)<0)return s;const out=[],re=/(^|[^\\w@])@([a-z][a-z0-9-]{1,40})/gi;let last=0,m,k=0;"
        "while(m=re.exec(s)){const st=m.index+m[1].length;if(st>last)out.push(s.slice(last,st));"
        "out.push((0,L.jsx)(`span`,{className:`pp-ment`,\"data-gpb\":m[2],children:`@`+m[2]},`m`+k++));last=st+1+m[2].length}"
        "if(!out.length)return s;if(last<s.length)out.push(s.slice(last));return out}")
c = c.replace('function _ppIco(k){', MENT + 'function _ppIco(k){', 1)
patch("_ct?(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:_ct})", "_ct?(0,L.jsx)(`span`,{className:`chat-bubble-text`,children:_ppMent(_ct)})", 'chirp text')
patch("!c.is_huddle&&e&&(0,L.jsx)(`p`,{style:{margin:0,color:`#d4dde7`,fontSize:14,lineHeight:1.55,whiteSpace:`pre-wrap`,overflowWrap:`anywhere`,textAlign:`left`},children:e})",
      "!c.is_huddle&&e&&(0,L.jsx)(`p`,{style:{margin:0,color:`#d4dde7`,fontSize:14,lineHeight:1.55,whiteSpace:`pre-wrap`,overflowWrap:`anywhere`,textAlign:`left`},children:_ppMent(e)})", 'post body')
patch("e.icon===`👥`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,style:{color:`#fb923c`},dangerouslySetInnerHTML:{__html:_ppIco(`HUDDLE`)}}):e.icon",
      "e.icon===`👥`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,style:{color:`#fb923c`},dangerouslySetInnerHTML:{__html:_ppIco(`HUDDLE`)}}):e.icon===`AT`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,style:{color:`#c084fc`},dangerouslySetInnerHTML:{__html:_ppIco(`AT`)}}):e.icon", 'notif @ badge')
patch("body .lb-ic{", "body .pp-ment{color:#c084fc;font-weight:700;cursor:pointer}body .lb-ic{", 'css')
c += r"""
;(()=>{try{
  const st=document.createElement(`style`);st.textContent=`.pp-at{position:fixed;z-index:2147482000;background:#1b1d24;border:1px solid #2e303a;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.55);padding:4px;max-height:212px;overflow-y:auto;box-sizing:border-box}.pp-at button{display:flex;width:100%;align-items:center;gap:8px;padding:9px 10px;border:0;background:none;color:#e2e8f0;font:inherit;font-size:14px;font-weight:700;border-radius:10px;text-align:left;cursor:pointer;-webkit-tap-highlight-color:transparent}.pp-at button.on{background:#2a2340}.pp-at b{color:#c084fc}`;document.head.appendChild(st);
  let box=null,el=null,list=[],sel=0,tm=0,seq=0;
  const ok=t=>t&&(t.tagName===`TEXTAREA`||(t.tagName===`INPUT`&&t.classList.contains(`nh-title`)))&&!t.closest(`.search-bar`)&&!t.classList.contains(`chat-emoji-picker-input`);
  const tok=t=>{try{const p=t.selectionStart;if(p==null||p!==t.selectionEnd)return null;const m=t.value.slice(0,p).match(/(^|[^\w@])@([a-z0-9-]{1,40})$/i);return m?{q:m[2],a:p-m[2].length-1,b:p}:null}catch(e){return null}};
  const close=()=>{if(box){box.remove();box=null}list=[];sel=0};
  const setV=(t,v)=>{const pr=t.tagName===`TEXTAREA`?HTMLTextAreaElement.prototype:HTMLInputElement.prototype;Object.getOwnPropertyDescriptor(pr,`value`).set.call(t,v);t.dispatchEvent(new Event(`input`,{bubbles:!0}))};
  const pick=i=>{const t=el,u=list[i];if(!t||!u)return close();const k=tok(t);if(!k)return close();const v=t.value,nv=v.slice(0,k.a)+`@`+u+` `+v.slice(k.b);close();setV(t,nv);const np=k.a+u.length+2;try{t.focus();t.setSelectionRange(np,np)}catch(e){}};
  const place=()=>{if(!box||!el)return;const r=el.getBoundingClientRect(),w=Math.min(260,innerWidth-16);box.style.width=w+`px`;box.style.left=Math.max(8,Math.min(r.left,innerWidth-w-8))+`px`;const h=box.offsetHeight;box.style.top=(r.top-h-6>8?r.top-h-6:r.bottom+6)+`px`};
  const draw=()=>{if(!list.length)return close();if(!box){box=document.createElement(`div`);box.className=`pp-at`;box.setAttribute(`role`,`listbox`);document.body.appendChild(box);
      box.addEventListener(`mousedown`,e=>e.preventDefault());box.addEventListener(`touchstart`,e=>{},{passive:!0});
      box.addEventListener(`click`,e=>{const b=e.target.closest(`button`);if(b){e.preventDefault();e.stopPropagation();pick(+b.dataset.i)}})}
    box.innerHTML=``;list.forEach((u,i)=>{const b=document.createElement(`button`);b.type=`button`;b.dataset.i=i;b.className=i===sel?`on`:``;b.innerHTML=`<b>@</b>`;b.appendChild(document.createTextNode(u));box.appendChild(b)});place()};
  const look=t=>{const k=tok(t);if(!k){close();return}el=t;clearTimeout(tm);const my=++seq;tm=setTimeout(()=>{fetch(`${R}/search-users?q=${encodeURIComponent(k.q)}`).then(r=>r.ok?r.json():{users:[]}).then(d=>{if(my!==seq||el!==t||!tok(t))return;const me=(localStorage.getItem(`_myUsername`)||``).toLowerCase(),q=k.q.toLowerCase();
      list=(d.users||[]).map(x=>x.username).filter(n=>n&&n.toLowerCase()!==me).sort((a,b)=>(b.toLowerCase().startsWith(q)?1:0)-(a.toLowerCase().startsWith(q)?1:0)).slice(0,6);sel=0;draw()}).catch(()=>{})},140)};
  document.addEventListener(`input`,e=>{if(ok(e.target))look(e.target)},!0);
  document.addEventListener(`keydown`,e=>{if(!box||e.target!==el)return;if(e.key===`ArrowDown`||e.key===`ArrowUp`){e.preventDefault();sel=(sel+(e.key===`ArrowDown`?1:list.length-1))%list.length;draw()}else if(e.key===`Enter`||e.key===`Tab`){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();pick(sel)}else if(e.key===`Escape`){e.preventDefault();e.stopPropagation();close()}},!0);
  document.addEventListener(`focusout`,e=>{if(e.target===el)setTimeout(()=>{if(document.activeElement!==el)close()},180)},!0);
  document.addEventListener(`selectionchange`,()=>{if(box&&el&&document.activeElement===el&&!tok(el))close()});
  addEventListener(`resize`,place);window.visualViewport&&visualViewport.addEventListener(`resize`,place);
}catch(e){console.error(e)}})();
"""
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
