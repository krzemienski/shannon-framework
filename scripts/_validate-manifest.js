#!/usr/bin/env node
// Asserts Shannon's .claude-plugin/plugin.json + hooks/hooks.json shape match CC schema patterns.
// Cross-checks against the live OMC + VF manifest examples.
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const errors = [];

function read(p) { return JSON.parse(fs.readFileSync(p, 'utf-8')); }

const plugin = read(path.join(ROOT, '.claude-plugin/plugin.json'));
const market = read(path.join(ROOT, '.claude-plugin/marketplace.json'));
const hooksJson = read(path.join(ROOT, 'hooks/hooks.json'));

// Required plugin.json fields
['name', 'version', 'description', 'author', 'license'].forEach(k => {
  if (!plugin[k]) errors.push(`plugin.json missing required field: ${k}`);
});

if (plugin.name !== 'shannon') errors.push(`plugin.json name must be "shannon", got "${plugin.name}"`);
if (!/^6\./.test(String(plugin.version))) errors.push(`plugin.json version must be 6.x, got "${plugin.version}"`);
if (plugin.hooks !== './hooks/hooks.json') errors.push(`plugin.json must declare hooks: ./hooks/hooks.json`);

// marketplace.json shape
if (market.name !== 'shannon-local') errors.push(`marketplace.json name must be shannon-local, got "${market.name}"`);
if (!Array.isArray(market.plugins) || !market.plugins.length) errors.push(`marketplace.json must list ≥1 plugin`);
if (market.plugins && market.plugins[0] && market.plugins[0].name !== 'shannon') {
  errors.push(`marketplace.json plugins[0].name must be "shannon"`);
}

// hooks.json: count distinct scripts, verify each exists
const scripts = new Set();
for (const ev of Object.keys(hooksJson.hooks || {})) {
  for (const entry of hooksJson.hooks[ev]) {
    for (const h of (entry.hooks || [])) {
      const m = String(h.command).match(/hooks\/([a-z0-9._-]+\.[a-z]+)/);
      if (m) scripts.add(m[1]);
    }
  }
}
for (const s of scripts) {
  if (!fs.existsSync(path.join(ROOT, 'hooks', s))) errors.push(`hooks.json references missing script: hooks/${s}`);
}
if (scripts.size < 13) errors.push(`hooks.json should reference ≥13 scripts, got ${scripts.size}`);

// Layer modules
['context', 'hook', 'invocation', 'dispatch'].forEach(layer => {
  const mod = path.join(ROOT, `core/layers/${layer}/module.js`);
  const val = path.join(ROOT, `core/layers/${layer}/validate.sh`);
  if (!fs.existsSync(mod)) errors.push(`missing layer module: ${mod}`);
  if (!fs.existsSync(val)) errors.push(`missing layer validate.sh: ${val}`);
});

// lib/
['hook-runner.js', 'logger.js'].forEach(f => {
  if (!fs.existsSync(path.join(ROOT, 'lib', f))) errors.push(`missing lib/${f}`);
});

// scripts/
['setup.sh', 'uninstall-others.sh', 'install.sh'].forEach(f => {
  if (!fs.existsSync(path.join(ROOT, 'scripts', f))) errors.push(`missing scripts/${f}`);
});

const summary = {
  pluginName: plugin.name,
  pluginVersion: plugin.version,
  marketplaceName: market.name,
  hookEvents: Object.keys(hooksJson.hooks || {}),
  hookScriptCount: scripts.size,
  hookScripts: [...scripts].sort(),
  errors,
  ok: errors.length === 0,
};

console.log(JSON.stringify(summary, null, 2));
process.exit(errors.length ? 1 : 0);
