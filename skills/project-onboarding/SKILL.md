# Project Onboarding Skill

## Overview

**Purpose**: Deep codebase analysis and Shannon infrastructure setup for projects that weren't built with Shannon from the start.

**When invoked**: By `/shannon:init` command for comprehensive project onboarding.

**Responsibilities**:
1. Deep-scan entire codebase (every file)
2. Generate comprehensive project index
3. Detect architecture patterns
4. Configure validation gates
5. Audit testing compliance (NO MOCKS)
6. Generate Shannon documentation
7. Create initial checkpoint

---

## Invocation

### By Command

```markdown
@skill project-onboarding
- Input:
  * project_root: {absolute_path_to_project}
  * mode: "quick" | "standard" | "full"
  * dry_run: true | false
- Options:
  * analyze_all_files: true (always true for init)
  * run_validation: true (only for --full flag)
  * create_checkpoint: true
- Output: onboarding_result
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| project_root | string | Yes | Absolute path to project root |
| mode | enum | No | "quick", "standard" (default), "full" |
| dry_run | boolean | No | Show plan without executing (default: false) |
| analyze_all_files | boolean | No | Analyze every file (default: true) |
| run_validation | boolean | No | Run validation gates (default: false, true for --full) |
| create_checkpoint | boolean | No | Create initial checkpoint (default: true) |

---

## Workflow

### Phase 1: Environment Validation

**Step 1.1: Validate Project Root**

```python
def validate_project_root(project_root):
    """Ensure we're in a valid project directory"""
    
    # Check directory exists
    if not os.path.exists(project_root):
        return error("Project root does not exist")
    
    # Check not empty
    if len(os.listdir(project_root)) == 0:
        return error("Project root is empty")
    
    # Check for project indicators
    indicators = [
        ".git",
        "package.json",
        "Cargo.toml",
        "go.mod",
        "pom.xml",
        "build.gradle",
        "CMakeLists.txt",
        "Makefile",
        "setup.py",
        "pyproject.toml"
    ]
    
    has_indicator = any(
        os.path.exists(os.path.join(project_root, indicator))
        for indicator in indicators
    )
    
    if not has_indicator:
        return warning("No project files detected (package.json, etc.). Continue anyway?")
    
    return success()
```

**Step 1.2: Check Existing Shannon Init**

```python
def check_existing_init(project_root):
    """Check if project already Shannon-initialized"""
    
    shannon_dir = os.path.join(project_root, ".shannon")
    
    if os.path.exists(shannon_dir):
        # Check config file
        config_file = os.path.join(shannon_dir, "config.json")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            init_date = config.get("initialized_at")
            version = config.get("shannon_version")
            
            return {
                "already_initialized": True,
                "init_date": init_date,
                "shannon_version": version,
                "ask_reinit": True
            }
    
    return {"already_initialized": False}
```

**Step 1.3: Verify Serena MCP**

```python
def verify_serena_mcp():
    """Check if Serena MCP is available"""
    
    try:
        # Attempt to connect to Serena
        result = mcp_call("serena", "ping")
        return {"available": True, "version": result.version}
    except MCPNotFoundError:
        return {
            "available": False,
            "offer_setup": True,
            "impact": "Limited persistence, no cross-session context"
        }
```

**Step 1.4: Estimate Project Size**

```python
def estimate_project_size(project_root):
    """Estimate project size for time estimate"""
    
    file_count = 0
    total_size = 0
    
    # Respect .gitignore
    gitignore_patterns = parse_gitignore(project_root)
    
    for root, dirs, files in os.walk(project_root):
        # Filter directories
        dirs[:] = [d for d in dirs if not should_ignore(d, gitignore_patterns)]
        
        for file in files:
            if not should_ignore(file, gitignore_patterns):
                file_count += 1
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
    
    # Estimate time
    if file_count < 100:
        time_estimate = "2-3 minutes"
        size_category = "small"
    elif file_count < 1000:
        time_estimate = "5-10 minutes"
        size_category = "medium"
    elif file_count < 10000:
        time_estimate = "15-30 minutes"
        size_category = "large"
    else:
        time_estimate = "30-60 minutes"
        size_category = "huge"
    
    return {
        "file_count": file_count,
        "total_size_mb": total_size / (1024 * 1024),
        "size_category": size_category,
        "time_estimate": time_estimate
    }
