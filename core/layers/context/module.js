#!/usr/bin/env node
// ContextLayer — SessionStart context injector.
// Per SHANNON-V6-ARCHITECTURE.md §4 and SHANNON-V6-HOOKS.md hook #11.

const fs = require('fs');
const path = require('path');
const os = require('os');
const { LOG_DIR, ensureLogDir, appendJsonl } = require('../../../lib/logger');

const GLOBAL_CLAUDE_MD = path.join(os.homedir(), '.claude/CLAUDE.md');
const GLOBAL_RULES_DIR = path.join(os.homedir(), '.claude/rules');
const PROJECT_CLAUDE_MD = path.join(process.cwd(), 'CLAUDE.md');
const PROJECT_RULES_DIR = path.join(process.cwd(), '.claude/rules');

function readIfExists(p) {
  try {
    if (!fs.existsSync(p)) return null;
    return fs.readFileSync(p, 'utf-8');
  } catch (_) {
    return null;
  }
}

function readRulesDir(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter(f => f.endsWith('.md')).map(f => ({
    name: f, path: path.join(dir, f), body: readIfExists(path.join(dir, f))
  })).filter(r => r.body);
}

function buildContext() {
  const blocks = [];
  const global = readIfExists(GLOBAL_CLAUDE_MD);
  if (global) blocks.push(`# Global CLAUDE.md\n\n${global}`);
  const proj = readIfExists(PROJECT_CLAUDE_MD);
  if (proj) blocks.push(`# Project CLAUDE.md\n\n${proj}`);
  for (const r of readRulesDir(GLOBAL_RULES_DIR)) {
    blocks.push(`# Global rule: ${r.name}\n\n${r.body}`);
  }
  for (const r of readRulesDir(PROJECT_RULES_DIR)) {
    blocks.push(`# Project rule: ${r.name}\n\n${r.body}`);
  }
  return blocks.join('\n\n---\n\n');
}

function collectSkillTriggers() {
  const skillsRoot = path.join(__dirname, '../../../skills');
  if (!fs.existsSync(skillsRoot)) return {};
  const triggers = {};
  for (const slug of fs.readdirSync(skillsRoot)) {
    const skillFile = path.join(skillsRoot, slug, 'SKILL.md');
    const body = readIfExists(skillFile);
    if (!body) continue;
    const m = body.match(/^---\s*\n([\s\S]*?)\n---/);
    if (!m) continue;
    const fm = m[1];
    const tm = fm.match(/triggers:\s*\n((?:\s*-\s*.+\n?)+)/);
    if (!tm) continue;
    triggers[slug] = tm[1].split('\n').map(l => l.replace(/^\s*-\s*/, '').trim()).filter(Boolean);
  }
  return triggers;
}

function cacheTriggers() {
  ensureLogDir();
  const triggers = collectSkillTriggers();
  const p = path.join(LOG_DIR, 'skill-triggers.json');
  try {
    fs.writeFileSync(p, JSON.stringify({ ts: new Date().toISOString(), skills: triggers }, null, 2));
    return p;
  } catch (_) {
    return null;
  }
}

function run() {
  const ctx = buildContext();
  const cachePath = cacheTriggers();
  appendJsonl('layer-fires.jsonl', {
    ts: new Date().toISOString(), layer: 'context',
    contextBytes: ctx.length, triggersCache: cachePath,
  });
  if (ctx) process.stdout.write(`<system-reminder>\nShannon ContextLayer: governance loaded.\n\n${ctx}\n</system-reminder>\n`);
}

module.exports = { buildContext, collectSkillTriggers, cacheTriggers, run };

if (require.main === module) run();
