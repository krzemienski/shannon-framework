#!/usr/bin/env node
// PreToolUse Edit|MultiEdit|Write — warn if no plan/*/plan.md touched in last hour
// AND about to edit code under src/lib/app. Heuristic; advisory only (exit 2 + stderr).
//
// Goal: surface "you're editing code without an active plan" to user before they
// commit several hours into the wrong direction. Cheap, no-block warn.
const { runHook } = require('../lib/hook-runner');
const fs = require('fs');
const path = require('path');

const ACTIVE_SCOPE = [/\/src\//, /\/lib\//, /\/app\//, /^src\//, /^lib\//, /^app\//];
const PLAN_FRESH_MS = 60 * 60 * 1000; // 1 hour

function findPlansDir() {
  const cwd = process.cwd();
  const cand = path.join(cwd, 'plans');
  try {
    if (fs.existsSync(cand) && fs.statSync(cand).isDirectory()) return cand;
  } catch (_) {}
  return null;
}

function hasFreshPlan() {
  const plansDir = findPlansDir();
  if (!plansDir) return false;
  const now = Date.now();
  try {
    const entries = fs.readdirSync(plansDir);
    for (const e of entries) {
      const planMd = path.join(plansDir, e, 'plan.md');
      try {
        if (!fs.existsSync(planMd)) continue;
        const stat = fs.statSync(planMd);
        if (now - stat.mtimeMs < PLAN_FRESH_MS) return true;
      } catch (_) {}
    }
  } catch (_) {}
  return false;
}

runHook('plan-before-execute', (payload) => {
  const toolInput = (payload && payload.tool_input) || {};
  const filePath = toolInput.file_path || toolInput.filePath || '';
  if (!filePath) return { decision: 'allow', exitCode: 0 };

  // Only nudge when editing within active code scope
  if (!ACTIVE_SCOPE.some(re => re.test(filePath))) {
    return { decision: 'allow', exitCode: 0 };
  }

  if (hasFreshPlan()) return { decision: 'allow', exitCode: 0 };

  return {
    decision: 'allow',
    exitCode: 2,
    stderrPayload: `[shannon] plan-before-execute: editing "${filePath}" in code scope but no plans/*/plan.md modified in last hour. Consider running /shannon:plan first to anchor the change.\n`,
  };
});