```

---

### Phase 2: Deep Codebase Analysis

**Step 2.1: Scan All Files**

```python
def scan_all_files(project_root, mode="standard"):
    """Scan every file in project"""
    
    results = {
        "files": [],
        "languages": Counter(),
        "file_types": Counter(),
        "total_loc": 0
    }
    
    gitignore_patterns = parse_gitignore(project_root)
    
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if not should_ignore(d, gitignore_patterns)]
        
        for file in files:
            if should_ignore(file, gitignore_patterns):
                continue
            
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_root)
            
            # Detect language
            extension = os.path.splitext(file)[1]
            language = detect_language(extension)
            
            # Count lines
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    loc = len([l for l in lines if l.strip() and not l.strip().startswith(('//', '#', '/*'))])
            except:
                loc = 0
            
            # Analyze file (quick vs full)
            if mode == "quick":
                analysis = {"path": relative_path, "language": language, "loc": loc}
            else:
                analysis = analyze_file_deep(file_path, language)
            
            results["files"].append(analysis)
            results["languages"][language] += loc
            results["total_loc"] += loc
            
            # Progress indicator every 50 files
            if len(results["files"]) % 50 == 0:
                print(f"   📁 {len(results['files'])} files scanned...")
    
    return results
```

**Step 2.2: Detect Architecture Pattern**

```python
def detect_architecture(file_structure):
    """Detect architectural pattern from directory structure"""
    
    directories = set()
    for file_info in file_structure["files"]:
        dir_path = os.path.dirname(file_info["path"])
        directories.add(dir_path)
    
    # Pattern detection
    patterns = {
        "mvc": ["models", "views", "controllers"],
        "mvvm": ["models", "views", "viewmodels"],
        "clean": ["domain", "data", "presentation"],
        "layered": ["ui", "business", "data"],
        "microservices": ["services", "gateway"],
        "monolith": ["src", "lib"],
        "serverless": ["functions", "lambda"],
        "frontend-spa": ["components", "pages", "hooks"]
    }
    
    detected_patterns = []
    for pattern_name, required_dirs in patterns.items():
        matches = sum(1 for req_dir in required_dirs 
                      if any(req_dir in dir_path for dir_path in directories))
        confidence = matches / len(required_dirs)
        
        if confidence >= 0.6:
            detected_patterns.append({
                "pattern": pattern_name,
                "confidence": confidence
            })
    
    # Return best match
    if detected_patterns:
        best_pattern = max(detected_patterns, key=lambda x: x["confidence"])
        return best_pattern["pattern"]
    else:
        return "unstructured"
```

**Step 2.3: Calculate Complexity Metrics**

```python
def calculate_complexity_metrics(file_structure):
    """Calculate project-wide complexity metrics"""
    
    metrics = {
        "total_files": len(file_structure["files"]),
        "total_loc": file_structure["total_loc"],
        "avg_file_size": file_structure["total_loc"] / len(file_structure["files"]),
        "complexity_hotspots": [],
        "technical_debt_score": 0
    }
    
    # Find complexity hotspots (files > 500 LOC)
    for file_info in file_structure["files"]:
        if file_info.get("loc", 0) > 500:
            metrics["complexity_hotspots"].append({
                "path": file_info["path"],
                "loc": file_info["loc"],
                "reason": "Large file (>500 LOC)"
            })
    
    # Calculate technical debt (simplified)
    # Real implementation would analyze code quality
    debt_factors = []
    if metrics["avg_file_size"] > 300:
        debt_factors.append("Large average file size")
    if len(metrics["complexity_hotspots"]) > 10:
        debt_factors.append("Many large files")
    
    metrics["technical_debt_score"] = len(debt_factors) * 20
    metrics["debt_factors"] = debt_factors
    
    return metrics
