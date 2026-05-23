#!/usr/bin/env node
// Shannon shared structured logger. Wraps fs.appendFile for shannon log dir.

const fs = require('fs');
const path = require('path');
const os = require('os');

const LOG_DIR = process.env.SHANNON_LOG_DIR || path.join(os.homedir(), '.claude/logs/shannon');

function ensureLogDir() {
  try { fs.mkdirSync(LOG_DIR, { recursive: true }); } catch (_) { /* silent */ }
}

function appendJsonl(name, record) {
  try {
    ensureLogDir();
    fs.appendFileSync(path.join(LOG_DIR, name), JSON.stringify(record) + '\n');
  } catch (_) { /* silent */ }
}

function readJsonl(name) {
  const p = path.join(LOG_DIR, name);
  if (!fs.existsSync(p)) return [];
  return fs.readFileSync(p, 'utf-8').split('\n').filter(Boolean).map(line => {
    try { return JSON.parse(line); } catch (_) { return null; }
  }).filter(Boolean);
}

module.exports = { LOG_DIR, appendJsonl, readJsonl, ensureLogDir };
