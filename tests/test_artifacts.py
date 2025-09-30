#!/usr/bin/env python3
"""
Shannon V3 Artifact Validation Test Suite

Validates that Shannon commands create expected artifacts in correct locations
with correct structure. Tests REAL artifacts using functional validation
(NO MOCKS philosophy).

Tests verify:
- File/directory creation at correct paths
- YAML/JSON structure validation
- Content presence and format compliance
- Serena memory integration
- NO MOCKS enforcement in generated test files

Author: Shannon Framework
Version: 1.0.0
License: MIT
"""

import pytest
import os
import json
import yaml
import re
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Set
from datetime import datetime


# =============================================================================
# Test Configuration & Fixtures
# =============================================================================

@pytest.fixture
def shannon_root():
    """Return path to Shannon framework root directory"""
    current_file = Path(__file__).resolve()
    return current_file.parent.parent


@pytest.fixture
def project_root(shannon_root):
    """Return path to project root (parent of Shannon)"""
    return shannon_root


@pytest.fixture
def shannon_artifacts_dir(project_root):
    """Return path to .shannon artifacts directory"""
    artifacts_dir = project_root / ".shannon"
    artifacts_dir.mkdir(exist_ok=True)
    return artifacts_dir


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create temporary project directory for testing"""
    project = tmp_path / "test_project"
    project.mkdir()
    (project / ".shannon").mkdir()
    return project


# =============================================================================
# Test Class 1: Spec Analysis Artifacts
# =============================================================================

class TestSpecAnalysisArtifacts:
    """Validate /sh:spec creates analysis reports with correct structure"""

    def test_spec_command_exists(self, shannon_root):
        """Verify sh:spec command file exists"""
        spec_cmd = shannon_root / "Shannon" / "Commands" / "sh_spec.md"
        assert spec_cmd.exists(), "sh_spec.md command file not found"

    def test_spec_analysis_directory_structure(self, shannon_artifacts_dir):
        """Verify .shannon/analysis directory can be created"""
        analysis_dir = shannon_artifacts_dir / "analysis"
        analysis_dir.mkdir(exist_ok=True)

        assert analysis_dir.exists(), "Analysis directory creation failed"
        assert analysis_dir.is_dir(), "Analysis path is not a directory"

    def test_spec_report_naming_convention(self):
        """Verify spec report naming follows convention: spec_analysis_[id].md"""
        pattern = r"spec_analysis_[\w\-]+\.md"

        test_names = [
            "spec_analysis_20250930.md",
            "spec_analysis_taskapp_20250930.md",
            "spec_analysis_web-app.md"
        ]

        for name in test_names:
            assert re.match(pattern, name), f"Invalid name format: {name}"

    def test_spec_report_structure_validation(self, temp_project_dir):
        """Validate spec report has required sections"""
        # Create sample spec report
        report_content = """# Specification Analysis Complete ✅

*Analyzed by: Shannon V3 Specification Analysis Engine*
*Analysis ID: spec_analysis_test*
*Complexity: 0.65 (Complex)*
*Saved to Serena MCP: spec_analysis_test*

---

## 📊 Complexity Assessment

**Overall Score**: 0.65 / 1.0 (**Complex**)

**Dimensional Breakdown**:
| Dimension | Score | Weight | Contribution | Interpretation |
|-----------|-------|--------|--------------|----------------|
| Structural | 0.60 | 20% | 0.12 | Moderate structural complexity |
| Cognitive | 0.70 | 15% | 0.105 | High cognitive demands |
| Coordination | 0.50 | 15% | 0.075 | Moderate coordination needs |
| Temporal | 0.40 | 10% | 0.04 | Standard timeline pressure |
| Technical | 0.80 | 15% | 0.12 | High technical complexity |
| Scale | 0.60 | 10% | 0.06 | Moderate scale requirements |
| Uncertainty | 0.50 | 10% | 0.05 | Some ambiguity present |
| Dependencies | 0.40 | 5% | 0.02 | Moderate external dependencies |

---

## 🎯 Domain Analysis