```

---

### Phase 3: Tech Stack Detection

**Step 3.1: Detect Tech Stack**

```python
def detect_tech_stack(project_root, file_structure):
    """Detect technologies, frameworks, and versions"""
    
    tech_stack = {
        "languages": {},
        "frontend": [],
        "backend": [],
        "database": [],
        "testing": [],
        "build": [],
        "infrastructure": []
    }
    
    # Language breakdown from file structure
    total_loc = file_structure["total_loc"]
    for lang, loc in file_structure["languages"].items():
        percentage = (loc / total_loc) * 100
        tech_stack["languages"][lang] = {
            "lines": loc,
            "percentage": round(percentage, 1)
        }
    
    # Detect from package managers
    package_files = {
        "package.json": detect_npm_stack,
        "Cargo.toml": detect_rust_stack,
        "go.mod": detect_go_stack,
        "requirements.txt": detect_python_stack,
        "Gemfile": detect_ruby_stack,
        "build.gradle": detect_java_stack
    }
    
    for package_file, detector_func in package_files.items():
        file_path = os.path.join(project_root, package_file)
        if os.path.exists(file_path):
            detected = detector_func(file_path)
            tech_stack = merge_detected_stack(tech_stack, detected)
    
    return tech_stack

def detect_npm_stack(package_json_path):
    """Detect Node.js/npm stack"""
    
    with open(package_json_path, 'r') as f:
        package = json.load(f)
    
    dependencies = {**package.get("dependencies", {}), **package.get("devDependencies", {})}
    
    stack = {
        "frontend": [],
        "backend": [],
        "testing": [],
        "build": []
    }
    
    # Frontend detection
    if "react" in dependencies:
        stack["frontend"].append(f"React {dependencies['react']}")
    if "vue" in dependencies:
        stack["frontend"].append(f"Vue {dependencies['vue']}")
    if "next" in dependencies:
        stack["frontend"].append(f"Next.js {dependencies['next']}")
    
    # Backend detection
    if "express" in dependencies:
        stack["backend"].append(f"Express {dependencies['express']}")
    if "fastify" in dependencies:
        stack["backend"].append(f"Fastify {dependencies['fastify']}")
    
    # Testing detection
    if "jest" in dependencies:
        stack["testing"].append(f"Jest {dependencies['jest']}")
    if "vitest" in dependencies:
        stack["testing"].append(f"Vitest {dependencies['vitest']}")
    if "playwright" in dependencies:
        stack["testing"].append(f"Playwright {dependencies['playwright']}")
    if "puppeteer" in dependencies:
        stack["testing"].append(f"Puppeteer {dependencies['puppeteer']}")
    
    # Build detection
    if "vite" in dependencies:
        stack["build"].append(f"Vite {dependencies['vite']}")
    if "webpack" in dependencies:
        stack["build"].append(f"Webpack {dependencies['webpack']}")
    
    return stack
