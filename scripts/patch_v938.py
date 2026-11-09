#!/usr/bin/env python3
"""Patch v937 -> v938:
- Notification read state syncs across devices: it now lives on the account (worker /notif-read,
  /notif-read-all, and /notif-count returns {count, seen_at, read}). The red bubble count comes from the
  server (already minus tapped ones); each device mirrors seen_at/read into localStorage for highlighting.
  Tapping a notification / Mark all read / Clear all save to the account.
- "Mark all read" / "Clear all" are hidden again until you tap the Notifications tab button (toggle).
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v937.js'
dst = '_deploy/assets/index-DUcNPOLc-v938.js'
c = open(src, encoding='utf-8').read()
errors = []
def patch(old, new, label):
    global c
    n = c.count(old)
    if n != 1: errors.append(f'FAIL ({label}): {n}')
    else: c = c.replace(old, new); print('OK: ' + label)
patch('e.ok&&p(Math.max(0,((await e.json()).count||0)-_nReadSince(t)))', 'if(e.ok){const _j=await e.json();_nSync(_j);p(_j.count||0)}', 'bubble from server state')
patch('c===`notifications`&&j.length>0&&(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,justifyContent:`space-between`,padding:`10px 16px 6px`',
      '_showClear&&c===`notifications`&&j.length>0&&(0,L.jsxs)(`div`,{style:{display:`flex`,alignItems:`center`,justifyContent:`space-between`,padding:`10px 16px 6px`', 'bar only after tapping the tab')
old_js_start = "\nfunction _nList(){"
i = c.index(old_js_start)
c = c[:i] + r'''
function _nList(){try{return JSON.parse(localStorage.getItem('notif_read')||'[]')}catch(e){return[]}}
function _nRead(){return new Set(_nList().map(x=>x.id))}
function _nReadSince(s){return 0}
function _nSync(j){try{if(j&&j.seen_at){localStorage.setItem('notif_last_seen',j.seen_at);localStorage.setItem('notif_read',JSON.stringify((j.read||[]).map(id=>({id,t:''}))))}}catch(e){}}
function _nPost(path,body){try{if(!localStorage.getItem('auth_token'))return;fetch(R+path,{method:'POST',headers:{'Content-Type':'application/json',...er()},body:JSON.stringify(body||{})}).then(()=>window.dispatchEvent(new Event('notif-read'))).catch(()=>{})}catch(e){}}
function _nMark(n){try{const a=_nList();if(!a.some(x=>x.id===n.id)){a.push({id:n.id,t:n.time||''});localStorage.setItem('notif_read',JSON.stringify(a.slice(-400)))}}catch(e){}window.dispatchEvent(new Event('notif-read'));_nPost('/notif-read',{id:n.id,time:n.time||new Date().toISOString()})}
function _nAllRead(ref){const now=new Date().toISOString();try{localStorage.setItem('notif_last_seen',now);localStorage.setItem('notif_read','[]')}catch(e){}if(ref)ref.current=now;window.dispatchEvent(new Event('notif-read'));_nPost('/notif-read-all',{})}
'''
print('OK: helpers now sync with the account')
if errors: print('\n'.join(errors)); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(c); print('Wrote ' + dst)