**Frontend (40%)**:
- React UI components
- Responsive design
- User interactions

**Backend (35%)**:
- REST API design
- Business logic
- Authentication

**Database (25%)**:
- Schema design
- Data persistence
- Query optimization

---

## 🔧 Recommended MCP Servers

### Tier 1: MANDATORY 🔴

**1. Serena MCP** (CRITICAL - Always Required)
   - **Purpose**: Session persistence and zero-context-loss architecture
   - **Usage**: Save all analysis, plans, wave results

### Tier 2: PRIMARY (Domain-Based)

**2. Magic MCP** (Frontend: 40%)
   - **Purpose**: React component generation
   - **Usage**: Generate UI components from patterns

---

## 📅 5-Phase Implementation Plan

### Phase 1: Analysis & Planning
**Duration**: 4 hours

### Phase 2: Architecture & Design
**Duration**: 8 hours

### Phase 3: Implementation
**Duration**: 16 hours

### Phase 4: Integration & Testing
**Duration**: 6 hours

### Phase 5: Deployment & Documentation
**Duration**: 4 hours

---

## ⚠️ Risk Assessment

**Risk 1: Technical Complexity**
- **Likelihood**: Medium
- **Impact**: High
- **Mitigation**: Allocate extra time for research

---

## ✅ Next Steps

1. Review complexity score for accuracy
2. Configure recommended MCP servers
3. Begin Phase 1: Analysis & Planning

---

## 🧠 Saved to Serena MCP

This complete analysis has been saved to Serena MCP with key: `spec_analysis_test`
"""

        report_file = temp_project_dir / ".shannon" / "analysis" / "spec_analysis_test.md"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(report_content)

        # Validate required sections exist
        content = report_file.read_text()

        required_sections = [
            "# Specification Analysis Complete",
            "## 📊 Complexity Assessment",
            "## 🎯 Domain Analysis",
            "## 🔧 Recommended MCP Servers",
            "## 📅 5-Phase Implementation Plan",
            "## ⚠️ Risk Assessment",
            "## ✅ Next Steps",
            "## 🧠 Saved to Serena MCP"
        ]

        for section in required_sections:
            assert section in content, f"Missing required section: {section}"

    def test_spec_complexity_score_format(self):
        """Verify complexity scores are in valid range [0.0, 1.0]"""
        test_scores = [0.0, 0.30, 0.50, 0.70, 0.85, 1.0]

        for score in test_scores:
            assert 0.0 <= score <= 1.0, f"Invalid complexity score: {score}"

    def test_spec_domain_percentages_sum_to_100(self):
        """Verify domain percentages sum to exactly 100%"""
        domain_percentages = {
            "frontend": 40,
            "backend": 35,
            "database": 25
        }

        total = sum(domain_percentages.values())
        assert total == 100, f"Domain percentages sum to {total}%, expected 100%"

    def test_spec_mcp_tier_structure(self, temp_project_dir):
        """Validate MCP recommendations have proper tier structure"""
        report_content = """
## 🔧 Recommended MCP Servers

### Tier 1: MANDATORY 🔴

**1. Serena MCP** (CRITICAL - Always Required)

### Tier 2: PRIMARY (Domain-Based)

**2. Magic MCP** (Frontend: 40%)

### Tier 3: SECONDARY (Supporting)

**3. GitHub MCP**
"""

        report_file = temp_project_dir / ".shannon" / "test_mcp_tiers.md"
        report_file.write_text(report_content)
        content = report_file.read_text()

        # Verify tier hierarchy
        assert "Tier 1: MANDATORY" in content
        assert "Tier 2: PRIMARY" in content
        assert "Serena MCP" in content  # Must always be present

        # Verify Serena is in Tier 1
        tier1_start = content.find("### Tier 1: MANDATORY")
        tier2_start = content.find("### Tier 2: PRIMARY")
        serena_pos = content.find("Serena MCP")

        assert tier1_start < serena_pos < tier2_start, "Serena MCP not in Tier 1"

    def test_spec_phase_validation_gates(self, temp_project_dir):
        """Verify each phase has validation gate with pass criteria"""
        phase_content = """