```

---

### Phase 4: Validation Gates Configuration

**Step 4.1: Auto-Detect Validation Commands**

```python
def detect_validation_gates(project_root, tech_stack):
    """Auto-detect test, build, lint commands"""
    
    gates = {
        "test": None,
        "build": None,
        "lint": None
    }
    
    # Check package.json scripts
    package_json_path = os.path.join(project_root, "package.json")
    if os.path.exists(package_json_path):
        with open(package_json_path, 'r') as f:
            package = json.load(f)
        
        scripts = package.get("scripts", {})
        
        if "test" in scripts:
            gates["test"] = {"command": "npm test", "source": "package.json"}
        if "build" in scripts:
            gates["build"] = {"command": "npm run build", "source": "package.json"}
        if "lint" in scripts:
            gates["lint"] = {"command": "npm run lint", "source": "package.json"}
    
    # Check Makefile
    makefile_path = os.path.join(project_root, "Makefile")
    if os.path.exists(makefile_path):
        with open(makefile_path, 'r') as f:
            makefile_content = f.read()
        
        if "test:" in makefile_content and not gates["test"]:
            gates["test"] = {"command": "make test", "source": "Makefile"}
        if "build:" in makefile_content and not gates["build"]:
            gates["build"] = {"command": "make build", "source": "Makefile"}
    
    # Check language-specific defaults
    if "Python" in tech_stack["languages"]:
        if not gates["test"]:
            if os.path.exists(os.path.join(project_root, "pytest.ini")):
                gates["test"] = {"command": "pytest", "source": "detected (pytest.ini)"}
    
    if "Go" in tech_stack["languages"]:
        if not gates["test"]:
            gates["test"] = {"command": "go test ./...", "source": "language default"}
    
    # Prompt for missing gates
    for gate_name, gate_info in gates.items():
        if not gate_info:
            gates[gate_name] = {"command": None, "source": "user-prompted"}
    
    return gates
```

---

### Phase 5: NO MOCKS Compliance Audit

**Step 5.1: Audit Testing Compliance**

```python
def audit_testing_compliance(project_root, tech_stack):
    """Check NO MOCKS compliance in existing tests"""
    
    test_dirs = find_test_directories(project_root)
    test_files = []
    
    for test_dir in test_dirs:
        for root, dirs, files in os.walk(test_dir):
            for file in files:
                if is_test_file(file):
                    test_files.append(os.path.join(root, file))
    
    violations = []
    total_tests = 0
    
    for test_file in test_files:
        with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Count tests
        test_count = count_tests(content, tech_stack["testing"])
        total_tests += test_count
        
        # Check for mock violations
        mock_patterns = [
            r"jest\.mock\(",
            r"@mock",
            r"\.mock\(",
            r"sinon\.",
            r"unittest\.mock",
            r"from unittest.mock import",
            r"MockK",
            r"mock\s+object"
        ]
        
        for pattern in mock_patterns:
            matches = re.findall(pattern, content)
            if matches:
                violations.append({
                    "file": os.path.relpath(test_file, project_root),
                    "violation_type": "mock_usage",
                    "pattern": pattern,
                    "count": len(matches)
                })
    
    # Calculate compliance
    violation_count = sum(v["count"] for v in violations)
    compliant_tests = max(0, total_tests - violation_count)
    compliance_percentage = (compliant_tests / total_tests * 100) if total_tests > 0 else 100
    
    return {
        "total_tests": total_tests,
        "compliant_tests": compliant_tests,
        "violations": violations,
        "compliance_percentage": round(compliance_percentage, 1)
    }
