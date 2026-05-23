#!/usr/bin/env node
// PostToolUse Edit|Write|MultiEdit — scan written content for fabrication patterns.
const { runHook } = require('../lib/hook-runner');

const FAB_HINTS = [
  /\bjest\.fn\(/i,
  /\bsinon\.stub\b/i,
  /\bvi\.fn\(/i,
  /\bfaker\.(name|address|company)/i,
  /\bMockedFunction\b/,
  /^\s*describe\(\s*['"]/m,
  /^\s*it\(\s*['"]/m,
];

runHook('fab-pattern-detection', (payload) => {
  const tin = (payload && payload.tool_input) || {};
  const content = String(tin.content || tin.new_string || '');
  if (!content) return { decision: 'allow', exitCode: 0 };
  const matched = FAB_HINTS.find(re => re.test(content));
  if (!matched) return { decision: 'allow', exitCode: 0 };
  return {
    decision: 'allow',
    exitCode: 2,
    stderrPayload: `[shannon] fab-pattern-detection: content matches fabrication pattern ${matched}. IRON RULE: build the real system; never wire fake-test scaffolding.\n`,
  };
});