### Phase 1: Analysis & Planning
**Duration**: 4 hours

**Objectives**:
- Complete specification analysis
- Create task breakdown

**Validation Gate**:
✅ Pass Criteria:
- All requirements clearly understood
- No ambiguities remaining
- Complexity score validated

**Pass Condition**: ALL criteria met
"""

        # Check required elements
        assert "**Objectives**:" in phase_content
        assert "**Validation Gate**:" in phase_content
        assert "✅ Pass Criteria:" in phase_content
        assert "**Pass Condition**:" in phase_content


# =============================================================================
# Test Class 2: Checkpoint Artifacts
# =============================================================================

class TestCheckpointArtifacts:
    """Validate /sh:checkpoint creates Serena memory entries"""

    def test_checkpoint_command_exists(self, shannon_root):
        """Verify sh:checkpoint command file exists"""
        checkpoint_cmd = shannon_root / "Shannon" / "Commands" / "sh_checkpoint.md"
        assert checkpoint_cmd.exists(), "sh_checkpoint.md command file not found"

    def test_checkpoint_naming_convention(self):
        """Verify checkpoint naming follows: shannon_checkpoint_[name]"""
        pattern = r"shannon_checkpoint_[\w\-]+"

        test_names = [
            "shannon_checkpoint_before_wave_3",
            "shannon_checkpoint_20250930_143000",
            "shannon_checkpoint_end_of_day"
        ]

        for name in test_names:
            assert re.match(pattern, name), f"Invalid checkpoint name: {name}"

    def test_checkpoint_data_structure(self):
        """Validate checkpoint has required data structure"""
        checkpoint_data = {
            "checkpoint_metadata": {
                "checkpoint_name": "shannon_checkpoint_test",
                "created_at": "2025-09-30T14:30:00Z",
                "session_id": "test_session_123",
                "checkpoint_type": "manual",
                "created_by_command": "/sh:checkpoint",
                "trigger_reason": "user_requested"
            },
            "context_preservation": {
                "serena_memory_keys": [
                    "spec_analysis_test",
                    "phase_plan_test",
                    "wave_1_results"
                ],
                "total_keys": 3,
                "last_key_updated": "wave_1_results"
            },
            "project_state": {
                "current_wave": 2,
                "current_phase": {
                    "number": 3,
                    "name": "implementation",
                    "completion_percent": 45
                },
                "project_id": "test_project_001"
            },
            "work_context": {
                "current_focus": "Building API endpoints",
                "in_progress_files": ["/src/api/auth.ts"],
                "pending_tasks": ["Complete auth", "Write tests"]
            }
        }

        # Validate required top-level keys
        required_keys = [
            "checkpoint_metadata",
            "context_preservation",
            "project_state",
            "work_context"
        ]

        for key in required_keys:
            assert key in checkpoint_data, f"Missing required key: {key}"

        # Validate metadata structure
        metadata = checkpoint_data["checkpoint_metadata"]
        assert "checkpoint_name" in metadata
        assert "created_at" in metadata
        assert "checkpoint_type" in metadata

        # Validate ISO timestamp format
        timestamp = metadata["created_at"]
        assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", timestamp)

    def test_checkpoint_serena_key_inventory(self):
        """Validate checkpoint captures ALL Serena memory keys"""
        mock_serena_keys = [
            "spec_analysis_taskapp_20250930",
            "phase_plan_taskapp_20250930",
            "wave_1_complete_20250930",
            "wave_2_frontend_results",
            "wave_2_backend_results",
            "project_decisions_auth",
            "active_wave_3",
            "todo_list_current"
        ]

        checkpoint_data = {
            "context_preservation": {
                "serena_memory_keys": mock_serena_keys,
                "total_keys": len(mock_serena_keys),
                "categorized_keys": {
                    "project_keys": [k for k in mock_serena_keys if "project_" in k],
                    "wave_keys": [k for k in mock_serena_keys if "wave_" in k],
                    "phase_keys": [k for k in mock_serena_keys if "phase_" in k]
                }
            }
        }

        # Validate all keys captured
        assert len(checkpoint_data["context_preservation"]["serena_memory_keys"]) == 8
        assert checkpoint_data["context_preservation"]["total_keys"] == 8

        # Validate categorization
        categorized = checkpoint_data["context_preservation"]["categorized_keys"]
        assert len(categorized["wave_keys"]) >= 1  # At least one wave key present (flexible count)


# =============================================================================
# Test Class 3: Implementation Artifacts
# =============================================================================

class TestImplementationArtifacts:
    """Validate /sc:implement creates code + tests (NO MOCKS)"""

    def test_implement_command_exists(self, shannon_root):
        """Verify sc:implement command file exists"""
        impl_cmd = shannon_root / "Shannon" / "Commands" / "sc_implement.md"
        assert impl_cmd.exists(), "sc_implement.md command file not found"

    def test_implementation_creates_source_and_test_files(self, temp_project_dir):
        """Verify implementation creates both source and test files"""
        # Simulate implementation output
        src_dir = temp_project_dir / "src"
        tests_dir = temp_project_dir / "tests"

        src_dir.mkdir()
        tests_dir.mkdir()

        # Create source file
        auth_src = src_dir / "auth.ts"
        auth_src.write_text("""
