"""
Artifact Validator for Shannon Framework
Validates command outputs and artifacts against specifications.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import yaml
import json
import re


@dataclass
class ValidationResult:
    """Result of artifact validation"""
    artifact_path: Path
    artifact_type: str
    passed: bool
    checks_passed: List[str]
    checks_failed: List[str]
    warnings: List[str]
    score: float  # 0.0-1.0
    validation_time: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        status = "✅ PASSED" if self.passed else "❌ FAILED"
        return f"{status} {self.artifact_type} (Score: {self.score:.2f})"

    def detailed_report(self) -> str:
        """Generate detailed validation report"""
        lines = [
            f"\n{'='*70}",
            f"Validation Report: {self.artifact_type}",
            f"Artifact: {self.artifact_path}",
            f"Score: {self.score:.2%}",
            f"Status: {'PASSED' if self.passed else 'FAILED'}",
            f"Time: {self.validation_time}",
            f"{'='*70}\n"
        ]

        if self.checks_passed:
            lines.append("✅ PASSED CHECKS:")
            for check in self.checks_passed:
                lines.append(f"  ✓ {check}")
            lines.append("")

        if self.checks_failed:
            lines.append("❌ FAILED CHECKS:")
            for check in self.checks_failed:
                lines.append(f"  ✗ {check}")
            lines.append("")

        if self.warnings:
            lines.append("⚠️  WARNINGS:")
            for warning in self.warnings:
                lines.append(f"  ⚠ {warning}")
            lines.append("")

        return "\n".join(lines)


class SpecAnalysisValidator:
    """Validates /sh:spec command outputs"""

    REQUIRED_SECTIONS = [
        "8-Dimensional Complexity Analysis",
        "Domain Analysis",
        "MCP Server Recommendations",
        "5-Phase Implementation Plan",
        "Timeline Estimation",
        "Risk Assessment",
        "Todo List Generation",
        "Executive Summary"
    ]

    REQUIRED_SUBSECTIONS = {
        "8-Dimensional Complexity Analysis": [
            "Structural Complexity",
            "Cognitive Load",
            "Dependency Depth",
            "Domain Breadth",
            "State Management",
            "Concurrency Requirements",
            "Integration Surface",
            "Change Volatility"
        ],
        "MCP Server Recommendations": [
            "Tier 1",
            "Tier 2",
            "Integration Strategy"
        ]
    }

    def validate(self, spec_file: Path) -> ValidationResult:
        """Validate spec analysis artifact"""
        checks_passed = []
        checks_failed = []
        warnings = []

        if not spec_file.exists():
            return ValidationResult(
                artifact_path=spec_file,
                artifact_type="SpecAnalysis",
                passed=False,
                checks_passed=[],
                checks_failed=["Artifact file does not exist"],
                warnings=[],
                score=0.0
            )

        content = spec_file.read_text()

        # Check 1: All required sections present
        for section in self.REQUIRED_SECTIONS:
            if section in content:
                checks_passed.append(f"Section '{section}' present")
            else:
                checks_failed.append(f"Missing required section: {section}")

        # Check 2: Required subsections
        for section, subsections in self.REQUIRED_SUBSECTIONS.items():
            if section in content:
                section_start = content.find(section)
                # Find next major section or end of file
                next_section_idx = len(content)
                for other_section in self.REQUIRED_SECTIONS:
                    if other_section != section:
                        idx = content.find(other_section, section_start + 1)
                        if idx != -1 and idx < next_section_idx:
                            next_section_idx = idx

                section_content = content[section_start:next_section_idx]
                for subsection in subsections:
                    if subsection in section_content:
                        checks_passed.append(f"Subsection '{subsection}' present in {section}")
                    else:
                        checks_failed.append(f"Missing subsection '{subsection}' in {section}")

        # Check 3: Complexity score format and range
        complexity_match = re.search(r'(?:Overall\s+)?Complexity Score:\s*([0-9.]+)', content, re.IGNORECASE)
        if complexity_match:
            score = float(complexity_match.group(1))
            if 0.0 <= score <= 1.0:
                checks_passed.append(f"Valid complexity score: {score}")
            else:
                checks_failed.append(f"Complexity score out of range [0.0-1.0]: {score}")
        else:
            checks_failed.append("No complexity score found")

        # Check 4: Domain percentages
        domain_pattern = r'-\s+([A-Za-z/]+):\s+([0-9]+)%'
        domains = re.findall(domain_pattern, content)
        if domains:
            total = sum(int(pct) for _, pct in domains)
            if 95 <= total <= 105:  # Allow small rounding errors
                checks_passed.append(f"Domain percentages sum to {total}% (acceptable)")
            else:
                checks_failed.append(f"Domain percentages sum to {total}%, not ~100%")
        else:
            warnings.append("No domain percentages found")

        # Check 5: Serena in Tier 1 (required for Shannon)
        tier1_pattern = r'(?:Tier 1|Primary)[:\s]*(?:.*?Serena|Serena.*?)(?=\n\n|Tier 2|$)'
        if re.search(tier1_pattern, content, re.IGNORECASE | re.DOTALL):
            checks_passed.append("Serena MCP in Tier 1/Primary")
        else:
            warnings.append("Serena MCP not clearly identified in Tier 1/Primary")

        # Check 6: 5-Phase plan structure
        phase_pattern = r'Phase\s+(\d+):\s+([^\n]+)'
        phases = re.findall(phase_pattern, content)
        if len(phases) >= 5:
            checks_passed.append(f"Found {len(phases)} implementation phases")
            # Verify sequential numbering
            phase_numbers = [int(num) for num, _ in phases]
            if phase_numbers == sorted(phase_numbers):
                checks_passed.append("Phases are sequentially numbered")
            else:
                warnings.append("Phase numbering may not be sequential")
        else:
            checks_failed.append(f"Only found {len(phases)} phases, expected at least 5")

        # Check 7: Timeline estimation present
        timeline_pattern = r'(?:Total\s+)?(?:Estimated\s+)?(?:Time|Duration):\s*([0-9.]+)\s*(hours?|days?|weeks?)'
        if re.search(timeline_pattern, content, re.IGNORECASE):
            checks_passed.append("Timeline estimation present")
        else:
            checks_failed.append("No timeline estimation found")

        # Check 8: Risk assessment
        risk_keywords = ['risk', 'challenge', 'concern', 'mitigation']
        risk_section_idx = content.lower().find('risk assessment')
        if risk_section_idx != -1:
            risk_section = content[risk_section_idx:risk_section_idx+1000]
            found_keywords = [kw for kw in risk_keywords if kw in risk_section.lower()]
            if len(found_keywords) >= 2:
                checks_passed.append(f"Risk assessment contains relevant keywords: {found_keywords}")
            else:
                warnings.append("Risk assessment section may be incomplete")

        # Check 9: Todo list generation
        todo_pattern = r'(?:^|\n)(?:\d+\.|-|\*)\s+\[[ x]\]\s+'
        todos = re.findall(todo_pattern, content)
        if len(todos) >= 5:
            checks_passed.append(f"Found {len(todos)} todo items")
        else:
            warnings.append(f"Only found {len(todos)} todo items, may need more")

        # Calculate score
        total_checks = len(checks_passed) + len(checks_failed)
        score = len(checks_passed) / total_checks if total_checks > 0 else 0.0

        return ValidationResult(
            artifact_path=spec_file,
            artifact_type="SpecAnalysis",
            passed=len(checks_failed) == 0,
            checks_passed=checks_passed,
            checks_failed=checks_failed,
            warnings=warnings,
            score=score
        )


class CheckpointValidator:
    """Validates checkpoint structure"""

    REQUIRED_FIELDS = [
        "timestamp",
        "trigger",
        "serena_memory_keys",
        "wave_state",
        "phase_state",
        "todo_state"
    ]

    REQUIRED_WAVE_STATE_FIELDS = [
        "current_wave",
        "total_waves",
        "wave_status"
    ]

    REQUIRED_PHASE_STATE_FIELDS = [
        "current_phase",
        "phase_name",
        "phase_status"
    ]

    def validate(self, checkpoint_file: Path) -> ValidationResult:
        """Validate checkpoint data structure"""
        checks_passed = []
        checks_failed = []
        warnings = []

        if not checkpoint_file.exists():
            return ValidationResult(
                artifact_path=checkpoint_file,
                artifact_type="Checkpoint",
                passed=False,
                checks_passed=[],
                checks_failed=["Checkpoint file does not exist"],
                warnings=[],
                score=0.0
            )

        try:
            # Try JSON first, then YAML
            try:
                with open(checkpoint_file) as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                with open(checkpoint_file) as f:
                    data = yaml.safe_load(f)
        except Exception as e:
            return ValidationResult(
                artifact_path=checkpoint_file,
                artifact_type="Checkpoint",
                passed=False,
                checks_passed=[],
                checks_failed=[f"Failed to parse checkpoint file: {e}"],
                warnings=[],
                score=0.0
            )

        # Check 1: Top-level required fields
        for field in self.REQUIRED_FIELDS:
            if field in data:
                checks_passed.append(f"Required field '{field}' present")
            else:
                checks_failed.append(f"Missing required field: {field}")

        # Check 2: Timestamp format
        if "timestamp" in data:
            try:
                timestamp = data["timestamp"]
                # Try parsing as ISO format
                datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                checks_passed.append("Timestamp is valid ISO format")
            except (ValueError, AttributeError):
                checks_failed.append("Timestamp is not valid ISO format")

        # Check 3: Wave state structure
        if "wave_state" in data:
            wave_state = data["wave_state"]
            for field in self.REQUIRED_WAVE_STATE_FIELDS:
                if field in wave_state:
                    checks_passed.append(f"Wave state field '{field}' present")
                else:
                    checks_failed.append(f"Missing wave state field: {field}")

            # Validate wave numbers
            if "current_wave" in wave_state and "total_waves" in wave_state:
                current = wave_state["current_wave"]
                total = wave_state["total_waves"]
                if isinstance(current, int) and isinstance(total, int):
                    if 0 <= current <= total:
                        checks_passed.append(f"Wave numbers valid: {current}/{total}")
                    else:
                        checks_failed.append(f"Invalid wave numbers: {current}/{total}")

        # Check 4: Phase state structure
        if "phase_state" in data:
            phase_state = data["phase_state"]
            for field in self.REQUIRED_PHASE_STATE_FIELDS:
                if field in phase_state:
                    checks_passed.append(f"Phase state field '{field}' present")
                else:
                    checks_failed.append(f"Missing phase state field: {field}")

            # Validate phase number
            if "current_phase" in phase_state:
                phase = phase_state["current_phase"]
                if isinstance(phase, int) and 1 <= phase <= 5:
                    checks_passed.append(f"Phase number valid: {phase}")
                else:
                    warnings.append(f"Phase number outside typical range [1-5]: {phase}")

        # Check 5: Serena memory keys are non-empty
        if "serena_memory_keys" in data:
            keys = data["serena_memory_keys"]
            if isinstance(keys, (list, dict)) and len(keys) > 0:
                checks_passed.append(f"Serena memory keys present ({len(keys)} items)")
            else:
                warnings.append("Serena memory keys are empty")

        # Check 6: Todo state has required structure
        if "todo_state" in data:
            todo_state = data["todo_state"]
            if isinstance(todo_state, list):
                checks_passed.append(f"Todo state is list with {len(todo_state)} items")
                # Check for status fields
                if todo_state:
                    if all("status" in item for item in todo_state if isinstance(item, dict)):
                        checks_passed.append("All todo items have status field")
                    else:
                        warnings.append("Some todo items missing status field")
            elif isinstance(todo_state, dict):
                checks_passed.append("Todo state is dictionary structure")
            else:
                warnings.append("Todo state has unexpected type")

        # Check 7: Trigger type validation
        valid_triggers = ["manual", "time_interval", "phase_completion", "wave_completion", "risk_threshold"]
        if "trigger" in data:
            trigger = data["trigger"]
            if trigger in valid_triggers:
                checks_passed.append(f"Valid trigger type: {trigger}")
            else:
                warnings.append(f"Unusual trigger type: {trigger}")

        # Calculate score
        total_checks = len(checks_passed) + len(checks_failed)
        score = len(checks_passed) / total_checks if total_checks > 0 else 0.0

        return ValidationResult(
            artifact_path=checkpoint_file,
            artifact_type="Checkpoint",
            passed=len(checks_failed) == 0,
            checks_passed=checks_passed,
            checks_failed=checks_failed,
            warnings=warnings,
            score=score
        )


class ImplementationValidator:
    """Validates code generation and implementation artifacts"""

    def validate(self, impl_path: Path, spec: Optional[Dict] = None) -> ValidationResult:
        """Validate implementation artifact"""
        checks_passed = []
        checks_failed = []
        warnings = []

        if not impl_path.exists():
            return ValidationResult(
                artifact_path=impl_path,
                artifact_type="Implementation",
                passed=False,
                checks_passed=[],
                checks_failed=["Implementation file does not exist"],
                warnings=[],
                score=0.0
            )

        content = impl_path.read_text()

        # Check 1: File is non-empty
        if len(content.strip()) > 0:
            checks_passed.append(f"File is non-empty ({len(content)} chars)")
        else:
            checks_failed.append("File is empty")
            return ValidationResult(
                artifact_path=impl_path,
                artifact_type="Implementation",
                passed=False,
                checks_passed=checks_passed,
                checks_failed=checks_failed,
                warnings=warnings,
                score=0.0
            )

        # Check 2: Python syntax (basic)
        if impl_path.suffix == ".py":
            # Check for common Python structures
            python_indicators = [
                (r'^def\s+\w+\s*\(', "Function definitions"),
                (r'^class\s+\w+', "Class definitions"),
                (r'^import\s+\w+|^from\s+\w+\s+import', "Import statements"),
            ]

            for pattern, desc in python_indicators:
                if re.search(pattern, content, re.MULTILINE):
                    checks_passed.append(f"{desc} found")

            # Check for NO MOCK indicators
            mock_patterns = [
                r'raise\s+NotImplementedError',
                r'pass\s*(?:#.*)?$',
                r'TODO',
                r'FIXME',
                r'placeholder'
            ]

            mock_found = False
            for pattern in mock_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
                if matches:
                    warnings.append(f"Potential mock/placeholder code: {pattern} ({len(matches)} instances)")
                    mock_found = True

            if not mock_found:
                checks_passed.append("No obvious mock or placeholder code")

        # Check 3: Docstrings present (for Python)
        if impl_path.suffix == ".py":
            docstring_pattern = r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\''
            docstrings = re.findall(docstring_pattern, content)
            if len(docstrings) >= 1:
                checks_passed.append(f"Docstrings present ({len(docstrings)} found)")
            else:
                warnings.append("No docstrings found")

        # Check 4: Type hints (for Python)
        if impl_path.suffix == ".py":
            type_hint_pattern = r':\s*(?:str|int|float|bool|List|Dict|Optional|Any|Path)\s*[,\)]'
            type_hints = re.findall(type_hint_pattern, content)
            if len(type_hints) >= 3:
                checks_passed.append(f"Type hints present ({len(type_hints)} found)")
            else:
                warnings.append("Limited type hints found")

        # Check 5: Spec compliance (if spec provided)
        if spec:
            # Check for required classes/functions mentioned in spec
            if "required_classes" in spec:
                for cls in spec["required_classes"]:
                    if f"class {cls}" in content:
                        checks_passed.append(f"Required class '{cls}' implemented")
                    else:
                        checks_failed.append(f"Required class '{cls}' missing")

            if "required_functions" in spec:
                for func in spec["required_functions"]:
                    if f"def {func}" in content:
                        checks_passed.append(f"Required function '{func}' implemented")
                    else:
                        checks_failed.append(f"Required function '{func}' missing")

        # Check 6: Error handling present
        error_handling_patterns = [
            r'try:',
            r'except\s+\w+',
            r'raise\s+\w+Error'
        ]
        error_handling_found = any(re.search(p, content) for p in error_handling_patterns)
        if error_handling_found:
            checks_passed.append("Error handling code present")
        else:
            warnings.append("No explicit error handling found")

        # Calculate score
        total_checks = len(checks_passed) + len(checks_failed)
        score = len(checks_passed) / total_checks if total_checks > 0 else 0.0

        return ValidationResult(
            artifact_path=impl_path,
            artifact_type="Implementation",
            passed=len(checks_failed) == 0,
            checks_passed=checks_passed,
            checks_failed=checks_failed,
            warnings=warnings,
            score=score
        )


class WaveValidator:
    """Validates wave synthesis artifacts"""

    REQUIRED_SECTIONS = [
        "Wave Summary",
        "Key Achievements",
        "Integration Points",
        "Quality Metrics",
        "Next Wave Preview"
    ]

    def validate(self, wave_file: Path) -> ValidationResult:
        """Validate wave synthesis artifact"""
        checks_passed = []
        checks_failed = []
        warnings = []

        if not wave_file.exists():
            return ValidationResult(
                artifact_path=wave_file,
                artifact_type="WaveSynthesis",
                passed=False,
                checks_passed=[],
                checks_failed=["Wave file does not exist"],
                warnings=[],
                score=0.0
            )

        content = wave_file.read_text()

        # Check 1: Required sections
        for section in self.REQUIRED_SECTIONS:
            if section in content:
                checks_passed.append(f"Section '{section}' present")
            else:
                checks_failed.append(f"Missing section: {section}")

        # Check 2: Wave number identification
        wave_pattern = r'Wave\s+(\d+)(?:\s+of\s+(\d+))?'
        wave_match = re.search(wave_pattern, content, re.IGNORECASE)
        if wave_match:
            wave_num = wave_match.group(1)
            checks_passed.append(f"Wave number identified: {wave_num}")
        else:
            checks_failed.append("No wave number found")

        # Check 3: Quality metrics present
        metric_patterns = [
            r'(?:Test\s+)?Coverage:\s*([0-9.]+)%',
            r'(?:Code\s+)?Quality:\s*([0-9.]+)',
            r'(?:Performance|Speed):\s*([0-9.]+)'
        ]

        metrics_found = 0
        for pattern in metric_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                metrics_found += 1

        if metrics_found >= 2:
            checks_passed.append(f"Quality metrics present ({metrics_found} found)")
        else:
            warnings.append(f"Limited quality metrics ({metrics_found} found)")

        # Check 4: Integration with Serena mentioned
        serena_keywords = ['serena', 'memory', 'checkpoint', 'session']
        serena_mentions = sum(1 for kw in serena_keywords if kw in content.lower())
        if serena_mentions >= 2:
            checks_passed.append(f"Serena integration mentioned ({serena_mentions} references)")
        else:
            warnings.append("Limited Serena integration documentation")

        # Check 5: Deliverables list
        deliverable_pattern = r'(?:^|\n)(?:\d+\.|-|\*)\s+(?:\[x\]|\[\s\])?\s*\w+'
        deliverables = re.findall(deliverable_pattern, content, re.MULTILINE)
        if len(deliverables) >= 3:
            checks_passed.append(f"Deliverables documented ({len(deliverables)} items)")
        else:
            warnings.append(f"Limited deliverables list ({len(deliverables)} items)")

        # Check 6: Next wave preview
        if "Next Wave" in content or "Wave Preview" in content:
            next_wave_section = content[content.lower().find("next wave"):]
            if len(next_wave_section) > 100:
                checks_passed.append("Substantive next wave preview")
            else:
                warnings.append("Next wave preview may be too brief")

        # Calculate score
        total_checks = len(checks_passed) + len(checks_failed)
        score = len(checks_passed) / total_checks if total_checks > 0 else 0.0

        return ValidationResult(
            artifact_path=wave_file,
            artifact_type="WaveSynthesis",
            passed=len(checks_failed) == 0,
            checks_passed=checks_passed,
            checks_failed=checks_failed,
            warnings=warnings,
            score=score
        )


class ArtifactValidator:
    """Main validation orchestrator"""

    def __init__(self):
        self.spec_validator = SpecAnalysisValidator()
        self.checkpoint_validator = CheckpointValidator()
        self.implementation_validator = ImplementationValidator()
        self.wave_validator = WaveValidator()

    def validate_artifact(
        self,
        artifact_path: Path,
        artifact_type: Optional[str] = None,
        spec: Optional[Dict] = None
    ) -> ValidationResult:
        """
        Validate artifact with auto-detection of type

        Args:
            artifact_path: Path to artifact file
            artifact_type: Optional explicit type, otherwise auto-detect
            spec: Optional specification for validation

        Returns:
            ValidationResult with detailed checks
        """
        if artifact_type is None:
            artifact_type = self._detect_artifact_type(artifact_path)

        if artifact_type == "spec":
            return self.spec_validator.validate(artifact_path)
        elif artifact_type == "checkpoint":
            return self.checkpoint_validator.validate(artifact_path)
        elif artifact_type == "implementation":
            return self.implementation_validator.validate(artifact_path, spec)
        elif artifact_type == "wave":
            return self.wave_validator.validate(artifact_path)
        else:
            return ValidationResult(
                artifact_path=artifact_path,
                artifact_type="Unknown",
                passed=False,
                checks_passed=[],
                checks_failed=[f"Unknown artifact type: {artifact_type}"],
                warnings=[],
                score=0.0
            )

    def _detect_artifact_type(self, artifact_path: Path) -> str:
        """Auto-detect artifact type from filename and content"""
        name = artifact_path.name.lower()

        if "spec" in name or "analysis" in name:
            return "spec"
        elif "checkpoint" in name:
            return "checkpoint"
        elif "wave" in name or "synthesis" in name:
            return "wave"
        elif artifact_path.suffix in [".py", ".js", ".ts", ".java"]:
            return "implementation"

        # Try content-based detection
        if artifact_path.exists():
            content = artifact_path.read_text()
            if "8-Dimensional Complexity Analysis" in content:
                return "spec"
            elif "wave_state" in content or "phase_state" in content:
                return "checkpoint"
            elif "Wave Summary" in content:
                return "wave"

        return "unknown"

    def validate_command_output(
        self,
        command: str,
        output_dir: Path,
        expected_artifacts: List[str]
    ) -> Dict[str, ValidationResult]:
        """
        Validate all artifacts from a command execution

        Args:
            command: Shannon command that was run
            output_dir: Directory containing command outputs
            expected_artifacts: List of expected artifact filenames

        Returns:
            Dictionary mapping artifact names to validation results
        """
        results = {}

        for artifact_name in expected_artifacts:
            artifact_path = output_dir / artifact_name
            result = self.validate_artifact(artifact_path)
            results[artifact_name] = result

        return results

    def generate_summary_report(self, results: Dict[str, ValidationResult]) -> str:
        """Generate summary report for multiple validations"""
        lines = [
            "\n" + "="*70,
            "VALIDATION SUMMARY REPORT",
            "="*70,
            f"Total Artifacts: {len(results)}",
            f"Passed: {sum(1 for r in results.values() if r.passed)}",
            f"Failed: {sum(1 for r in results.values() if not r.passed)}",
            f"Average Score: {sum(r.score for r in results.values()) / len(results):.2%}",
            "="*70,
            ""
        ]

        for name, result in results.items():
            status = "✅" if result.passed else "❌"
            lines.append(f"{status} {name}: {result.score:.2%}")

        lines.append("")
        return "\n".join(lines)
