// v1392 -> v1393: strip the OLD post page / OLD huddle page code (unreachable since v1389: the post component
// returns the loader until the chat is open, so the old "chirp preview" mode (_pv) can never be true).
// Scope-aware: only the `let _pv=!_cf&&…` inside the post component (Wr) is folded to false; a different, live `_pv`
// (the chat refresh function in an effect) is left alone. Then constant branches are folded and whole functions that
// nothing references any more are removed.
import fs from 'fs';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const acorn = require('acorn');
const SRC = '_deploy/assets/index-DUcNPOLc-v1392.js', DST = '_deploy/assets/index-DUcNPOLc-v1393.js';
let code = fs.readFileSync(SRC, 'utf8');
const parse = c => acorn.parse(c, { ecmaVersion: 'latest', sourceType: 'module', allowReturnOutsideFunction: true });
const kids = n => { const o = []; for (const k in n) { if (k === 'type' || k === 'start' || k === 'end') continue; const v = n[k]; if (Array.isArray(v)) v.forEach(x => x && typeof x.type === 'string' && o.push(x)); else if (v && typeof v.type === 'string') o.push(v); } return o; };
const isFn = n => /Function/.test(n.type);
const declares = (fn, name) => { // does this function (params or its own body, not nested fns) declare `name`?
  if (fn.params && JSON.stringify(fn.params).includes(`"name":"${name}"`)) return true;
  let hit = false; const walk = n => { if (hit || !n) return; if (n !== fn && isFn(n)) { if (n.type === 'FunctionDeclaration' && n.id && n.id.name === name) hit = true; return; }
    if (n.type === 'VariableDeclarator' && n.id.type === 'Identifier' && n.id.name === name) hit = true; kids(n).forEach(walk); }; walk(fn.body); return hit; };
const edits = [];
const apply = () => { edits.sort((a, b) => b.s - a.s); let last = Infinity; for (const e of edits) { if (e.e > last) continue; code = code.slice(0, e.s) + e.t + code.slice(e.e); last = e.s; } edits.length = 0; };
const findWr = ast => { let wr = null; const w = n => { if (wr || !n) return; if (n.type === 'FunctionDeclaration' && n.id && n.id.name === 'Wr') { wr = n; return; } kids(n).forEach(w); }; w(ast); return wr; };

// 1) _pv -> !1 inside Wr (not in nested functions that declare their own _pv); the declaration becomes `_pv=!1`
{ const ast = parse(code), wr = findWr(ast); let n0 = 0;
  const walk = (n, shadow) => { if (!n) return; if (n !== wr && isFn(n) && declares(n, '_pv')) return; // shadowed subtree
    if (n.type === 'VariableDeclarator' && n.id.name === '_pv') { edits.push({ s: n.init.start, e: n.init.end, t: '!1' }); n0++; return; }
    if (n.type === 'Property' && !n.computed && n.key.type === 'Identifier' && n.shorthand && n.key.name === '_pv') { edits.push({ s: n.start, e: n.end, t: '_pv:!1' }); n0++; return; }
    if (n.type === 'Property' && !n.computed) { walk(n.value); return; }
    if (n.type === 'MemberExpression' && !n.computed) { walk(n.object); return; }
    if (n.type === 'Identifier' && n.name === '_pv') { edits.push({ s: n.start, e: n.end, t: '!1' }); n0++; return; }
    kids(n).forEach(k => walk(k)); };
  walk(wr); apply(); console.log('_pv references folded:', n0); }


// 1b) the old huddle card: the post card block is only for posts now (huddles show the members list instead), so the
// block is skipped for huddles and every `c.is_huddle` / `c?.is_huddle` inside it is false
{ const ast = parse(code), wr = findWr(ast); let call = null, n0 = 0;
  const w = n => { if (call || !n) return; if (n.type === 'CallExpression' && n.callee.type === 'Identifier' && n.callee.name === '_PBlk') { call = n; return; } kids(n).forEach(w); }; w(wr);
  const card = call.arguments[2];
  const walk = n => { if (!n) return; if (isFn(n) && declares(n, 'c')) return;
    if (n.type === 'MemberExpression' && !n.computed && n.object.type === 'Identifier' && n.object.name === 'c' && n.property.name === 'is_huddle') { edits.push({ s: n.start, e: n.end, t: '!1' }); n0++; return; }
    if (n.type === 'ChainExpression' && n.expression.type === 'MemberExpression' && n.expression.object.type === 'Identifier' && n.expression.object.name === 'c' && n.expression.property.name === 'is_huddle') { edits.push({ s: n.start, e: n.end, t: '!1' }); n0++; return; }
    kids(n).forEach(walk); };
  walk(card); edits.push({ s: call.start, e: call.start, t: '!c.is_huddle&&' }); apply(); console.log('huddle-card branches folded:', n0); }

