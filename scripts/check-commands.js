#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const DIR = path.join(ROOT, "commands");
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
const files = fs.readdirSync(DIR).filter(f => f.endsWith(".md")).sort();
for (const f of files) {
  const p = path.join(DIR, f);
  const real = fs.realpathSync(p);
  const content = fs.readFileSync(real, "utf8");
  const fm = parseFM(content);
  if (!fm) { errors.push(f + ": missing frontmatter"); continue; }
  const missing = REQUIRED.filter(k => !fm[k]);
  if (missing.length) { errors.push(f + ": missing " + missing.join(", ")); continue; }
  const hasBody = content.indexOf("## Behavior") >= 0 || content.indexOf("## Inputs") >= 0;
  if (!hasBody) { errors.push(f + ": body lacks Behavior or Inputs"); continue; }
  ok.push({ file: f, name: fm.name });
}
console.log(JSON.stringify({ total: files.length, ok: ok.length, errors: errors.length, commands: ok, errorDetails: errors }, null, 2));
process.exit(errors.length ? 1 : 0);
