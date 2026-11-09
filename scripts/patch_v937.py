#!/usr/bin/env python3
"""Patch v936 -> v937: notifications stay unread until you tap them.
- Opening the notification panel no longer marks everything seen (it set notif_last_seen on open) and the
  bell no longer zeroes the red bubble on tap.
- Each notification stays highlighted and counted until you tap it (tapped ids kept in localStorage
  notif_read; the red bubble = server count since last-seen minus tapped ones).
- The Notifications tab always shows a bar (when there are notifications) with "Mark all read" (clears the
  bubble + highlights, keeps the list) and "Clear all" (empties the list, and marks read). Before, "Clear
  all" only appeared after tapping the tab a second time.
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v936.js'
dst = '_deploy/assets/index-DUcNPOLc-v937.js'
c = open(src, encoding='utf-8').read()
errors = []
def patch(old, new, label):
    global c
    n = c.count(old)
    if n != 1: errors.append(f'FAIL ({label}): {n}')
    else: c = c.replace(old, new); print('OK: ' + label)
patch('(0,_.useEffect)(()=>{localStorage.setItem(`notif_last_seen`,new Date().toISOString())},[]);', '', 'opening panel no longer marks seen')
patch('let t=!!e.time&&e.time>ee.current;', 'let t=!!e.time&&e.time>ee.current&&!_nRead().has(e.id);', 'unread until tapped')
patch('onClick:a,style:{display:`flex`,alignItems:`flex-start`,gap:12,padding:`12px 18px`', 'onClick:()=>{_nMark(e);a()},style:{display:`flex`,alignItems:`flex-start`,gap:12,padding:`12px 18px`', 'tap marks read')
patch('onClick:()=>{p(0),d(!0)}', 'onClick:()=>{d(!0)}', 'bell no longer zeroes bubble')
patch('e.ok&&p((await e.json()).count||0)', 'e.ok&&p(Math.max(0,((await e.json()).count||0)-_nReadSince(t)))', 'bubble minus tapped')
patch('e();let t=setInterval(()=>{document.hidden||e()},3e4);return()=>clearInterval(t)},[])',
      'e();let t=setInterval(()=>{document.hidden||e()},3e4),_nr=()=>e();window.addEventListener(`notif-read`,_nr);return()=>{clearInterval(t);window.removeEventListener(`notif-read`,_nr)}},[])', 'bubble refreshes on read')
patch('_showClear&&c===`notifications`&&(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,justifyContent:`space-between`,padding:`10px 16px 6px`,flexShrink:0,borderBottom:`1px solid rgba(255,255,255,0.06)`},children:[_showClear&&j.length>0&&(0,L.jsx)(`button`,{type:`button`,onClick:async()=>{',
      'c===`notifications`&&j.length>0&&(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,justifyContent:`space-between`,padding:`10px 16px 6px`,flexShrink:0,borderBottom:`1px solid rgba(255,255,255,0.06)`},children:['
      '(0,L.jsx)(`button`,{type:`button`,onClick:()=>{_nAllRead(ee);h(x=>[...x])},style:{background:`none`,border:`none`,color:`#c084fc`,fontSize:12,fontWeight:700,cursor:`pointer`,padding:`2px 6px`,borderRadius:6},children:`Mark all read`}),'
      '(0,L.jsx)(`button`,{type:`button`,onClick:async()=>{', 'always-visible bar + Mark all read')
patch('h([]);},style:{background:`none`,border:`none`,color:`#64748b`,fontSize:12,cursor:`pointer`,padding:`2px 6px`,borderRadius:6},children:`Clear all`})]})',
      'h([]);_nAllRead(ee);},style:{background:`none`,border:`none`,color:`#64748b`,fontSize:12,cursor:`pointer`,padding:`2px 6px`,borderRadius:6},children:`Clear all`})]})', 'clear all also marks read')
JS = r'''
function _nList(){try{return JSON.parse(localStorage.getItem('notif_read')||'[]')}catch(e){return[]}}
function _nRead(){return new Set(_nList().map(x=>x.id))}
function _nReadSince(s){return _nList().filter(x=>x.t>s).length}
function _nMark(n){try{const a=_nList();if(!a.some(x=>x.id===n.id)){a.push({id:n.id,t:n.time||new Date().toISOString()});localStorage.setItem('notif_read',JSON.stringify(a.slice(-400)))}}catch(e){}window.dispatchEvent(new Event('notif-read'))}
function _nAllRead(ref){const now=new Date().toISOString();try{localStorage.setItem('notif_last_seen',now);localStorage.setItem('notif_read','[]')}catch(e){}if(ref)ref.current=now;window.dispatchEvent(new Event('notif-read'))}
'''
if errors: print('\n'.join(errors)); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(c + JS); print('Wrote ' + dst)
