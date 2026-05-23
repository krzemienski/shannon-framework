#!/usr/bin/env node
// SessionStart hook → delegate to ContextLayer.
const { run } = require('../core/layers/context/module.js');
try { run(); } catch (e) {
  try {
    require('fs').appendFileSync(
      require('path').join(process.env.HOME, '.claude/logs/shannon/hook-errors.jsonl'),
      JSON.stringify({ ts: new Date().toISOString(), script: 'session-context-inject', error: String(e), stack: e && e.stack }) + '\n'
    );
  } catch (_) {}
}
process.exit(0);
