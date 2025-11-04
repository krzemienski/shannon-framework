# Shannon Framework V4 - Troubleshooting Guide

Solutions for common Shannon V4 issues.

---

## Quick Diagnostics

Run these commands when something goes wrong:

```bash
/sh_status          # Check overall status
/sh_check_mcps      # Verify MCP connections
/sh_memory --list   # List available checkpoints
```

---

## Installation Issues

### Shannon Not Found

**Symptoms:**
- `/sh_spec` returns "command not found"
- Shannon commands don't work

**Causes:**
- Plugin not installed
- Plugin not loaded
- Claude Code needs restart

**Solutions:**

1. **Verify installation:**
   ```bash
   /plugin list
   # Look for "shannon@shannon-framework"
   ```

2. **Install if missing:**
   ```bash
   /plugin install shannon@shannon-framework
   ```

3. **Restart Claude Code:**
   - Close and reopen application
   - Wait for full initialization

4. **Verify after restart:**
   ```bash
   /sh_status
   # Should show Shannon version and status
   ```

---

### Plugin Installation Fails

**Symptoms:**
- `/plugin install` returns error
- Installation hangs

**Solutions:**

1. **Check marketplace access:**
   ```bash
   /plugin marketplace list
   # Should show available plugins
   ```

2. **Add marketplace if missing:**
   ```bash
   /plugin marketplace add shannon-framework/shannon
   ```

3. **Clear plugin cache:**
   - Close Claude Code
   - Clear cache (system-dependent)
   - Restart and try again

4. **Manual installation:**
   - Download Shannon plugin zip
   - Install from local file
   - Follow local installation docs

---

## MCP Issues

### Serena MCP Not Connected

**Symptoms:**
- "Serena MCP required but not available"
- Checkpoints won't save
- Memory commands fail

**Causes:**
- Serena MCP not installed
- Serena MCP not configured
- Configuration error

**Solutions:**

1. **Check MCP status:**
   ```bash
   /sh_check_mcps
   ```

2. **Install Serena MCP:**
   ```bash
   npm install -g @anthropic/serena-mcp
   ```

3. **Configure in Claude Code:**
   - Open Settings
   - Navigate to MCPs section
   - Add Serena MCP configuration:
     ```json
     {
       "mcps": {
         "serena": {
           "command": "serena-mcp",
           "enabled": true
         }
       }
     }
     ```

4. **Restart Claude Code:**
   - Full restart required after configuration

5. **Verify connection:**
   ```bash
   /sh_check_mcps
   # Serena should show ✅ Connected
   ```

---

### Puppeteer MCP Not Found

**Symptoms:**
- `/sh_test --platform web` falls back to manual guidance
- "Puppeteer MCP not available" warning

**Impact:** Non-critical. Shannon provides manual test guidance as fallback.

**Solutions:**

1. **Install Puppeteer MCP (optional):**
   ```bash
   npm install -g @anthropic/puppeteer-mcp
   ```

2. **Configure in Claude Code:**
   ```json
   {
     "mcps": {
       "puppeteer": {
         "command": "puppeteer-mcp",
         "enabled": true
       }
     }
   }
   ```

3. **Restart Claude Code**

4. **Verify:**
   ```bash
   /sh_check_mcps
   ```

---

### Sequential MCP Issues

**Symptoms:**
- Complex specs don't use deep thinking
- Analysis seems shallow

**Impact:** Shannon works without Sequential but complex specs benefit from it.

**Solutions:**

1. **Install Sequential MCP (recommended):**
   ```bash
   npm install -g @anthropic/sequential-mcp
   ```

2. **Configure:**
   ```json
   {
     "mcps": {
       "sequential": {
         "command": "sequential-mcp",
         "enabled": true
       }
     }
   }
   ```

3. **Restart Claude Code**

4. **Test with complex spec:**
   ```bash
   /sh_spec "Build distributed microservices platform with event sourcing..."
   # Should show "Using Sequential MCP for deep analysis"
   ```

---

## Command Issues

### Specification Analysis Seems Wrong

**Symptoms:**
- Complexity score doesn't match expectations
- Missing domains
- Incorrect wave recommendations

**Causes:**
- Specification too vague
- Missing technical details
- Ambiguous requirements

**Solutions:**

