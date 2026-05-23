#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const DIR = path.join(ROOT, "agents");
const errors = [];
const ok = [];
const REQUIRED = ["name", "description", "model"];
function parseFM(content) {
  const m = content.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return null;
  const fm = {};
  for (const line of m[1].split("\n")) {
    const kv = line.match(/^(\w[\w-]*):\s*(.*)$/);
    if (kv) fm[kv[1]] = kv[2].trim();
  }
  return fm;
}
const files = fs.readdirSync(DIR).filter(f => f.endsWith(".md")).sort();
for (const f of files) {
  const p = path.join(DIR, f);
  const real = fs.realpathSync(p);
  const content = fs.readFileSync(real, "utf8");
  const fm = parseFM(content);
  if (!fm) { errors.push(f + ": missing frontmatter"); continue; }
  const missing = REQUIRED.filter(k => !fm[k]);
  if (missing.length) { errors.push(f + ": missing " + missing.join(", ")); continue; }
  if (fm.model !== "opus" && fm.model !== "sonnet" && fm.model !== "haiku") {
    errors.push(f + ": model invalid: " + fm.model);
    continue;
  }
  ok.push({ agent: f, name: fm.name, model: fm.model });
}
console.log(JSON.stringify({ total: files.length, ok: ok.length, errors: errors.length, agents: ok, errorDetails: errors }, null, 2));
process.exit(errors.length ? 1 : 0);
