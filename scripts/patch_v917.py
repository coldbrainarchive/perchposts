#!/usr/bin/env python3
"""Patch v916 -> v917: staff tag colours are consistent everywhere.
- The admin's own chirp flashed purple for a moment after sending: the instant (pending) copy was marked
  is_mod but not is_admin. It now carries is_admin too.
- Tags decided "mod" only from the is_mod flag stored on each post/chirp when it was made, so older posts
  (before someone was promoted) and records without the flag missed the purple. get-ban-lists now also
  returns the current mods/admins; tags (qn, the user pill, chirp headers) also check those lists, so mod
  purple / admin white show on every tag. The lists are cached in localStorage (_bl) for the first render.
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v916.js'
dst = '_deploy/assets/index-DUcNPOLc-v917.js'
content = open(src, encoding='utf-8').read()
errors = []
def patch(old, new, label):
    global content
    n = content.count(old)
    if n != 1: errors.append(f'FAIL ({label}): {n}')
    else: content = content.replace(old, new); print('OK: ' + label)
patch('is_mod:s.is_mod,isPending:!0', 'is_mod:s.is_mod,is_admin:s.is_admin,isPending:!0', 'pending chirp is_admin')
patch('function qn(e){return e?.is_mod===!0}',
      'function qn(e){return e?.is_mod===!0||(!!e?.username&&typeof _modUsers!==`undefined`&&_modUsers.has(String(e.username).toLowerCase()))}', 'qn: current mods')
patch('s=!a&&!o&&e?.is_mod===!0', 's=!a&&!o&&qn(e)', 'user pill: qn')
patch('background:e.is_admin===true?`#ffffff`:h}',
      'background:(e.is_admin===true||(!!e.username&&_adminUsers.has(String(e.username).toLowerCase())))?`#ffffff`:h}', 'chirp header: current admins')
patch('fetch("https://daboysforumip.coldbrainarchive.workers.dev/get-ban-lists")',
      'try{var _blm=JSON.parse(localStorage.getItem(`_bl`)||`null`);if(_blm){(_blm.m||[]).forEach(function(u){_modUsers.add(String(u).toLowerCase())});(_blm.a||[]).forEach(function(u){_addAdmin(u)})}}catch(_){}'
      'fetch("https://daboysforumip.coldbrainarchive.workers.dev/get-ban-lists")', 'staff lists: load cached')
patch('try{localStorage.setItem(`_bl`,JSON.stringify({j:d.jailed||[],b:d.banned||[]}))}catch(_){}',
      'if(d.mods){_modUsers.clear();d.mods.forEach(function(u){_modUsers.add(String(u).toLowerCase())})}(d.admins||[]).forEach(function(u){_addAdmin(u)});'
      'try{localStorage.setItem(`_bl`,JSON.stringify({j:d.jailed||[],b:d.banned||[],m:d.mods||[],a:d.admins||[]}))}catch(_){}', 'staff lists: refresh + cache')
if errors: print('\n'.join(errors)); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
