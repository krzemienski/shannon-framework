#!/usr/bin/env node
// Stop * — defer Stop if open tasks exist + last assistant text suggests mid-action.
const { runHook } = require('../lib/hook-runner');
const { readOpenTasks, isMidAction } = require('../core/layers/dispatch/module.js');

runHook('stop-task-semantics', (payload) => {
  const open = readOpenTasks();
  const lastText = (payload && (payload.last_assistant_text || payload.assistant_text || '')) || '';
  if (!open.length) return { decision: 'allow', exitCode: 0 };
  if (!isMidAction(lastText)) return { decision: 'allow', exitCode: 0 };
  return {
    decision: 'allow',
    exitCode: 2,
    stderrPayload: `[shannon] stop-task-semantics: Stop deferred — ${open.length} open task(s) + mid-action phrasing detected. Complete or update tasks before stopping.\n`,
  };
});
