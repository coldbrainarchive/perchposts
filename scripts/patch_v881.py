#!/usr/bin/env python3
"""Patch v880 -> v881: temporary silent recorder for the search-bar cursor jumping on iPhone while typing.
Simulated typing (execCommand) on the user's iPhone didn't reproduce it, so this records the real keyboard.
On with /?vvdebug=type (kept in localStorage), off with /?vvdebug=0. Nothing changes on screen while typing
(a live readout hid the last bug); when search loses focus, a static box shows the last events:
input events with value + cursor, cursor moves, every setSelectionRange call on the search box (the site's own
cursor-restore code), the suggestions box changing, and whether the input element was replaced. Remove after.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v880.js'
dst = '_deploy/assets/index-DUcNPOLc-v881.js'
content = open(src, encoding='utf-8').read()

REC = r'''
;(()=>{try{
const q=new URLSearchParams(location.search).get('vvdebug');
if(q==='type')localStorage.setItem('vvdebug','type');
if(q==='0')localStorage.removeItem('vvdebug');
if(localStorage.getItem('vvdebug')!=='type')return;
const box=document.createElement('div');
box.style.cssText='position:fixed;left:6px;right:6px;top:120px;z-index:2147483647;background:rgba(0,0,0,.9);color:#7CFC9A;font:9.5px/1.3 ui-monospace,Menlo,monospace;padding:6px 8px;border-radius:8px;border:1px solid #7CFC9A;pointer-events:none;white-space:pre;max-height:70vh;overflow:hidden;';
box.textContent='type mode: tap search, type, then close the keyboard';
document.body.appendChild(box);
let log=[],t0=0,lastEl=null,elN=0,lastV=null,lastC=null,urdN=0;
const T=()=>String(Math.round(performance.now()-t0)).padStart(5);
const isS=e=>e&&e.classList&&e.classList.contains('search-input');
const cur=i=>i.selectionStart===i.selectionEnd?String(i.selectionStart):i.selectionStart+'-'+i.selectionEnd;
const add=s=>{log.push(s);if(log.length>400)log.shift()};
const ssr=HTMLInputElement.prototype.setSelectionRange;
HTMLInputElement.prototype.setSelectionRange=function(a,b,c){if(isS(this))add(T()+' SETSEL->'+a+' (was '+cur(this)+') v='+JSON.stringify(this.value));return ssr.call(this,a,b,c)};
document.addEventListener('focusin',e=>{if(!isS(e.target))return;if(e.target!==lastEl){elN++;lastEl=e.target}
 if(!t0||!log.length){t0=performance.now()}add(T()+' FOCUS el#'+elN+' v='+JSON.stringify(e.target.value)+' c='+cur(e.target))},true);
document.addEventListener('beforeinput',e=>{if(isS(e.target))add(T()+' before '+e.inputType+' '+JSON.stringify(e.data)+' c='+cur(e.target))},true);
document.addEventListener('input',e=>{if(!isS(e.target))return;const i=e.target;if(i!==lastEl){elN++;lastEl=i;add(T()+' NEW INPUT ELEMENT el#'+elN)}
 add(T()+' input '+(e.inputType||'')+' v='+JSON.stringify(i.value)+' c='+cur(i));lastV=i.value;lastC=cur(i)},true);
document.addEventListener('selectionchange',()=>{const i=document.activeElement;if(!isS(i))return;const c=cur(i);
 if(i.value===lastV&&c===lastC)return;if(i.value!==lastV&&lastV!==null&&i.value.length!==lastV.length){}add(T()+' cursor '+c+' v='+JSON.stringify(i.value));lastV=i.value;lastC=c});
const mo=new MutationObserver(()=>{const u=document.getElementById('_urd');const n=u?u.querySelectorAll('*').length:-1;if(n!==urdN){urdN=n;add(T()+' tags changed ('+n+')')}
 const i=document.querySelector('.search-input');if(i&&i!==lastEl&&lastEl){elN++;lastEl=i;add(T()+' INPUT REPLACED el#'+elN+' v='+JSON.stringify(i.value))}});
mo.observe(document.body,{childList:true,subtree:true});
document.addEventListener('focusout',e=>{if(!isS(e.target))return;add(T()+' BLUR v='+JSON.stringify(e.target.value));
 setTimeout(()=>{const lines=log.slice(-48);box.textContent='TYPING RECORDING ('+log.length+' events, last '+lines.length+'):\n'+lines.join('\n');log=[];t0=0},50)},true);
}catch(e){}})();
'''

open(dst, 'w', encoding='utf-8').write(content + REC)
print('Wrote ' + dst)
