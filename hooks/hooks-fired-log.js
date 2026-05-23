#!/usr/bin/env node
// PostToolUse * — passive append-only log of every tool use through hook layer.
const { runHook } = require('../lib/hook-runner');

runHook('hooks-fired-log', () => ({ decision: 'allow', exitCode: 0 }));
