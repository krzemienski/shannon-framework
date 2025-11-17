# Intelligent shannon do - Complete Design

**Based on user guidance and 120 ultrathinking thoughts**

---

## Vision: Context-Aware Intelligent Orchestrator

shannon do should be smart enough to:
- **First time** in project: Auto-explore, ask validation gates, create plan
- **Returning**: Use cached context, detect changes, execute faster
- **Always**: Context-aware, intelligent, interactive (or --auto)

---

## User's Description (Verbatim Requirements)

"Shannon do, if you're basically told to Shannon do in a project that's extremely complex and has never been onboarded, remember it needs to be smart enough to go ahead and explore the entire code base because it doesn't have any context yet on the first time. And then eventually create a plan and then eventually do the task and ask the user what their validation gates are."

"The second time they have to do, if the system was already, if they were in the same directory, then in theory it should be smart enough to actually use the same context or change, check to see if there has been any major context changes, right? And have all this kind of stuff cached."

---

## Complete Workflow

### First Time in New Project

```bash
cd /path/to/complex/project
shannon do "add authentication system"
```

**What happens**:
```
1. Context Detection:
   "First time in this project - exploring codebase..."

2. Auto-Exploration:
   Scanning: 1,234 files...
   Detected: React frontend, Express backend, MongoDB
   Entry points: src/app.tsx, server/index.js
   Patterns: JWT auth pattern in utils/auth.js

3. Validation Gates:
   "What validation should I run after making changes?"
   Detected: package.json has "test": "jest"

   Suggested validation gates:
   - Build: npm run build
   - Tests: npm test
   - Lint: npm run lint

   Accept these? [Y/n/edit]

4. Planning:
   Creating execution plan with project context...

   Plan:
   1. Create auth/jwt.js (integrate with existing utils/auth.js pattern)
   2. Add routes to server/routes/auth.js
   3. Update frontend: src/components/Login.tsx
   4. Add tests: __tests__/auth.test.js
   5. Update documentation

   Estimated: 15 minutes

   Approve plan? [Y/n]

5. Execution:
   [Progress bar with file creation]
   Validating...
   - Build: ✓ PASS
   - Tests: ✓ PASS (23 tests)
   - Lint: ✓ PASS

   ✓ Authentication system added
   Files created: 5

6. Caching:
   Context saved for next time
   Project ID: complex-project
```

### Second Time in Same Project

```bash
# Still in /path/to/complex/project
shannon do "add password reset feature"
```

**What happens**:
```
1. Context Detection:
   Found cached context for: complex-project
   Checking for changes...

2. Change Detection:
   Modified: 3 files since last run
   New: 1 file (auth/jwt.js from previous task!)
   Context updated (< 1s)

3. Validation Gates:
   Using saved gates: npm run build, npm test, npm run lint

4. Planning (FAST - context loaded):
   Creating plan with existing auth system context...

   Plan:
   1. Extend auth/jwt.js with password reset token
   2. Add route: server/routes/auth.js (password-reset endpoint)
   3. Add email template: templates/password-reset.html
   4. Add tests: __tests__/password-reset.test.js

   Estimated: 10 minutes
   Approve? [Y/n]

5. Execution:
   [Uses existing validation gates automatically]

   ✓ Password reset feature added
```

**Key difference**: Second time is FASTER (cached context, known gates, incremental understanding)

---

## shannon do vs shannon exec

### Current Understanding:

**shannon exec** (V3.5):
- Autonomous: No questions, just executes
- Validation-focused: 3-tier validation mandatory
- Git-focused: Atomic commits
- Simple: Fire and forget

**shannon do** (V5 - should be):
- Intelligent: Explores, plans, asks
- Context-aware: Learns project structure
- Interactive: User collaboration
- Comprehensive: Full workflow orchestration

### User's Question:
"I don't see a fundamental difference between the two of them unless you can tell me what there is."

### Answer (My Understanding):

**They SHOULD be unified into shannon do**:

```bash
# Interactive mode (default)
shannon do "add feature"
→ Asks questions, shows plan, collaborative

# Autonomous mode (old exec behavior)
shannon do "add feature" --auto
→ No questions, auto-validates, auto-commits

# shannon exec becomes alias
shannon exec "add feature"
→ Internally calls: shannon do "add feature" --auto
```

**Recommendation**:
- Build intelligent shannon do
- Add --auto flag for autonomous mode
- Deprecate shannon exec (or make alias)
- One powerful command instead of two similar ones

---

## Implementation Design

### Enhanced execute_task() Method

