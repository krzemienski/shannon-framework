#!/usr/bin/env node
// PreToolUse TaskUpdate — inject 5-question evidence checklist on status:completed.
const { runHook } = require('../lib/hook-runner');

const CHECKLIST = [
  '[shannon] evidence-gate before marking TaskUpdate status:completed:',
  '  1. READ the actual evidence file (not just a report about it)?',
  '  2. VIEW the actual screenshot (not just confirm it exists)?',
  '  3. EXAMINE actual command output (not just exit code)?',
  '  4. CITE specific evidence for each validation criterion?',
  '  5. Would a skeptical reviewer agree this is complete?',
  'If any answer is "no" → REFUSE completion. Build evidence first.',
  '',
].join('\n');

runHook('evidence-gate-reminder', (payload) => {
  const toolInput = (payload && payload.tool_input) || {};
  const status = toolInput.status || '';
  if (status !== 'completed') return { decision: 'allow', exitCode: 0 };
  return { decision: 'allow', exitCode: 2, stderrPayload: CHECKLIST };
});