// 2) fold constant branches inside Wr until nothing changes
const isConst = n => n && n.type === 'UnaryExpression' && n.operator === '!' && n.argument.type === 'Literal' && (n.argument.value === 1 || n.argument.value === 0) ? (n.argument.value === 0) : undefined; // !0 -> true, !1 -> false
const truthy = n => { const k = isConst(n); if (k !== undefined) return k; if (n && n.type === 'UnaryExpression' && n.operator === '!') { const j = truthy(n.argument); return j === undefined ? undefined : !j; } return undefined; };
let passes = 0, total = 0;
for (;;) { const ast = parse(code), wr = findWr(ast); let n1 = 0; const src = code;
  const walk = n => { if (!n) return false;
    if (n.type === 'LogicalExpression') { const l = truthy(n.left);
      if (n.operator === '&&' && l === false) { edits.push({ s: n.start, e: n.end, t: '!1' }); n1++; return true; }
      if (n.operator === '&&' && l === true) { edits.push({ s: n.start, e: n.end, t: '(' + src.slice(n.right.start, n.right.end) + ')' }); n1++; return true; }
      if (n.operator === '||' && l === true) { edits.push({ s: n.start, e: n.end, t: '!0' }); n1++; return true; }
      if (n.operator === '||' && l === false) { edits.push({ s: n.start, e: n.end, t: '(' + src.slice(n.right.start, n.right.end) + ')' }); n1++; return true; } }
    if (n.type === 'ConditionalExpression') { const t = truthy(n.test); if (t !== undefined) { const keep = t ? n.consequent : n.alternate; edits.push({ s: n.start, e: n.end, t: '(' + src.slice(keep.start, keep.end) + ')' }); n1++; return true; } }
    if (n.type === 'IfStatement') { const t = truthy(n.test); if (t !== undefined) { const keep = t ? n.consequent : n.alternate; edits.push({ s: n.start, e: n.end, t: keep ? (keep.type === 'BlockStatement' ? src.slice(keep.start, keep.end) : '{' + src.slice(keep.start, keep.end) + '}') : ';' }); n1++; return true; } }
    if (n.type === 'UnaryExpression' && n.operator === '!' && n.argument.type === 'UnaryExpression' && truthy(n.argument) !== undefined && !(n.argument.argument.type === 'Literal')) { }
    let any = false; for (const k of kids(n)) if (walk(k)) any = true; return any; };
  walk(wr); if (!n1) break; apply(); passes++; total += n1; }
console.log('constant branches folded:', total, 'in', passes, 'passes');

// 3) remove top-level functions / consts that nothing references any more (only the known old-page pieces)
for (let round = 0; round < 6; round++) {
  const ast = parse(code); let removed = 0;
  for (const name of ['_ChPanel', '_hxSheetOld', '_cpMenu', '_HxRow', '_CPL', '_hxDotsOld']) {
    const refs = (code.match(new RegExp('(?<![\\w$.])' + name.replace('$', '\\$') + '(?![\\w$])', 'g')) || []).length;
    if (refs !== 1) continue; // only the definition left
    for (const st of ast.body) {
      if (st.type === 'FunctionDeclaration' && st.id.name === name) { edits.push({ s: st.start, e: st.end, t: '' }); removed++; }
      if (st.type === 'VariableDeclaration' && st.declarations.length === 1 && st.declarations[0].id.name === name) { edits.push({ s: st.start, e: st.end, t: '' }); removed++; }
    }
  }
  if (!removed) break; apply(); console.log('round', round, 'removed', removed, 'unused function(s)');
}
fs.writeFileSync(DST, code);
console.log('size', fs.statSync(SRC).size, '->', code.length);