```

---

### Phase 6: Documentation Generation

**Step 6.1: Generate SHANNON.md**

```python
def generate_shannon_md(onboarding_data):
    """Generate SHANNON.md integration guide"""
    
    content = f"""# Shannon Framework Integration

This project has been initialized with Shannon Framework on {onboarding_data["timestamp"]}.

## Quick Start

```bash
# Start new session
/shannon:prime

# Check project status
/shannon:status

# Analyze specification
/shannon:spec "your task description"

# Execute with waves
/shannon:wave
```

## Project Profile

- **Complexity**: {onboarding_data["complexity_score"]}/1.0 ({onboarding_data["complexity_label"]})
- **Domains**: {format_domain_breakdown(onboarding_data["domains"])}
- **Architecture**: {onboarding_data["architecture_pattern"]}
- **Testing**: {onboarding_data["test_framework"]} ({onboarding_data["no_mocks_compliance"]}% NO MOCKS compliant)

## Tech Stack

{format_tech_stack(onboarding_data["tech_stack"])}

## Validation Gates

- **Test**: `{onboarding_data["validation_gates"]["test"]["command"]}`
- **Build**: `{onboarding_data["validation_gates"]["build"]["command"]}`
{f'- **Lint**: `{onboarding_data["validation_gates"]["lint"]["command"]}`' if onboarding_data["validation_gates"]["lint"] else ''}

## MCP Requirements

{format_mcp_requirements(onboarding_data["mcp_recommendations"])}

## Shannon Readiness Score: {onboarding_data["readiness_score"]}/100

{format_readiness_breakdown(onboarding_data["readiness_breakdown"])}

## Next Steps

1. Configure missing MCPs: `/shannon:check_mcps`
{f'2. Migrate tests to NO MOCKS: See TESTING_PHILOSOPHY.md' if onboarding_data["no_mocks_compliance"] < 80 else ''}
{f'{"3" if onboarding_data["no_mocks_compliance"] < 80 else "2"}. Set North Star goal: `/shannon:north_star "your project goal"`'}
{f'{"4" if onboarding_data["no_mocks_compliance"] < 80 else "3"}. Begin development with Shannon'}

---

**Shannon Version**: {onboarding_data["shannon_version"]}
**Initialized**: {onboarding_data["timestamp"]}
"""
    
    return content
```

**Step 6.2: Generate AGENTS.md**

```python
def generate_agents_md(onboarding_data):
    """Generate AGENTS.md for agent onboarding"""
    
    content = f"""# Project Context for AI Agents

## Architecture Overview

**Pattern**: {onboarding_data["architecture_pattern"]}

{onboarding_data["architecture_description"]}

## Directory Structure

```
{generate_tree_view(onboarding_data["file_structure"])}
```

## Key Components

{format_key_components(onboarding_data["components"])}

## Tech Stack

**Languages**:
{format_languages(onboarding_data["tech_stack"]["languages"])}

**Frameworks**:
- Frontend: {", ".join(onboarding_data["tech_stack"]["frontend"])}
- Backend: {", ".join(onboarding_data["tech_stack"]["backend"])}
- Testing: {", ".join(onboarding_data["tech_stack"]["testing"])}

## Development Workflow

**Building**:
```bash
{onboarding_data["validation_gates"]["build"]["command"]}
```

**Testing**:
```bash
{onboarding_data["validation_gates"]["test"]["command"]}
```

**Linting**:
```bash
{onboarding_data["validation_gates"]["lint"]["command"] if onboarding_data["validation_gates"]["lint"] else "Not configured"}
```

## Testing Strategy

{format_testing_strategy(onboarding_data)}

## Complexity Hotspots

{format_complexity_hotspots(onboarding_data["complexity_hotspots"])}

---

**Generated by Shannon Framework** v{onboarding_data["shannon_version"]}
**Last Updated**: {onboarding_data["timestamp"]}
"""
    
    return content
```

---

### Phase 7: Checkpoint Creation

**Step 7.1: Create Initial Checkpoint**

```python
def create_initial_checkpoint(onboarding_data, serena_available):
    """Create shannon-init-baseline checkpoint"""
    
    checkpoint_data = {
        "checkpoint_name": "shannon-init-baseline",
        "timestamp": onboarding_data["timestamp"],
        "project_index": onboarding_data["file_structure"],
        "architecture_map": onboarding_data["architecture"],
        "tech_stack_profile": onboarding_data["tech_stack"],
        "baseline_metrics": onboarding_data["metrics"],
        "validation_gates": onboarding_data["validation_gates"],
        "mcp_recommendations": onboarding_data["mcp_recommendations"],
        "testing_compliance": onboarding_data["testing_compliance"],
        "readiness_score": onboarding_data["readiness_score"]
    }
    
    if serena_available:
        # Save to Serena MCP
        mcp_call("serena", "write_memory", {
            "key": "shannon-init-baseline",
            "value": checkpoint_data
        })
        return {"saved": True, "location": "Serena MCP"}
    else:
        # Save locally
        local_path = os.path.join(onboarding_data["project_root"], ".shannon", "baseline-checkpoint.json")
        with open(local_path, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)
        return {"saved": True, "location": "Local (.shannon/)"}
