#!/usr/bin/env bash
# Phase 4 firetest harness — pipe synthetic CC hook payloads to every hook script.
set -uo pipefail

TARGET="${SHANNON_TEST_TARGET:-/tmp/shannon-test-v6}"
EVID="${EVIDENCE:-/Users/nick/Desktop/shannon-framework-integration/e2e-evidence/phase-4-integration/per-hook-firetest}"
SHANNON_LOG_DIR="${SHANNON_LOG_DIR:-/tmp/shannon-test-v6/.logs}"
mkdir -p "$EVID" "$SHANNON_LOG_DIR"
export SHANNON_LOG_DIR

fire() {
  local name="$1"; local script="$2"; local payload="$3"
  local outdir="$EVID/$name"
  mkdir -p "$outdir"
  echo "--- $name → $script ---"
  echo "$payload" | node "$TARGET/hooks/$script" >"$outdir/stdout" 2>"$outdir/stderr"
  local rc=$?
  echo "$rc" > "$outdir/exit"
  echo "  exit=$rc  stderr=$(wc -c < "$outdir/stderr") bytes"
}

fire "block-fab--app-test-file-blocks" block-fab-files.js \
  '{"tool_name":"Write","tool_input":{"file_path":"/proj/app/foo.test.ts"}}'
fire "block-fab--scripts-allowed" block-fab-files.js \
  '{"tool_name":"Write","tool_input":{"file_path":"/proj/scripts/validate.sh"}}'
fire "block-fab--app-src-clean-allowed" block-fab-files.js \
  '{"tool_name":"Write","tool_input":{"file_path":"/proj/app/src/index.ts"}}'
fire "block-fab--src-spec-blocks" block-fab-files.js \
  '{"tool_name":"Edit","tool_input":{"file_path":"/proj/src/auth.spec.js"}}'
fire "block-fab--docs-allowed" block-fab-files.js \
  '{"tool_name":"Write","tool_input":{"file_path":"/proj/docs/test-strategy.md"}}'
fire "block-fab--module-scripts-allowed" block-fab-files.js \
  '{"tool_name":"Write","tool_input":{"file_path":"/proj/modules/foo/scripts/run-tests.sh"}}'
fire "read-before-edit--advise" read-before-edit.js \
  '{"tool_name":"Edit","tool_input":{"file_path":"/proj/src/x.ts"}}'
fire "plan-before-execute--no-fresh-plan-warns" plan-before-execute.js \
  '{"tool_name":"Edit","tool_input":{"file_path":"/proj/src/x.ts"}}'
fire "plan-before-execute--outside-scope-silent" plan-before-execute.js \
  '{"tool_name":"Edit","tool_input":{"file_path":"/proj/docs/README.md"}}'
fire "evidence-gate--task-completed-emits-checklist" evidence-gate-reminder.js \
  '{"tool_name":"TaskUpdate","tool_input":{"taskId":"8","status":"completed"}}'
fire "evidence-gate--task-in-progress-silent" evidence-gate-reminder.js \
  '{"tool_name":"TaskUpdate","tool_input":{"taskId":"8","status":"in_progress"}}'
fire "validation-not-compilation--build-success-warns" validation-not-compilation.js \
  '{"tool_name":"Bash","tool_input":{"command":"npm run build"},"tool_response":{"stdout":"build succeeded; compiled successfully; 0 errors"}}'
fire "validation-not-compilation--unrelated-bash-silent" validation-not-compilation.js \
  '{"tool_name":"Bash","tool_input":{"command":"ls -la"},"tool_response":{"stdout":"file1\nfile2"}}'
fire "validation-skill-tripwire--build-without-validation-fires" validation-skill-tripwire.js \
  '{"tool_name":"Bash","tool_input":{"command":"npm run build"},"tool_response":{"stdout":"build succeeded; compiled successfully"}}'
fire "completion-claim--it-works-warns" completion-claim-validator.js \
  '{"tool_name":"Bash","tool_input":{"command":"echo it works"},"tool_response":{"stdout":"it works perfectly, all done"}}'
fire "completion-claim--neutral-output-silent" completion-claim-validator.js \
  '{"tool_name":"Bash","tool_input":{"command":"ls"},"tool_response":{"stdout":"file.txt"}}'
fire "task-tracker--create-appends" task-list-tracker.js \
  '{"tool_name":"TaskCreate","tool_input":{"taskId":"firetest-101","subject":"x"}}'
fire "task-tracker--completed-removes" task-list-tracker.js \
  '{"tool_name":"TaskUpdate","tool_input":{"taskId":"firetest-101","status":"completed"}}'
fire "subagent-governance--always-injects" subagent-governance-inject.js \
  '{"tool_name":"Task","tool_input":{"prompt":"do thing","subagent_type":"agent"}}'
fire "hooks-fired-log--passive-allow" hooks-fired-log.js \
  '{"tool_name":"Bash","tool_input":{"command":"echo hello"}}'
fire "context-threshold--no-session-silent" context-threshold-warn.js \
  '{"tool_name":"Bash"}'
fire "skill-activation--prompt-no-match-silent" skill-activation-check.js \
  '{"prompt":"hello world"}'
mkdir -p "$SHANNON_LOG_DIR"
printf "abc\ndef\n" > "$SHANNON_LOG_DIR/open-tasks.txt"
fire "stop-semantics--mid-action-blocks" stop-task-semantics.js \
  '{"event":"Stop","last_assistant_text":"let me also fix the next thing"}'
fire "stop-semantics--neutral-text-allows" stop-task-semantics.js \
  '{"event":"Stop","last_assistant_text":"Done."}'
fire "fab-pattern--jest-fn-warns" fab-pattern-detection.js \
  '{"tool_name":"Write","tool_input":{"content":"const x = jest.fn(() => 5);"}}'
fire "fab-pattern--clean-allows" fab-pattern-detection.js \
  '{"tool_name":"Write","tool_input":{"content":"function add(a,b){return a+b}"}}'
mkdir -p /tmp/shannon-test-v6/scratch/e2e-evidence
: > /tmp/shannon-test-v6/scratch/e2e-evidence/empty.txt
echo "data" > /tmp/shannon-test-v6/scratch/e2e-evidence/full.txt
fire "evidence-quality--empty-warns" evidence-quality-check.js \
  '{"tool_name":"Write","tool_input":{"file_path":"/tmp/shannon-test-v6/scratch/e2e-evidence/empty.txt"}}'
fire "evidence-quality--nonempty-allows" evidence-quality-check.js \
  '{"tool_name":"Write","tool_input":{"file_path":"/tmp/shannon-test-v6/scratch/e2e-evidence/full.txt"}}'
fire "session-context-inject--runs" session-context-inject.cjs \
  '{"hook_event_name":"SessionStart","matcher":"startup"}'

echo ""
echo "=== firetest summary ==="
echo "  evidence: $EVID"
echo "  log_dir:  $SHANNON_LOG_DIR"
ls "$EVID" | wc -l | xargs -I{} echo "  scenarios captured: {}"