1. **Add technical details:**
   ```bash
   # ❌ Too vague
   /sh_spec "Build an app"

   # ✅ Better
   /sh_spec "Build React web app with Node.js backend, PostgreSQL database, user authentication with JWT, REST API, deployed on AWS EC2"
   ```

2. **Specify integrations:**
   ```bash
   # Include all third-party services
   /sh_spec "Build e-commerce with Stripe payments, SendGrid email, Twilio SMS, AWS S3 storage"
   ```

3. **Mention constraints:**
   ```bash
   # Include performance/scale requirements
   /sh_spec "Build API handling 10k req/sec with 99.99% uptime, multi-region deployment"
   ```

4. **Re-analyze with details:**
   ```bash
   /sh_spec "<improved specification>"
   ```

---

### Wave Won't Execute

**Symptoms:**
- `/sh_wave 1` returns error
- "Wave cannot proceed" message

**Causes:**
- No specification analyzed
- Complexity too low for waves
- Previous wave incomplete
- Missing dependencies

**Solutions:**

1. **Check status:**
   ```bash
   /sh_status
   # Look for "Specification: " line
   ```

2. **Analyze spec first:**
   ```bash
   /sh_spec "Your specification here"
   ```

3. **Verify complexity:**
   - Waves recommended only for complexity ≥ 0.50
   - Low complexity specs should implement directly

4. **Check wave sequence:**
   ```bash
   # ❌ Don't skip waves
   /sh_wave 3  # Error if Wave 2 incomplete

   # ✅ Execute sequentially
   /sh_wave 1
   /sh_wave 2
   /sh_wave 3
   ```

5. **Review wave plan first:**
   ```bash
   /sh_wave 1 --plan  # Review before executing
   /sh_wave 1         # Then execute
   ```

---

### Checkpoint Won't Save

**Symptoms:**
- `/sh_checkpoint` returns error
- Checkpoint save fails

**Causes:**
- Serena MCP not connected
- Invalid checkpoint name
- No project state to save

**Solutions:**

1. **Verify Serena MCP:**
   ```bash
   /sh_check_mcps
   # Serena must be connected
   ```

2. **Use valid names:**
   ```bash
   # ❌ Invalid names
   /sh_checkpoint ""
   /sh_checkpoint "my checkpoint"  # No spaces

   # ✅ Valid names
   /sh_checkpoint "my-checkpoint"
   /sh_checkpoint "wave-1-complete"
   /sh_checkpoint "feature-auth"
   ```

3. **Ensure project state exists:**
   ```bash
   /sh_status
   # Should show active specification
   ```

4. **Try with explicit name:**
   ```bash
   /sh_checkpoint "test-checkpoint-$(date +%s)"
   ```

---

### Restore Fails

**Symptoms:**
- `/sh_restore` returns "checkpoint not found"
- Restoration incomplete

**Causes:**
- Checkpoint name typo
- Checkpoint doesn't exist
- Serena MCP issue

**Solutions:**

1. **List available checkpoints:**
   ```bash
   /sh_memory --list
   ```

2. **Use exact name:**
   ```bash
   # Use name exactly as shown in list
   /sh_restore "wave-1-complete"
   ```

3. **Check for typos:**
   ```bash
   # ❌ Wrong
   /sh_restore "wave_1_complete"

   # ✅ Correct
   /sh_restore "wave-1-complete"
   ```

4. **Verify Serena connection:**
   ```bash
   /sh_check_mcps
   ```

5. **Create new checkpoint if lost:**
   ```bash
   # If checkpoint truly lost, create new baseline
   /sh_spec "Re-enter specification"
   /sh_checkpoint "new-baseline"
   ```

---

### Memory Commands Fail

**Symptoms:**
- `/sh_memory --list` returns error
- Cannot read/write memories

**Causes:**
- Serena MCP not connected
- Memory corruption (rare)
- Permission issues

**Solutions:**

1. **Verify Serena:**
   ```bash
   /sh_check_mcps
   ```

2. **Test basic memory operation:**
   ```bash
   /sh_memory --write "test" "Test content"
   /sh_memory --read "test"
   /sh_memory --delete "test"
   ```

