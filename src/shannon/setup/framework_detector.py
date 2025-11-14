"""Detect and verify Shannon Framework installation.

This module provides robust detection and validation of Shannon Framework
installations across multiple possible locations including:
- Environment variable overrides
- Claude Code plugin directory
- Bundled distributions
- Development installations
- System-wide installations

The detector verifies framework completeness by checking:
- Plugin metadata presence
- Required skills availability
- Command directory structure
- Core framework files
"""

from pathlib import Path
import json
import os
from typing import Optional, Tuple, Dict, List


class FrameworkDetector:
    """Detect Shannon Framework in multiple locations with validation.

    Searches known installation locations in priority order and verifies
    framework completeness before returning paths.

    Priority order:
    1. SHANNON_FRAMEWORK_PATH environment variable
    2. Claude Code plugin directory (~/.claude/plugins/shannon)
    3. Bundled with CLI (src/shannon/bundled/shannon-framework)
    4. Development location (~/Desktop/shannon-framework)
    5. System installation (/usr/local/share/shannon-framework)

    Attributes:
        FRAMEWORK_LOCATIONS: List of lambda functions returning potential paths
        REQUIRED_SKILLS: Minimum number of skills expected (18 in full framework)
        REQUIRED_COMMANDS: Minimum number of commands expected (15 in full framework)

    Example:
        >>> detector = FrameworkDetector()
        >>> path = detector.find_framework()
        >>> if path:
        ...     is_valid, msg = detector.verify_framework(path)
        ...     print(f"Valid: {is_valid}, Message: {msg}")
    """

    # Expected minimums for framework validation
    REQUIRED_SKILLS = 15  # Allow some tolerance (18 total)
    REQUIRED_COMMANDS = 12  # Allow some tolerance (15 total)

    # Search locations in priority order
    FRAMEWORK_LOCATIONS = [
        # Environment variable (highest priority - allows user override)
        lambda: Path(os.getenv('SHANNON_FRAMEWORK_PATH', '')) if os.getenv('SHANNON_FRAMEWORK_PATH') else None,

        # Claude Code plugin directory (standard installation)
        lambda: Path.home() / '.claude' / 'plugins' / 'shannon',

        # Bundled with CLI (fallback for offline/airgapped systems)
        lambda: Path(__file__).parent.parent / 'bundled' / 'shannon-framework',

        # Development location (for contributors)
        lambda: Path.home() / 'Desktop' / 'shannon-framework',

        # System install (for multi-user systems)
        lambda: Path('/usr/local/share/shannon-framework'),
    ]

    @classmethod
    def find_framework(cls) -> Optional[Path]:
        """Search for Shannon Framework in known locations.

        Iterates through FRAMEWORK_LOCATIONS in priority order, checking
        each location for a valid Shannon Framework installation. Returns
        the first valid location found.

        Returns:
            Path to framework directory if found and valid, None otherwise.

        Note:
            Does basic validation (plugin.json exists) but does not perform
            full verification. Use verify_framework() for comprehensive checks.
        """
        for location_fn in cls.FRAMEWORK_LOCATIONS:
            try:
                path = location_fn()
                if path and path.exists():
                    # Quick validation: check for plugin metadata
                    plugin_json = path / '.claude-plugin' / 'plugin.json'
                    if plugin_json.exists():
                        return path
            except Exception:
                # Ignore errors in location functions (e.g., permission denied)
                continue

        return None

    @classmethod
    def verify_framework(cls, path: Path) -> Tuple[bool, str]:
        """Verify Shannon Framework is complete and functional.

        Performs comprehensive validation of framework installation including:
        - Plugin metadata presence and validity
        - Skills directory structure and content
        - Commands directory structure and content
        - Core framework files presence
        - Version information extraction

        Args:
            path: Path to potential Shannon Framework installation

        Returns:
            Tuple of (is_valid, message) where:
            - is_valid: True if all checks pass, False otherwise
            - message: Descriptive message about validation result

        Example:
            >>> path = Path('/path/to/shannon')
            >>> is_valid, msg = FrameworkDetector.verify_framework(path)
            >>> if not is_valid:
            ...     print(f"Invalid: {msg}")
        """
        # Check 1: Plugin metadata exists and is valid JSON
        plugin_json = path / '.claude-plugin' / 'plugin.json'
        if not plugin_json.exists():
            return False, "Missing .claude-plugin/plugin.json"

        try:
            with open(plugin_json) as f:
                plugin_data = json.load(f)
                version = plugin_data.get('version', 'unknown')
        except (json.JSONDecodeError, OSError) as e:
            return False, f"Invalid plugin.json: {e}"

        # Check 2: Skills directory exists and has content
        skills_dir = path / 'skills'
        if not skills_dir.exists():
            return False, "Missing skills directory"

        # Count skills by looking for SKILL.md files in subdirectories
        skills = list(skills_dir.glob('*/SKILL.md'))
        if len(skills) < cls.REQUIRED_SKILLS:
            return False, (
                f"Only {len(skills)} skills found (expected at least {cls.REQUIRED_SKILLS}). "
                "Framework may be incomplete."
            )

        # Check 3: Commands directory exists and has content
        commands_dir = path / 'commands'
        if not commands_dir.exists():
            return False, "Missing commands directory"

        # Count commands
        commands = list(commands_dir.glob('*.md'))
        if len(commands) < cls.REQUIRED_COMMANDS:
            return False, (
                f"Only {len(commands)} commands found (expected at least {cls.REQUIRED_COMMANDS}). "
                "Framework may be incomplete."
            )

        # Check 4: Core directory exists (optional but recommended)
        core_dir = path / 'core'
        if not core_dir.exists():
            # Warning, not error - core may be optional in some versions
            return True, (
                f"Shannon Framework {version} verified ({len(skills)} skills, {len(commands)} commands) "
                "but missing core directory (non-critical)"
            )

        # All checks passed
        return True, f"Shannon Framework {version} verified ({len(skills)} skills, {len(commands)} commands)"

    @classmethod
    def get_framework_info(cls, path: Path) -> Dict[str, any]:
        """Extract detailed information about a framework installation.

        Retrieves metadata and statistics about a Shannon Framework installation
        including version, skill count, command count, and directory structure.

        Args:
            path: Path to Shannon Framework installation

        Returns:
            Dictionary containing:
            - path: Absolute path to framework
            - version: Framework version from plugin.json
            - skills: List of available skills
            - commands: List of available commands
            - is_valid: Whether framework passes verification
            - validation_message: Result of verification

        Example:
            >>> info = FrameworkDetector.get_framework_info(Path('/path/to/shannon'))
            >>> print(f"Version: {info['version']}")
            >>> print(f"Skills: {len(info['skills'])}")
        """
        info = {
            'path': str(path.absolute()),
            'version': 'unknown',
            'skills': [],
            'commands': [],
            'is_valid': False,
            'validation_message': ''
        }

        # Get version from plugin.json
        plugin_json = path / '.claude-plugin' / 'plugin.json'
        if plugin_json.exists():
            try:
                with open(plugin_json) as f:
                    plugin_data = json.load(f)
                    info['version'] = plugin_data.get('version', 'unknown')
            except (json.JSONDecodeError, OSError):
                pass

        # Get skills
        skills_dir = path / 'skills'
        if skills_dir.exists():
            for skill_md in skills_dir.glob('*/SKILL.md'):
                skill_name = skill_md.parent.name
                info['skills'].append(skill_name)

        # Get commands
        commands_dir = path / 'commands'
        if commands_dir.exists():
            for cmd_md in commands_dir.glob('*.md'):
                cmd_name = cmd_md.stem
                info['commands'].append(cmd_name)

        # Run verification
        is_valid, message = cls.verify_framework(path)
        info['is_valid'] = is_valid
        info['validation_message'] = message

        return info

    @classmethod
    def search_all_locations(cls) -> List[Dict[str, any]]:
        """Search all known locations and return information about each.

        Useful for diagnostics and showing users all available installations.

        Returns:
            List of dictionaries, one per found installation, each containing:
            - location_name: Human-readable location description
            - path: Absolute path to framework
            - exists: Whether path exists
            - is_valid: Whether framework is valid (if exists)
            - info: Detailed framework info (if valid)

        Example:
            >>> for loc in FrameworkDetector.search_all_locations():
            ...     if loc['exists']:
            ...         print(f"{loc['location_name']}: {loc['path']}")
        """
        location_names = [
            "Environment Variable (SHANNON_FRAMEWORK_PATH)",
            "Claude Code Plugin Directory",
            "Bundled with CLI",
            "Development Location",
            "System Installation"
        ]

        results = []

        for location_fn, location_name in zip(cls.FRAMEWORK_LOCATIONS, location_names):
            try:
                path = location_fn()
                if path is None:
                    continue

                result = {
                    'location_name': location_name,
                    'path': str(path.absolute()) if path else None,
                    'exists': path.exists() if path else False,
                    'is_valid': False,
                    'info': None
                }

                if result['exists']:
                    info = cls.get_framework_info(path)
                    result['is_valid'] = info['is_valid']
                    result['info'] = info

                results.append(result)

            except Exception as e:
                # Include failed searches for diagnostics
                results.append({
                    'location_name': location_name,
                    'path': None,
                    'exists': False,
                    'is_valid': False,
                    'info': None,
                    'error': str(e)
                })

        return results
