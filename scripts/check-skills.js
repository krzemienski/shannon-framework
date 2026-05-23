#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const DIR = path.join(ROOT, "skills");
const errors = [];
const ok = [];
const REQUIRED = ["name", "description"];
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
const dirs = fs.readdirSync(DIR, { withFileTypes: true })
  .filter(d => d.isDirectory() || d.isSymbolicLink())
  .map(d => d.name).sort();
for (const d of dirs) {
  const skillFile = path.join(DIR, d, "SKILL.md");
  if (!fs.existsSync(skillFile)) { errors.push(d + ": SKILL.md missing"); continue; }
  const real = fs.realpathSync(skillFile);
  const content = fs.readFileSync(real, "utf8");
  const fm = parseFM(content);
  if (!fm) { errors.push(d + ": SKILL.md missing frontmatter"); continue; }
  const missing = REQUIRED.filter(k => !fm[k]);
  if (missing.length) { errors.push(d + ": missing " + missing.join(", ")); continue; }
  ok.push({ skill: d, name: fm.name });
}
console.log(JSON.stringify({ total: dirs.length, ok: ok.length, errors: errors.length, skills: ok, errorDetails: errors }, null, 2));
process.exit(errors.length ? 1 : 0);
