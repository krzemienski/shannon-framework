"""
Shannon Framework v4 - Skill Loader

Handles progressive skill loading (3 levels) for token efficiency.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Optional, List
from .models import (
    Skill, SkillMetadata, SkillContent, SkillReferences,
    LoadLevel, SkillType
)


class SkillLoadError(Exception):
    """Exception raised when skill loading fails."""
    pass


class SkillLoader:
    """
    Loads skills with progressive disclosure.

    Level 1: Frontmatter only (~50 tokens) - Always loaded for all skills
    Level 2: Full SKILL.md body (~500 lines) - Loaded on skill invocation
    Level 3: All references/* - Loaded when explicitly referenced
    """

    def __init__(self, skills_dir: Path):
        """
        Initialize skill loader.

        Args:
            skills_dir: Base directory containing skill definitions
        """
        self.skills_dir = Path(skills_dir)
        if not self.skills_dir.exists():
            raise SkillLoadError(f"Skills directory not found: {skills_dir}")

    def discover_skills(self) -> List[Path]:
        """
        Discover all skill files in skills directory.

        Returns:
            List of paths to SKILL.md files
        """
        skill_files = []

        # Pattern 1: skills/skill-name/SKILL.md
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / 'SKILL.md'
                if skill_file.exists():
                    skill_files.append(skill_file)

        # Pattern 2: skills/SKILL_NAME.md (flat structure)
        for skill_file in self.skills_dir.glob('*.md'):
            if skill_file.name.upper() != 'README.MD':
                skill_files.append(skill_file)

        return skill_files

    def load_skill(self, skill_path: Path, level: LoadLevel = LoadLevel.FRONTMATTER) -> Skill:
        """
        Load skill to specified level.

        Args:
            skill_path: Path to SKILL.md file
            level: Load level (FRONTMATTER, SKILL_BODY, or REFERENCES)

        Returns:
            Skill object loaded to specified level
        """
        # Always load metadata first
        metadata = self._load_metadata(skill_path)
        skill = Skill(metadata=metadata, loaded_level=LoadLevel.FRONTMATTER)

        # Load additional levels if requested
        if level.value >= LoadLevel.SKILL_BODY.value:
            skill = self._load_skill_body(skill, skill_path)

        if level.value >= LoadLevel.REFERENCES.value:
            skill = self._load_references(skill)

        return skill

    def upgrade_skill_load(self, skill: Skill, level: LoadLevel) -> Skill:
        """
        Upgrade skill to higher load level.

        Args:
            skill: Existing skill instance
            level: Target load level

        Returns:
            Skill upgraded to target level
        """
        if skill.is_loaded(level):
            return skill  # Already loaded to this level

        if level.value >= LoadLevel.SKILL_BODY.value and skill.content is None:
            skill = self._load_skill_body(skill, skill.metadata.skill_file)

        if level.value >= LoadLevel.REFERENCES.value and skill.references is None:
            skill = self._load_references(skill)

        return skill

    def _load_metadata(self, skill_path: Path) -> SkillMetadata:
        """
        Load only frontmatter metadata (~50 tokens).

        Args:
            skill_path: Path to SKILL.md

        Returns:
            SkillMetadata object
        """
        if not skill_path.exists():
            raise SkillLoadError(f"Skill file not found: {skill_path}")

        content = skill_path.read_text(encoding='utf-8')

        # Extract frontmatter
        frontmatter = self._extract_frontmatter(content)
        if not frontmatter:
            raise SkillLoadError(f"No frontmatter found in {skill_path}")

        # Validate required fields
        required_fields = ['name', 'description', 'skill-type']
        missing = [f for f in required_fields if f not in frontmatter]
        if missing:
            raise SkillLoadError(f"Missing required frontmatter fields: {missing}")

        # Create metadata
        return SkillMetadata.from_frontmatter(frontmatter, skill_path)

    def _load_skill_body(self, skill: Skill, skill_path: Path) -> Skill:
        """
        Load full SKILL.md body (~500 lines).

        Args:
            skill: Existing skill with metadata
            skill_path: Path to SKILL.md

        Returns:
            Skill with content loaded
        """
        content = skill_path.read_text(encoding='utf-8')

        # Remove frontmatter to get just the body
        body = self._extract_body(content)

        # Parse sections
        sections = self._parse_sections(body)

        # Extract examples
        examples = self._extract_examples(body)

        # Create content object
        skill_content = SkillContent(
            metadata=skill.metadata,
            body=body,
            sections=sections,
            examples=examples
        )

        skill.content = skill_content
        skill.loaded_level = LoadLevel.SKILL_BODY

        return skill

    def _load_references(self, skill: Skill) -> Skill:
        """
        Load all reference files (unlimited size).

        Args:
            skill: Existing skill with content

        Returns:
            Skill with references loaded
        """
        references = {}

        if skill.metadata.references_dir and skill.metadata.references_dir.exists():
            # Load all files in references/ directory
            for ref_file in skill.metadata.references_dir.rglob('*'):
                if ref_file.is_file():
                    relative_path = ref_file.relative_to(skill.metadata.references_dir)
                    try:
                        content = ref_file.read_text(encoding='utf-8')
                        references[str(relative_path)] = content
                    except Exception as e:
                        print(f"Warning: Failed to load reference {ref_file}: {e}")

        skill.references = SkillReferences(
            skill_name=skill.metadata.name,
            references=references
        )
        skill.loaded_level = LoadLevel.REFERENCES

        return skill

    def _extract_frontmatter(self, content: str) -> Optional[Dict]:
        """
        Extract YAML frontmatter from markdown.

        Args:
            content: Full markdown content

        Returns:
            Parsed frontmatter dict or None
        """
        # Match frontmatter between --- delimiters
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)

        if not match:
            return None

        frontmatter_yaml = match.group(1)
        try:
            return yaml.safe_load(frontmatter_yaml)
        except yaml.YAMLError as e:
            raise SkillLoadError(f"Invalid YAML in frontmatter: {e}")

    def _extract_body(self, content: str) -> str:
        """
        Extract body content (everything after frontmatter).

        Args:
            content: Full markdown content

        Returns:
            Body content without frontmatter
        """
        # Remove frontmatter
        pattern = r'^---\s*\n.*?\n---\s*\n'
        body = re.sub(pattern, '', content, count=1, flags=re.DOTALL)
        return body.strip()

    def _parse_sections(self, body: str) -> Dict[str, str]:
        """
        Parse markdown sections (H1 and H2 headers).

        Args:
            body: Markdown body content

        Returns:
            Dictionary mapping section names to content
        """
        sections = {}
        current_section = None
        current_content = []

        for line in body.split('\n'):
            # Check for headers
            if line.startswith('# ') or line.startswith('## '):
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()

                # Start new section
                current_section = line.lstrip('#').strip()
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    def _extract_examples(self, body: str) -> List[str]:
        """
        Extract code examples from markdown.

        Args:
            body: Markdown body content

        Returns:
            List of code examples
        """
        examples = []

        # Match code blocks (``` delimited)
        pattern = r'```[\w]*\n(.*?)\n```'
        matches = re.findall(pattern, body, re.DOTALL)

        for match in matches:
            examples.append(match.strip())

        return examples

    def get_skill_size_estimate(self, skill_path: Path) -> Dict[str, int]:
        """
        Estimate token sizes for each load level.

        Args:
            skill_path: Path to SKILL.md

        Returns:
            Dictionary with estimates for each level
        """
        estimates = {
            'frontmatter': 50,
            'skill_body': 0,
            'references': 0,
        }

        if not skill_path.exists():
            return estimates

        # Get full file size
        content = skill_path.read_text(encoding='utf-8')
        # Rough estimate: 1 token ≈ 4 characters
        estimates['skill_body'] = len(content) // 4

        # Get references size
        references_dir = skill_path.parent / 'references'
        if references_dir.exists():
            total_chars = 0
            for ref_file in references_dir.rglob('*'):
                if ref_file.is_file():
                    total_chars += ref_file.stat().st_size
            estimates['references'] = total_chars // 4

        return estimates
