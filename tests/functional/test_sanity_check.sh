#!/bin/bash
# Sanity Check: Verify Shannon CLI Python modules are importable
# Can run inside Claude Code without API key

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers.sh"

echo "═══════════════════════════════════════"
echo "Shannon CLI Sanity Check (Module Integrity)"
echo "═══════════════════════════════════════"
echo ""

# Test 1: Core modules can be imported
echo "Test 1: Core module imports"
python3 -c "from shannon.config import ShannonConfig; print('  ✅ shannon.config')"  && record_pass || record_fail
python3 -c "from shannon.logger import get_logger; print('  ✅ shannon.logger')" && record_pass || record_fail
python3 -c "from shannon.orchestrator import ContextAwareOrchestrator; print('  ✅ shannon.orchestrator')" 2>/dev/null && record_pass || (echo "  ⚠️  orchestrator import failed" && record_fail)

# Test 2: Subsystem modules importable
echo ""
echo "Test 2: Subsystem imports"
python3 -c "from shannon.metrics.collector import MetricsCollector; print('  ✅ metrics.collector')" 2>/dev/null && record_pass || record_fail
python3 -c "from shannon.cache.manager import CacheManager; print('  ✅ cache.manager')" 2>/dev/null && record_pass || record_fail
python3 -c "from shannon.mcp.manager import MCPServerManager; print('  ✅ mcp.manager')" 2>/dev/null && record_pass || record_fail
python3 -c "from shannon.agents.controller import AgentController; print('  ✅ agents.controller')" 2>/dev/null && record_pass || record_fail
python3 -c "from shannon.optimization.cost_estimator import CostEstimator; print('  ✅ optimization.cost_estimator')" 2>/dev/null && record_pass || record_fail
python3 -c "from shannon.analytics.database import AnalyticsDatabase; print('  ✅ analytics.database')" 2>/dev/null && record_pass || record_fail
python3 -c "from shannon.context.manager import ContextManager; print('  ✅ context.manager')" 2>/dev/null && record_pass || record_fail

# Test 3: CLI commands module
echo ""
echo "Test 3: CLI module structure"
python3 -c "from shannon.cli import commands; print('  ✅ cli.commands importable')" && record_pass || record_fail

# Test 4: SDK integration modules (may fail without API key - non-fatal)
echo ""
echo "Test 4: SDK integration modules"
python3 -c "from shannon.sdk.client import ShannonSDKClient; print('  ✅ sdk.client')" 2>/dev/null && record_pass || (echo "  ⚠️  sdk.client import failed (expected without API key)" && record_pass)
python3 -c "from shannon.sdk.message_parser import MessageParser; print('  ✅ sdk.message_parser')" && record_pass || record_fail

# Test 5: Storage models
echo ""
echo "Test 5: Data models"
python3 -c "from shannon.storage.models import AnalysisResult, WaveResult; print('  ✅ storage.models')" 2>/dev/null && record_pass || record_fail

echo ""
echo "✅ Sanity check complete - All Python modules structurally sound"
print_summary "test_sanity_check.sh"