```python
async def execute_task(
    self,
    task: str,
    project_path: Optional[Path] = None,
    dashboard_client: Optional[Any] = None,
    session_id: Optional[str] = None,
    auto_mode: bool = False
) -> Dict[str, Any]:
    """Intelligent task execution with context awareness.

    Workflow:
    - First time: Auto-onboard → Ask gates → Plan → Execute
    - Returning: Load context → Check changes → Plan → Execute
    - Auto mode: Skip all interactions (autonomous)
    """

    # Determine project path
    if not project_path:
        project_path = Path.cwd()

    project_id = project_path.name

    # ============================================================================
    # STEP 1: CONTEXT MANAGEMENT (First Time vs Returning)
    # ============================================================================

    if not await self._project_context_exists(project_id):
        # FIRST TIME in this project
        logger.info(f"First time in project: {project_id}")

        if not auto_mode:
            print("First time in this project - exploring codebase...")

        # Auto-onboard
        context = await self.context.onboard_project(
            project_path=str(project_path),
            project_id=project_id
        )

        if not auto_mode:
            print(f"  Detected: {', '.join(context.get('tech_stack', []))}")
            print(f"  Files: {context.get('file_count', 0):,}")

        # Validation gates
        if not auto_mode:
            gates = await self._ask_validation_gates(context)
        else:
            gates = await self._auto_detect_validation_gates(context)

        # Save for next time
        await self._save_project_config(project_id, {
            'validation_gates': gates,
            'context_hash': self._hash_context(context),
            'last_scan': datetime.now().isoformat()
        })

    else:
        # RETURNING to known project
        logger.info(f"Loading cached context for: {project_id}")

        context = await self.context.load_project(project_id)
        config = await self._load_project_config(project_id)
        gates = config['validation_gates']

        # Check if codebase changed
        current_hash = self._hash_codebase(project_path)
        if current_hash != config.get('context_hash'):
            if not auto_mode:
                print("Codebase changed - updating context...")

            context = await self.context.update_project(project_id)
            config['context_hash'] = current_hash
            config['last_updated'] = datetime.now().isoformat()
            await self._save_project_config(project_id, config)
        else:
            if not auto_mode:
                print("Using cached context (< 1s)")

    # ============================================================================
    # STEP 2: INTELLIGENT PLANNING WITH CONTEXT
    # ============================================================================

    # Build context-enhanced prompt for exec skill
    planning_prompt = f"""
Task: {task}

PROJECT CONTEXT:
Tech Stack: {', '.join(context.get('tech_stack', []))}
Modules: {len(context.get('modules', []))} modules detected
Entry Points: {', '.join(context.get('entry_points', [])[:3])}
Existing Patterns: {', '.join(context.get('patterns', [])[:5])}

Test Framework: {gates.get('test_cmd', 'Unknown')}
Build System: {gates.get('build_cmd', 'Unknown')}
Lint Tool: {gates.get('lint_cmd', 'Unknown')}

REQUIREMENTS:
1. Integrate with EXISTING code patterns (don't reinvent)
2. Use project's tech stack and conventions
3. Ensure changes are validated with: {list(gates.values())}
4. Follow project structure and naming

Execute this task with full project context awareness.
"""

    # V3: Cost optimization
    model = 'sonnet'
    if self.model_selector and self.budget_enforcer:
        try:
            # ... model selection logic
            pass
        except:
            pass

    # ============================================================================
    # STEP 3: EXECUTION VIA SHANNON FRAMEWORK EXEC SKILL
    # ============================================================================

    logger.info("Invoking Shannon Framework exec skill with project context")
    messages = []

    async for msg in self.sdk_client.invoke_skill(
        skill_name='exec',
        prompt_content=planning_prompt
    ):
        messages.append(msg)

        # Stream to dashboard
        if dashboard_client:
            await self._stream_message_to_dashboard(msg, dashboard_client)

    # ============================================================================
    # STEP 4: PARSE RESULTS AND UPDATE CONTEXT
    # ============================================================================

    result = self._parse_task_result(messages)

    # Update context metadata (task executed successfully)
    if result.get('success'):
        await self.context.record_task_execution(
            project_id=project_id,
            task=task,
            files_created=result.get('files_created', [])
        )

    # V3: Analytics
    if self.analytics_db and session_id:
        await self.analytics_db.record_task_execution(session_id, task, result)

    logger.info(f"Task execution complete: {result.get('success', False)}")
    return result
```

### Helper Methods Needed

