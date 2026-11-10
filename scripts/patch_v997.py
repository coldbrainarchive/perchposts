#!/usr/bin/env python3
"""Patch v996 -> v997: bird pills work in any order with Huddles.
- Picking a bird from "Users" in the search dropdown adds their pill to the pills you already have (it used to
  reload the page to that bird alone, dropping Huddles or any other pill).
- In the Huddles space, a bird pill shows every huddle that bird is in (owner or member), not just ones they
  started; the bird's ID card isn't shown above the list there."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v996.js'
dst = '_deploy/assets/index-DUcNPOLc-v997.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('onClick:()=>{a(!1);setUR([]);window.location.href=`/?user=${encodeURIComponent(_u.username)}`;}',
      'onClick:()=>{clearTimeout(c.current?._dbt);a(!1);setUR([]);let n=new URLSearchParams(e);n.set(`user`,_u.username);n.delete(`q`);t(n);r(``);s(null);if(c.current){c.current.value=``;c.current.blur()}}',
      'user pick adds a pill')
patch('.filter(e=>!p||(e.username||``).toLowerCase()===p)',
      '.filter(e=>!p||(e.username||``).toLowerCase()===p||(e.is_huddle&&_hxIn(e,p)))', 'huddle membership match')
patch('p&&(0,L.jsx)(_UserCard,{username:p,record:b[0]||null,',
      'p&&!(u===`feedback`||u===`huddles`)&&(0,L.jsx)(_UserCard,{username:p,record:b[0]||null,', 'no bird card in Huddles')
c += r'''
function _hxIn(post,name){try{const n=String(name||``).toLowerCase();return JSON.parse(post.huddle_members||`[]`).some(x=>{const s=String(typeof x===`string`?x:x&&x.u||``).toLowerCase();return s===n||s.startsWith(n+`:`)})}catch(e){return!1}}
'''
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
