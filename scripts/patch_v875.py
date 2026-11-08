#!/usr/bin/env python3
"""Patch v873 -> v875 (v874 was a temporary viewport readout, never kept): on iPhone, tapping the search bar
while scrolled down sometimes slid the sticky header and search bar off the top of the screen.

Cause: the feed loads 10 posts at a time, so a scrolled-down reader is usually near the bottom of the page.
When the keyboard opens, Safari moves the page; if it can't scroll any further down, it pans the visible area
instead, carrying the sticky header and search bar out of view. v874's readout appended a 100lvh measuring box
to the bottom of the page, which gave Safari that room, and the bug vanished while it was live.

Fix: on iPhone only, while the search bar is being tapped or is focused, add one screen of invisible space
below the page. It's added on touchstart, before Safari handles the focus, and removed when search loses focus.
"""
import sys

src = '_deploy/assets/index-DUcNPOLc-v873.js'
dst = '_deploy/assets/index-DUcNPOLc-v875.js'

content = open(src, encoding='utf-8').read()

FIX = r'''
;(()=>{try{
if(!(window.CSS&&CSS.supports&&CSS.supports('-webkit-touch-callout','none')))return;
const room=document.createElement('div');
room.setAttribute('aria-hidden','true');
room.style.cssText='position:absolute;left:0;width:1px;height:100lvh;visibility:hidden;pointer-events:none;display:none';
document.body.appendChild(room);
const isSearch=t=>!!(t&&t.closest&&t.closest('.search-input'));
let tm=0;
const show=()=>{clearTimeout(tm);room.style.display='block'};
const hideSoon=()=>{clearTimeout(tm);tm=setTimeout(()=>{if(!isSearch(document.activeElement))room.style.display='none'},400)};
document.addEventListener('touchstart',e=>{if(isSearch(e.target)){show();hideSoon()}},{passive:true,capture:true});
document.addEventListener('focusin',e=>{if(isSearch(e.target))show()},true);
document.addEventListener('focusout',e=>{if(isSearch(e.target))hideSoon()},true);
}catch(e){}})();
'''

if '-webkit-touch-callout\',\'none\'' in content and 'aria-hidden\',\'true\');\nroom' in content:
    print('FAIL: fix already present')
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write(content + FIX)
print('Wrote ' + dst)