3. **If corruption suspected:**
   ```bash
   # Backup important memories
   /sh_memory --list > memories-backup.txt

   # Clear and reinitialize (last resort)
   # Contact support before doing this
   ```

---

## Testing Issues

### Tests Not Generating

**Symptoms:**
- `/sh_test` returns error
- No test files created

**Causes:**
- Puppeteer MCP not available (for web tests)
- Invalid platform
- Missing feature specification

**Solutions:**

1. **Check platform:**
   ```bash
   # Valid platforms: web, api, mobile
   /sh_test --create --platform web --feature "login"
   ```

2. **For web tests without Puppeteer:**
   ```bash
   /sh_check_mcps
   # Shows: Puppeteer not available
   # Shannon falls back to manual test guidance
   # Install Puppeteer MCP for automated tests
   ```

3. **Specify feature clearly:**
   ```bash
   # ❌ Too vague
   /sh_test --create --platform web

   # ✅ Clear
   /sh_test --create --platform web --feature "user login flow"
   ```

4. **Use API tests as alternative:**
   ```bash
   # API tests don't require Puppeteer
   /sh_test --create --platform api --feature "authentication"
   ```

---

## Performance Issues

### Slow Analysis

**Symptoms:**
- `/sh_spec` takes very long
- Analysis seems stuck

**Causes:**
- Very complex specification
- Sequential MCP processing large spec
- Network latency

**Solutions:**

1. **Break spec into chunks:**
   ```bash
   # Instead of one massive spec, analyze components separately
   /sh_spec "Backend: Node.js API with PostgreSQL"
   /sh_spec "Frontend: React SPA with Redux"
   /sh_spec "Infrastructure: AWS with Kubernetes"
   ```

2. **Simplify specification:**
   - Remove unnecessary details
   - Focus on core requirements
   - Add details later

3. **Check MCP status:**
   ```bash
   /sh_check_mcps
   # Slow Sequential MCP? May need restart
   ```

4. **Be patient for complex specs:**
   - Complex specs (≥ 0.70) legitimately take 1-3 minutes
   - Sequential MCP deep thinking is worth the wait

---

### Wave Execution Slow

**Symptoms:**
- Wave takes much longer than estimated
- Progress seems stalled

**Causes:**
- Underestimated complexity
- Blocking dependencies
- Agent coordination delays

**Solutions:**

1. **Check current status:**
   ```bash
   /sh_status
   # Shows current phase and progress
   ```

2. **Review wave plan:**
   ```bash
   /sh_wave <N> --plan
   # Check for dependency bottlenecks
   ```

3. **Create checkpoint and pause:**
   ```bash
   /sh_checkpoint "pause-point"
   # Take break, resume later
   ```

4. **Break wave into smaller tasks:**
   - Consider splitting complex wave
   - Execute critical path first

---

## Agent Issues

### Wrong Agent Activated

**Symptoms:**
- Frontend agent activates for backend task
- Agent seems mismatched to task

**Impact:** Usually minimal. Agents coordinate and self-correct.

**Solutions:**

1. **Trust agent coordination:**
   - WAVE_COORDINATOR manages agent assignments
   - Agents can activate supporting agents
   - Cross-domain tasks legitimately use multiple agents

2. **Check specification clarity:**
   ```bash
   # Vague spec → wrong agents
   /sh_spec "Build app"  # Too vague

   # Clear spec → correct agents
   /sh_spec "Build React frontend with Express backend"
   ```

3. **If persistent issue:**
   - Report to support with spec details
   - Include `/sh_status` output

---

### Agent Not Activating

**Symptoms:**
- Expected agent doesn't activate
- Task proceeds without specialized agent

**Causes:**
- Task complexity too low for agent
- Agent already active in parent task
- Specification doesn't trigger agent

**Solutions:**

1. **Check if agent needed:**
   - Simple tasks may not need specialized agents
   - Agent overhead not worth it for trivial tasks

2. **Make requirement explicit:**
   ```bash
   # Make security needs explicit
   /sh_spec "Build API with OAuth2, JWT, rate limiting, SQL injection protection"
   # SECURITY agent should activate
   ```

3. **Use analyze command:**
   ```bash
   /sh_analyze --domains
   # Shows which agents recommended
   ```

---

## Context Loss Issues

### Lost Project State

