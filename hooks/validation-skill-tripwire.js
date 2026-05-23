#!/usr/bin/env node
// PostToolUse Bash — tripwire: build success + no functional-validation skill since last build → stderr + tripwires.jsonl.
const { runHook } = require('../lib/hook-runner');
const { appendTripwire } = require('../core/layers/invocation/module.js');

const BUILD_CMDS = /\b(npm run build|pnpm build|yarn build|cargo build|go build|make build|xcodebuild)\b/i;
const SUCCESS = /(build (succeeded|complete|successful)|compiled successfully|0 errors)/i;

runHook('validation-skill-tripwire', (payload) => {
  const tin = (payload && payload.tool_input) || {};
  const tres = (payload && (payload.tool_result || payload.tool_response)) || {};
  const cmd = String(tin.command || '');
  const out = typeof tres === 'string' ? tres : String((tres.stdout || tres.output || ''));
  if (!BUILD_CMDS.test(cmd) || !SUCCESS.test(out)) return { decision: 'allow', exitCode: 0 };
  appendTripwire({
    ts: new Date().toISOString(),
    event: 'build-success-without-validation',
    command: cmd.slice(0, 200),
  });
  return {
    decision: 'allow',
    exitCode: 2,
    stderrPayload: '[shannon] TRIPWIRE: build succeeded but functional-validation skill has not been invoked since last build. Run /shannon:validate or invoke functional-validation skill before claiming completion.\n',
  };
});
