#!/usr/bin/env node
// PostToolUse * — passive observer. If session JSONL size > 80% of typical
// context budget (~200KB), emit /compact suggestion via stderr. Always exit 0;
// never blocks tool flow.
//
// Heuristic threshold: 200KB ≈ ~80% of 250KB JSONL → roughly ~150K tokens session.
// Conservative — meant to catch heavy sessions before auto-compact fires unpredictably.
const { runHook } = require('../lib/hook-runner');
const fs = require('fs');
const path = require('path');
const os = require('os');

const THRESHOLD_BYTES = parseInt(process.env.SHANNON_CTX_WARN_BYTES || '', 10) || 200 * 1024;
const SESSIONS_ROOT = path.join(os.homedir(), '.claude/projects');

function findSessionJsonl() {
  const sid = process.env.CLAUDE_SESSION_ID;
  if (!sid) return null;
  try {
    if (!fs.existsSync(SESSIONS_ROOT)) return null;
    const projects = fs.readdirSync(SESSIONS_ROOT);
    for (const proj of projects) {
      const cand = path.join(SESSIONS_ROOT, proj, `${sid}.jsonl`);
      if (fs.existsSync(cand)) return cand;
    }
  } catch (_) {}
  return null;
}

runHook('context-threshold-warn', () => {
  const jsonl = findSessionJsonl();
  if (!jsonl) return { decision: 'allow', exitCode: 0 };
  try {
    const stat = fs.statSync(jsonl);
    if (stat.size < THRESHOLD_BYTES) return { decision: 'allow', exitCode: 0 };
    const kb = Math.round(stat.size / 1024);
    return {
      decision: 'allow',
      exitCode: 0,
      stderrPayload: `[shannon] context-threshold-warn: session JSONL is ${kb}KB (>${Math.round(THRESHOLD_BYTES/1024)}KB threshold). Consider /compact to preserve performance before auto-compact fires.\n`,
    };
  } catch (_) {
    return { decision: 'allow', exitCode: 0 };
  }
});
