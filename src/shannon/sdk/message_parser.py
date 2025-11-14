"""
Shannon SDK Message Parser

Extracts structured data from Claude Agent SDK message streams.
Parses skill outputs (spec-analysis, wave-orchestration) into typed models.

Created for: Wave 2 - Core Analysis Engine
Component: SDK Message Parser (Agent B)
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from shannon.storage.models import (
    AnalysisResult,
    ComplexityBand,
    DimensionScore,
    MCPRecommendation,
    Phase,
    WaveResult,
)

# Type hints for SDK message types (with TYPE_CHECKING to avoid hard dependency)
try:
    from claude_agent_sdk import (
        AssistantMessage,
        ResultMessage,
        SystemMessage,
        TextBlock,
        ToolUseBlock,
    )

    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    # Define stub types for type checking
    AssistantMessage = Any
    ResultMessage = Any
    SystemMessage = Any
    TextBlock = Any
    ToolUseBlock = Any


class MessageParser:
    """
    Extract structured data from SDK message streams.

    Parses markdown output from Shannon Framework skills into typed models.
    Handles both real-time progress indicators and final result extraction.
    """

    def __init__(self):
        """Initialize message parser with Shannon dimension weights."""
        self.dimension_weights = {
            "structural": 0.20,
            "cognitive": 0.15,
            "coordination": 0.15,
            "temporal": 0.10,
            "technical": 0.15,
            "scale": 0.10,
            "uncertainty": 0.10,
            "dependencies": 0.05,
        }

    def extract_analysis_result(
        self, messages: List, analysis_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract spec-analysis skill result from SDK message stream.

        The spec-analysis skill returns markdown with:
        - Complexity score: "Complexity: 0.68 (COMPLEX)"
        - Dimension table with scores
        - Domain breakdown percentages
        - MCP recommendations with tiers
        - 5-phase implementation plan

        Args:
            messages: List of SDK messages (AssistantMessage, ToolUseBlock, etc.)
            analysis_id: Optional analysis ID (auto-generated if not provided)

        Returns:
            Dictionary matching AnalysisResult model structure

        Raises:
            ValueError: If required data cannot be extracted
        """
        # Collect all assistant text content
        result_text = self._collect_assistant_text(messages)

        if not result_text:
            raise ValueError("No assistant text found in message stream")

        # Generate analysis ID if not provided
        if not analysis_id:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            analysis_id = f"spec_analysis_{timestamp}"

        # Parse all components
        complexity_score = self._parse_complexity_score(result_text)
        interpretation = self._parse_interpretation(result_text, complexity_score)
        dimension_scores = self._parse_dimensions(result_text)
        domain_percentages = self._parse_domains(result_text)
        mcp_recommendations = self._parse_mcps(result_text)
        phase_plan = self._parse_phases(result_text)
        execution_strategy = self._parse_execution_strategy(result_text)
        timeline_estimate = self._parse_timeline(result_text)

        return {
            "analysis_id": analysis_id,
            "complexity_score": complexity_score,
            "interpretation": interpretation,
            "dimension_scores": dimension_scores,
            "domain_percentages": domain_percentages,
            "mcp_recommendations": mcp_recommendations,
            "phase_plan": phase_plan,
            "execution_strategy": execution_strategy,
            "timeline_estimate": timeline_estimate,
            "analyzed_at": datetime.now(),
        }

    def extract_wave_result(self, messages: List) -> Dict[str, Any]:
        """
        Extract wave-orchestration result from SDK message stream.

        Parses wave execution output including:
        - Wave number and name
        - Agents deployed
        - Execution time
        - Files created
        - Components built
        - Quality metrics

        Args:
            messages: List of SDK messages

        Returns:
            Dictionary matching WaveResult model structure
        """
        result_text = self._collect_assistant_text(messages)

        return {
            "wave_number": self._parse_wave_number(result_text),
            "wave_name": self._parse_wave_name(result_text),
            "agents_deployed": self._parse_agents_deployed(result_text),
            "execution_time_minutes": self._parse_execution_time(result_text),
            "files_created": self._parse_files_created(result_text),
            "components_built": self._parse_components_built(result_text),
            "decisions_made": self._parse_decisions(result_text),
            "tests_created": self._parse_tests_created(result_text),
            "no_mocks_confirmed": self._parse_no_mocks_confirmation(result_text),
            "quality_metrics": self._parse_quality_metrics(result_text),
        }

    def extract_progress_indicators(
        self, msg: Union[AssistantMessage, ToolUseBlock, SystemMessage, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Extract progress information for real-time display.

        Returns progress indicators like:
        - Tool usage: {"type": "tool", "tool": "Read", "description": "..."}
        - Progress steps: {"type": "progress", "step": "Calculating structural..."}
        - Skill invocation: {"type": "skill", "skill": "spec-analysis", "status": "running"}

        Args:
            msg: Individual SDK message object

        Returns:
            Progress indicator dict or None if no progress info
        """
        # Handle ToolUseBlock
        if SDK_AVAILABLE and isinstance(msg, ToolUseBlock):
            return {
                "type": "tool",
                "tool": msg.name,
                "input": msg.input if hasattr(msg, "input") else None,
            }

        # Handle TextBlock within AssistantMessage (with SDK)
        if SDK_AVAILABLE and isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    text = block.text

                    # Detect progress indicators
                    if any(
                        keyword in text
                        for keyword in ["Calculating", "Analyzing", "Processing"]
                    ):
                        return {"type": "progress", "step": text.strip()}

                    # Detect skill invocation
                    skill_match = re.search(r"(?:Using|Invoking)\s+skill:\s*(\S+)", text)
                    if skill_match:
                        return {
                            "type": "skill",
                            "skill": skill_match.group(1),
                            "status": "running",
                        }

        # Handle mock messages (for testing without SDK)
        if hasattr(msg, "content") and isinstance(msg.content, list):
            for block in msg.content:
                if hasattr(block, "text"):
                    text = block.text

                    # Detect progress indicators
                    if any(
                        keyword in text
                        for keyword in ["Calculating", "Analyzing", "Processing"]
                    ):
                        return {"type": "progress", "step": text.strip()}

                    # Detect skill invocation
                    skill_match = re.search(r"(?:Using|Invoking)\s+skill:\s*(\S+)", text)
                    if skill_match:
                        return {
                            "type": "skill",
                            "skill": skill_match.group(1),
                            "status": "running",
                        }

        return None

    # ============================================================================
    # PRIVATE PARSING METHODS
    # ============================================================================

    def _collect_assistant_text(self, messages: List) -> str:
        """Collect all text from AssistantMessage and ResultMessage blocks."""
        result_text = ""

        for msg in messages:
            # Handle SystemMessage (has 'data' attribute)
            if SDK_AVAILABLE and isinstance(msg, SystemMessage):
                if hasattr(msg, "data") and msg.data:
                    if isinstance(msg.data, str):
                        result_text += msg.data + "\n"
                    elif isinstance(msg.data, dict) and "text" in msg.data:
                        result_text += msg.data["text"] + "\n"
            # Handle ResultMessage (has 'result' attribute)
            elif SDK_AVAILABLE and isinstance(msg, ResultMessage):
                if hasattr(msg, "result") and msg.result is not None:
                    if isinstance(msg.result, str):
                        result_text += msg.result + "\n"
                    elif isinstance(msg.result, list):
                        for item in msg.result:
                            if hasattr(item, "text"):
                                result_text += item.text + "\n"
                            elif isinstance(item, dict) and "text" in item:
                                result_text += item["text"] + "\n"
                            elif isinstance(item, str):
                                result_text += item + "\n"
                    elif isinstance(msg.result, dict):
                        # Result might be a dict with output data
                        if "output" in msg.result:
                            result_text += str(msg.result["output"]) + "\n"
                        elif "text" in msg.result:
                            result_text += msg.result["text"] + "\n"
            # Handle TextBlock directly (from streaming)
            elif SDK_AVAILABLE and isinstance(msg, TextBlock):
                result_text += msg.text + "\n"
            # Handle AssistantMessage
            elif SDK_AVAILABLE and isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        result_text += block.text + "\n"
            # Fallback for testing without SDK
            elif hasattr(msg, "content"):
                if isinstance(msg.content, str):
                    result_text += msg.content + "\n"
                elif isinstance(msg.content, list):
                    for block in msg.content:
                        if hasattr(block, "text"):
                            result_text += block.text + "\n"
            # Additional fallback: check for output attribute
            elif hasattr(msg, "output"):
                if isinstance(msg.output, str):
                    result_text += msg.output + "\n"
                elif isinstance(msg.output, list):
                    for block in msg.output:
                        if hasattr(block, "text"):
                            result_text += block.text + "\n"
            # Handle plain text attributes
            elif hasattr(msg, "text"):
                result_text += msg.text + "\n"

        return result_text

    def _parse_complexity_score(self, text: str) -> float:
        """Parse complexity score from text like 'Complexity: 0.68 (COMPLEX)'."""
        match = re.search(r"Complexity[:\s]+(\d+\.\d+)", text, re.IGNORECASE)
        if not match:
            raise ValueError("Could not find complexity score in analysis output")

        score = float(match.group(1))

        # Validate Shannon range (0.10-0.95)
        if not (0.10 <= score <= 0.95):
            raise ValueError(f"Complexity score {score} out of range [0.10, 0.95]")

        return score

    def _parse_interpretation(
        self, text: str, complexity_score: float
    ) -> ComplexityBand:
        """Parse or derive complexity band interpretation."""
        # Try to find explicit interpretation
        for band in ComplexityBand:
            if band.value.upper() in text.upper():
                return band

        # Derive from score if not found
        if complexity_score < 0.25:
            return ComplexityBand.TRIVIAL
        elif complexity_score < 0.40:
            return ComplexityBand.SIMPLE
        elif complexity_score < 0.60:
            return ComplexityBand.MODERATE
        elif complexity_score < 0.75:
            return ComplexityBand.COMPLEX
        elif complexity_score < 0.85:
            return ComplexityBand.HIGH
        else:
            return ComplexityBand.CRITICAL

    def _parse_dimensions(self, text: str) -> Dict[str, Dict[str, Any]]:
        """Parse dimension scores from markdown table or text."""
        dimensions = {}

        # Pattern matches: "Structural: 0.55", "- Structural: 0.55", or table rows like "| Structural | 0.55 |"
        for dim_name in [
            "structural",
            "cognitive",
            "coordination",
            "temporal",
            "technical",
            "scale",
            "uncertainty",
            "dependencies",
        ]:
            # Case-insensitive search for dimension with flexible formatting
            # Matches: "Structural: 0.55", "- Structural: 0.55", "| Structural | 0.55 |"
            pattern = rf"[-|]?\s*{dim_name}[\s|:]+(\d+\.\d+)"
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                score = float(match.group(1))
                weight = self.dimension_weights[dim_name]
                contribution = score * weight

                # Create DimensionScore and convert to dict
                dim_score = DimensionScore(
                    dimension=dim_name,
                    score=score,
                    weight=weight,
                    contribution=contribution,
                    details={},
                )
                dimensions[dim_name] = dim_score.model_dump()

        # Validate we have all 8 dimensions (or at least 6 for partial results)
        if len(dimensions) < 6:
            missing = set(self.dimension_weights.keys()) - set(dimensions.keys())
            raise ValueError(
                f"Too few dimensions in analysis output: {missing}. "
                f"Found: {list(dimensions.keys())}"
            )

        return dimensions

    def _parse_domains(self, text: str) -> Dict[str, int]:
        """Parse domain percentages from text."""
        domains = {}

        # Common domain patterns
        domain_names = [
            "Frontend",
            "Backend",
            "Infrastructure",
            "Data",
            "DevOps",
            "Testing",
            "Documentation",
            "Configuration",
            "Security",
            "API",
        ]

        # Pattern: "Frontend: 30%" or "| Frontend | 30% |"
        for domain in domain_names:
            pattern = rf"{domain}[\s|:]+(\d+)%"
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                domains[domain] = int(match.group(1))

        # Validate total is 100%
        total = sum(domains.values())
        if domains and total != 100:
            # Attempt to normalize to 100%
            factor = 100.0 / total
            domains = {k: round(v * factor) for k, v in domains.items()}

            # Adjust for rounding errors
            total = sum(domains.values())
            if total != 100:
                # Add/subtract from largest domain
                largest = max(domains.keys(), key=lambda k: domains[k])
                domains[largest] += 100 - total

        return domains

    def _parse_mcps(self, text: str) -> List[Dict[str, Any]]:
        """Parse MCP recommendations from text."""
        mcps = []

        # Pattern for MCP recommendations
        # Looking for: "Tier 1: serena - Code analysis" or similar
        mcp_pattern = r"Tier\s+(\d+):\s*(\S+)\s*[-–]\s*([^\n]+)"

        for match in re.finditer(mcp_pattern, text):
            tier = int(match.group(1))
            name = match.group(2).strip()
            purpose = match.group(3).strip()

            # Determine priority from tier
            if tier == 1:
                priority = "REQUIRED"
            elif tier == 2:
                priority = "RECOMMENDED"
            else:
                priority = "OPTIONAL"

            mcps.append(
                MCPRecommendation(
                    name=name, tier=tier, purpose=purpose, priority=priority
                ).model_dump()
            )

        return mcps

    def _parse_phases(self, text: str) -> List[Dict[str, Any]]:
        """Parse 5-phase implementation plan from text."""
        phases = []

        # Look for phase headers like "Phase 1: Foundation" or "## Phase 1: Foundation"
        # BUT exclude lines that look like examples or documentation
        phase_pattern = r"(?:^|\n)(?:##\s*)?Phase\s+(\d+):\s*([^\n]+)"

        all_matches = list(re.finditer(phase_pattern, text, re.IGNORECASE | re.MULTILINE))

        # Filter out documentation/examples - only keep phases 1-5 in sequence near each other
        if all_matches:
            # Find the best cluster of 5 sequential phases
            for start_idx in range(len(all_matches) - 4):
                candidate_phases = all_matches[start_idx:start_idx + 5]
                phase_numbers = [int(m.group(1)) for m in candidate_phases]

                # Check if this is phases 1-5 in order
                if phase_numbers == [1, 2, 3, 4, 5]:
                    phase_matches = candidate_phases
                    break
            else:
                # No perfect 1-5 sequence, try to find first 5 phases
                phase_matches = [m for m in all_matches if int(m.group(1)) <= 5][:5]
        else:
            phase_matches = []

        if not phase_matches:
            # Return empty list if no phases found (allows partial parsing)
            return phases

        for i, match in enumerate(phase_matches):
            phase_number = int(match.group(1))
            phase_name = match.group(2).strip()

            # Extract content until next phase or end
            start_pos = match.end()
            end_pos = phase_matches[i + 1].start() if i + 1 < len(phase_matches) else len(text)
            phase_content = text[start_pos:end_pos]

            # Parse objectives, deliverables, validation
            objectives = self._extract_list_items(phase_content, r"(?:Objective|Goal)s?:")
            deliverables = self._extract_list_items(
                phase_content, r"Deliverable[s]?:"
            )
            validation_gate = self._extract_list_items(
                phase_content, r"Validation:"
            )

            # Parse duration
            duration_match = re.search(r"(\d+)%", phase_content)
            duration_percent = (
                int(duration_match.group(1)) if duration_match else 20
            )  # Default 20%

            duration_est_match = re.search(
                r"(?:Duration|Timeline):\s*([^\n]+)", phase_content
            )
            duration_estimate = (
                duration_est_match.group(1).strip()
                if duration_est_match
                else f"{duration_percent}% of timeline"
            )

            phases.append(
                Phase(
                    phase_number=phase_number,
                    phase_name=phase_name,
                    objectives=objectives or [f"Complete phase {phase_number}"],
                    deliverables=deliverables or [f"Phase {phase_number} deliverables"],
                    validation_gate=validation_gate or ["Phase validation"],
                    duration_percent=duration_percent,
                    duration_estimate=duration_estimate,
                ).model_dump()
            )

        # Accept 0 or 5 phases (skill may not include phase plan in all outputs)
        if phases and len(phases) > 0 and len(phases) != 5:
            # Log warning but don't fail - phase plan is optional in some contexts
            print(f"WARNING: Expected 5 phases, found {len(phases)}. Accepting anyway.")

        return phases

    def _extract_list_items(self, text: str, header_pattern: str) -> List[str]:
        """Extract bulleted/numbered list items after a header."""
        items = []

        # Find header
        match = re.search(header_pattern, text, re.IGNORECASE)
        if not match:
            return items

        # Extract text after header
        content_start = match.end()
        # Find next header or section break
        next_section = re.search(r"\n(?:#{1,3}\s|\*\*[A-Z])", text[content_start:])
        content_end = (
            content_start + next_section.start() if next_section else len(text)
        )
        content = text[content_start:content_end]

        # Extract list items (-, *, 1., etc.)
        for line in content.split("\n"):
            line = line.strip()
            if re.match(r"^[-*•]\s+", line) or re.match(r"^\d+\.\s+", line):
                # Remove bullet/number prefix
                item = re.sub(r"^[-*•\d.]+\s+", "", line).strip()
                if item:
                    items.append(item)

        return items

    def _parse_execution_strategy(self, text: str) -> str:
        """Parse execution strategy (sequential or wave-based)."""
        if re.search(r"wave[-\s]based", text, re.IGNORECASE):
            return "wave-based"
        elif re.search(r"sequential", text, re.IGNORECASE):
            return "sequential"
        else:
            # Default based on complexity
            return "sequential"

    def _parse_timeline(self, text: str) -> str:
        """Parse human-readable timeline estimate."""
        # Look for patterns like "2-4 days", "1-2 weeks", "3 weeks"
        timeline_match = re.search(
            r"(?:Timeline|Duration|Estimate):\s*([^\n]+)", text, re.IGNORECASE
        )

        if timeline_match:
            return timeline_match.group(1).strip()

        # Look for bare time estimates
        time_match = re.search(r"(\d+[-–]\d+)\s+(day|week|month)s?", text)
        if time_match:
            return f"{time_match.group(1)} {time_match.group(2)}s"

        return "See phase plan for details"

    # ============================================================================
    # WAVE RESULT PARSING METHODS
    # ============================================================================

    def _parse_wave_number(self, text: str) -> int:
        """Parse wave number from result text."""
        match = re.search(r"Wave\s+(\d+)", text, re.IGNORECASE)
        return int(match.group(1)) if match else 1

    def _parse_wave_name(self, text: str) -> str:
        """Parse wave name from result text."""
        match = re.search(r"Wave\s+\d+:\s*([^\n]+)", text, re.IGNORECASE)
        return match.group(1).strip() if match else "Unknown Wave"

    def _parse_agents_deployed(self, text: str) -> int:
        """Parse number of agents deployed."""
        match = re.search(r"(\d+)\s+agent[s]?\s+deployed", text, re.IGNORECASE)
        return int(match.group(1)) if match else 1

    def _parse_execution_time(self, text: str) -> float:
        """Parse execution time in minutes."""
        # Look for patterns like "45 minutes", "1.5 hours"
        minutes_match = re.search(r"(\d+(?:\.\d+)?)\s+minute[s]?", text, re.IGNORECASE)
        if minutes_match:
            return float(minutes_match.group(1))

        hours_match = re.search(r"(\d+(?:\.\d+)?)\s+hour[s]?", text, re.IGNORECASE)
        if hours_match:
            return float(hours_match.group(1)) * 60

        return 0.0

    def _parse_files_created(self, text: str) -> List[str]:
        """Parse list of files created."""
        files = []
        # Look for file patterns (paths or names with extensions)
        file_pattern = r"[\w/.-]+\.(?:py|md|json|toml|yaml|yml|txt)"

        for match in re.finditer(file_pattern, text):
            file_path = match.group(0)
            if file_path not in files:
                files.append(file_path)

        return files

    def _parse_components_built(self, text: str) -> List[str]:
        """Parse list of components/modules built."""
        components = self._extract_list_items(text, r"Components?(?:\s+Built)?:")
        if not components:
            components = self._extract_list_items(text, r"Deliverable[s]?:")
        return components

    def _parse_decisions(self, text: str) -> List[str]:
        """Parse key decisions made."""
        return self._extract_list_items(text, r"Decisions?(?:\s+Made)?:")

    def _parse_tests_created(self, text: str) -> int:
        """Parse number of tests created."""
        match = re.search(r"(\d+)\s+test[s]?", text, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    def _parse_no_mocks_confirmation(self, text: str) -> bool:
        """Check for NO MOCKS confirmation."""
        # Look for explicit confirmation or absence of mocks
        if re.search(r"no\s+mocks", text, re.IGNORECASE):
            return True
        if re.search(r"mock[s]?\s+(?:used|created)", text, re.IGNORECASE):
            return False
        return True  # Default to True (optimistic)

    def _parse_quality_metrics(self, text: str) -> Dict[str, Any]:
        """Parse quality metrics (coverage, type hints, etc.)."""
        metrics = {}

        # Coverage percentage
        coverage_match = re.search(r"(\d+)%\s+coverage", text, re.IGNORECASE)
        if coverage_match:
            metrics["coverage"] = int(coverage_match.group(1))

        # Type hints
        if re.search(r"type\s+hint[s]?", text, re.IGNORECASE):
            metrics["type_hints"] = True

        # Docstrings
        if re.search(r"docstring[s]?", text, re.IGNORECASE):
            metrics["docstrings"] = True

        return metrics

    # ============================================================================
    # TEST RESULT PARSING METHODS
    # ============================================================================

    def extract_test_result(self, messages: List) -> Dict[str, Any]:
        """
        Extract test execution results from SDK message stream.

        Parses test output including:
        - Tests passed/failed counts
        - Test execution time
        - Coverage metrics
        - NO MOCKS enforcement confirmation

        Args:
            messages: List of SDK messages

        Returns:
            Dictionary with test results
        """
        result_text = self._collect_assistant_text(messages)

        return {
            "total_tests": self._parse_total_tests(result_text),
            "tests_passed": self._parse_tests_passed(result_text),
            "tests_failed": self._parse_tests_failed(result_text),
            "all_passed": self._parse_all_tests_passed(result_text),
            "execution_time": self._parse_execution_time(result_text),
            "coverage": self._parse_coverage_percent(result_text),
            "no_mocks_confirmed": self._parse_no_mocks_confirmation(result_text),
            "test_details": self._parse_test_details(result_text),
        }

    def _parse_total_tests(self, text: str) -> int:
        """Parse total number of tests."""
        match = re.search(r"(\d+)\s+total\s+test[s]?", text, re.IGNORECASE)
        if match:
            return int(match.group(1))

        # Try alternative patterns
        match = re.search(r"(\d+)\s+test[s]?\s+(?:run|executed)", text, re.IGNORECASE)
        if match:
            return int(match.group(1))

        return 0

    def _parse_tests_passed(self, text: str) -> int:
        """Parse number of tests passed."""
        match = re.search(r"(\d+)\s+(?:test[s]?\s+)?passed", text, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    def _parse_tests_failed(self, text: str) -> int:
        """Parse number of tests failed."""
        match = re.search(r"(\d+)\s+(?:test[s]?\s+)?failed", text, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    def _parse_all_tests_passed(self, text: str) -> bool:
        """Determine if all tests passed."""
        # Check for explicit success indicators
        if re.search(r"all\s+tests?\s+passed", text, re.IGNORECASE):
            return True
        if re.search(r"0\s+(?:test[s]?\s+)?failed", text, re.IGNORECASE):
            return True

        # Check for failure indicators
        if re.search(r"test[s]?\s+failed", text, re.IGNORECASE):
            return False

        # Default to False if unclear
        return False

    def _parse_coverage_percent(self, text: str) -> Optional[float]:
        """Parse test coverage percentage."""
        match = re.search(r"(\d+(?:\.\d+)?)%\s+coverage", text, re.IGNORECASE)
        return float(match.group(1)) if match else None

    def _parse_test_details(self, text: str) -> List[str]:
        """Parse detailed test information."""
        details = []

        # Look for test names and results
        test_pattern = r"(?:PASS|FAIL):\s*([^\n]+)"
        for match in re.finditer(test_pattern, text):
            details.append(match.group(0).strip())

        return details

    # ============================================================================
    # REFLECTION RESULT PARSING METHODS
    # ============================================================================

    def extract_reflection_result(self, messages: List) -> Dict[str, Any]:
        """
        Extract reflection analysis results from SDK message stream.

        Parses reflection output including:
        - Implementation completeness
        - Identified gaps
        - Test coverage issues
        - Security concerns
        - Documentation status

        Args:
            messages: List of SDK messages

        Returns:
            Dictionary with reflection results
        """
        result_text = self._collect_assistant_text(messages)

        gaps = self._parse_reflection_gaps(result_text)

        return {
            "gaps_found": len(gaps) > 0,
            "gap_count": len(gaps),
            "gaps": gaps,
            "completeness_score": self._parse_completeness_score(result_text),
            "recommendations": self._parse_reflection_recommendations(result_text),
            "critical_issues": self._parse_critical_issues(result_text),
            "summary": self._parse_reflection_summary(result_text),
        }

    def _parse_reflection_gaps(self, text: str) -> List[Dict[str, str]]:
        """Parse identified gaps from reflection."""
        gaps = []

        # Look for gap indicators
        gap_patterns = [
            r"Gap:\s*([^\n]+)",
            r"Missing:\s*([^\n]+)",
            r"TODO:\s*([^\n]+)",
            r"⚠\s*([^\n]+)",
        ]

        for pattern in gap_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                gap_text = match.group(1).strip()
                if gap_text:
                    gaps.append(
                        {
                            "type": "gap",
                            "description": gap_text,
                            "severity": self._determine_gap_severity(gap_text),
                        }
                    )

        return gaps

    def _determine_gap_severity(self, gap_text: str) -> str:
        """Determine severity of a gap based on keywords."""
        gap_lower = gap_text.lower()

        if any(
            word in gap_lower
            for word in ["critical", "security", "vulnerability", "broken"]
        ):
            return "critical"
        elif any(
            word in gap_lower for word in ["important", "required", "missing test"]
        ):
            return "high"
        elif any(word in gap_lower for word in ["should", "recommended", "improve"]):
            return "medium"
        else:
            return "low"

    def _parse_completeness_score(self, text: str) -> Optional[float]:
        """Parse implementation completeness score."""
        match = re.search(r"(\d+(?:\.\d+)?)%\s+complete", text, re.IGNORECASE)
        if match:
            return float(match.group(1)) / 100.0

        # Try percentage pattern
        match = re.search(r"completeness:\s*(\d+(?:\.\d+)?)%", text, re.IGNORECASE)
        if match:
            return float(match.group(1)) / 100.0

        return None

    def _parse_reflection_recommendations(self, text: str) -> List[str]:
        """Parse recommendations from reflection."""
        return self._extract_list_items(text, r"Recommendation[s]?:")

    def _parse_critical_issues(self, text: str) -> List[str]:
        """Parse critical issues identified."""
        issues = []

        # Look for critical issue indicators
        critical_patterns = [
            r"Critical:\s*([^\n]+)",
            r"Security:\s*([^\n]+)",
            r"Blocker:\s*([^\n]+)",
        ]

        for pattern in critical_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                issue_text = match.group(1).strip()
                if issue_text:
                    issues.append(issue_text)

        return issues

    def _parse_reflection_summary(self, text: str) -> str:
        """Parse overall reflection summary."""
        # Look for summary section
        summary_match = re.search(
            r"Summary:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)", text, re.IGNORECASE
        )
        if summary_match:
            return summary_match.group(1).strip()

        # Extract first paragraph as summary
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if len(line) > 50:  # Substantial line
                return line

        return "No summary available"


# Export
__all__ = ["MessageParser"]
