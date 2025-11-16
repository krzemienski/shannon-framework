"""
Shannon Skills Framework - Discovery Engine

The DiscoveryEngine automatically discovers skills from multiple sources:
1. Built-in skills (skills/built-in/) - Core Shannon skills
2. Project skills (.shannon/skills/) - Project-specific custom skills
3. User global skills (~/.shannon/skills/) - User's custom skills
4. package.json scripts - Converted to executable script skills
5. Makefile targets - Converted to executable script skills
6. MCP servers - Tools from connected MCP servers
7. Memory MCP - Cached discoveries from previous runs

Features:
- Priority-based discovery (built-in > project > user > package.json > Makefile > MCP)
- Automatic skill generation for scripts and build tools
- Graceful error handling for missing/invalid sources
- Caching support for MCP tool discovery
- Comprehensive logging for debugging discovery issues

Usage:
    registry = SkillRegistry(schema_path=Path("schemas/skill.schema.json"))
    loader = SkillLoader(registry)
    engine = DiscoveryEngine(registry, loader)

    # Discover all skills
    skills = await engine.discover_all(project_root=Path("/path/to/project"))

    # Discover from specific sources
    builtin = await engine.discover_built_in()
    project = await engine.discover_project_skills(Path("/path/to/project"))
    npm = await engine.discover_from_package_json(Path("/path/to/project"))
"""

import asyncio
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
import logging

from shannon.skills.models import (
    Skill, Execution, ExecutionType, Parameter,
    SkillMetadata, Hooks
)
from shannon.skills.registry import SkillRegistry
from shannon.skills.loader import SkillLoader, SkillLoadError

logger = logging.getLogger(__name__)


class DiscoveryError(Exception):
    """Base exception for discovery errors"""
    pass


class SourceDiscoveryError(DiscoveryError):
    """Raised when a specific discovery source fails"""
    pass


