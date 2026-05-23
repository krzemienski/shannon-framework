#!/usr/bin/env node
// PreToolUse Edit|MultiEdit — advisory reminder to Read first.
const { runHook } = require('../lib/hook-runner');

runHook('read-before-edit', (payload) => {
  const toolInput = (payload && payload.tool_input) || {};
  const filePath = toolInput.file_path || '';
  if (!filePath) return { decision: 'allow', exitCode: 0 };
  // Advisory only — CC tracks Read state internally; this is a soft hint.
  return {
    decision: 'allow',
    exitCode: 0,
    stderrPayload: `[shannon] read-before-edit: confirm you Read "${filePath}" before editing (stale context risk).\n`,
  };
});