**Symptoms:**
- New conversation, Shannon forgets project
- `/sh_status` shows no active project

**Causes:**
- Normal behavior - new conversation = fresh context
- Checkpoints exist, just need restoration

**Solutions:**

1. **List checkpoints:**
   ```bash
   /sh_memory --list
   ```

2. **Restore most recent:**
   ```bash
   /sh_restore "most-recent-checkpoint"
   ```

3. **Verify restoration:**
   ```bash
   /sh_status
   # Should show restored project
   ```

4. **Create checkpoints regularly:**
   ```bash
   # Checkpoint after major milestones
   /sh_checkpoint "after-<milestone>"
   ```

---

### Checkpoint Missing

**Symptoms:**
- Expected checkpoint not in list
- `/sh_restore` says checkpoint doesn't exist

**Causes:**
- Checkpoint never created
- Checkpoint name misremembered
- Serena MCP issue (rare)

**Solutions:**

1. **Search memory list carefully:**
   ```bash
   /sh_memory --list
   # Look for similar names
   ```

2. **Check all memory types:**
   ```bash
   /sh_memory --list
   # Checkpoints are memories too
   ```

3. **Recreate if truly lost:**
   ```bash
   /sh_spec "<re-enter specification>"
   /sh_north_star "<re-enter goal>"
   /sh_checkpoint "recovery-baseline"
   ```

---

## Error Messages

### "Complexity calculation failed"

**Cause:** Invalid or malformed specification

**Solution:**
- Provide complete, well-formed specification
- Include technical details
- Remove special characters

---

### "Wave dependencies not met"

**Cause:** Trying to execute Wave N before Wave N-1

**Solution:**
```bash
# Execute waves sequentially
/sh_wave 1
/sh_wave 2  # Only after Wave 1
/sh_wave 3  # Only after Wave 2
```

---

### "MCP connection timeout"

**Cause:** MCP server not responding

**Solution:**
1. Check MCP server running
2. Restart MCP server
3. Verify network connectivity
4. Check MCP logs

---

### "Invalid checkpoint format"

**Cause:** Corrupted checkpoint (very rare)

**Solution:**
1. Try different checkpoint
2. Create new checkpoint
3. Contact support if persistent

---

## Getting Help

If issues persist after trying solutions:

### 1. Gather Diagnostic Info

```bash
# Run diagnostics
/sh_status > shannon-status.txt
/sh_check_mcps > shannon-mcps.txt
/sh_memory --list > shannon-memory.txt

# Include:
# - Shannon version
# - Claude Code version
# - OS version
# - Error messages (full text)
# - Steps to reproduce
```

### 2. Check Documentation

- User Guide: `SHANNON_V4_USER_GUIDE.md`
- Command Reference: `SHANNON_V4_COMMAND_REFERENCE.md`
- Migration Guide: `SHANNON_V4_MIGRATION_GUIDE.md`

### 3. Search Known Issues

- GitHub Issues: https://github.com/shannon-framework/shannon/issues
- Look for similar problems
- Check if already solved

### 4. Report Issue

If not found in docs or known issues:

**GitHub Issue Template:**
```markdown
**Shannon Version:** 4.0.0
**Claude Code Version:** [version]
**OS:** [macOS/Windows/Linux version]

**Description:**
[Clear description of problem]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Error occurs]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Error Messages:**
```
[Full error text]
```

**Diagnostic Output:**
```
[Output from /sh_status]
[Output from /sh_check_mcps]
```

**Additional Context:**
[Screenshots, logs, etc.]
```

### 5. Community Support

- Documentation: https://shannon-framework.dev/docs
- Community Forum: https://shannon-framework.dev/community
- Discord: [Link if available]

---

## Prevention Tips

### Regular Checkpoints

```bash
# Checkpoint frequently
/sh_checkpoint "before-<action>"
/sh_checkpoint "after-<milestone>"
```

### Verify MCPs Regularly

```bash
# Weekly check
/sh_check_mcps
```

### Keep Documentation Handy

- Bookmark documentation files
- Reference command reference often
- Review troubleshooting guide periodically

### Update Shannon

```bash
# Check for updates monthly
/plugin update shannon@shannon-framework
```

---

**Most issues have simple solutions. When in doubt, check `/sh_status` and `/sh_check_mcps` first!**
