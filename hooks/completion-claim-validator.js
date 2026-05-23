#!/usr/bin/env node
// PostToolUse Bash — catch "build succeeded" claims without subsequent functional validation.
const { runHook } = require('../lib/hook-runner');

const CLAIM = /\b(it works|all done|complete|finished|shipped|ready to ship|ready for review|done!)\b/i;

runHook('completion-claim-validator', (payload) => {
  const tres = (payload && (payload.tool_result || payload.tool_response)) || {};
  const out = typeof tres === 'string' ? tres : String((tres.stdout || tres.output || ''));
  if (!CLAIM.test(out)) return { decision: 'allow', exitCode: 0 };
  return {
    decision: 'allow',
    exitCode: 2,
    stderrPayload: '[shannon] completion-claim-validator: completion-style phrase detected in output. Verify with cited evidence (screenshot path, log line, response body) before claiming done.\n',
  };
});
