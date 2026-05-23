#!/usr/bin/env node
// HookLayer — PreToolUse / PostToolUse mechanical enforcement dispatcher.
// Per SHANNON-V6-ARCHITECTURE.md §4. Not a hook itself; this module is the
// dispatch table the individual hook scripts in hooks/*.js consult to know
// which enforcement to run.
//
// Domain contributions:
//   - Validation: block-fab-files, validation-not-compilation, evidence-gate-reminder,
//     fab-pattern-detection, evidence-quality-check
//   - Completion: evidence-gate-reminder (TaskUpdate)
//   - Dispatch: subagent-governance-inject
//   - Planning: plan-before-execute (advisory; lives in skill, not hook)

const path = require('path');
const fs = require('fs');

// Authoritative dispatch table — mirrors hooks/hooks.json. Used by validate.sh
// to confirm every spec'd hook has a backing script on disk.
const DISPATCH = {
  PreToolUse: [
    { matcher: 'Write|Edit|MultiEdit', script: 'block-fab-files.js' },
    { matcher: 'Edit|MultiEdit', script: 'read-before-edit.js' },
    { matcher: 'TaskUpdate', script: 'evidence-gate-reminder.js' },
    { matcher: 'Task|Agent', script: 'subagent-governance-inject.js' },
  ],
  PostToolUse: [
    { matcher: 'Bash', script: 'validation-not-compilation.js' },
    { matcher: 'Bash', script: 'validation-skill-tripwire.js' },
    { matcher: 'Bash', script: 'completion-claim-validator.js' },
    { matcher: 'Edit|Write|MultiEdit', script: 'fab-pattern-detection.js' },
    { matcher: 'Edit|Write|MultiEdit', script: 'evidence-quality-check.js' },
    { matcher: 'TaskCreate|TaskUpdate', script: 'task-list-tracker.js' },
    { matcher: '*', script: 'hooks-fired-log.js' },
  ],
};

function listExpectedScripts() {
  const out = new Set();
  for (const event of Object.keys(DISPATCH)) {
    for (const entry of DISPATCH[event]) out.add(entry.script);
  }
  return Array.from(out);
}

function verifyScriptsExist(hooksDir) {
  const missing = [];
  for (const s of listExpectedScripts()) {
    const p = path.join(hooksDir, s);
    if (!fs.existsSync(p)) missing.push(s);
  }
  return missing;
}

module.exports = { DISPATCH, listExpectedScripts, verifyScriptsExist };

if (require.main === module) {
  const hooksDir = path.join(__dirname, '../../../hooks');
  const missing = verifyScriptsExist(hooksDir);
  if (missing.length) {
    console.error(`HookLayer: ${missing.length} expected script(s) missing in ${hooksDir}:`);
    missing.forEach(m => console.error(`  - ${m}`));
    process.exit(1);
  }
  console.log(`HookLayer OK — ${listExpectedScripts().length} HookLayer-bound scripts present`);
}
