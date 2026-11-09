#!/usr/bin/env python3
"""Patch v909 -> v910: caged birds show the empty nest 🪹 everywhere, including the big bird at the top of
the Notifications / Your Nest screen, the BIRD card on profiles and the header button.
- Jn() returned a bare string for caged (🪹), banned (❌) and bots (🤖); the big-bird displays read .e from
  an object and fell back to a default bird. It now returns {e, f, s} objects like every other bird.
- The caged/banned name lists are cached in localStorage (_bl) so they're known on the very first render
  (the header drew before the list arrived), and refreshed from the server each load (clearing anyone
  who's been released).
"""
import sys
src = '_deploy/assets/index-DUcNPOLc-v909.js'
dst = '_deploy/assets/index-DUcNPOLc-v910.js'
content = open(src, encoding='utf-8').read()
errors = []
def patch(old, new, label):
    global content
    n = content.count(old)
    if n != 1: errors.append('FAIL (' + label + '): found ' + str(n))
    else: content = content.replace(old, new); print('OK: ' + label)
patch("if(e.username&&_jailed.has(e.username))return`🪹`;if(e.username&&_banned.has(e.username))return`❌`;if(e.browser_id&&String(e.browser_id).startsWith(`bot-`))return`🤖`;",
      "if(e.username&&_jailed.has(e.username))return{e:`🪹`,f:``,s:null,caged:!0};if(e.username&&_banned.has(e.username))return{e:`❌`,f:``,s:null,banned:!0};if(e.browser_id&&String(e.browser_id).startsWith(`bot-`))return{e:`🤖`,f:``,s:null,bot:!0};",
      'Jn: objects for caged/banned/bots')
patch("var _jailed=new Set(),_banned=new Set();",
      "var _jailed=new Set(),_banned=new Set();try{var _blc=JSON.parse(localStorage.getItem(`_bl`)||`null`);if(_blc){(_blc.j||[]).forEach(function(u){_jailed.add(u)});(_blc.b||[]).forEach(function(u){_banned.add(u)})}}catch(_){}",
      'ban lists: load cached')
patch("(d.jailed||[]).forEach(function(u){{_jailed.add(u)}});(d.banned||[]).forEach(function(u){{_banned.add(u)}})",
      "_jailed.clear();_banned.clear();(d.jailed||[]).forEach(function(u){{_jailed.add(u)}});(d.banned||[]).forEach(function(u){{_banned.add(u)}});try{localStorage.setItem(`_bl`,JSON.stringify({j:d.jailed||[],b:d.banned||[]}))}catch(_){}",
      'ban lists: refresh + cache')
if errors: print('\n'.join(errors)); sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content); print('Wrote ' + dst)
