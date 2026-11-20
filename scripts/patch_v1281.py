#!/usr/bin/env python3
"""Patch v1280 -> v1281: tag colours.
- @names in chirps / post bodies use the tagged bird's pill colour (admins and mods: purple #c084fc).
- Composer: once a bird is picked from the @ list, the tag shows in that colour inside the text box ("locked in").
  A text box can't colour words, so a mirror div with identical metrics sits behind it (text box text goes
  transparent while a locked tag is in it; caret stays visible)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1280.js'
dst = '_deploy/assets/index-DUcNPOLc-v1281.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
TC = ("function _ppTagCol(n){try{const l=String(n).toLowerCase();if((typeof _adminUsers!==`undefined`&&(_adminUsers.has(l)||_adminUsers.has(n)))||(typeof _modUsers!==`undefined`&&_modUsers.has(l)))return`#c084fc`;return Hn(null,n)}catch(e){return`#c084fc`}}")
patch("function _ppMent(s){", TC + "function _ppMent(s){", 'colour helper')
patch("out.push((0,L.jsx)(`span`,{className:`pp-ment`,\"data-gpb\":m[2],children:`@`+m[2]},`m`+k++))",
      "out.push((0,L.jsx)(`span`,{className:`pp-ment`,\"data-gpb\":m[2],style:{color:_ppTagCol(m[2])},children:`@`+m[2]},`m`+k++))", 'rendered tag colour')
patch("body .pp-ment{color:#c084fc;font-weight:700;cursor:pointer}", "body .pp-ment{color:#c084fc;font-weight:700;cursor:pointer}", 'css kept')
# remember the picked bird's colour and turn on the mirror for that box
patch("close();setV(t,nv);const np=k.a+u.n.length+2;try{t.focus();t.setSelectionRange(np,np)}catch(e){}};",
      "close();setV(t,nv);const np=k.a+u.n.length+2;try{t.focus();t.setSelectionRange(np,np)}catch(e){}try{window._ppTagLk&&window._ppTagLk(t,u.n,u.r===`admin`||u.r===`mod`?`#c084fc`:Hn(null,u.n))}catch(e){}};", 'lock on pick')
c += r"""
;(()=>{try{
  const st=document.createElement(`style`);st.textContent=`.pp-tm{position:absolute;pointer-events:none;overflow:hidden;white-space:pre-wrap;overflow-wrap:break-word;word-wrap:break-word;box-sizing:border-box;border-color:transparent!important;margin:0;z-index:0}.pp-tm i{font-style:normal;border-radius:4px}.pp-tm-on{color:transparent!important;-webkit-text-fill-color:transparent!important;background:transparent!important;position:relative;z-index:1}`;document.head.appendChild(st);
  const cols=new Map(),live=new Set();
  const esc=s=>s.replace(/[&<>]/g,ch=>({"&":`&amp;`,"<":`&lt;`,">":`&gt;`})[ch]);
  const html=v=>{let out=``,last=0,m;const re=/(^|[^\w@])@([a-z][a-z0-9-]{1,40})/gi;while(m=re.exec(v)){const n=m[2].toLowerCase(),col=cols.get(n);if(!col)continue;const s=m.index+m[1].length;out+=esc(v.slice(last,s))+`<i style="color:${col}">@${esc(m[2])}</i>`;last=s+1+m[2].length}return out?out+esc(v.slice(last))+`​`:null};
  const COPY=[`fontFamily`,`fontSize`,`fontWeight`,`fontStyle`,`letterSpacing`,`lineHeight`,`textTransform`,`textIndent`,`wordSpacing`,`tabSize`,`paddingTop`,`paddingRight`,`paddingBottom`,`paddingLeft`,`borderTopWidth`,`borderRightWidth`,`borderBottomWidth`,`borderLeftWidth`,`borderTopStyle`,`borderRightStyle`,`borderBottomStyle`,`borderLeftStyle`,`borderRadius`,`boxSizing`,`textAlign`];
  const sync=t=>{const mr=t._ppTm;if(!mr)return;if(!t.isConnected){mr.remove();t._ppTm=null;live.delete(t);return}
    const h=html(t.value),ON=[[`color`,`transparent`],[`-webkit-text-fill-color`,`transparent`],[`background`,`transparent`]];if(!h){if(t.classList.contains(`pp-tm-on`)){t.classList.remove(`pp-tm-on`);ON.forEach(([k])=>t.style.removeProperty(k))}mr.style.display=`none`;return}
    const cs=getComputedStyle(t);for(const k of COPY)mr.style[k]=cs[k];if(t.tagName===`INPUT`){mr.style.whiteSpace=`pre`;mr.style.overflowWrap=`normal`}
    mr.style.color=t._ppCol;mr.style.background=t._ppBg;
    mr.style.left=t.offsetLeft+`px`;mr.style.top=t.offsetTop+`px`;mr.style.width=t.offsetWidth+`px`;mr.style.height=t.offsetHeight+`px`;
    if(mr.innerHTML!==h)mr.innerHTML=h;mr.style.display=``;t.classList.add(`pp-tm-on`);ON.forEach(([k,v])=>t.style.setProperty(k,v,`important`));mr.scrollTop=t.scrollTop;mr.scrollLeft=t.scrollLeft};
  window._ppTagLk=(t,name,col)=>{cols.set(String(name).toLowerCase(),col);if(!t._ppTm){const cs=getComputedStyle(t);t._ppCol=cs.color;t._ppBg=cs.backgroundColor;t.style.caretColor=cs.color;
      const mr=document.createElement(`div`);mr.className=`pp-tm`;mr.setAttribute(`aria-hidden`,`true`);const par=t.offsetParent||t.parentElement;if(par&&getComputedStyle(par).position===`static`)par.style.position=`relative`;t.parentElement.insertBefore(mr,t);t._ppTm=mr;live.add(t);
      [`input`,`scroll`,`focus`,`blur`,`keyup`].forEach(ev=>t.addEventListener(ev,()=>sync(t)));if(window.ResizeObserver)new ResizeObserver(()=>sync(t)).observe(t)}
    sync(t)};
  setInterval(()=>{for(const t of live){if(t._ppLast!==t.value||!t.isConnected){t._ppLast=t.value;sync(t)}}},300);
}catch(e){console.error(e)}})();
"""
patch("_a.replace(/ ago$/,` old`)})()},`a`):null]:c.title}),", "_a.replace(/ ago$/,` old`)})()},`a`):null]:_ppMent(c.title)}),", 'post title tags')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
