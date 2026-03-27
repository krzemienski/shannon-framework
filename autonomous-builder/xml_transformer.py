"""
XML Prompt Transformer for Autonomous Claude Code Builder.

Transforms user requests into structured XML prompts for Claude,
following best practices from Claude documentation:
- Consistent tag naming
- Hierarchical structure
- Meaningful content organization
- Easy parsability
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from pathlib import Path
import re


@dataclass
class CodebaseContext:
    """Context information about an existing codebase."""
    exists: bool = False
    project_type: Optional[str] = None
    languages: List[str] = None
    frameworks: List[str] = None
    dependencies: Dict[str, str] = None
    structure: Dict[str, Any] = None
    patterns: List[str] = None
    readme_summary: Optional[str] = None

    def __post_init__(self):
        if self.languages is None:
            self.languages = []
        if self.frameworks is None:
            self.frameworks = []
        if self.dependencies is None:
            self.dependencies = {}
        if self.structure is None:
            self.structure = {}
        if self.patterns is None:
            self.patterns = []

    @classmethod
    def empty(cls) -> "CodebaseContext":
        """Create empty context for new projects."""
        return cls(exists=False)

    def to_xml(self) -> str:
        """Convert context to XML format."""
        if not self.exists:
            return "<existing_codebase>None - new project</existing_codebase>"

        parts = ["<existing_codebase>"]

        if self.project_type:
            parts.append(f"  <project_type>{self.project_type}</project_type>")

        if self.languages:
            parts.append(f"  <languages>{', '.join(self.languages)}</languages>")

        if self.frameworks:
            parts.append(f"  <frameworks>{', '.join(self.frameworks)}</frameworks>")

        if self.dependencies:
            parts.append("  <dependencies>")
            for name, version in list(self.dependencies.items())[:10]:  # Limit
                parts.append(f"    <dep name=\"{name}\" version=\"{version}\"/>")
            if len(self.dependencies) > 10:
                parts.append(f"    <!-- and {len(self.dependencies) - 10} more -->")
            parts.append("  </dependencies>")

        if self.patterns:
            parts.append("  <patterns>")
            for pattern in self.patterns[:5]:  # Limit
                parts.append(f"    <pattern>{pattern}</pattern>")
            parts.append("  </patterns>")

        if self.readme_summary:
            parts.append(f"  <readme_summary>{self.readme_summary}</readme_summary>")

        parts.append("</existing_codebase>")
        return "\n".join(parts)


@dataclass
class Scenario:
    """Scenario information for the build task."""
    is_existing: bool
    target_dir: Path
    has_package_json: bool = False
    has_requirements_txt: bool = False
    has_cargo_toml: bool = False
    has_go_mod: bool = False
    git_initialized: bool = False

    def to_xml(self) -> str:
        """Convert scenario to XML format."""
        scenario_type = "existing_directory" if self.is_existing else "new_project"
        parts = [f"<scenario type=\"{scenario_type}\">"]
        parts.append(f"  <target_directory>{self.target_dir}</target_directory>")
        parts.append(f"  <git_initialized>{self.git_initialized}</git_initialized>")

        if self.is_existing:
            parts.append("  <detected_configs>")
            if self.has_package_json:
                parts.append("    <config>package.json (Node.js)</config>")
            if self.has_requirements_txt:
                parts.append("    <config>requirements.txt (Python)</config>")
            if self.has_cargo_toml:
                parts.append("    <config>Cargo.toml (Rust)</config>")
            if self.has_go_mod:
                parts.append("    <config>go.mod (Go)</config>")
            parts.append("  </detected_configs>")

        parts.append("</scenario>")
        return "\n".join(parts)


class XMLPromptTransformer:
    """
    Transforms user requests into structured XML prompts for Claude.

    Follows Claude's XML best practices:
    - Consistent tag naming throughout
    - Hierarchical nesting for layered information
    - Meaningful, descriptive tag names
    - Combines with other techniques (examples, chain-of-thought)
    """

    def __init__(self):
        """Initialize transformer."""
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """Load prompt templates."""
        return {
            "initializer": INITIALIZER_TEMPLATE,
            "coding": CODING_TEMPLATE,
            "analysis": ANALYSIS_TEMPLATE
        }

    def transform(
        self,
        request: str,
        context: CodebaseContext,
        scenario: Scenario,
        available_mcps: List[str] = None,
        template_type: str = "initializer"
    ) -> str:
        """
        Transform user request into XML prompt.

        Args:
            request: User's natural language request
            context: Codebase context from Serena
            scenario: Build scenario (existing vs new)
            available_mcps: List of available MCP servers
            template_type: Which template to use

        Returns:
            Structured XML prompt
        """
        if available_mcps is None:
            available_mcps = []

        template = self.templates.get(template_type, INITIALIZER_TEMPLATE)

        # Build XML sections
        context_xml = context.to_xml()
        scenario_xml = scenario.to_xml()
        mcps_xml = self._format_mcps(available_mcps)

        # Extract key information from request
        extracted = self._extract_request_info(request)

        # Fill template
        prompt = template.format(
            context_xml=context_xml,
            scenario_xml=scenario_xml,
            mcps_xml=mcps_xml,
            user_request=self._escape_xml(request),
            objective=self._escape_xml(extracted.get("objective", request)),
            requirements=self._format_requirements(extracted.get("requirements", [])),
            constraints=self._format_constraints(extracted.get("constraints", [])),
            target_dir=scenario.target_dir
        )

        return prompt

    def transform_for_coding(
        self,
        target_dir: Path,
        session_number: int,
        previous_progress: Optional[str] = None
    ) -> str:
        """
        Create coding agent prompt for continuation session.

        Args:
            target_dir: Project directory
            session_number: Which session this is (2+)
            previous_progress: Summary from previous session

        Returns:
            XML prompt for coding agent
        """
        progress_section = ""
        if previous_progress:
            progress_section = f"""
  <previous_session>
    <session_number>{session_number - 1}</session_number>
    <summary>{self._escape_xml(previous_progress)}</summary>
  </previous_session>"""

        return CODING_TEMPLATE.format(
            target_dir=target_dir,
            session_number=session_number,
            progress_section=progress_section
        )

    def _format_mcps(self, mcps: List[str]) -> str:
        """Format available MCPs as XML."""
        if not mcps:
            return "<mcps_available>None configured</mcps_available>"

        parts = ["<mcps_available>"]
        for mcp in mcps:
            parts.append(f"  <mcp>{mcp}</mcp>")
        parts.append("</mcps_available>")
        return "\n".join(parts)

    def _extract_request_info(self, request: str) -> Dict[str, Any]:
        """
        Extract structured information from natural language request.

        Args:
            request: User's request

        Returns:
            Dictionary with objective, requirements, constraints
        """
        # Simple extraction - could be enhanced with LLM
        info = {
            "objective": request,
            "requirements": [],
            "constraints": []
        }

        # Look for explicit requirements
        req_patterns = [
            r"with (\w+(?:\s+and\s+\w+)*)",  # "with React and Node.js"
            r"using (\w+(?:\s+and\s+\w+)*)",  # "using TypeScript"
            r"include[s]? ([\w\s,]+)",        # "includes authentication"
        ]

        for pattern in req_patterns:
            matches = re.findall(pattern, request, re.IGNORECASE)
            for match in matches:
                items = re.split(r'\s+and\s+|,\s*', match)
                info["requirements"].extend([i.strip() for i in items if i.strip()])

        # Look for constraints
        constraint_patterns = [
            r"must (?:be|have|use) ([\w\s]+)",
            r"should (?:be|have|use) ([\w\s]+)",
            r"needs? to ([\w\s]+)",
        ]

        for pattern in constraint_patterns:
            matches = re.findall(pattern, request, re.IGNORECASE)
            info["constraints"].extend(matches)

        return info

    def _format_requirements(self, requirements: List[str]) -> str:
        """Format requirements as XML list."""
        if not requirements:
            return "<requirements>Infer from specification</requirements>"

        parts = ["<requirements>"]
        for req in requirements:
            parts.append(f"  <requirement>{self._escape_xml(req)}</requirement>")
        parts.append("</requirements>")
        return "\n".join(parts)

    def _format_constraints(self, constraints: List[str]) -> str:
        """Format constraints as XML list."""
        if not constraints:
            return "<constraints>Standard best practices</constraints>"

        parts = ["<constraints>"]
        for con in constraints:
            parts.append(f"  <constraint>{self._escape_xml(con)}</constraint>")
        parts.append("</constraints>")
        return "\n".join(parts)

    def _escape_xml(self, text: str) -> str:
        """Escape special XML characters."""
        if not text:
            return ""
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace('"', "&quot;")
        text = text.replace("'", "&apos;")
        return text

    def parse_response(self, response: str, tags: List[str]) -> Dict[str, str]:
        """
        Extract content from tagged response sections.

        Args:
            response: Claude's response text
            tags: List of tag names to extract

        Returns:
            Dictionary mapping tag names to their content
        """
        result = {}
        for tag in tags:
            pattern = rf"<{tag}>(.*?)</{tag}>"
            match = re.search(pattern, response, re.DOTALL)
            if match:
                result[tag] = match.group(1).strip()
        return result


# Prompt Templates

INITIALIZER_TEMPLATE = """<system>
You are an Initializer Agent for an autonomous code builder. Your task is to set up
the foundation for a multi-session development project.