```

---

### Phase 8: Readiness Score Calculation

**Step 8.1: Calculate Shannon Readiness Score**

```python
def calculate_readiness_score(onboarding_data):
    """Calculate Shannon Readiness Score (0-100)"""
    
    score = 0
    breakdown = {}
    
    # MCP Coverage (30 points)
    mcp_required = len([m for m in onboarding_data["mcp_recommendations"] if m["tier"] == "required"])
    mcp_configured = len([m for m in onboarding_data["mcp_recommendations"] if m["tier"] == "required" and m["available"]])
    mcp_score = (mcp_configured / mcp_required * 30) if mcp_required > 0 else 30
    score += mcp_score
    breakdown["mcp_coverage"] = round(mcp_score, 1)
    
    # Testing Quality (25 points)
    compliance = onboarding_data["testing_compliance"]["compliance_percentage"]
    testing_score = (compliance / 100 * 25)
    score += testing_score
    breakdown["testing_quality"] = round(testing_score, 1)
    
    # Documentation (20 points)
    docs_created = [
        os.path.exists(os.path.join(onboarding_data["project_root"], "SHANNON.md")),
        os.path.exists(os.path.join(onboarding_data["project_root"], "AGENTS.md")),
        os.path.exists(os.path.join(onboarding_data["project_root"], ".shannon", "config.json"))
    ]
    docs_score = (sum(docs_created) / len(docs_created) * 20)
    score += docs_score
    breakdown["documentation"] = round(docs_score, 1)
    
    # Validation Gates (15 points)
    gates_configured = sum(1 for g in onboarding_data["validation_gates"].values() if g and g["command"])
    gates_score = (gates_configured / 3 * 15)  # 3 gates: test, build, lint
    score += gates_score
    breakdown["validation_gates"] = round(gates_score, 1)
    
    # Architecture Clarity (10 points)
    arch_pattern = onboarding_data["architecture_pattern"]
    if arch_pattern != "unstructured":
        arch_score = 10
    elif len(onboarding_data["file_structure"]["files"]) < 50:
        arch_score = 8  # Small project, acceptable
    else:
        arch_score = 5  # Large unstructured project
    score += arch_score
    breakdown["architecture_clarity"] = arch_score
    
    return {
        "total_score": round(score, 1),
        "breakdown": breakdown,
        "grade": get_readiness_grade(score)
    }

def get_readiness_grade(score):
    """Convert readiness score to grade"""
    if score >= 90:
        return "Excellent"
    elif score >= 80:
        return "Shannon-Ready"
    elif score >= 60:
        return "Good Start"
    else:
        return "Needs Setup"
