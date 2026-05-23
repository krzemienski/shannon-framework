#!/usr/bin/env node
// PreToolUse Write|Edit|MultiEdit — block fabricated-artifact filenames.
// Patterns canonical to spec post-16 §4.2.
//
// SCOPE (V6 update — fixes lynx false-positive that dev-domains hit):
//   - Active scope: src/ lib/ app/ paths
//   - Exemptions: scripts/ tools/ tests/ modules/*/scripts/ paths containing /scripts/
//     and any SKILL.md or AGENT.md file
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

// EXEMPTIONS — paths that may contain "test" / "mock" / "fixture" tokens legitimately.
// Scripts that BUILD validators, tools, plugin internals, and skill/agent markdown
// are all exempt from the fab block.
const EXEMPTIONS = [
  /\/e2e-evidence\//,
  /\/evidence\//,
  /\.claude-plugin\//,
  /\/scripts\//,                     // any scripts/ subtree
  /\/tools\//,                       // tools/ subtree
  /\/modules\/[^/]+\/scripts\//,     // per-module scripts
  /\bSKILL\.md$/,                    // skill markdown
  /\bAGENT\.md$/i,                   // agent markdown
  /\/skills\/[^/]+\//,               // any file under skills/<slug>/
  /\/agents\/[^/]+\.md$/i,           // agent .md
  /\/commands\/[^/]+\.md$/i,         // command .md
  /\/docs\//,                        // documentation
  /\/research\//,                    // research artifacts
  /^tests\//,                        // top-level tests/ dir (Shannon's own validation surface)
];

// Active scope: only enforce against src/ lib/ app/ subtrees. Files outside these
// scopes are allowed even if they match fab patterns (those are project internals,
// not application code under validation discipline).
const ACTIVE_SCOPE = [
  /\/src\//,
  /\/lib\//,
  /\/app\//,
  /^src\//,
  /^lib\//,
  /^app\//,
];

runHook('block-fab-files', (payload) => {
  const toolInput = (payload && payload.tool_input) || {};
  const filePath = toolInput.file_path || toolInput.filePath || '';
  if (!filePath) return { decision: 'allow', exitCode: 0 };

  // Exemption check first (highest priority — never block exempt paths)
  if (EXEMPTIONS.some(re => re.test(filePath))) {
    return { decision: 'allow', exitCode: 0 };
  }

  // Only enforce within active scope (src/ lib/ app/)
  if (!ACTIVE_SCOPE.some(re => re.test(filePath))) {
    return { decision: 'allow', exitCode: 0 };
  }

  const matched = FAB_PATTERNS.find(re => re.test(filePath));
  if (!matched) return { decision: 'allow', exitCode: 0 };

  return {
    decision: 'block',
    exitCode: 2,
    stderrPayload: `[shannon] block-fab-files: "${filePath}" matches fabricated-artifact pattern ${matched} within active scope (src/lib/app).\nIRON RULE: build and validate the real system; never ship fake-data files.\n`,
  };
});
