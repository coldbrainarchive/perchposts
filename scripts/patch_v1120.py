#!/usr/bin/env python3
"""Patch v1119 -> v1120: worm trading, and posts take only flaps and worms.
- The worm symbol is the 🪱 emoji again (everywhere: picker, chirp pills, reaction bar, who-did-what).
- Holding the bird on a post opens just the worm row (no other emoji on posts). It shows how many worms you have and
  won't let you pick more; giving moves worms from you to them (the server checks too)."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1119.js'
dst = '_deploy/assets/index-DUcNPOLc-v1120.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)

i = c.index('"WORM": "<svg'); j = c.index('</svg>"', i) + len('</svg>"')
c = c[:i] + '"WORM": "<span class=\\"ri wemo\\" aria-hidden=\\"true\\">🪱</span>"' + c[j:]; print('OK: worm emoji')

# picker: no emoji row on posts; worm row knows your balance
i = c.index(" if(kind===`p`){const row=document.createElement(`div`);row.className=`pp-pick-row`;"); j = c.index("pk.append(row)}", i) + len("pk.append(row)}")
c = c[:i] + c[j:]; print('OK: no emoji on posts')
patch("const upd=()=>{nb.textContent=cnt;gv.textContent=cnt===1?`Give 1`:`Give ${cnt}`};upd();\n mn.onclick=()=>{cnt=Math.max(1,cnt-1);upd()};pls.onclick=()=>{cnt=Math.min(50,cnt+1);upd()};\n gv.onclick=()=>{_ppWorm.give(kind,id,cnt);close()};pk.append(wr);",
      "let bal=_ppWorm.bal();const bl=document.createElement(`div`);bl.className=`pp-pick-bal`;\n"
      " const upd=()=>{if(bal!=null&&cnt>Math.max(1,bal))cnt=Math.max(1,bal);nb.textContent=cnt;gv.textContent=cnt===1?`Give 1`:`Give ${cnt}`;gv.disabled=bal===0;pls.disabled=bal!=null&&cnt>=bal;mn.disabled=cnt<=1;"
      "bl.textContent=bal==null?`Counting your worms…`:bal===0?`You don't have any worms to give`:`You have ${bal} worm${bal===1?``:`s`}`};upd();\n"
      " _ppWorm.loadBal().then(v=>{bal=v;upd()});\n"
      " mn.onclick=()=>{cnt=Math.max(1,cnt-1);upd()};pls.onclick=()=>{cnt=Math.min(50,bal==null?cnt+1:Math.min(bal,cnt+1));upd()};\n"
      " gv.onclick=()=>{if(bal===0)return;_ppWorm.give(kind,id,cnt);close()};pk.append(wr,bl);", 'balance in the picker')

# the worm store keeps your balance
patch("const _ppWorm=(()=>{const cnt=new Map(),mine=new Map(),subs=new Map(),q=new Set(),pend=new Map();let t=null;",
      "const _ppWorm=(()=>{const cnt=new Map(),mine=new Map(),subs=new Map(),q=new Set(),pend=new Map();let t=null,bal=null;\n"
      " const loadBal=()=>fetch(`${R}/my-worms`,{headers:er()}).then(r=>r.ok?r.json():null).then(d=>{if(d&&d.balance!=null)bal=d.balance;return bal}).catch(()=>bal);", 'balance store')
patch("if(k===`p`&&d.score!=null)_ppResp.set(id,{n:d.score,m:d.myVote});", "if(k===`p`&&d.score!=null)_ppResp.set(id,{n:d.score,m:d.myVote});if(d.balance!=null)bal=d.balance;", 'balance after giving')
patch("return{key,want,give,sub,n:K=>cnt.get(K)||0,m:K=>mine.get(K)||0}})();", "return{key,want,give,sub,n:K=>cnt.get(K)||0,m:K=>mine.get(K)||0,bal:()=>bal,loadBal}})();", 'balance exported')

css = ("body .ri.wemo{display:inline-flex!important;align-items:center;justify-content:center;width:auto!important;height:auto!important;font-size:14px;line-height:1;transform:none}"
       "body .pp-pick-worm .ri.wemo{font-size:19px}body .rx-q.rx-worm .ri.wemo{font-size:24px}body .pr-did .ri.wemo{font-size:16px}"
       "body .pp-pick-worm:first-child{border-top:0;padding-top:2px}body .pp-pick-bal{font-size:12px;font-weight:600;color:#94a3b8;text-align:center;padding:0 6px 2px}"
       "body .pp-pick-st:disabled,body .pp-pick-give:disabled{opacity:.35;cursor:default}")
patch("body .lb-ic{", css + "body .lb-ic{", 'styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