```

---

## Output Format

```python
{
    "status": "success",
    "project_name": "my-project",
    "project_root": "/path/to/project",
    "initialized_at": "2025-01-15T10:30:00Z",
    "duration_seconds": 420,
    
    "file_structure": {
        "files": [...],
        "languages": {...},
        "total_loc": 15000
    },
    
    "architecture": {
        "pattern": "mvc",
        "description": "...",
        "components": [...]
    },
    
    "tech_stack": {
        "languages": {"JavaScript": {"lines": 10000, "percentage": 66.7}},
        "frontend": ["React 18.2.0", "Vite 4.3.0"],
        "backend": ["Express 4.18.0"],
        "testing": ["Jest 29.5.0"],
        "build": ["Vite"],
        "infrastructure": []
    },
    
    "metrics": {
        "total_files": 234,
        "total_loc": 15000,
        "complexity_score": 0.58,
        "complexity_label": "MODERATE",
        "technical_debt_score": 40,
        "complexity_hotspots": [...]
    },
    
    "validation_gates": {
        "test": {"command": "npm test", "source": "package.json"},
        "build": {"command": "npm run build", "source": "package.json"},
        "lint": {"command": "npm run lint", "source": "package.json"}
    },
    
    "testing_compliance": {
        "total_tests": 234,
        "compliant_tests": 157,
        "violations": [...],
        "compliance_percentage": 67.1
    },
    
    "mcp_recommendations": [
        {"name": "Serena", "tier": "required", "available": true},
        {"name": "Puppeteer", "tier": "primary", "available": false},
        {"name": "Context7", "tier": "primary", "available": false}
    ],
    
    "files_created": [
        ".shannon/config.json",
        ".shannon/project-index.json",
        ".shannon/architecture.json",
        ".shannon/baseline-metrics.json",
        "SHANNON.md",
        "AGENTS.md"
    ],
    
    "checkpoint": {
        "saved": true,
        "location": "Serena MCP",
        "key": "shannon-init-baseline"
    },
    
    "readiness_score": {
        "total_score": 72.5,
        "breakdown": {
            "mcp_coverage": 10.0,
            "testing_quality": 16.8,
            "documentation": 20.0,
            "validation_gates": 15.0,
            "architecture_clarity": 10.0
        },
        "grade": "Good Start"
    },
    
    "next_steps": [
        "Configure Puppeteer MCP: /shannon:check_mcps --setup puppeteer",
        "Configure Context7 MCP: /shannon:check_mcps --setup context7",
        "Migrate 77 mocked tests to NO MOCKS",
        "Prime first Shannon session: /shannon:prime"
    ]
}
```

---

## Anti-Patterns

### ❌ Shallow Scanning

**Don't**:
```python
# Just scan directory names
for dir in os.listdir(project_root):
    print(dir)
```

**Do**:
```python
# Analyze EVERY file
for root, dirs, files in os.walk(project_root):
    for file in files:
        analyze_file_deep(os.path.join(root, file))
```

### ❌ Guessing Tech Stack

**Don't**:
```python
if "src/" in directories:
    tech_stack = "React"  # Assumption
```

**Do**:
```python
# Parse package.json
with open("package.json") as f:
    deps = json.load(f)["dependencies"]
    if "react" in deps:
        tech_stack["frontend"].append(f"React {deps['react']}")
```

### ❌ Skipping Compliance Audit

**Don't**:
```python
# Assume tests are compliant
compliance = 100
```

**Do**:
```python
# Audit every test file for mock usage
for test_file in test_files:
    violations = check_for_mocks(test_file)
    if violations:
        record_violations(violations)
```

---

## Integration with Commands

### `/shannon:init` Command

```markdown
The /shannon:init command delegates all work to this skill:

@skill project-onboarding
- Input:
  * project_root: {cwd}
  * mode: {from flags}
  * dry_run: {--dry-run flag}
- Output: onboarding_result

Then formats and presents the skill output to the user.
```

---

## References

### Core Files
- **PROJECT_MEMORY.md**: Context preservation patterns
- **TESTING_PHILOSOPHY.md**: NO MOCKS enforcement
- **MCP_DISCOVERY.md**: MCP recommendation logic
- **SPEC_ANALYSIS.md**: Complexity scoring

### Related Skills
- **project-indexing**: Codebase scanning (invoked internally)
- **spec-analysis**: Tech stack detection (invoked internally)
- **functional-testing**: Compliance audit (invoked internally)
- **mcp-discovery**: MCP recommendations (invoked internally)
- **context-preservation**: Checkpoint creation (invoked internally)

---

## Notes

- **Comprehensive**: Analyzes EVERY file (no sampling)
- **Accurate**: Detects tech stack from actual project files
- **Actionable**: Provides specific next steps
- **Persistent**: Creates .shannon/ directory with all config
- **Score-Based**: Quantitative readiness score (0-100)

---

**Version**: 5.5.0 (NEW)
**Status**: Core onboarding skill
**Invoked By**: `/shannon:init` command

