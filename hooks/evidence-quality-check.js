#!/usr/bin/env node
// PostToolUse Edit|Write|MultiEdit — warn on empty (0-byte) evidence files in e2e-evidence/.
const { runHook } = require('../lib/hook-runner');
const fs = require('fs');

runHook('evidence-quality-check', (payload) => {
  const tin = (payload && payload.tool_input) || {};
  const filePath = tin.file_path || '';
  if (!filePath) return { decision: 'allow', exitCode: 0 };
  if (!/\/e2e-evidence\//.test(filePath) && !/\/evidence\//.test(filePath)) {
    return { decision: 'allow', exitCode: 0 };
  }
  try {
    if (!fs.existsSync(filePath)) return { decision: 'allow', exitCode: 0 };
    const stat = fs.statSync(filePath);
    if (stat.size === 0) {
      return {
        decision: 'allow',
        exitCode: 2,
        stderrPayload: `[shannon] evidence-quality-check: "${filePath}" is 0 bytes. Empty files are INVALID evidence.\n`,
      };
    }
  } catch (_) { /* silent */ }
  return { decision: 'allow', exitCode: 0 };
});
