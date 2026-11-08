#!/usr/bin/env python3
"""Patch v806 -> v807:
Safari on iPhone: the chat could freeze on and off after the keyboard closed. Ruled out: touch
handlers (all passive) and the 2s refresh (no DOM or layout work when nothing changed). Suspected: iOS
leaves the page shifted after the keyboard closes (WebKit bug 300523), so swipes move the page instead
of the messages. Once the keyboard is down, clear any leftover shift, at most once per keyboard close.
Does nothing when there's no shift, and skips Chrome on iOS, whose page is meant to scroll.

Temporary: ?vvdebug=1 shows the shift, how many resets ran, and "stuck": swipes on the messages that
moved the finger but not the list. Remove once the freeze is solved.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v806.js'
dst = '_deploy/assets/index-DUcNPOLc-v807.js'

q = chr(0x60)
content = open(src, encoding='utf-8').read()
errors = []

def patch(old, new, label, count=1):
    global content
    n = content.count(old)
    if n != count:
        errors.append('FAIL (' + label + '): expected ' + str(count) + ' matches, found ' + str(n))
    else:
        content = content.replace(old, new)
        print('OK: ' + label)

def t(s):
    return s.replace('`', q)

setup = (
 '_rc=0,_ro=0,_rt=0,_rd=!1,'
 '_rs=()=>{if(!_vv||_h.classList.contains(`chat-crios`))return;if(_vv.height<window.innerHeight-60){_rd=!1;return}'
 'let _o=_vv.pageTop||_vv.offsetTop||window.scrollY;if(!_o||_rd)return;_rd=!0;_rc++;_ro=_o;window.scrollTo(0,0);_f()},'
 '_dv=/vvdebug/.test(location.search),_st=0,_ty=0,_tt=0,'
 '_ds=()=>{if(!_dv)return;let _e=document.getElementById(`vvd`);'
 'if(!_e){_e=document.createElement(`div`);_e.id=`vvd`;_e.style.cssText=`position:fixed;top:8px;left:8px;right:8px;z-index:99999;background:#000;color:#0f0;font:12px/1.4 monospace;padding:6px;white-space:pre-wrap;pointer-events:none`;document.body.appendChild(_e)}'
 '_e.textContent=`v807 vv ${_vv?.height} top ${_vv?.offsetTop} page ${_vv?.pageTop}\\ninner ${window.innerHeight} y ${window.scrollY} focus ${document.activeElement?.tagName}\\nresets ${_rc} last ${_ro} stuck ${_st} list ${Math.round(D.current?.scrollTop||0)}`},'
 '_tsd=_e=>{_ty=_e.touches[0].clientY;_tt=D.current?.scrollTop},'
 '_tmv=_e=>{let _w=D.current,_y2=_e.touches[0].clientY;if(!_w||!_w.contains(_e.target)||Math.abs(_y2-_ty)<30)return;let _s=_w.scrollTop;'
 'if(_s===_tt&&_s!==0&&Math.abs(_s)+_w.clientHeight<_w.scrollHeight-1)_st++;_ty=_y2;_tt=_s;_ds()},'
)
patch(t('_vv=window.visualViewport,_r=0,_ts=[],_f=()=>{cancelAnimationFrame(_r);'),
      t('_vv=window.visualViewport,_r=0,_ts=[],' + setup + '_f=()=>{cancelAnimationFrame(_r);if(!_rt)_rt=setTimeout(()=>{_rt=0;_rs()},450);'),
      'clear the leftover shift, freeze counter')
patch(t('_fo=()=>{_f();_ts.forEach(clearTimeout);'),
      t('_fo=()=>{_rd=!1;_f();_ts.forEach(clearTimeout);'),
      'allow one reset per keyboard close')
patch(t('.test(document.activeElement?.tagName||``))})}'),
      t('.test(document.activeElement?.tagName||``));_ds()})}'),
      'update the readout')
patch(t('_fo();document.addEventListener(`focusin`,_fo);'),
      t('_fo();if(_dv){document.addEventListener(`touchstart`,_tsd,{passive:!0});document.addEventListener(`touchmove`,_tmv,{passive:!0})}document.addEventListener(`focusin`,_fo);'),
      'watch swipes with the readout on')
patch(t('return()=>{cancelAnimationFrame(_r);_ts.forEach(clearTimeout);'),
      t('return()=>{cancelAnimationFrame(_r);clearTimeout(_rt);_ts.forEach(clearTimeout);document.removeEventListener(`touchstart`,_tsd);document.removeEventListener(`touchmove`,_tmv);document.getElementById(`vvd`)?.remove();'),
      'clean up on close')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)

base = open(src, encoding='utf-8').read()
p_delta = (content.count('(') - content.count(')')) - (base.count('(') - base.count(')'))
b_delta = (content.count('{') - content.count('}')) - (base.count('{') - base.count('}'))
print('Paren delta: ' + str(p_delta) + ', Brace delta: ' + str(b_delta))
open(dst, 'w', encoding='utf-8').write(content)
print('Wrote ' + dst)
