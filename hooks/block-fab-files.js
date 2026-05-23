#!/usr/bin/env node
// PreToolUse Write|Edit|MultiEdit — block fabricated-artifact filenames.
// Patterns canonical to spec post-16 §4.2.
const { runHook } = require('../lib/hook-runner');

const FAB_PATTERNS = [
  /\.test\.[a-z]+$/i,
  /\.spec\.[a-z]+$/i,
  /__mocks__\//,
  /\/tests?\//,
  /\/__tests__\//,
  /\.fixture\.[a-z]+$/i,
  /\/fixtures?\//,
  /\/stubs?\//,
  /-stub\.[a-z]+$/i,
  /\.mock\.[a-z]+$/i,
  /^mock-/i,
  /-fake\.[a-z]+$/i,
];

const ALLOW = [
  /\/e2e-evidence\//,
  /\/evidence\//,
  /\.claude-plugin\//,
];

runHook('block-fab-files', (payload) => {
  const toolInput = (payload && payload.tool_input) || {};
  const filePath = toolInput.file_path || toolInput.filePath || '';
  if (!filePath) return { decision: 'allow', exitCode: 0 };
  if (ALLOW.some(re => re.test(filePath))) return { decision: 'allow', exitCode: 0 };
  const matched = FAB_PATTERNS.find(re => re.test(filePath));
  if (!matched) return { decision: 'allow', exitCode: 0 };
  return {
    decision: 'block',
    exitCode: 2,
    stderrPayload: `[shannon] block-fab-files: "${filePath}" matches fabricated-artifact pattern ${matched}.\nIRON RULE: build and validate the real system; never ship fake-data files.\n`,
  };
});
