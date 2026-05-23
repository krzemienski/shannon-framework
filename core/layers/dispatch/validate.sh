#!/usr/bin/env bash
# DispatchLayer validate.sh — exercise open-tasks tracker + isMidAction regex.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
SHANNON_LOG_DIR="${SHANNON_LOG_DIR:-/tmp/shannon-validate-dispatch}"
rm -rf "$SHANNON_LOG_DIR"
mkdir -p "$SHANNON_LOG_DIR"
export SHANNON_LOG_DIR
cd "$ROOT"

OUT=$(node -e "
process.env.SHANNON_LOG_DIR='$SHANNON_LOG_DIR';
delete require.cache[require.resolve('./core/layers/dispatch/module.js')];
const m=require('./core/layers/dispatch/module.js');
m.appendOpenTask('task-001');
m.appendOpenTask('task-002');
m.appendOpenTask('task-001');
const after = m.readOpenTasks();
m.removeOpenTask('task-001');
const final = m.readOpenTasks();
const midA = m.isMidAction('Let me now investigate the next file');
const midB = m.isMidAction('All done, ready for review.');
console.log(JSON.stringify({afterAppend: after, finalCount: final.length, midA, midB, ironLen: m.IRON_RULE.length}));
")
echo "DispatchLayer probe: $OUT"

# Assert: dedup worked (afterAppend should have 2 entries), remove worked (finalCount=1), midA true, midB false.
node -e "
let d='';
process.stdin.on('data',c=>d+=c);
process.stdin.on('end',()=>{
  const j=JSON.parse(d);
  const errs=[];
  if(j.afterAppend.length!==2) errs.push('expected 2 tasks after dedup, got '+j.afterAppend.length);
  if(j.finalCount!==1) errs.push('expected 1 task after remove, got '+j.finalCount);
  if(!j.midA) errs.push('isMidAction should match \"Let me now\"');
  if(j.midB) errs.push('isMidAction should NOT match \"All done\"');
  if(j.ironLen<200) errs.push('IRON_RULE too short: '+j.ironLen);
  if(errs.length){console.error('FAIL: '+errs.join('; ')); process.exit(1);}
  console.log('asserts OK');
});
" <<<"$OUT"

echo "PASS: DispatchLayer — open-tasks tracker + isMidAction + IRON_RULE all OK"
