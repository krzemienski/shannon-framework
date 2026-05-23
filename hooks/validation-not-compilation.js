#!/usr/bin/env node
// PostToolUse Bash — reminder when build commands succeed.
const { runHook } = require('../lib/hook-runner');

const BUILD_CMDS = /\b(npm run build|pnpm build|yarn build|cargo build|go build|make build|xcodebuild|gradle build|mvn package|tsc)\b/i;
const SUCCESS = /(build (succeeded|complete|successful)|compiled successfully|0 errors|✓ built|Build SUCCESSFUL)/i;

runHook('validation-not-compilation', (payload) => {
  const tin = (payload && payload.tool_input) || {};
  const tres = (payload && (payload.tool_result || payload.tool_response)) || {};
  const cmd = String(tin.command || '');
  const out = typeof tres === 'string' ? tres : String((tres.stdout || tres.output || ''));
  if (!BUILD_CMDS.test(cmd)) return { decision: 'allow', exitCode: 0 };
  if (!SUCCESS.test(out)) return { decision: 'allow', exitCode: 0 };
  return {
    decision: 'allow',
    exitCode: 2,
    stderrPayload: '[shannon] validation-not-compilation: build succeeded, but compilation is NOT functional validation. Invoke /shannon:validate to verify through real interfaces.\n',
  };
});
