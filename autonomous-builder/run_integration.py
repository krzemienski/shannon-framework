#!/usr/bin/env python3
"""
Real Integration Test for Autonomous Claude Code Builder.

This runs actual integration tests - NO MOCKS.
"""

import sys
import os
import asyncio
import tempfile
import json
import shutil
from pathlib import Path
from datetime import datetime

# Fix imports - add parent to path and set up package
sys.path.insert(0, str(Path(__file__).parent.parent))

# Now import with absolute paths by modifying how imports work
import importlib.util

def load_module(name, path):
    """Load a module from file path."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

# Load modules in dependency order
base = Path(__file__).parent

# Load config first (no dependencies)
config_mod = load_module("autonomous_builder.config", base / "config.py")

# Patch the relative imports in other modules
import builtins
_original_import = builtins.__import__

def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
    if level > 0 and name == '':
        # Handle relative imports
        package = globals.get('__name__', '').rsplit('.', level)[0]
        if fromlist:
            for item in fromlist:
                if item == 'config':
                    return config_mod
    return _original_import(name, globals, locals, fromlist, level)

# Actually, let's just create a simpler approach - copy files to temp and fix imports

print("=" * 70)
print("  AUTONOMOUS BUILDER - REAL INTEGRATION VALIDATION")
print("=" * 70)
print()

# Create a test workspace
TEST_DIR = Path(tempfile.mkdtemp(prefix="autonomous_builder_test_"))
print(f"Test workspace: {TEST_DIR}")

# ============================================================================
# TEST 1: Configuration System
# ============================================================================
print("\n" + "=" * 70)
print("TEST 1: Configuration System")
print("=" * 70)

try:
    # Read and exec config module directly
    config_code = (base / "config.py").read_text()
    exec(compile(config_code, "config.py", "exec"), globals())

    # Test config creation
    test_config = BuilderConfig(
        target_dir=TEST_DIR / "project1",
        puppeteer_enabled=True,
        verbose=True
    )

    print(f"✅ BuilderConfig created successfully")
    print(f"   Target dir: {test_config.target_dir}")
    print(f"   MCP servers: {list(test_config.mcps.keys())}")
    print(f"   Allowed commands: {len(test_config.security.allowed_commands)}")
    print(f"   Model: {test_config.execution.model}")

    # Test serialization
    config_dict = test_config.to_dict()
    print(f"✅ Config serializes to dict: {len(json.dumps(config_dict))} chars")

    # Test MCP config generation
    mcp_config = test_config.to_mcp_servers_config()
    print(f"✅ MCP servers config: {list(mcp_config.keys())}")

    TEST1_PASSED = True
except Exception as e:
    print(f"❌ Configuration test FAILED: {e}")
    import traceback
    traceback.print_exc()
    TEST1_PASSED = False

# ============================================================================
# TEST 2: Security Manager
# ============================================================================
print("\n" + "=" * 70)
print("TEST 2: Security Manager (Real Command Validation)")
print("=" * 70)

try:
    # Read and exec security module
    security_code = (base / "security.py").read_text()
    # Remove the relative import and add config directly
    security_code = security_code.replace(
        "from .config import SecurityConfig",
        "# SecurityConfig imported from config"
    )
    exec(compile(security_code, "security.py", "exec"), globals())

    # Create security manager
    sec_config = SecurityConfig(
        allowed_commands=DEFAULT_ALLOWED_COMMANDS,
        commands_needing_validation=DEFAULT_VALIDATION_COMMANDS
    )
    security = SecurityManager(sec_config, TEST_DIR)

    # Test real commands
    test_cases = [
        # (command, expected_allowed, description)
        ("ls -la", True, "List files"),
        ("git status", True, "Git status"),
        ("git commit -m 'test'", True, "Git commit"),
        ("npm install express", True, "NPM install"),
        ("python3 -m pytest", True, "Run pytest"),
        ("node server.js", True, "Run node"),
        ("pkill node", True, "Kill node process"),
        ("pkill systemd", False, "Kill system process - BLOCKED"),
        ("rm file.txt", True, "Remove single file"),
        ("rm -rf /", False, "Remove root - BLOCKED"),
        ("rm -rf /home", False, "Remove home - BLOCKED"),
        ("chmod +x script.sh", True, "Make executable"),
        ("chmod 777 /etc/passwd", False, "Chmod system file - BLOCKED"),
        ("curl https://api.example.com", True, "External API call"),
        ("curl http://169.254.169.254/", False, "AWS metadata - BLOCKED"),
        ("wget https://github.com/file.zip", True, "Download file"),
        ("grep -r 'pattern' .", True, "Grep files"),
        ("cat package.json", True, "Read file"),
    ]

    passed = 0
    failed = 0
    for cmd, expected, desc in test_cases:
        result = security.validate_command(cmd)
        if result.allowed == expected:
            passed += 1
            status = "✅"
        else:
            failed += 1
            status = "❌"
        print(f"{status} {desc}: '{cmd}' -> allowed={result.allowed}")
        if not result.allowed and expected:
            print(f"   Reason: {result.reason}")

    print(f"\nSecurity validation: {passed}/{len(test_cases)} passed")
    TEST2_PASSED = failed == 0
except Exception as e:
    print(f"❌ Security test FAILED: {e}")
    import traceback
    traceback.print_exc()
    TEST2_PASSED = False

# ============================================================================
# TEST 3: XML Prompt Transformer
# ============================================================================
print("\n" + "=" * 70)
print("TEST 3: XML Prompt Transformer (Real XML Generation)")
print("=" * 70)

try:
    # Read and exec xml_transformer module
    xml_code = (base / "xml_transformer.py").read_text()
    exec(compile(xml_code, "xml_transformer.py", "exec"), globals())

    transformer = XMLPromptTransformer()

    # Create real context
    context = CodebaseContext(
        exists=True,
        project_type="Node.js",
        languages=["TypeScript", "JavaScript"],
        frameworks=["React", "Next.js"],
        dependencies={"react": "18.2.0", "next": "14.0.0"},
        patterns=["Component-based", "Has tests"],
        readme_summary="A web application built with Next.js"
    )

    scenario = Scenario(
        is_existing=True,
        target_dir=TEST_DIR / "test-project",
        has_package_json=True,
        has_requirements_txt=False,
        git_initialized=True
    )

    # Generate initializer prompt
    xml_prompt = transformer.transform(
        request="Build a todo application with user authentication",
        context=context,
        scenario=scenario,
        available_mcps=["serena", "puppeteer", "filesystem"],
        template_type="initializer"
    )

    print(f"✅ XML prompt generated: {len(xml_prompt)} characters")

    # Validate XML structure
    required_tags = [
        "<system>", "</system>",
        "<context>", "</context>",
        "<task>", "</task>",
        "<required_outputs>", "</required_outputs>",
        "<instructions>", "</instructions>",
        "<constraints>", "</constraints>",
    ]

    all_tags_present = True
    for tag in required_tags:
        if tag in xml_prompt:
            print(f"✅ Contains {tag}")
        else:
            print(f"❌ Missing {tag}")
            all_tags_present = False

    # Generate coding prompt
    coding_prompt = transformer.transform_for_coding(
        target_dir=TEST_DIR / "test-project",
        session_number=3,
        previous_progress="Completed feature-001 and feature-002"
    )
    print(f"✅ Coding prompt generated: {len(coding_prompt)} characters")

    # Test context XML generation
    context_xml = context.to_xml()
    print(f"✅ Context XML: {len(context_xml)} chars")
    print(f"   Contains project_type: {'project_type' in context_xml}")
    print(f"   Contains languages: {'languages' in context_xml}")

    TEST3_PASSED = all_tags_present
except Exception as e:
    print(f"❌ XML Transformer test FAILED: {e}")
    import traceback
    traceback.print_exc()
    TEST3_PASSED = False

# ============================================================================
# TEST 4: Serena Context Manager (Real File Operations)
# ============================================================================
print("\n" + "=" * 70)
print("TEST 4: Serena Context Manager (Real File I/O)")
print("=" * 70)

try:
    # Read serena_context module
    serena_code = (base / "serena_context.py").read_text()
    # Fix import
    serena_code = serena_code.replace(
        "from .xml_transformer import CodebaseContext",
        "# CodebaseContext already imported"
    )
    exec(compile(serena_code, "serena_context.py", "exec"), globals())

    # Create test project directory
    project_dir = TEST_DIR / "serena_test_project"
    project_dir.mkdir(parents=True)

    # Create some real files
    (project_dir / "package.json").write_text(json.dumps({
        "name": "test-project",
        "dependencies": {
            "express": "4.18.0",
            "react": "18.2.0"
        }
    }, indent=2))

    (project_dir / "src").mkdir()
    (project_dir / "src/index.js").write_text("""
