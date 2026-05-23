#!/usr/bin/env node
// Two-tier skill-activation benchmark.
// Tier 1 Recall: every cached trigger x {terse, wrapped} -> target skill must match.
// Tier 2 Precision: innocent-corpus prompts must match NOTHING.
// Out: <prefix>.jsonl (per-prompt rows) + <prefix>-summary.json (per-skill metrics).

const fs = require('fs');
const path = require('path');
const HERE = __dirname;
const FRAMEWORK = path.resolve(HERE, '..');
const { matchSkills } = require(path.join(FRAMEWORK, 'core/layers/invocation/module.js'));
const INNOCENT = require(path.join(HERE, 'innocent-corpus.json'));
const TRIGGERS_PATH = path.join(process.env.HOME, '.claude/logs/shannon/skill-triggers.json');
const TRIGGERS_DB = JSON.parse(fs.readFileSync(TRIGGERS_PATH, 'utf-8')).skills;

const args = Object.fromEntries(process.argv.slice(2).map(a => { const [k,v]=a.split('='); return [k, v??true]; }));
const OUT_PREFIX = args.out || path.join(HERE, 'results', `baseline-${Date.now()}`);
fs.mkdirSync(path.dirname(OUT_PREFIX), { recursive: true });

const WRAPS = [t=>`Hey, can you ${t} for me?`, t=>`I would like to ${t} now.`, t=>`Please ${t} when you can.`];
const wrap = t => WRAPS[t.length % WRAPS.length](t);

const rows = [];
const stat = {};
const S = s => (stat[s] = stat[s] || {hit:0,total:0,fp:0});

for (const [skill, triggers] of Object.entries(TRIGGERS_DB)) {
  S(skill);
  for (const raw of triggers) {
    const trig = String(raw).replace(/^["'\s]+|["'\s]+$/g,'').toLowerCase();
    if (!trig) continue;
    for (const v of [{variant:'terse',prompt:trig},{variant:'wrapped',prompt:wrap(trig)}]) {
      const m = matchSkills(v.prompt).map(x=>x.skill);
      const hit = m.includes(skill);
      const spurious = m.filter(s=>s!==skill);
      rows.push({tier:'recall',skill,trigger:trig,variant:v.variant,prompt:v.prompt,matched:m,target_hit:hit,spurious});
      S(skill).total++; if (hit) S(skill).hit++;
      spurious.forEach(sp=>S(sp).fp++);
    }
  }
}

const innocentFP = [];
for (const prompt of INNOCENT.prompts) {
  const m = matchSkills(prompt);
  rows.push({tier:'precision',variant:'innocent',prompt,matched:m.map(x=>x.skill),target_hit:m.length===0,spurious:m.map(x=>`${x.skill}:${x.trigger}`)});
  if (m.length) { innocentFP.push({prompt, fired:m}); m.forEach(x=>S(x.skill).fp++); }
}

fs.writeFileSync(OUT_PREFIX+'.jsonl', rows.map(r=>JSON.stringify(r)).join('\n')+'\n');

const recallRows = rows.filter(r=>r.tier==='recall');
const recallHits = recallRows.filter(r=>r.target_hit).length;
const cleanInn = INNOCENT.prompts.length - innocentFP.length;
const perSkill = Object.entries(stat).map(([s,st])=>{
  const recall = st.total? st.hit/st.total : 0;
  const fires = st.hit + st.fp;
  const precision = fires? st.hit/fires : 1;
  const f1 = (precision+recall)? 2*precision*recall/(precision+recall) : 0;
  return {skill:s, hit:st.hit, total:st.total, recall:+recall.toFixed(3), fp:st.fp, precision:+precision.toFixed(3), f1:+f1.toFixed(3)};
}).sort((a,b)=>a.f1-b.f1);

const summary = {
  run_ts:new Date().toISOString(), framework_root:FRAMEWORK, total_rows:rows.length,
  global:{ recall:+(recallHits/recallRows.length).toFixed(3), recall_hits:recallHits, recall_total:recallRows.length,
           innocent_precision:+(cleanInn/INNOCENT.prompts.length).toFixed(3), innocent_clean:cleanInn,
           innocent_total:INNOCENT.prompts.length, innocent_fp:innocentFP.length },
  per_skill:perSkill, innocent_false_positives:innocentFP,
};
fs.writeFileSync(OUT_PREFIX+'-summary.json', JSON.stringify(summary,null,2));

console.log('=== BASELINE ===');
console.log(`rows: ${rows.length}`);
console.log(`recall: ${(summary.global.recall*100).toFixed(1)}% (${recallHits}/${recallRows.length})`);
console.log(`innocent-clean: ${(summary.global.innocent_precision*100).toFixed(1)}% (${cleanInn}/${INNOCENT.prompts.length})  FPs=${innocentFP.length}`);
console.log('\n--- bottom 8 by F1 ---');
perSkill.slice(0,8).forEach(s=>console.log(`  ${s.skill.padEnd(26)} F1=${s.f1.toFixed(2)} R=${s.recall.toFixed(2)} P=${s.precision.toFixed(2)} fp=${s.fp}`));
console.log('\n--- innocent false positives ---');
innocentFP.slice(0,12).forEach(fp=>{ console.log(`  "${fp.prompt.slice(0,52)}"`); fp.fired.forEach(f=>console.log(`     -> ${f.skill} (trigger: "${f.trigger}")`)); });
console.log(`\nresults: ${OUT_PREFIX}.jsonl`);
console.log(`summary: ${OUT_PREFIX}-summary.json`);