<context>
{context_xml}
{scenario_xml}
{mcps_xml}
</context>

<task>
<specification>
{user_request}
</specification>
<objective>{objective}</objective>
{requirements}
{constraints}
<target_directory>{target_dir}</target_directory>
</task>

<required_outputs>
<output name="feature_list.json">
Generate a comprehensive feature list with:
- Minimum 50 features (scale with project complexity)
- ALL features start with "passes": false
- CRITICAL: IT IS CATASTROPHIC TO REMOVE OR EDIT FEATURES IN FUTURE SESSIONS
- Categories: functional, style, integration, performance, security
- Each feature has testable verification steps

Schema:
{{
  "project_name": "string",
  "created_at": "ISO datetime",
  "features": [
    {{
      "id": "unique-id",
      "category": "functional|style|integration|performance|security",
      "description": "What this feature does",
      "priority": 1-10,
      "steps": ["Verification step 1", "Step 2", ...],
      "passes": false
    }}
  ]
}}
</output>

<output name="init.sh">
Environment setup script:
- Install all dependencies
- Start development server(s)
- Print access instructions (URLs, ports)
- Handle errors gracefully
</output>

<output name="claude-progress.txt">
Session summary including:
- What was accomplished this session
- Current project state
- Files created/modified
- Next steps for coding agent
- Any blockers or decisions needed
</output>
</required_outputs>