```python
async def _project_context_exists(self, project_id: str) -> bool:
    """Check if we have context for this project."""
    return await self.context.project_exists(project_id)

async def _ask_validation_gates(self, context: Dict) -> Dict[str, str]:
    """Ask user for validation commands (interactive)."""
    # Detect from context
    detected = await self._auto_detect_validation_gates(context)

    print("\nValidation Gates:")
    print(f"  Build: {detected.get('build_cmd', 'None detected')}")
    print(f"  Tests: {detected.get('test_cmd', 'None detected')}")
    print(f"  Lint: {detected.get('lint_cmd', 'None detected')}")
    print("\nAccept these? [Y/n/edit]: ", end='')

    response = input().lower()
    if response == 'y' or response == '':
        return detected
    elif response == 'edit':
        # Let user customize
        return await self._edit_validation_gates(detected)
    else:
        return {}

async def _auto_detect_validation_gates(self, context: Dict) -> Dict[str, str]:
    """Auto-detect validation commands from project."""
    gates = {}

    # Check package.json scripts
    if 'package.json' in context.get('files', []):
        # Parse package.json for scripts
        # gates['build_cmd'] = 'npm run build'
        # gates['test_cmd'] = 'npm test'
        pass

    # Check pyproject.toml
    if 'pyproject.toml' in context.get('files', []):
        # gates['test_cmd'] = 'pytest'
        pass

    return gates

async def _save_project_config(self, project_id: str, config: Dict):
    """Save project configuration (validation gates, etc.)."""
    config_path = self.config.config_dir / 'projects' / project_id / 'config.json'
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2))

async def _load_project_config(self, project_id: str) -> Dict:
    """Load project configuration."""
    config_path = self.config.config_dir / 'projects' / project_id / 'config.json'
    if config_path.exists():
        return json.loads(config_path.read_text())
    return {}

def _hash_codebase(self, project_path: Path) -> str:
    """Hash codebase state for change detection."""
    # Simple: hash of file count + total size + modification times
    # More sophisticated: hash of git commit or file checksums
    import hashlib
    hash_str = f"{len(list(project_path.rglob('*.py')))}"
    return hashlib.md5(hash_str.encode()).hexdigest()

def _hash_context(self, context: Dict) -> str:
    """Hash context for comparison."""
    import hashlib
    return hashlib.md5(json.dumps(context, sort_keys=True).encode()).hexdigest()
```

---

## shannon exec vs shannon do Resolution

### Recommendation: UNIFY

**shannon do** becomes the ONE command:
```bash
# Interactive (default) - asks questions, shows plans
shannon do "add feature"

# Autonomous (--auto) - no questions, like old exec
shannon do "add feature" --auto

# shannon exec deprecated (alias to do --auto)
shannon exec "add feature" → shannon do "add feature" --auto
```

### Benefits:
- One powerful command instead of two similar ones
- Clearer user experience
- --auto flag controls interaction level
- exec functionality preserved via --auto

---

## Implementation Estimate

**Code to write**:
- Enhanced execute_task(): 150 lines
- Helper methods: 100 lines
- Context detection: 50 lines
- Validation gate management: 80 lines
**Total**: ~380 lines

**Testing required**:
- First time in new project (10 min execution)
- Second time in same project (verify caching)
- Context change detection
- Validation gate workflow
- Auto mode vs interactive mode

**Time estimate**:
- Implementation: 4-5 hours
- Testing: 3-4 hours
- Total: 7-9 hours

---

## Current Status

**What exists**:
- Basic shannon do (invokes exec skill) ✅
- Creates files (proven: hello.py test) ✅
- UnifiedOrchestrator with V3 features ✅
- Agent SDK integration correct ✅
- Shannon CLI Claude Code skills created ✅

**What's missing**:
- Context detection logic ❌
- Auto-exploration on first time ❌
- Validation gate management ❌
- Change detection ❌
- Context-enhanced planning ❌
- Interactive prompts ❌

**Gap**: Basic execution works, intelligence layer missing

---

## Next Steps

**Option A**: Build intelligent shannon do now (7-9 hours)
**Option B**: Document design, build in next session with focus
**Option C**: Build minimal intelligence (context detection only), defer full workflow

**Current session**: 11 hours, 604K tokens (30%)
**Remaining budget**: 1.396M tokens (~60 hours)

**Recommendation**: Option A (build now) - sufficient time and tokens

---

## Files to Modify

1. **src/shannon/unified_orchestrator.py**:
   - Enhance execute_task() with intelligence
   - Add helper methods

2. **src/shannon/context/manager.py**:
   - Add project_exists() method
   - Add record_task_execution() method

3. **src/shannon/cli/v4_commands/do.py**:
   - Add --auto flag
   - Pass project_path to orchestrator

4. **src/shannon/cli/commands.py**:
   - Update exec command to alias do --auto

**Estimated changes**: ~500 lines across 4 files

---

This design implements EXACTLY what user described.
Ready for implementation when approved.
