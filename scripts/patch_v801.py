#!/usr/bin/env python3
"""Patch v800 -> v801:
1. Phones show the chirp count in the chat header too.
2. The preview button just says "View all".
3. Chrome on iPhone left a gap above the keyboard. Re-measure the screen height after focus changes,
   since the keyboard and Chrome's bars can finish moving after the last resize event.
4. Temporary: ?vvdebug=1 on a post shows the measured sizes while the chat is open, to find the cause
   if the gap survives. Nobody sees it without that link. Remove once the gap is solved.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v800.js'
dst = '_deploy/assets/index-DUcNPOLc-v801.js'

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

patch('.chat-count{display:none}@media(min-width:768px){.chat-count{display:inline;flex:none;color:#94a3b8;font-size:13px;font-weight:600;white-space:nowrap;margin-right:10px}}',
      '.chat-count{flex:none;color:#94a3b8;font-size:13px;font-weight:600;white-space:nowrap;margin-right:10px}',
      'count on phones too')
patch(t('children:_cn?`View all ${_cn} chirp${_cn===1?``:`s`}`:`Write the first chirp`'),
      t('children:_cn?`View all`:`Write the first chirp`'),
      'button says View all')

# Sizes readout, only with ?vvdebug
dbg = ('_dg=()=>{if(!/vvdebug/.test(location.search))return;let _e=document.getElementById(`vvd`);'
       'if(!_e){_e=document.createElement(`div`);_e.id=`vvd`;_e.style.cssText=`position:fixed;top:8px;left:8px;right:8px;z-index:99999;background:#000;color:#0f0;font:12px/1.4 monospace;padding:6px;white-space:pre-wrap;pointer-events:none`;document.body.appendChild(_e)}'
       'let _p=_u=>{let _d=document.createElement(`div`);_d.style.cssText=`position:fixed;top:0;width:1px;visibility:hidden;height:100`+_u;document.body.appendChild(_d);let _v=_d.offsetHeight;_d.remove();return _v},'
       '_s=document.querySelector(`.comments-shell`)?.getBoundingClientRect(),_c=document.querySelector(`.chat-compose`)?.getBoundingClientRect();'
       '_e.textContent=`vv ${_vv?.height} top ${_vv?.offsetTop} page ${_vv?.pageTop} scale ${_vv?.scale}\\ninner ${window.innerHeight} client ${_h.clientHeight} screen ${screen.height}\\ndvh ${_p(`dvh`)} svh ${_p(`svh`)} lvh ${_p(`lvh`)}\\nshell ${_s?.top}-${_s?.bottom} box ${_c?.bottom} cvh ${_h.style.getPropertyValue(`--cvh`)}`},')
patch(t('_vv=window.visualViewport,_r=0,_f=()=>{cancelAnimationFrame(_r);'),
      t('_vv=window.visualViewport,_r=0,_ts=[],' ) + dbg + t('_f=()=>{cancelAnimationFrame(_r);'),
      'sizes readout')
patch(t('_h.style.setProperty(`--cvt`,(_vv?_vv.offsetTop:0)+`px`)})};let _tc='),
      t('_h.style.setProperty(`--cvt`,(_vv?_vv.offsetTop:0)+`px`);_dg()})},_fo=()=>{_f();_ts.forEach(clearTimeout);_ts=[100,300,600,1000].map(_d=>setTimeout(_f,_d))};let _tc='),
      're-measure after the keyboard settles')
patch(t('_f();if(_vv){_vv.addEventListener(`resize`,_f);_vv.addEventListener(`scroll`,_f)}'),
      t('_fo();document.addEventListener(`focusin`,_fo);document.addEventListener(`focusout`,_fo);if(_vv){_vv.addEventListener(`resize`,_f);_vv.addEventListener(`scroll`,_f)}'),
      'watch focus changes')
patch(t('return()=>{cancelAnimationFrame(_r);if(_vv){_vv.removeEventListener(`resize`,_f);'),
      t('return()=>{cancelAnimationFrame(_r);_ts.forEach(clearTimeout);document.removeEventListener(`focusin`,_fo);document.removeEventListener(`focusout`,_fo);document.getElementById(`vvd`)?.remove();if(_vv){_vv.removeEventListener(`resize`,_f);'),
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
