#!/usr/bin/env python3
"""Patch v1246 -> v1247: the space tags use black line icons instead of emoji (like The Cage and Perch News).
Each icon copies its old emoji's subject: feather (Activity), newspaper (General), football (Sports),
microscope (Science), leaf (Nature), clapperboard (Entertainment), die (Random), megaphone (Announcements).
Huddles gets two chat bubbles instead of 👥, on its tag, its empty screens and the "added to huddle" notification.
Country and region flags stay emoji."""
import sys
src = '_deploy/assets/index-DUcNPOLc-v1246.js'
dst = '_deploy/assets/index-DUcNPOLc-v1247.js'
c = open(src, encoding='utf-8').read()
def patch(old, new, label, n=1):
    global c
    if c.count(old) != n: print('FAIL', label, c.count(old)); sys.exit(1)
    c = c.replace(old, new); print('OK:', label)
HEAD = '<svg class="ri" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
ICONS = {
 'FEATHER': '<path d="M12.67 19a2 2 0 0 0 1.416-.588l6.154-6.172a6 6 0 0 0-8.49-8.49L5.586 9.914A2 2 0 0 0 5 11.328V18a1 1 0 0 0 1 1z"/><path d="M16 8 2 22"/><path d="M17.5 15H9"/>',
 'NEWS': '<path d="M15 18h-5"/><path d="M18 14h-8"/><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-4 0v-9a2 2 0 0 1 2-2h2"/><rect width="8" height="4" x="10" y="6" rx="1"/>',
 'BALL': '<ellipse cx="12" cy="12" rx="10.5" ry="6" transform="rotate(-45 12 12)"/><path d="M9 15l6-6"/><path d="M11 11.5l1.5 1.5"/>',
 'SCOPE': '<path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 1 0 0-14h-1"/><path d="M9 14h2"/><path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z"/><path d="M12 6V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3"/>',
 'LEAF': '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
 'CLAP': '<path d="M20.2 6 3 11l-.9-2.4c-.3-1.1.3-2.2 1.3-2.5l13.5-4c1.1-.3 2.2.3 2.5 1.3Z"/><path d="m6.2 5.3 3.1 3.9"/><path d="m12.4 3.4 3.1 4"/><path d="M3 11h18v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>',
 'DIE': '<rect width="18" height="18" x="3" y="3" rx="3"/><path d="M8 8h.01M16 8h.01M12 12h.01M8 16h.01M16 16h.01"/>',
 'HORN': '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
 'HUDDLE': '<path d="M14.5 8.5c0 3.3-2.9 6-6.5 6-.9 0-1.8-.2-2.6-.5L2.5 15l1-2.6C2.9 11.3 2.5 10 2.5 8.5c0-3.3 2.9-6 6-6s6 2.7 6 6z"/><path d="M17 9.6c2.7.6 4.5 2.8 4.5 5.4 0 1.3-.4 2.5-1.1 3.4l.9 2.6-2.9-1c-.8.3-1.6.5-2.5.5-2.5 0-4.6-1.3-5.5-3.2"/>',
}
add = ''.join('"%s": "%s", ' % (k, (HEAD + v + '</svg>').replace('"', '\\"')) for k, v in ICONS.items())
patch('function _ppIco(k){return ({', 'const _SPK={activity:`FEATHER`,general:`NEWS`,sports:`BALL`,"science-nature":`SCOPE`,nature:`LEAF`,entertainment:`CLAP`,random:`DIE`,announcements:`HORN`,feedback:`HUDDLE`,cage:`CAGE`};function _ppIco(k){return ({' + add, 'new icons + space→icon map')
# drop the emoji from the space list itself so nothing can fall back to them
for slug, em in [('activity','🪶'),('feedback','👥'),('general','📰'),('sports','🏈'),('science-nature','🔬'),('nature','🌿'),('entertainment','🎬'),('random','🎲'),('announcements','📢'),('cage','🪹')]:
    patch('slug:`%s`,icon:`%s`' % (slug, em), 'slug:`%s`,icon:``' % slug, 'no emoji: ' + slug)
# tag pill (every tag, the Spaces list and the search menu go through Ar)
patch("children:[n.slug===`cage`?(0,L.jsx)(`span`,{className:`pp-cage-ic`,\"aria-hidden\":!0,dangerouslySetInnerHTML:{__html:_ppIco(`CAGE`)}})",
      "children:[_SPK[n.slug]?(0,L.jsx)(`span`,{className:`pp-cage-ic`,\"aria-hidden\":!0,dangerouslySetInnerHTML:{__html:_ppIco(_SPK[n.slug])}})",
      'tag pill icons')
# mod panel post rows (grey "<icon> Sports" text)
patch("i&&(0,L.jsxs)(`span`,{style:{color:`#94a3b8`},children:[i.icon,` `,i.name]})",
      "i&&(0,L.jsxs)(`span`,{style:{color:`#94a3b8`,display:`inline-flex`,alignItems:`center`,gap:4},children:[_SPK[i.slug]?(0,L.jsx)(`span`,{className:`pp-sp-ic`,\"aria-hidden\":!0,dangerouslySetInnerHTML:{__html:_ppIco(_SPK[i.slug])}}):null,i.name]})",
      'mod row icons', n=2)
# bot feed tag picker (plain <option> text can't hold an icon)
patch("(0,L.jsxs)(`option`,{value:e.slug,children:[e.icon,` `,e.name]},e.slug)", "(0,L.jsx)(`option`,{value:e.slug,children:e.name},e.slug)", 'feed tag picker')
# Huddles empty screens
patch("(0,L.jsx)(`div`,{style:{fontSize:48,marginBottom:4},children:`👥`})",
      "(0,L.jsx)(`div`,{className:`pp-big-ic`,style:{width:48,height:48,marginBottom:4,color:`#fb923c`},dangerouslySetInnerHTML:{__html:_ppIco(`HUDDLE`)}})", 'sign in to huddle icon')
patch("(0,L.jsx)(`div`,{style:{fontSize:32,marginBottom:12},children:`👥`})",
      "(0,L.jsx)(`div`,{className:`pp-big-ic`,style:{width:32,height:32,margin:`0 auto 12px`,color:`#fb923c`},dangerouslySetInnerHTML:{__html:_ppIco(`HUDDLE`)}})", 'members only icon')
# "You added X to the huddle" notification badge
patch(":e.icon===`SHIELD`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,style:{color:`#f87171`},dangerouslySetInnerHTML:{__html:_ppIco(`SHIELD`)}}):e.icon}",
      ":e.icon===`SHIELD`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,style:{color:`#f87171`},dangerouslySetInnerHTML:{__html:_ppIco(`SHIELD`)}}):e.icon===`👥`?(0,L.jsx)(`span`,{className:`pp-ic n-flap`,style:{color:`#fb923c`},dangerouslySetInnerHTML:{__html:_ppIco(`HUDDLE`)}}):e.icon}",
      'huddle notification badge')
patch("body .lb-ic{", "body .pp-cage-ic svg.ri{display:block}body .pp-sp-ic{display:inline-flex;width:12px;height:12px}body .pp-sp-ic svg{width:100%!important;height:100%!important;stroke-width:2.3}body .pp-big-ic svg{width:100%!important;height:100%!important;display:block;stroke-width:1.8}body .lb-ic{", 'icon styles')
open(dst, 'w', encoding='utf-8').write(c); print('Wrote', dst)
