#!/usr/bin/env node
// UserPromptSubmit → match prompt against cached skill triggers, emit hint.
const { runHook } = require('../lib/hook-runner');
const { matchSkills } = require('../core/layers/invocation/module.js');

runHook('skill-activation-check', (payload) => {
  const prompt = payload && (payload.prompt || payload.user_prompt || payload.text || '');
  const matches = matchSkills(prompt);
  if (!matches.length) return { decision: 'allow', exitCode: 0 };
  const lines = matches.slice(0, 5).map(m => `  • /shannon:${m.skill} (trigger: "${m.trigger}")`);
  return {
    decision: 'allow',
    exitCode: 2,
    stderrPayload: `[shannon] Skill hints (${matches.length} match):\n${lines.join('\n')}\n`,
  };
});
