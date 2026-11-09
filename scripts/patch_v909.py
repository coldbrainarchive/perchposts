#!/usr/bin/env python3
"""Patch v908 -> v909: mod panel bans are account-only by default.
- Ban sends username + browser only (it used to send the IP too, which banned everyone on that network,
  mods included). The worker now only stores an IP when ban_ip is set.
- New "🌐 Ban IP" button (with a warning) for repeat offenders making new accounts: account + IP.
- The panel's banned / caged labels only match on a real username or browser id (blank ids and shared IPs
  no longer mark other members as banned/caged). Unban still clears IP bans for that member's IP.
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v908.js'
dst = '_deploy/assets/index-DUcNPOLc-v909.js'
content = open(src, encoding='utf-8').read()
errors = []
def patch(old, new, label):
    global content
    n = content.count(old)
    if n != 1: errors.append('FAIL (' + label + '): found ' + str(n))
    else: content = content.replace(old, new); print('OK: ' + label)

patch('be=e=>a.some(t=>t.browser_id===e.browser_id||t.ip_hash===e.ip_hash||t.username===e.username)',
      'be=e=>a.some(t=>(!!t.username&&t.username===e.username)||(!!t.browser_id&&t.browser_id===e.browser_id))',
      'banned label: real matches only')
patch('Se=e=>s.some(t=>t.browser_id===e.browser_id||t.ip_hash===e.ip_hash||t.username===e.username)',
      'Se=e=>s.some(t=>(!!t.username&&t.username===e.username)||(!!t.browser_id&&t.browser_id===e.browser_id))',
      'caged label: real matches only')
patch(':await zr({type:`ban`,browser_id:e.browser_id,username:e.username,ip_hash:e.ip_hash}),_e()}',
      ':await zr({type:`ban`,browser_id:e.browser_id,username:e.username}),_e()},'
      '_banIp=async e=>{if(!e.ip_hash){alert(`No IP on record for this bird yet.`);return}'
      'if(!confirm(`Ban ${e.username||`this bird`} AND their IP?\\n\\nThis blocks every non-mod account on that network too (same Wi-Fi, school, café or mobile carrier). Use it for someone who keeps making new accounts.`))return;'
      'await zr({type:`ban`,browser_id:e.browser_id,username:e.username,ip_hash:e.ip_hash,ban_ip:!0}),_e()}',
      'ban: account only + Ban IP')
patch("(0,L.jsx)(`button`,{onClick:()=>xe(o),style:{padding:`2px 8px`,borderRadius:6,border:`none`,background:s?`#1f2937`:`#7f1d1d`,color:s?`#f8fafc`:`#fca5a5`,fontWeight:600,cursor:`pointer`,fontSize:10},children:s?`Unban`:`Ban`})]}),",
      "(0,L.jsx)(`button`,{onClick:()=>xe(o),style:{padding:`2px 8px`,borderRadius:6,border:`none`,background:s?`#1f2937`:`#7f1d1d`,color:s?`#f8fafc`:`#fca5a5`,fontWeight:600,cursor:`pointer`,fontSize:10},children:s?`Unban`:`Ban`}),"
      "!s&&(0,L.jsx)(`button`,{onClick:()=>_banIp(o),title:`Ban this account and its IP (blocks everyone on that network)`,style:{padding:`2px 8px`,borderRadius:6,border:`1px solid #7f1d1d`,background:`transparent`,color:`#fca5a5`,fontWeight:600,cursor:`pointer`,fontSize:10},children:`🌐 Ban IP`})]}),",
      'Ban IP button')
if errors: print('\n'.join(errors)); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