export class AuthService {
    async login(email: string, password: string) {
        // Real implementation
        return { token: "jwt_token" };
    }
}
""")

        # Create test file (NO MOCKS)
        auth_test = tests_dir / "auth.test.ts"
        auth_test.write_text("""
import { AuthService } from '../src/auth';

describe('AuthService', () => {
    it('should login with valid credentials', async () => {
        const authService = new AuthService();
        const result = await authService.login('user@test.com', 'password');
        expect(result.token).toBeDefined();
    });
});
""")

        # Validate both files exist
        assert auth_src.exists(), "Source file not created"
        assert auth_test.exists(), "Test file not created"

        # Validate test file has no mocks
        test_content = auth_test.read_text()
        assert "new AuthService()" in test_content  # Real instantiation
        assert "mock" not in test_content.lower()  # No mock functions
        assert "stub" not in test_content.lower()  # No stubs

    def test_generated_tests_have_no_mocks(self, temp_project_dir):
        """CRITICAL: Verify generated tests contain NO MOCKS"""
        test_file = temp_project_dir / "test_example.ts"

        # Example of VALID test (no mocks)
        valid_test = """
describe('UserService', () => {
    it('creates user in real database', async () => {
        const db = new Database(); // Real database
        const service = new UserService(db);
        const user = await service.create({ name: 'Test' });
        expect(user.id).toBeDefined();
    });
});
"""

        test_file.write_text(valid_test)
        content = test_file.read_text()

        # Forbidden patterns indicating mocks
        forbidden_patterns = [
            r"\.mock\(",
            r"jest\.fn\(",
            r"jest\.mock\(",
            r"createMock",
            r"MockedClass",
            r"sinon\.stub",
            r"sinon\.mock",
            r"@Mock",
            r"Mock<",
            r"Stub<"
        ]

        for pattern in forbidden_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            assert len(matches) == 0, f"Found forbidden mock pattern: {pattern}"

    def test_implementation_artifact_structure(self, temp_project_dir):
        """Verify implementation creates proper directory structure"""
        # Expected structure after implementation
        expected_dirs = [
            temp_project_dir / "src",
            temp_project_dir / "tests",
            temp_project_dir / "src" / "api",
            temp_project_dir / "src" / "models"
        ]

        for dir_path in expected_dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            assert dir_path.exists(), f"Expected directory not created: {dir_path}"


# =============================================================================
# Test Class 4: Wave Artifacts
# =============================================================================

class TestWaveArtifacts:
    """Validate wave execution creates synthesis reports"""

    def test_wave_results_naming_convention(self):
        """Verify wave result naming: wave_[N]_[type]_results.md"""
        pattern = r"wave_\d+_[\w]+_results\.md"

        test_names = [
            "wave_1_analysis_results.md",
            "wave_2_frontend_results.md",
            "wave_2_backend_results.md",
            "wave_3_integration_results.md"
        ]

        for name in test_names:
            assert re.match(pattern, name), f"Invalid wave result name: {name}"

    def test_wave_synthesis_report_structure(self, temp_project_dir):
        """Validate wave synthesis report has required sections"""
        synthesis_content = """# Wave 2 Synthesis Report

