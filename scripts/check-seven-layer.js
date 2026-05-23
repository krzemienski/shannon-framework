#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const DOC = path.join(ROOT, "docs", "seven-layer-conceptual.md");
const errors = [];
if (!fs.existsSync(DOC)) {
  console.log(JSON.stringify({ ok: false, errors: ["docs/seven-layer-conceptual.md missing"] }, null, 2));
  process.exit(1);
}
const content = fs.readFileSync(DOC, "utf8");
const expectedLayers = [
  "1. Global CLAUDE.md",
  "2. Project CLAUDE.md",
  "3. `.claude/rules/*.md`",
  "4. Hooks",
  "5. Skills",
  "6. MCP servers",
  "7. SessionStart",
];
for (const layer of expectedLayers) {
  if (content.indexOf(layer) < 0) errors.push("missing conceptual layer: " + layer);
}
const expectedModules = ["context", "hook", "invocation", "dispatch"];
for (const m of expectedModules) {
  const p = path.join(ROOT, "core", "layers", m);
  if (!fs.existsSync(p)) errors.push("core/layers/" + m + "/ missing");
}
console.log(JSON.stringify({
  ok: errors.length === 0,
  expectedConceptualLayers: expectedLayers.length,
  expectedEnforcementModules: expectedModules.length,
  errors,
}, null, 2));
process.exit(errors.length ? 1 : 0);