class DiscoveryEngine:
    """
    Automatic skill discovery from multiple sources.

    The DiscoveryEngine scans various locations and formats to find
    executable skills that can be registered in Shannon. It handles:

    1. YAML/JSON skill definitions (via SkillLoader)
    2. package.json npm/yarn scripts
    3. Makefile targets
    4. MCP server tools
    5. Cached discoveries

    Discovery follows a priority order to handle conflicts:
    - Built-in skills have highest priority
    - Project-local skills override user-global
    - Explicit skill definitions override auto-generated

    Thread Safety:
        Discovery operations are async-safe and can be called
        concurrently. Registration is handled by SkillRegistry
        which provides thread-safe operations.
    """

    # Built-in skills directory (relative to package root)
    BUILTIN_SKILLS_DIR = Path(__file__).parent.parent.parent.parent / "skills" / "built-in"

    # User global skills directory
    USER_SKILLS_DIR = Path.home() / ".shannon" / "skills"

    # Project skills subdirectory
    PROJECT_SKILLS_SUBDIR = ".shannon/skills"

    # Cache directory for MCP discoveries
    CACHE_DIR = Path.home() / ".shannon" / "cache"

    def __init__(self, registry: SkillRegistry, loader: SkillLoader):
        """
        Initialize the discovery engine.

        Args:
            registry: SkillRegistry for managing discovered skills
            loader: SkillLoader for loading YAML/JSON skill files

        Example:
            registry = SkillRegistry(schema_path=Path("schemas/skill.schema.json"))
            loader = SkillLoader(registry)
            engine = DiscoveryEngine(registry, loader)
        """
        self.registry = registry
        self.loader = loader

        # Track discovered skill names to handle conflicts
        self._discovered_names: Set[str] = set()

        # Statistics for reporting
        self._stats = {
            'builtin': 0,
            'project': 0,
            'user': 0,
            'package_json': 0,
            'makefile': 0,
            'mcp': 0,
            'memory': 0,
            'failed': 0,
            'conflicts': 0
        }

        logger.info("DiscoveryEngine initialized")

    async def discover_all(
        self,
        project_root: Path,
        include_mcp: bool = False
    ) -> List[Skill]:
        """
        Discover skills from all available sources.

        This is the main entry point for comprehensive skill discovery.
        It follows priority order to handle conflicts:
        1. Built-in skills (highest priority)
        2. Project-local skills
        3. User-global skills
        4. package.json scripts
        5. Makefile targets
        6. MCP servers (if enabled)

        Args:
            project_root: Path to project root directory
            include_mcp: Whether to discover from MCP servers (default: False)

        Returns:
            List of all discovered skills (registered in registry)

        Raises:
            DiscoveryError: If critical discovery errors occur

        Example:
            skills = await engine.discover_all(
                project_root=Path("/path/to/project"),
                include_mcp=True
            )
            print(f"Discovered {len(skills)} skills")
        """
        logger.info(f"Starting comprehensive skill discovery for {project_root}")

        all_skills: List[Skill] = []
        self._discovered_names.clear()
        self._reset_stats()

        # 1. Built-in skills (highest priority)
        logger.info("Phase 1/7: Discovering built-in skills")
        try:
            builtin_skills = await self.discover_built_in()
            all_skills.extend(builtin_skills)
            self._stats['builtin'] = len(builtin_skills)
            logger.info(f"✓ Discovered {len(builtin_skills)} built-in skills")
        except Exception as e:
            logger.error(f"Failed to discover built-in skills: {e}")
            self._stats['failed'] += 1

        # 2. Project-local skills
        logger.info("Phase 2/7: Discovering project-local skills")
        try:
            project_skills = await self.discover_project_skills(project_root)
            all_skills.extend(project_skills)
            self._stats['project'] = len(project_skills)
            logger.info(f"✓ Discovered {len(project_skills)} project skills")
        except Exception as e:
            logger.warning(f"Project skills discovery skipped: {e}")

        # 3. User-global skills
        logger.info("Phase 3/7: Discovering user-global skills")
        try:
            user_skills = await self.discover_user_skills()
            all_skills.extend(user_skills)
            self._stats['user'] = len(user_skills)
            logger.info(f"✓ Discovered {len(user_skills)} user-global skills")
        except Exception as e:
            logger.warning(f"User skills discovery skipped: {e}")

        # 4. package.json scripts
        logger.info("Phase 4/7: Discovering package.json scripts")
        try:
            npm_skills = await self.discover_from_package_json(project_root)
            all_skills.extend(npm_skills)
            self._stats['package_json'] = len(npm_skills)
            logger.info(f"✓ Discovered {len(npm_skills)} npm/yarn scripts")
        except Exception as e:
            logger.debug(f"package.json discovery skipped: {e}")

        # 5. Makefile targets
        logger.info("Phase 5/7: Discovering Makefile targets")
        try:
            make_skills = await self.discover_from_makefile(project_root)
            all_skills.extend(make_skills)
            self._stats['makefile'] = len(make_skills)
            logger.info(f"✓ Discovered {len(make_skills)} Makefile targets")
        except Exception as e:
            logger.debug(f"Makefile discovery skipped: {e}")

        # 6. MCP servers (optional)
        if include_mcp:
            logger.info("Phase 6/7: Discovering MCP server tools")
            try:
                mcp_skills = await self.discover_from_mcps()
                all_skills.extend(mcp_skills)
                self._stats['mcp'] = len(mcp_skills)
                logger.info(f"✓ Discovered {len(mcp_skills)} MCP tools")
            except Exception as e:
                logger.warning(f"MCP discovery skipped: {e}")
        else:
            logger.info("Phase 6/7: Skipping MCP discovery (not enabled)")

        # 7. Memory/cache (future enhancement)
        logger.info("Phase 7/7: Checking cached discoveries")
        # TODO: Implement memory MCP cache loading
        logger.debug("Memory cache not yet implemented")

        # Log discovery summary
        self._log_discovery_summary()

        return all_skills

    async def discover_built_in(self) -> List[Skill]:
        """
        Discover and load built-in skills.

        Built-in skills are core Shannon skills shipped with the framework.
        They are located in the skills/built-in/ directory relative to
        the package root.

        Returns:
            List of loaded built-in skills

        Raises:
            SourceDiscoveryError: If built-in skills directory doesn't exist

        Example:
            builtin = await engine.discover_built_in()
        """
        logger.info(f"Discovering built-in skills from {self.BUILTIN_SKILLS_DIR}")

        if not self.BUILTIN_SKILLS_DIR.exists():
            error_msg = f"Built-in skills directory not found: {self.BUILTIN_SKILLS_DIR}"
            logger.error(error_msg)
            raise SourceDiscoveryError(error_msg)

        if not self.BUILTIN_SKILLS_DIR.is_dir():
            error_msg = f"Built-in skills path is not a directory: {self.BUILTIN_SKILLS_DIR}"
            logger.error(error_msg)
            raise SourceDiscoveryError(error_msg)

        # Load all skills from built-in directory
        skills = await self.loader.load_from_directory(
            self.BUILTIN_SKILLS_DIR,
            recursive=False,  # Built-in skills are flat
            register=True
        )

        # Track discovered names
        for skill in skills:
            self._discovered_names.add(skill.name)

        logger.info(f"Loaded {len(skills)} built-in skills")
        return skills

    async def discover_project_skills(self, project_root: Path) -> List[Skill]:
        """
        Discover project-local skills.

        Project skills are located in .shannon/skills/ within the
        project root directory. These override user-global skills
        with the same name.

        Args:
            project_root: Path to project root directory

        Returns:
            List of loaded project skills (may be empty if directory doesn't exist)

        Example:
            project_skills = await engine.discover_project_skills(
                Path("/path/to/project")
            )
        """
        project_skills_dir = project_root / self.PROJECT_SKILLS_SUBDIR

        logger.info(f"Discovering project skills from {project_skills_dir}")

        # Skip if directory doesn't exist
        if not project_skills_dir.exists():
            logger.debug(f"Project skills directory not found: {project_skills_dir}")
            return []

        if not project_skills_dir.is_dir():
            logger.warning(f"Project skills path is not a directory: {project_skills_dir}")
            return []

        # Load all skills from project directory
        skills = await self.loader.load_from_directory(
            project_skills_dir,
            recursive=True,  # Allow subdirectories in project skills
            register=True
        )

        # Track discovered names
        for skill in skills:
            self._discovered_names.add(skill.name)

        logger.info(f"Loaded {len(skills)} project skills")
        return skills

    async def discover_user_skills(self) -> List[Skill]:
        """
        Discover user-global skills.

        User-global skills are located in ~/.shannon/skills/ and are
        available across all projects for the current user.

        Returns:
            List of loaded user-global skills (may be empty if directory doesn't exist)

        Example:
            user_skills = await engine.discover_user_skills()
        """
        logger.info(f"Discovering user-global skills from {self.USER_SKILLS_DIR}")

        # Skip if directory doesn't exist
        if not self.USER_SKILLS_DIR.exists():
            logger.debug(f"User skills directory not found: {self.USER_SKILLS_DIR}")
            return []

        if not self.USER_SKILLS_DIR.is_dir():
            logger.warning(f"User skills path is not a directory: {self.USER_SKILLS_DIR}")
            return []

        # Load all skills from user directory
        skills = await self.loader.load_from_directory(
            self.USER_SKILLS_DIR,
            recursive=True,
            register=True
        )

        # Track discovered names and handle conflicts
        for skill in skills:
            if skill.name in self._discovered_names:
                logger.warning(
                    f"User skill '{skill.name}' conflicts with existing skill "
                    f"(already registered)"
                )
                self._stats['conflicts'] += 1
            else:
                self._discovered_names.add(skill.name)

        logger.info(f"Loaded {len(skills)} user-global skills")
        return skills

    async def discover_from_package_json(self, project_root: Path) -> List[Skill]:
        """
        Discover and convert package.json scripts to skills.

        Each npm/yarn script is converted to an executable skill:
        - name: npm_{script_name}
        - execution: type=script, script="npm run {script_name}"
        - category: build-tools
        - auto_generated: true

        Args:
            project_root: Path to project root directory

        Returns:
            List of generated script skills (may be empty if no package.json)

        Example:
            npm_skills = await engine.discover_from_package_json(
                Path("/path/to/project")
            )
        """
        package_json_path = project_root / "package.json"

        logger.info(f"Discovering package.json scripts from {package_json_path}")

        # Skip if package.json doesn't exist
        if not package_json_path.exists():
            logger.debug(f"package.json not found: {package_json_path}")
            return []

        try:
            # Parse package.json
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)

            # Extract scripts
            scripts = package_data.get('scripts', {})

            if not scripts:
                logger.debug("No scripts found in package.json")
                return []

            logger.info(f"Found {len(scripts)} scripts in package.json")

            # Generate skills for each script
            skills = []
            for script_name, script_command in scripts.items():
                skill = self._create_npm_skill(script_name, script_command)

                # Check for conflicts
                if skill.name in self._discovered_names:
                    logger.warning(
                        f"npm script '{skill.name}' conflicts with existing skill "
                        f"(skipping)"
                    )
                    self._stats['conflicts'] += 1
                    continue

                # Register skill
                try:
                    await self.registry.register(skill)
                    skills.append(skill)
                    self._discovered_names.add(skill.name)
                    logger.debug(f"Registered npm skill: {skill.name}")
                except Exception as e:
                    logger.warning(f"Failed to register npm skill '{skill.name}': {e}")
                    self._stats['failed'] += 1

            logger.info(f"Created {len(skills)} npm script skills")
            return skills

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in package.json: {e}")
            raise SourceDiscoveryError(f"Invalid package.json: {e}")
        except Exception as e:
            logger.error(f"Error reading package.json: {e}")
            raise SourceDiscoveryError(f"Failed to read package.json: {e}")

    async def discover_from_makefile(self, project_root: Path) -> List[Skill]:
        """
        Discover and convert Makefile targets to skills.

        Each Makefile target is converted to an executable skill:
        - name: make_{target_name}
        - execution: type=script, script="make {target_name}"
        - category: build-tools
        - auto_generated: true

        Args:
            project_root: Path to project root directory

        Returns:
            List of generated Makefile skills (may be empty if no Makefile)

        Example:
            make_skills = await engine.discover_from_makefile(
                Path("/path/to/project")
            )
        """
        # Try common Makefile names
        makefile_names = ['Makefile', 'makefile', 'GNUmakefile']
        makefile_path = None

        for name in makefile_names:
            path = project_root / name
            if path.exists():
                makefile_path = path
                break

        logger.info(f"Discovering Makefile targets from {makefile_path or 'not found'}")

        # Skip if no Makefile found
        if not makefile_path:
            logger.debug("No Makefile found in project root")
            return []

        try:
            # Parse Makefile to extract targets
            targets = self._parse_makefile(makefile_path)

            if not targets:
                logger.debug("No targets found in Makefile")
                return []

            logger.info(f"Found {len(targets)} targets in Makefile")

            # Generate skills for each target
            skills = []
            for target_name, target_desc in targets.items():
                skill = self._create_make_skill(target_name, target_desc)

                # Check for conflicts
                if skill.name in self._discovered_names:
                    logger.warning(
                        f"Make target '{skill.name}' conflicts with existing skill "
                        f"(skipping)"
                    )
                    self._stats['conflicts'] += 1
                    continue

                # Register skill
                try:
                    await self.registry.register(skill)
                    skills.append(skill)
                    self._discovered_names.add(skill.name)
                    logger.debug(f"Registered make skill: {skill.name}")
                except Exception as e:
                    logger.warning(f"Failed to register make skill '{skill.name}': {e}")
                    self._stats['failed'] += 1

            logger.info(f"Created {len(skills)} Makefile skills")
            return skills

        except Exception as e:
            logger.error(f"Error parsing Makefile: {e}")
            raise SourceDiscoveryError(f"Failed to parse Makefile: {e}")

    async def discover_from_mcps(self) -> List[Skill]:
        """
        Discover tools from connected MCP servers.

        This method queries all configured MCP servers for their
        available tools and converts them to skills. Each MCP tool
        becomes an executable skill with type=mcp.

        Returns:
            List of generated MCP skills

        Note:
            This is a placeholder implementation. Full MCP integration
            requires connection to the MCP client and tool discovery API.

        Example:
            mcp_skills = await engine.discover_from_mcps()
        """
        logger.warning("MCP discovery not yet fully implemented")

        # TODO: Implement MCP server discovery
        # 1. Query MCP client for connected servers
        # 2. For each server, list available tools
        # 3. Convert each tool to a skill:
        #    - name: mcp_{server}_{tool}
        #    - execution: type=mcp, mcp_server=server, mcp_tool=tool
        #    - parameters: from tool schema
        #    - category: tools

        return []

    def _create_npm_skill(self, script_name: str, script_command: str) -> Skill:
        """
        Create a skill from an npm script.

        Args:
            script_name: Name of the npm script
            script_command: The script command to execute

        Returns:
            Generated Skill instance
        """
        skill_name = f"npm_{script_name}"

        # Clean script command for description
        desc = script_command[:100] + "..." if len(script_command) > 100 else script_command

        return Skill(
            name=skill_name,
            version="1.0.0",
            description=f"Execute npm script: {script_name} ({desc})",
            category="utility",  # Auto-generated build tool skills use utility category
            parameters=[
                Parameter(
                    name="working_dir",
                    type="string",
                    required=False,
                    description="Working directory to execute script in"
                )
            ],
            execution=Execution(
                type=ExecutionType.SCRIPT,
                script=f"npm run {script_name}",
                timeout=600,  # 10 minutes for build scripts
                retry=0
            ),
            metadata=SkillMetadata(
                author="Shannon DiscoveryEngine",
                auto_generated=True,
                tags=["npm", "build", "scripts", script_name]
            )
        )

    def _create_make_skill(self, target_name: str, description: str) -> Skill:
        """
        Create a skill from a Makefile target.

        Args:
            target_name: Name of the make target
            description: Description from Makefile comments (if any)

        Returns:
            Generated Skill instance
        """
        skill_name = f"make_{target_name}"

        # Use provided description or generate one
        # Ensure minimum length for schema validation (at least 20 chars)
        if description:
            desc = description if len(description) >= 20 else f"{description} - Makefile target: {target_name}"
        else:
            desc = f"Execute Makefile target: {target_name}"

        return Skill(
            name=skill_name,
            version="1.0.0",
            description=desc,
            category="utility",  # Auto-generated build tool skills use utility category
            parameters=[
                Parameter(
                    name="working_dir",
                    type="string",
                    required=False,
                    description="Working directory to execute make in"
                )
            ],
            execution=Execution(
                type=ExecutionType.SCRIPT,
                script=f"make {target_name}",
                timeout=600,  # 10 minutes for build targets
                retry=0
            ),
            metadata=SkillMetadata(
                author="Shannon DiscoveryEngine",
                auto_generated=True,
                tags=["make", "build", "targets", target_name]
            )
        )

    def _parse_makefile(self, makefile_path: Path) -> Dict[str, str]:
        """
        Parse Makefile to extract target names and descriptions.

        Extracts targets that:
        - Don't start with . (special targets)
        - Aren't variables
        - Are actual build targets

        Also attempts to extract descriptions from comments above targets.

        Args:
            makefile_path: Path to Makefile

        Returns:
            Dictionary mapping target names to descriptions
        """
        targets: Dict[str, str] = {}

        try:
            with open(makefile_path, 'r') as f:
                lines = f.readlines()

            # Regular expression for target definitions
            # Matches: target_name: [dependencies]
            target_pattern = re.compile(r'^([a-zA-Z0-9_-]+)\s*:(?!\=)')

            # Track previous comment for description
            prev_comment = ""

            for line in lines:
                stripped = line.strip()

                # Skip empty lines
                if not stripped:
                    prev_comment = ""
                    continue

                # Capture comments as potential descriptions
                if stripped.startswith('#'):
                    comment_text = stripped[1:].strip()
                    # Skip comment blocks that look like section headers
                    if not comment_text.isupper():
                        prev_comment = comment_text
                    continue

                # Match target definitions
                match = target_pattern.match(stripped)
                if match:
                    target_name = match.group(1)

                    # Skip special targets
                    if target_name.startswith('.'):
                        continue

                    # Skip PHONY declarations
                    if target_name == 'PHONY':
                        continue

                    # Add target with description
                    targets[target_name] = prev_comment or f"Makefile target: {target_name}"
                    prev_comment = ""
                else:
                    # Clear comment if line isn't a target
                    if not stripped.startswith('\t'):
                        prev_comment = ""

            logger.debug(f"Parsed {len(targets)} targets from Makefile")
            return targets

        except Exception as e:
            logger.error(f"Error parsing Makefile: {e}")
            return {}

    def _reset_stats(self):
        """Reset discovery statistics"""
        for key in self._stats:
            self._stats[key] = 0

    def _log_discovery_summary(self):
        """Log a summary of discovery results"""
        total_discovered = sum(
            self._stats[k] for k in
            ['builtin', 'project', 'user', 'package_json', 'makefile', 'mcp']
        )

        logger.info("=" * 60)
        logger.info("DISCOVERY SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total skills discovered: {total_discovered}")
        logger.info(f"  - Built-in skills: {self._stats['builtin']}")
        logger.info(f"  - Project skills: {self._stats['project']}")
        logger.info(f"  - User-global skills: {self._stats['user']}")
        logger.info(f"  - package.json scripts: {self._stats['package_json']}")
        logger.info(f"  - Makefile targets: {self._stats['makefile']}")
        logger.info(f"  - MCP tools: {self._stats['mcp']}")
        logger.info(f"Failed discoveries: {self._stats['failed']}")
        logger.info(f"Naming conflicts: {self._stats['conflicts']}")
        logger.info("=" * 60)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get discovery statistics.

        Returns:
            Dictionary with discovery statistics

        Example:
            stats = engine.get_statistics()
            print(f"Discovered {stats['total_discovered']} skills")
        """
        total = sum(
            self._stats[k] for k in
            ['builtin', 'project', 'user', 'package_json', 'makefile', 'mcp']
        )

        return {
            'total_discovered': total,
            'by_source': {
                'builtin': self._stats['builtin'],
                'project': self._stats['project'],
                'user_global': self._stats['user'],
                'package_json': self._stats['package_json'],
                'makefile': self._stats['makefile'],
                'mcp': self._stats['mcp'],
            },
            'failed': self._stats['failed'],
            'conflicts': self._stats['conflicts'],
            'unique_names': len(self._discovered_names)
        }

    def __repr__(self) -> str:
        """String representation of discovery engine"""
        total = sum(
            self._stats[k] for k in
            ['builtin', 'project', 'user', 'package_json', 'makefile', 'mcp']
        )
        return f"<DiscoveryEngine: {total} skills discovered>"
