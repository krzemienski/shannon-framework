#!/usr/bin/env node
// InvocationLayer — skill hint + tripwire.
// Per SHANNON-V6-ARCHITECTURE.md §4.
//
// Owns:
//   - skill-activation-check.js (UserPromptSubmit) — match user prompt against
//     cached skill triggers (from ContextLayer's skill-triggers.json), emit hint.
//   - validation-skill-tripwire.js (PostToolUse Bash) — if build success +
//     functional-validation skill NOT invoked since last build → tripwire stderr +
//     append tripwires.jsonl.
//
// This module exports the helpers those hooks call.

const fs = require('fs');
const path = require('path');
const os = require('os');

const LOG_DIR = process.env.SHANNON_LOG_DIR || path.join(os.homedir(), '.claude/logs/shannon');
const TRIGGERS_CACHE = path.join(LOG_DIR, 'skill-triggers.json');
const TRIPWIRES_LOG = path.join(LOG_DIR, 'tripwires.jsonl');

function readTriggers() {
  try {
    if (!fs.existsSync(TRIGGERS_CACHE)) return {};
    const j = JSON.parse(fs.readFileSync(TRIGGERS_CACHE, 'utf-8'));
    return j.skills || {};
  } catch (_) {
    return {};
  }
}

function matchSkills(prompt) {
  // Regex-match each skill's triggers against the user prompt. Return [{skill, trigger}].
  if (!prompt || typeof prompt !== 'string') return [];
  const triggers = readTriggers();
  const matches = [];
  const lower = prompt.toLowerCase();
  for (const skill of Object.keys(triggers)) {
    for (const trigger of triggers[skill]) {
      const t = String(trigger).toLowerCase().trim();
      if (!t) continue;
      // Strip quotes/colon prefixes the spec uses around trigger phrases.
      const clean = t.replace(/^["'\s]+|["'\s]+$/g, '');
      if (!clean) continue;
      if (lower.includes(clean)) {
        matches.push({ skill, trigger: clean });
        break;
      }
    }
  }
  return matches;
}

function appendTripwire(record) {
  try {
    fs.mkdirSync(LOG_DIR, { recursive: true });
    fs.appendFileSync(TRIPWIRES_LOG, JSON.stringify(record) + '\n');
  } catch (_) { /* silent */ }
}

module.exports = { LOG_DIR, TRIGGERS_CACHE, TRIPWIRES_LOG, readTriggers, matchSkills, appendTripwire };

if (require.main === module) {
  const triggers = readTriggers();
  const skillCount = Object.keys(triggers).length;
  console.log(`InvocationLayer OK — ${skillCount} skill(s) cached at ${TRIGGERS_CACHE}`);
}