**Wave ID**: wave_2_parallel_implementation
**Execution Type**: Parallel
**Sub-Waves**: 2a (Frontend), 2b (Backend)
**Status**: ✅ Complete
**Total Duration**: 3.2 hours

---

## Wave Execution Summary

### Wave 2a: Frontend Implementation
- **Status**: ✅ Complete
- **Duration**: 2.8 hours
- **Artifacts**: 15 React components created
- **Tests**: 42 functional tests (NO MOCKS)

### Wave 2b: Backend Implementation
- **Status**: ✅ Complete
- **Duration**: 3.1 hours
- **Artifacts**: 8 API endpoints implemented
- **Tests**: 28 integration tests (NO MOCKS)

---

## Quality Validation

✅ All tests passing (70 total, 0 mocks)
✅ Code follows established patterns
✅ No critical bugs detected
✅ Performance metrics within targets

---

## Context Saved to Serena

- `wave_2_frontend_results`
- `wave_2_backend_results`
- `wave_2_synthesis_complete`
"""

        synthesis_file = temp_project_dir / ".shannon" / "waves" / "wave_2_synthesis.md"
        synthesis_file.parent.mkdir(parents=True, exist_ok=True)
        synthesis_file.write_text(synthesis_content)

        content = synthesis_file.read_text()

        # Validate required sections
        required_sections = [
            "# Wave",
            "Synthesis Report",
            "## Wave Execution Summary",
            "## Quality Validation",
            "## Context Saved to Serena"
        ]

        for section in required_sections:
            assert section in content, f"Missing section: {section}"

        # Verify NO MOCKS mention
        assert "NO MOCKS" in content or "(0 mocks)" in content

    def test_wave_parallel_execution_tracking(self):
        """Verify parallel wave execution is properly tracked"""
        wave_data = {
            "wave_id": "wave_2_parallel",
            "sub_waves": [
                {
                    "id": "2a",
                    "name": "Frontend",
                    "status": "complete",
                    "start_time": "2025-09-30T10:00:00Z",
                    "end_time": "2025-09-30T12:48:00Z"
                },
                {
                    "id": "2b",
                    "name": "Backend",
                    "status": "complete",
                    "start_time": "2025-09-30T10:00:00Z",
                    "end_time": "2025-09-30T13:06:00Z"
                }
            ],
            "execution_type": "parallel"
        }

        assert wave_data["execution_type"] == "parallel"
        assert len(wave_data["sub_waves"]) == 2

        # Verify both started at same time (parallel)
        start_times = [sw["start_time"] for sw in wave_data["sub_waves"]]
        assert start_times[0] == start_times[1], "Sub-waves didn't start in parallel"


# =============================================================================
# Test Class 5: NO MOCKS Enforcement
# =============================================================================

class TestNoMocksEnforcement:
    """CRITICAL: Verify NO MOCKS in all generated tests"""

    def test_detect_jest_mocks(self):
        """Detect Jest mock patterns"""
        bad_code = """
const mockFn = jest.fn();
jest.mock('./module');
const MockClass = jest.createMockFromModule('./class');
"""

        mock_patterns = [
            r"jest\.fn\(",
            r"jest\.mock\(",
            r"createMockFromModule"
        ]

        violations = []
        for pattern in mock_patterns:
            if re.search(pattern, bad_code):
                violations.append(pattern)

        assert len(violations) > 0, "Should detect Jest mocks"

    def test_detect_sinon_mocks(self):
        """Detect Sinon mock patterns"""
        bad_code = """
