#!/usr/bin/env python3
"""Patch v989 -> v990: chirp preview shows dates for top / most-replied chirps too.
Date dividers now run through every preview view (Highlights' Top chirps / Most replied sections and the
Top / Most replied filters), not just Latest and Media. Since those lists aren't in time order, each chirp
gets its date above it whenever it differs from the one above, and every section starts with a date."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v989.js'
dst = '_deploy/assets/index-DUcNPOLc-v990.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('`rdnew`));if(_pv&&_tpOn&&_i<_nl);else if(_next){', '`rdnew`));if(_next){', 'dates everywhere')
patch('_d2=new Date(_next.created_at).toDateString();if(_d1!==_d2)_out.push(',
      '_d2=new Date(_next.created_at).toDateString();if(_d1!==_d2||(_pv&&(_i===_nR-1||_i===_nl-1)))_out.push(', 'each section starts with a date')
patch('if(String(_out[_out.length-1]?.key).startsWith(`dsep-`))_out.pop();',
      'if(_d&&String(_out[_out.length-1]?.key).startsWith(`dsep-`))_out.pop();', 'keep the date under a dateless title')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
