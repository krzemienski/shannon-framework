#!/usr/bin/env node
// PreToolUse Task|Agent — inject IRON RULE into subagent prompt.
const { runHook } = require('../lib/hook-runner');
const { IRON_RULE } = require('../core/layers/dispatch/module.js');

runHook('subagent-governance-inject', () => ({
  decision: 'allow',
  exitCode: 2,
  stderrPayload: `${IRON_RULE}\n`,
}));
