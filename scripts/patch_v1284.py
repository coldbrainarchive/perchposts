#!/usr/bin/env python3
"""Patch v1283 -> v1284: @tags are coloured (pill colour) in the post scroller title and text, for birds' posts only
(news posts can contain @handles that aren't birds). Feed cards stay plain."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1283.js'
dst = '_deploy/assets/index-DUcNPOLc-v1284.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
DOM = ("function _ppMentDom(el,s){s=String(s||``);const re=/(^|[^\\w@])@([a-z][a-z0-9-]{1,40})/gi;let last=0,m,any=!1;const f=document.createDocumentFragment();"
       "while(m=re.exec(s)){any=!0;const st=m.index+m[1].length;if(st>last)f.appendChild(document.createTextNode(s.slice(last,st)));"
       "const sp=document.createElement(`span`);sp.className=`pp-ment`;sp.style.color=_ppTagCol(m[2]);sp.textContent=`@`+m[2];f.appendChild(sp);last=st+1+m[2].length}"
       "if(!any){el.textContent=s;return}if(last<s.length)f.appendChild(document.createTextNode(s.slice(last)));el.replaceChildren(f)}")
patch("function _ppMent(s){", DOM + "function _ppMent(s){", 'dom helper')
patch("t.className=`reel-title`;t.textContent=d.title;", "t.className=`reel-title`;d.kind===`u`?_ppMentDom(t,d.title):t.textContent=d.title;", 'reel title')
patch("t.className=`reel-desc`;t.textContent=d.desc;", "t.className=`reel-desc`;d.kind===`u`?_ppMentDom(t,d.desc):t.textContent=d.desc;", 'reel text')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
