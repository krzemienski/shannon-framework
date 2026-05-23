#!/usr/bin/env node
// PostToolUse TaskCreate|TaskUpdate — maintain logs/shannon/open-tasks.txt.
const { runHook } = require('../lib/hook-runner');
const { appendOpenTask, removeOpenTask } = require('../core/layers/dispatch/module.js');

runHook('task-list-tracker', (payload) => {
  const tin = (payload && payload.tool_input) || {};
  const tool = String(payload && (payload.tool_name || payload.tool) || '');
  const taskId = tin.taskId || tin.task_id || tin.id || '';
  if (!taskId) return { decision: 'allow', exitCode: 0 };
  if (/TaskCreate/i.test(tool)) {
    appendOpenTask(taskId);
  } else if (/TaskUpdate/i.test(tool)) {
    const status = tin.status || '';
    if (status === 'completed' || status === 'deleted') removeOpenTask(taskId);
    else appendOpenTask(taskId);
  }
  return { decision: 'allow', exitCode: 0 };
});
