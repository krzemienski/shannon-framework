"""
Shannon Framework v4 - Specification Parser

Converts user input (text, JSON, YAML, markdown) to structured SpecificationObject.
"""

import re
import json
import yaml
from typing import Dict, List, Optional, Any
from .models import (
    SpecificationObject,
    Requirement,
    TechStack,
    SpecificationFormat,
)


class SpecificationParser:
    """Parse user specifications into structured format."""

    def __init__(self):
        self.tech_stack_keywords = {
            'languages': ['python', 'javascript', 'typescript', 'java', 'go', 'rust', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin'],
            'frameworks': ['react', 'vue', 'angular', 'next.js', 'express', 'fastapi', 'django', 'flask', 'spring', 'rails'],
            'databases': ['postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'dynamodb', 'cassandra'],
            'infrastructure': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
        }

    def parse(self, raw_input: str) -> SpecificationObject:
        """
        Parse raw specification input into SpecificationObject.

        Args:
            raw_input: User specification (text, JSON, YAML, markdown)

        Returns:
            SpecificationObject with parsed data

        Raises:
            ValueError: If input cannot be parsed
        """
        if not raw_input or not raw_input.strip():
            raise ValueError("Specification input cannot be empty")

        # Detect format
        spec_format = self._detect_format(raw_input)

        # Parse based on format
        if spec_format == SpecificationFormat.JSON:
            return self._parse_json(raw_input)
        elif spec_format == SpecificationFormat.YAML:
            return self._parse_yaml(raw_input)
        elif spec_format == SpecificationFormat.MARKDOWN:
            return self._parse_markdown(raw_input)
        else:
            return self._parse_text(raw_input)

    def _detect_format(self, raw_input: str) -> SpecificationFormat:
        """Detect input format."""
        stripped = raw_input.strip()

        # JSON detection
        if stripped.startswith('{') or stripped.startswith('['):
            try:
                json.loads(stripped)
                return SpecificationFormat.JSON
            except json.JSONDecodeError:
                pass

        # YAML detection
        if re.match(r'^[\w_-]+:\s', stripped, re.MULTILINE):
            try:
                yaml.safe_load(stripped)
                return SpecificationFormat.YAML
            except yaml.YAMLError:
                pass

        # Markdown detection
        if re.search(r'^#+\s', stripped, re.MULTILINE):
            return SpecificationFormat.MARKDOWN

        # Default to text
        return SpecificationFormat.TEXT

    def _parse_json(self, raw_input: str) -> SpecificationObject:
        """Parse JSON specification."""
        try:
            data = json.loads(raw_input)
            return self._dict_to_specification(data, SpecificationFormat.JSON, raw_input)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

    def _parse_yaml(self, raw_input: str) -> SpecificationObject:
        """Parse YAML specification."""
        try:
            data = yaml.safe_load(raw_input)
            return self._dict_to_specification(data, SpecificationFormat.YAML, raw_input)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {e}")

    def _parse_markdown(self, raw_input: str) -> SpecificationObject:
        """Parse markdown specification."""
        spec = SpecificationObject(
            raw_input=raw_input,
            title=self._extract_title_from_markdown(raw_input),
            description=self._extract_description_from_markdown(raw_input),
            format=SpecificationFormat.MARKDOWN,
        )

        # Extract requirements from markdown lists
        spec.requirements = self._extract_requirements_from_markdown(raw_input)

        # Extract tech stack from content
        spec.tech_stack = self._extract_tech_stack(raw_input)

        return spec

    def _parse_text(self, raw_input: str) -> SpecificationObject:
        """Parse plain text specification."""
        spec = SpecificationObject(
            raw_input=raw_input,
            title=self._extract_title_from_text(raw_input),
            description=self._extract_description_from_text(raw_input),
            format=SpecificationFormat.TEXT,
        )

        # Extract requirements from numbered/bulleted lists
        spec.requirements = self._extract_requirements_from_text(raw_input)

        # Extract tech stack from content
        spec.tech_stack = self._extract_tech_stack(raw_input)

        return spec

    def _dict_to_specification(
        self, data: Dict[str, Any], format: SpecificationFormat, raw_input: str
    ) -> SpecificationObject:
        """Convert dictionary to SpecificationObject."""
        spec = SpecificationObject(
            raw_input=raw_input,
            title=data.get('title', 'Untitled Specification'),
            description=data.get('description', ''),
            format=format,
        )

        # Parse requirements
        if 'requirements' in data:
            spec.requirements = [
                Requirement(
                    id=req.get('id', f"req-{i+1}"),
                    text=req.get('text', req.get('description', '')),
                    priority=req.get('priority', 'medium'),
                    category=req.get('category', 'functional'),
                    dependencies=req.get('dependencies', []),
                    metadata=req.get('metadata', {}),
                )
                for i, req in enumerate(data['requirements'])
            ]

        # Parse tech stack
        if 'tech_stack' in data:
            ts = data['tech_stack']
            spec.tech_stack = TechStack(
                languages=ts.get('languages', []),
                frameworks=ts.get('frameworks', []),
                databases=ts.get('databases', []),
                infrastructure=ts.get('infrastructure', []),
                tools=ts.get('tools', []),
            )

        # Other fields
        spec.architecture_pattern = data.get('architecture_pattern')
        spec.deployment_target = data.get('deployment_target')

        return spec

    def _extract_title_from_markdown(self, text: str) -> str:
        """Extract title from markdown (first # heading)."""
        match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
        return match.group(1) if match else "Untitled Specification"

    def _extract_title_from_text(self, text: str) -> str:
        """Extract title from text (first line or best guess)."""
        lines = text.strip().split('\n')
        first_line = lines[0].strip() if lines else "Untitled Specification"

        # If first line is short and descriptive, use it
        if len(first_line) < 100 and first_line:
            return first_line

        # Otherwise, try to find a short descriptive sentence
        for line in lines[:5]:
            if 10 < len(line) < 80:
                return line.strip()

        return "Untitled Specification"

    def _extract_description_from_markdown(self, text: str) -> str:
        """Extract description from markdown (text after title, before first ## heading)."""
        # Remove first # heading
        text_after_title = re.sub(r'^#\s+.+\n', '', text, count=1, flags=re.MULTILINE)

        # Get text before first ## heading
        match = re.search(r'^(.+?)(?=^##\s)', text_after_title, re.MULTILINE | re.DOTALL)
        description = match.group(1).strip() if match else text_after_title.strip()

        return description

    def _extract_description_from_text(self, text: str) -> str:
        """Extract description from text (first paragraph or multiple sentences)."""
        lines = text.strip().split('\n')

        # Skip first line (likely title)
        description_lines = lines[1:] if len(lines) > 1 else lines

        # Get first paragraph
        description = []
        for line in description_lines:
            if line.strip():
                description.append(line.strip())
            elif description:
                break  # End of first paragraph

        return ' '.join(description)

    def _extract_requirements_from_markdown(self, text: str) -> List[Requirement]:
        """Extract requirements from markdown lists."""
        requirements = []

        # Find markdown lists (- or * or 1.)
        list_pattern = r'^[\s]*[-*]\s+(.+)$|^[\s]*\d+\.\s+(.+)$'
        matches = re.finditer(list_pattern, text, re.MULTILINE)

        for i, match in enumerate(matches, 1):
            req_text = match.group(1) or match.group(2)
            priority = self._infer_priority(req_text)

            requirements.append(Requirement(
                id=f"req-{i}",
                text=req_text.strip(),
                priority=priority,
                category=self._infer_category(req_text),
            ))

        return requirements

    def _extract_requirements_from_text(self, text: str) -> List[Requirement]:
        """Extract requirements from text (numbered/bulleted lists)."""
        # Similar to markdown extraction
        return self._extract_requirements_from_markdown(text)

    def _extract_tech_stack(self, text: str) -> TechStack:
        """Extract tech stack from text content."""
        text_lower = text.lower()

        tech_stack = TechStack()

        # Search for keywords
        for tech_type, keywords in self.tech_stack_keywords.items():
            found_techs = []
            for keyword in keywords:
                # Word boundary search
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    found_techs.append(keyword.title())

            if tech_type == 'languages':
                tech_stack.languages = found_techs
            elif tech_type == 'frameworks':
                tech_stack.frameworks = found_techs
            elif tech_type == 'databases':
                tech_stack.databases = found_techs
            elif tech_type == 'infrastructure':
                tech_stack.infrastructure = found_techs

        return tech_stack

    def _infer_priority(self, text: str) -> str:
        """Infer requirement priority from text."""
        text_lower = text.lower()

        # High priority keywords
        if any(keyword in text_lower for keyword in ['critical', 'must', 'required', 'essential']):
            return 'high'

        # Low priority keywords
        if any(keyword in text_lower for keyword in ['nice to have', 'optional', 'could', 'might']):
            return 'low'

        # Default to medium
        return 'medium'

    def _infer_category(self, text: str) -> str:
        """Infer requirement category from text."""
        text_lower = text.lower()

        # Technical requirements
        if any(keyword in text_lower for keyword in ['database', 'api', 'server', 'infrastructure', 'deployment']):
            return 'technical'

        # Non-functional requirements
        if any(keyword in text_lower for keyword in ['performance', 'security', 'scalability', 'availability']):
            return 'non-functional'

        # Default to functional
        return 'functional'
