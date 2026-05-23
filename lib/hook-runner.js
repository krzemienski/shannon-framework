#!/usr/bin/env node
// Shannon shared hook entry-point.
// Every hook script in hooks/*.js delegates to runHook(scriptName, handler).
// Contract:
//   - parses stdin JSON payload (CC hook input)
//   - try/catch around handler; on crash → process.exit(0), log to hook-errors.jsonl
//   - logs every fire to hooks.jsonl (script, ms, decision, matched tool)
//   - handler returns { decision, exitCode, stderrPayload }
//   - default: { decision: 'allow', exitCode: 0 }
//
// CC hook output protocol:
//   - exit 0 + no stderr     → silent allow
//   - exit 0 + stderr        → advisory; allow continues
//   - exit 2 + stderr        → block (PreToolUse) or feedback (PostToolUse)
//   - JSON stdout with hookSpecificOutput.permissionDecision → permission dialog
//
// Performance budget: <50ms warn, >100ms log to hook-errors.jsonl (slow-fire bucket).

const fs = require('fs');
const path = require('path');
const os = require('os');

const LOG_DIR = process.env.SHANNON_LOG_DIR || path.join(os.homedir(), '.claude/logs/shannon');
const HOOKS_LOG = path.join(LOG_DIR, 'hooks.jsonl');
const HOOK_ERR = path.join(LOG_DIR, 'hook-errors.jsonl');

const MAX_INPUT_BYTES = 2 * 1024 * 1024; // 2MB cap on stdin (matches VF)
const BUDGET_WARN_MS = 50;
const BUDGET_SLOW_MS = 100;

function ensureLogDir() {
  try {
    fs.mkdirSync(LOG_DIR, { recursive: true });
  } catch (_) { /* silent — never break parent */ }
}

function appendJsonl(filePath, record) {
  try {
    ensureLogDir();
    fs.appendFileSync(filePath, JSON.stringify(record) + '\n');
  } catch (_) { /* silent */ }
}

function logFire(record) {
  appendJsonl(HOOKS_LOG, record);
}

function logError(scriptName, err, context) {
  appendJsonl(HOOK_ERR, {
    ts: new Date().toISOString(),
    script: scriptName,
    error: String(err && err.message ? err.message : err),
    stack: err && err.stack ? err.stack : null,
    context: context || null,
  });
}

function writeStderr(msg) {
  if (msg) process.stderr.write(String(msg));
}

function readStdinSync() {
  let buf = '';
  try {
    const chunk = fs.readFileSync(0, 'utf-8');
    if (chunk.length > MAX_INPUT_BYTES) {
      // Oversize → fail-safe; treat as empty payload
      return {};
    }
    buf = chunk;
  } catch (_) {
    return {};
  }
  if (!buf) return {};
  try {
    return JSON.parse(buf);
  } catch (_) {
    return {};
  }
}

function runHook(scriptName, handler) {
  const start = Date.now();
  let payload = {};
  let result = { decision: 'allow', exitCode: 0, stderrPayload: '' };

  try {
    payload = readStdinSync();
  } catch (err) {
    logError(scriptName, err, 'stdin-parse');
    process.exit(0);
    return;
  }

  try {
    const r = handler(payload) || {};
    result = {
      decision: r.decision || 'allow',
      exitCode: typeof r.exitCode === 'number' ? r.exitCode : 0,
      stderrPayload: r.stderrPayload || '',
    };
  } catch (err) {
    logError(scriptName, err, 'handler');
    process.exit(0);
    return;
  }

  const elapsed = Date.now() - start;

  logFire({
    ts: new Date().toISOString(),
    script: scriptName,
    matchedTool: (payload && (payload.tool_name || payload.tool || payload.event)) || null,
    decision: result.decision,
    exitCode: result.exitCode,
    ms: elapsed,
    sessionId: process.env.CLAUDE_SESSION_ID || null,
  });

  if (elapsed > BUDGET_SLOW_MS) {
    appendJsonl(HOOK_ERR, {
      ts: new Date().toISOString(),
      script: scriptName,
      slow: true,
      ms: elapsed,
      budget: BUDGET_SLOW_MS,
    });
  }

  if (result.stderrPayload) writeStderr(result.stderrPayload);
  process.exit(result.exitCode);
}

module.exports = {
  runHook,
  writeStderr,
  logFire,
  logError,
  LOG_DIR,
  HOOKS_LOG,
  HOOK_ERR,
  BUDGET_WARN_MS,
  BUDGET_SLOW_MS,
};
