#!/usr/bin/env node
// UserPromptSubmit → match prompt against cached skill triggers, emit hint.
const { runHook } = require('../lib/hook-runner');
const { matchSkills } = require('../core/layers/invocation/module.js');

// UserPromptSubmit hint protocol:
//   exit 0 + stdout  → context-injected as an advisory hint, prompt CONTINUES.
//   exit 2 + stderr  → blocks the prompt entirely (NOT what we want for hints).
// Earlier versions used exit 2; that produced the "shannon errors all over the
// place" symptom — every advisory hint hard-blocked the user's prompt. We now
// emit a system-reminder-shaped block to stdout and exit 0 so Claude sees the
// hint but the user's prompt still reaches the model.
runHook('skill-activation-check', (payload) => {
  const prompt = payload && (payload.prompt || payload.user_prompt || payload.text || '');
  const matches = matchSkills(prompt);
  if (!matches.length) return { decision: 'allow', exitCode: 0 };
  const lines = matches.slice(0, 5).map(m => `  • /shannon:${m.skill} (trigger: "${m.trigger}")`);
  return {
    decision: 'allow',
    exitCode: 0,
    stdoutPayload: `<system-reminder>\n[shannon] Skill hints (${matches.length} match):\n${lines.join('\n')}\n</system-reminder>\n`,
  };
});
