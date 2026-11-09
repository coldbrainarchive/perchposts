#!/usr/bin/env python3
"""Patch v905 -> v906: the three toggles (search Boards | Regions | Filters, comments Oldest | Newest,
new post POST | HUDDLE) get the search bar's purple outline (#c084fc instead of #a855f7) and a purple pill
that slides to the selected option. A small script adds the pill to every .srch-tabs / .sort-toggle and
moves it to the .active button (measured, so unequal button widths work). Until it's placed, the active
button keeps its own purple background, so there's no flash."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v905.js'
dst = '_deploy/assets/index-DUcNPOLc-v906.js'
content = open(src, encoding='utf-8').read()
reps = [
 ('.srch-tabs { display: flex; margin: 2px 40px 2px; height: 22px; box-sizing: border-box; border: 1px solid #a855f7;',
  '.srch-tabs { display: flex; margin: 2px 40px 2px; height: 22px; box-sizing: border-box; border: 1px solid #c084fc;'),
 ('.sort-toggle {\n        display: flex;\n        border-radius: 999px;\n        border: 1px solid #a855f7;',
  '.sort-toggle {\n        display: flex;\n        border-radius: 999px;\n        border: 1px solid #c084fc;'),
 ('.srch-tab.active { background: #c084fc; color: #fff; }',
  '.srch-tab.active { background: #c084fc; color: #fff; }\n'
  '      .srch-tabs, .sort-toggle { position: relative; isolation: isolate; }\n'
  '      .tg-thumb { position: absolute; top: 0; bottom: 0; left: 0; width: 0; border-radius: 999px; background: #c084fc; z-index: 0; pointer-events: none; opacity: 0; }\n'
  '      .tg-ready > .tg-thumb { opacity: 1; transition: left 0.25s cubic-bezier(.3,.7,.3,1), width 0.25s cubic-bezier(.3,.7,.3,1); }\n'
  '      .tg-ready > button { position: relative; z-index: 1; }\n'
  '      .tg-ready > button.active { background: transparent !important; }'),
]
for o, n in reps:
    if content.count(o) != 1: print('FAIL', content.count(o), o[:80]); sys.exit(1)
    content = content.replace(o, n)
JS = r'''
;(()=>{try{
const place=(el,anim)=>{let th=el.querySelector(':scope > .tg-thumb');if(!th){th=document.createElement('span');th.className='tg-thumb';el.prepend(th);anim=false}
 const a=el.querySelector(':scope > button.active');if(!a||!el.offsetWidth)return;
 const l=a.offsetLeft+'px',w=a.offsetWidth+'px';if(th.style.left===l&&th.style.width===w&&el.classList.contains('tg-ready'))return;
 if(!anim||!el.classList.contains('tg-ready')){th.style.transition='none';th.style.left=l;th.style.width=w;void th.offsetWidth;th.style.transition='';el.classList.add('tg-ready')}
 else{th.style.left=l;th.style.width=w}};
let q=0;const run=()=>{q=0;document.querySelectorAll('.srch-tabs,.sort-toggle').forEach(el=>place(el,true))};
const sched=()=>{if(!q){q=1;requestAnimationFrame(run)}};
new MutationObserver(sched).observe(document.body,{subtree:true,childList:true,attributes:true,attributeFilter:['class']});
addEventListener('resize',sched);sched();
}catch(e){}})();
'''
open(dst, 'w', encoding='utf-8').write(content + JS)
print('Wrote ' + dst)
