#!/usr/bin/env node
// DispatchLayer — subagent governance + Stop semantics.
// Per SHANNON-V6-ARCHITECTURE.md §4.

const fs = require('fs');
const path = require('path');
const os = require('os');

const LOG_DIR = process.env.SHANNON_LOG_DIR || path.join(os.homedir(), '.claude/logs/shannon');
const OPEN_TASKS = path.join(LOG_DIR, 'open-tasks.txt');

const IRON_RULE = [
  '# Shannon IRON RULE (injected by DispatchLayer)',
  '',
  '1. NO fabricated artifacts, fixtures, or fake-system files.',
  '2. Build and run the REAL system. Capture evidence under e2e-evidence/.',
  '3. Every PASS/FAIL verdict MUST cite a specific evidence file path.',
  '4. READ a file before EDITING it.',
  '5. If evidence is missing, write REFUSAL.md and stop. No override flag.',
  '',
  '— Shannon v6',
].join('\n');

const MID_ACTION_REGEX = /\b(let me|now i'?ll|next i'?ll|i'?ll now|moving on|let's also|let me also|next step|then i'?ll|going to also)\b/i;

function ensureLogDir() {
  try { fs.mkdirSync(LOG_DIR, { recursive: true }); } catch (_) { /* silent */ }
}

function readOpenTasks() {
  if (!fs.existsSync(OPEN_TASKS)) return [];
  try {
    return fs.readFileSync(OPEN_TASKS, 'utf-8').split('\n').filter(Boolean);
  } catch (_) {
    return [];
  }
}

function appendOpenTask(taskId) {
  if (!taskId) return;
  ensureLogDir();
  const cur = readOpenTasks();
  if (cur.includes(String(taskId))) return;
  try { fs.appendFileSync(OPEN_TASKS, String(taskId) + '\n'); } catch (_) { /* silent */ }
}

function removeOpenTask(taskId) {
  if (!taskId) return;
  const cur = readOpenTasks();
  const next = cur.filter(t => t !== String(taskId));
  try {
    ensureLogDir();
    fs.writeFileSync(OPEN_TASKS, next.length ? next.join('\n') + '\n' : '');
  } catch (_) { /* silent */ }
}

function isMidAction(lastAssistantText) {
  if (!lastAssistantText) return false;
  return MID_ACTION_REGEX.test(lastAssistantText);
}

module.exports = {
  IRON_RULE, MID_ACTION_REGEX, LOG_DIR, OPEN_TASKS,
  readOpenTasks, appendOpenTask, removeOpenTask, isMidAction,
};

if (require.main === module) {
  const open = readOpenTasks();
  console.log(`DispatchLayer OK — ${open.length} open task(s) tracked at ${OPEN_TASKS}`);
  console.log(`IRON_RULE length: ${IRON_RULE.length} chars`);
}