<instructions>
<step>Read the specification carefully and understand all requirements</step>
<step>If existing codebase, query Serena MCP for structure and patterns</step>
<step>Design feature list covering all specification requirements</step>
<step>Create init.sh appropriate for the technology stack</step>
<step>Initialize git repository if not exists</step>
<step>Create basic directory structure</step>
<step>Write feature_list.json with ALL features marked passes: false</step>
<step>Optionally begin implementing highest-priority features if context allows</step>
<step>Git commit all changes with descriptive message</step>
<step>Write claude-progress.txt summarizing session</step>
</instructions>

<constraints>
<constraint>Use Serena MCP for all codebase context queries</constraint>
<constraint>Respect existing code patterns if implementing in existing directory</constraint>
<constraint>Do NOT overwrite existing files without explicit instruction</constraint>
<constraint>Create git commit after initialization</constraint>
<constraint>Feature list is immutable - only passes field can change later</constraint>
</constraints>
</system>"""


CODING_TEMPLATE = """<system>
You are a Coding Agent continuing an autonomous development project.
Work incrementally on ONE feature per session.

<session_info>
<session_number>{session_number}</session_number>
<working_directory>{target_dir}</working_directory>
{progress_section}
</session_info>

<session_startup>
<step number="1">Run pwd to verify working directory</step>
<step number="2">Read git log --oneline -10 for recent history</step>
<step number="3">Read claude-progress.txt for previous session context</step>
<step number="4">Read feature_list.json to find next incomplete feature</step>
<step number="5">Run ./init.sh to start development environment</step>
<step number="6">Execute baseline smoke test to verify existing functionality</step>
</session_startup>

<task>
<objective>Implement the highest-priority incomplete feature</objective>
<verification_required>true</verification_required>
</task>

<verification_requirements>
<requirement>Test like a human user with visual verification</requirement>
<requirement>Use Puppeteer MCP for browser-based testing if applicable</requirement>
<requirement>Take screenshots to verify UI changes</requirement>
<requirement>Do NOT mark feature complete without verification</requirement>
<requirement>Run any existing test suites</requirement>
</verification_requirements>

<feature_completion>
When a feature passes verification:
<step>Update feature_list.json: ONLY change "passes" field to true</step>
<step>Add "implemented_at" timestamp</step>
<step>Add "session_id" for tracking</step>
<step>NEVER modify feature description or steps</step>
</feature_completion>

<session_closure>
<step>Git commit with descriptive message referencing feature ID</step>
<step>Update claude-progress.txt with session accomplishments</step>
<step>Leave codebase in mergeable state (no broken code)</step>
<step>Document any blockers or decisions for next session</step>
</session_closure>

<important>
<rule>Complete ONE feature thoroughly, not many features partially</rule>
<rule>It's acceptable to complete only one feature - more sessions will follow</rule>
<rule>NEVER remove or edit feature definitions in feature_list.json</rule>
<rule>Previous sessions may have introduced bugs - verify before continuing</rule>
<rule>Always verify with real testing before marking complete</rule>
</important>
</system>"""


ANALYSIS_TEMPLATE = """<system>
You are an Analysis Agent examining a codebase before modification.

<context>
{context_xml}
{scenario_xml}
</context>

<task>
<objective>Analyze codebase and create comprehensive context</objective>
</task>

<analysis_areas>
<area name="structure">Directory organization and file layout</area>
<area name="patterns">Coding patterns and conventions used</area>
<area name="dependencies">External dependencies and versions</area>
<area name="architecture">Overall architecture and design patterns</area>
<area name="testing">Testing approach and coverage</area>
</analysis_areas>

<output_format>
<findings>
Detailed analysis of each area
</findings>
<recommendations>
Suggestions for maintaining consistency
</recommendations>
<risks>
Potential issues with proposed changes
</risks>
</output_format>
</system>"""
