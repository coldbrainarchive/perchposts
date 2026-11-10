#!/usr/bin/env python3
"""Patch v990 -> v991:
- Highlights view has no dates (no dividers, no date on the Pinned heading) when it shows highlight sections;
  the Top / Most replied / Latest / Media filters keep their dates, and Highlights' Latest fallback keeps its.
- Tapping the filter pill while its menu is open closes the menu."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v990.js'
dst = '_deploy/assets/index-DUcNPOLc-v991.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label):
    global c
    if c.count(old) != 1: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
patch('`rdnew`));if(_next){', '`rdnew`));if(_pv&&_cpm===`hl`&&_tpOn);else if(_next){', 'no dividers in Highlights')
patch('if(_np&&_i===_rev.length-1)_st(`📌 Pinned`,_e.created_at)', 'if(_np&&_i===_rev.length-1)_st(`📌 Pinned`,_cpm===`hl`&&_tpOn?null:_e.created_at)', 'no date on Pinned heading')
patch('function _cpMenu(btn,cur,set){document.querySelectorAll(`.cp-menu`).forEach(x=>x.remove());',
      'function _cpMenu(btn,cur,set){const _ex=document.querySelector(`.cp-menu`);if(_ex){_ex._close?_ex._close():_ex.remove();return}', 'pill toggles the menu')
patch('const close=()=>{m.remove();document.removeEventListener(`pointerdown`,out,!0);removeEventListener(`scroll`,close,!0)};',
      'const close=()=>{m.remove();document.removeEventListener(`pointerdown`,out,!0);removeEventListener(`scroll`,close,!0)};m._close=close;', 'expose close')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