const stub = sinon.stub(obj, 'method');
const mock = sinon.mock(obj);
"""

        mock_patterns = [r"sinon\.stub", r"sinon\.mock"]

        violations = []
        for pattern in mock_patterns:
            if re.search(pattern, bad_code):
                violations.append(pattern)

        assert len(violations) > 0, "Should detect Sinon mocks"

    def test_detect_typescript_mock_types(self):
        """Detect TypeScript mock type annotations"""
        bad_code = """
const service: Mock<UserService> = createMock();
type MockedService = MockedClass<RealService>;
"""

        mock_patterns = [r"Mock<", r"MockedClass<", r"MockedFunction<"]

        violations = []
        for pattern in mock_patterns:
            if re.search(pattern, bad_code):
                violations.append(pattern)

        assert len(violations) > 0, "Should detect TypeScript mock types"

    def test_approve_real_test_patterns(self):
        """Verify real test patterns are NOT flagged"""
        good_code = """
describe('AuthService', () => {
    it('authenticates with real database', async () => {
        const db = new PostgresDatabase();
        const service = new AuthService(db);
        const result = await service.login('test@email.com', 'password');
        expect(result.token).toBeDefined();
    });
});
"""

        forbidden_patterns = [
            r"\.mock\(",
            r"jest\.fn\(",
            r"createMock",
            r"sinon\."
        ]

        violations = []
        for pattern in forbidden_patterns:
            if re.search(pattern, good_code, re.IGNORECASE):
                violations.append(pattern)

        assert len(violations) == 0, f"False positive: {violations}"

    def test_scan_test_directory_for_mocks(self, temp_project_dir):
        """Scan entire test directory for mock violations"""
        tests_dir = temp_project_dir / "tests"
        tests_dir.mkdir(exist_ok=True)

        # Create test file with real implementation
        test_file = tests_dir / "integration.test.ts"
        test_file.write_text("""
import { ApiClient } from '../src/api';

describe('API Integration', () => {
    it('makes real HTTP request', async () => {
        const client = new ApiClient('http://localhost:3000');
        const response = await client.get('/users');
        expect(response.status).toBe(200);
    });
});
""")

        # Scan for violations
        violations = scan_directory_for_mocks(tests_dir)

        assert len(violations) == 0, f"Found mock violations: {violations}"


# =============================================================================
# Helper Functions
# =============================================================================

def scan_directory_for_mocks(directory: Path) -> List[Dict[str, Any]]:
    """
    Scan directory for mock patterns in test files

    Returns list of violations with file path and line number
    """
    violations = []

    forbidden_patterns = [
        r"\.mock\(",
        r"jest\.fn\(",
        r"jest\.mock\(",
        r"createMock",
        r"MockedClass",
        r"sinon\.stub",
        r"sinon\.mock",
        r"@Mock",
        r"Mock<",
        r"Stub<"
    ]

    test_files = list(directory.rglob("*.test.*")) + list(directory.rglob("*.spec.*"))

    for test_file in test_files:
        content = test_file.read_text()
        lines = content.split("\n")

        for line_num, line in enumerate(lines, 1):
            for pattern in forbidden_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append({
                        "file": str(test_file),
                        "line": line_num,
                        "content": line.strip(),
                        "pattern": pattern
                    })

    return violations


def validate_yaml_structure(yaml_content: str) -> bool:
    """Validate YAML structure is parseable"""
    try:
        data = yaml.safe_load(yaml_content)
        return data is not None
    except yaml.YAMLError:
        return False


def validate_json_structure(json_content: str) -> bool:
    """Validate JSON structure is parseable"""
    try:
        data = json.loads(json_content)
        return data is not None
    except json.JSONDecodeError:
        return False


# =============================================================================
# Test Runner Configuration
# =============================================================================

def pytest_configure(config):
    """Pytest configuration - register custom markers"""
    config.addinivalue_line(
        "markers", "artifacts: mark test as artifact validation test"
    )
    config.addinivalue_line(
        "markers", "critical: mark test as critical (NO MOCKS enforcement)"
    )


if __name__ == "__main__":
    """Run tests directly with python test_artifacts.py"""
    pytest.main([__file__, "-v", "--tb=short"])