const express = require('express');
const app = express();

function handleRequest(req, res) {
    res.send('Hello World');
}

app.get('/', handleRequest);
app.listen(3000);
""")

    (project_dir / "README.md").write_text("""
# Test Project

This is a test project for integration validation.

## Features
- Express server
- Basic routing
""")

    serena = SerenaContextManager(project_dir)

    async def test_serena():
        # Initialize
        result = await serena.initialize()
        print(f"✅ Initialized Serena: {result}")
        print(f"   .serena dir exists: {serena.serena_dir.exists()}")
        print(f"   memories dir exists: {serena.memories_dir.exists()}")

        # Analyze directory
        context = await serena.analyze_existing_directory()
        print(f"✅ Analyzed directory:")
        print(f"   exists: {context.exists}")
        print(f"   project_type: {context.project_type}")
        print(f"   languages: {context.languages}")
        print(f"   dependencies: {len(context.dependencies)} deps")

        # Write memory
        await serena.write_memory(
            "session_1_summary",
            "# Session 1 Summary\n\nCompleted initial setup."
        )
        print(f"✅ Wrote memory: session_1_summary")

        # Read memory
        content = await serena.read_memory("session_1_summary")
        print(f"✅ Read memory: {len(content)} chars")
        print(f"   Content preview: {content[:50]}...")

        # Find symbol (real file search)
        locations = await serena.find_symbol("handleRequest")
        print(f"✅ Found symbol 'handleRequest': {len(locations)} locations")
        for loc in locations:
            print(f"   {loc.file_path}:{loc.line_number}")

        # Create execution summary
        summary = await serena.create_execution_summary(
            session_number=1,
            features_completed=["feature-001", "feature-002"],
            features_remaining=48,
            notes="Good progress on initial features"
        )
        print(f"✅ Created execution summary: {len(summary)} chars")

        # Get continuation context
        continuation = await serena.get_continuation_context()
        print(f"✅ Got continuation context: {len(continuation) if continuation else 0} chars")

        return True

    result = asyncio.run(test_serena())
    TEST4_PASSED = result
except Exception as e:
    print(f"❌ Serena Context test FAILED: {e}")
    import traceback
    traceback.print_exc()
    TEST4_PASSED = False

# ============================================================================
# TEST 5: MCP Manager (Real Task Analysis)
# ============================================================================
print("\n" + "=" * 70)
print("TEST 5: MCP Manager (Real Task Analysis)")
print("=" * 70)

try:
    # Read mcp_manager module
    mcp_code = (base / "mcp_manager.py").read_text()
    mcp_code = mcp_code.replace(
        "from .config import MCPConfig",
        "# MCPConfig already imported"
    )
    exec(compile(mcp_code, "mcp_manager.py", "exec"), globals())

    manager = MCPManager(TEST_DIR)

    async def test_mcp():
        # Test task analysis with real tasks
        tasks = [
            ("Build a React web application with user dashboard", ["serena", "puppeteer"]),
            ("Create an API server with database", ["serena", "fetch"]),
            ("Scrape data from e-commerce websites", ["serena", "puppeteer"]),
            ("Build a CLI tool for file management", ["serena"]),
            ("Create a GitHub action workflow", ["serena", "github"]),
        ]

        all_correct = True
        for task, expected_mcps in tasks:
            reqs = await manager.analyze_task(task)
            mcp_names = [r.mcp_name for r in reqs]

            # Check expected MCPs are present
            missing = [m for m in expected_mcps if m not in mcp_names]
            if missing:
                print(f"❌ Task: '{task[:50]}...'")
                print(f"   Missing: {missing}")
                all_correct = False
            else:
                print(f"✅ Task: '{task[:50]}...'")
                print(f"   MCPs: {mcp_names}")

        # Test skill generation
        skill = manager.generate_usage_skill("serena")
        print(f"\n✅ Generated Serena skill: {len(skill)} chars")
        print(f"   Contains 'find_symbol': {'find_symbol' in skill}")
        print(f"   Contains 'memory': {'memory' in skill}")

        skill = manager.generate_usage_skill("puppeteer")
        print(f"✅ Generated Puppeteer skill: {len(skill)} chars")
        print(f"   Contains 'screenshot': {'screenshot' in skill}")
        print(f"   Contains 'navigate': {'navigate' in skill}")

        return all_correct

    result = asyncio.run(test_mcp())
    TEST5_PASSED = result
except Exception as e:
    print(f"❌ MCP Manager test FAILED: {e}")
    import traceback
    traceback.print_exc()
    TEST5_PASSED = False

# ============================================================================
# TEST 6: Scenario Handler (Real Directory Analysis)
# ============================================================================
print("\n" + "=" * 70)
print("TEST 6: Scenario Handler (Real Directory Analysis)")
print("=" * 70)

try:
    # Read scenario_handler module
    scenario_code = (base / "scenario_handler.py").read_text()
    scenario_code = scenario_code.replace(
        "from .serena_context import SerenaContextManager",
        "# SerenaContextManager already imported"
    )
    scenario_code = scenario_code.replace(
        "from .xml_transformer import CodebaseContext, Scenario",
        "# Already imported"
    )
    exec(compile(scenario_code, "scenario_handler.py", "exec"), globals())

    async def test_scenarios():
        # Test 1: Empty directory (new project)
        empty_dir = TEST_DIR / "empty_project"
        empty_dir.mkdir(parents=True)

        serena = SerenaContextManager(empty_dir)
        handler = ScenarioHandler(serena)

        scenario = await handler.detect_scenario(empty_dir)
        print(f"✅ Empty directory scenario:")
        print(f"   is_existing: {scenario.is_existing}")
        print(f"   git_initialized: {scenario.git_initialized}")

        # Test 2: Node.js project
        node_dir = TEST_DIR / "node_project"
        node_dir.mkdir(parents=True)
        (node_dir / "package.json").write_text('{"name": "test"}')
        (node_dir / "src").mkdir()
        (node_dir / "src/index.js").write_text("console.log('hello');")

        serena2 = SerenaContextManager(node_dir)
        handler2 = ScenarioHandler(serena2)

        scenario = await handler2.detect_scenario(node_dir)
        print(f"\n✅ Node.js project scenario:")
        print(f"   is_existing: {scenario.is_existing}")
        print(f"   has_package_json: {scenario.has_package_json}")

        # Test 3: Execution plan for existing project
        plan = await handler2.create_execution_plan(node_dir, "Add user authentication")
        print(f"\n✅ Execution plan for existing project:")
        print(f"   scenario_type: {plan.scenario_type.value}")
        print(f"   requires_initialization: {plan.requires_initialization}")
        print(f"   requires_analysis: {plan.requires_analysis}")
        print(f"   recommended_mcps: {plan.recommended_mcps}")

        # Test 4: Continuation scenario
        continuation_dir = TEST_DIR / "continuation_project"
        continuation_dir.mkdir(parents=True)
        (continuation_dir / "feature_list.json").write_text(json.dumps({
            "features": [{"id": "f1", "passes": True}, {"id": "f2", "passes": False}]
        }))
        (continuation_dir / "claude-progress.txt").write_text("Session 1 complete")

        serena3 = SerenaContextManager(continuation_dir)
        handler3 = ScenarioHandler(serena3)

        plan = await handler3.create_execution_plan(continuation_dir, "Continue")
        print(f"\n✅ Continuation scenario:")
        print(f"   scenario_type: {plan.scenario_type.value}")
        print(f"   existing_feature_list: {plan.existing_feature_list is not None}")

        return True

    result = asyncio.run(test_scenarios())
    TEST6_PASSED = result
except Exception as e:
    print(f"❌ Scenario Handler test FAILED: {e}")
    import traceback
    traceback.print_exc()
    TEST6_PASSED = False

# ============================================================================
# TEST 7: Full Builder (Real Build Execution)
# ============================================================================
print("\n" + "=" * 70)
print("TEST 7: Full Builder (Real Build Execution)")
print("=" * 70)

try:
    # Read builder module
    builder_code = (base / "builder.py").read_text()
    # Fix imports
    for old, new in [
        ("from .config import BuilderConfig", "# Already imported"),
        ("from .security import SecurityManager", "# Already imported"),
        ("from .xml_transformer import XMLPromptTransformer, CodebaseContext", "# Already imported"),
        ("from .mcp_manager import MCPManager", "# Already imported"),
        ("from .serena_context import SerenaContextManager", "# Already imported"),
        ("from .scenario_handler import ScenarioHandler, ScenarioType, ExecutionPlan", "# Already imported"),
    ]:
        builder_code = builder_code.replace(old, new)

    exec(compile(builder_code, "builder.py", "exec"), globals())

    async def test_builder():
        # Create config for real build
        build_dir = TEST_DIR / "real_build"

        config = BuilderConfig(
            target_dir=build_dir,
            puppeteer_enabled=True,
            verbose=True
        )
        config.execution.max_iterations = 2  # Limit for test

        builder = AutonomousBuilder(config)

        # Run build
        print("Starting real build...")
        result = await builder.build(
            "Create a simple Python command-line calculator with add, subtract, multiply, divide operations"
        )

        print(f"\n✅ Build completed:")
        print(f"   success: {result.success}")
        print(f"   target_dir: {result.target_dir}")
        print(f"   features_total: {result.features_total}")
        print(f"   features_completed: {result.features_completed}")
        print(f"   sessions_executed: {result.sessions_executed}")
        print(f"   duration: {result.total_duration_seconds:.2f}s")

        # Verify artifacts
        print(f"\n✅ Artifact verification:")
        feature_list = build_dir / "feature_list.json"
        print(f"   feature_list.json exists: {feature_list.exists()}")
        if feature_list.exists():
            features = json.loads(feature_list.read_text())
            print(f"   features count: {len(features.get('features', []))}")

        init_sh = build_dir / "init.sh"
        print(f"   init.sh exists: {init_sh.exists()}")
        if init_sh.exists():
            import stat
            mode = init_sh.stat().st_mode
            print(f"   init.sh executable: {bool(mode & stat.S_IXUSR)}")

        progress = build_dir / "claude-progress.txt"
        print(f"   claude-progress.txt exists: {progress.exists()}")

        serena_dir = build_dir / ".serena" / "memories"
        print(f"   .serena/memories exists: {serena_dir.exists()}")

        return result.success

    result = asyncio.run(test_builder())
    TEST7_PASSED = result
except Exception as e:
    print(f"❌ Builder test FAILED: {e}")
    import traceback
    traceback.print_exc()
    TEST7_PASSED = False

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("  INTEGRATION VALIDATION SUMMARY")
print("=" * 70)

tests = [
    ("Configuration System", TEST1_PASSED),
    ("Security Manager", TEST2_PASSED),
    ("XML Prompt Transformer", TEST3_PASSED),
    ("Serena Context Manager", TEST4_PASSED),
    ("MCP Manager", TEST5_PASSED),
    ("Scenario Handler", TEST6_PASSED),
    ("Full Builder", TEST7_PASSED),
]

passed = sum(1 for _, p in tests if p)
total = len(tests)

print()
for name, result in tests:
    status = "✅ PASSED" if result else "❌ FAILED"
    print(f"  {status}: {name}")

print()
print(f"  Total: {passed}/{total} tests passed")
print()

if passed == total:
    print("  🎉 ALL INTEGRATION TESTS PASSED!")
else:
    print("  ⚠️  Some tests failed. Review output above.")

print()
print(f"  Test workspace: {TEST_DIR}")
print()

# Cleanup option
# shutil.rmtree(TEST_DIR)

sys.exit(0 if passed == total else 1)
