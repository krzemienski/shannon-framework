#!/usr/bin/env python3
"""
Shannon Plugin Comprehensive Audit
Verifies all components are properly structured and cross-referenced
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

class PluginAuditor:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir)
        self.issues = []
        self.warnings = []
        self.info = []

    def log_issue(self, msg: str):
        self.issues.append(f"❌ {msg}")

    def log_warning(self, msg: str):
        self.warnings.append(f"⚠️  {msg}")

    def log_info(self, msg: str):
        self.info.append(f"ℹ️  {msg}")

    def extract_yaml_frontmatter(self, content: str) -> Dict:
        """Extract YAML frontmatter from markdown file"""
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return {}

        yaml_content = match.group(1)
        # Simple YAML parser for our needs
        result = {}
        for line in yaml_content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip()] = value.strip().strip('"').strip("'")
        return result

    def extract_skill_references(self, content: str) -> Set[str]:
        """Extract skill references from command/agent files"""
        # Look for patterns like: /shannon-plugin:skill-name, @skill skill-name, Skill(skill="name")
        patterns = [
            r'/shannon-plugin:([a-z-]+)',
            r'@skill\s+([a-z-]+)',
            r'Skill\(skill="([a-z-]+)"\)',
            r'skills/([a-z-]+)/',
        ]
        skills = set()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            skills.update(matches)
        return skills

    def extract_agent_references(self, content: str) -> Set[str]:
        """Extract agent references from command files"""
        # Look for patterns like: Task(subagent_type="AGENT_NAME")
        patterns = [
            r'Task\(subagent_type="([A-Z_]+)"\)',
            r'subagent_type:\s*"([A-Z_]+)"',
            r'agents/([A-Z_]+)\.md',
        ]
        agents = set()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            agents.update(matches)
        return agents

    def audit_plugin_json(self):
        """Audit plugin.json"""
        print("\n📋 Auditing plugin.json...")
        plugin_json = self.root / ".claude-plugin" / "plugin.json"

        if not plugin_json.exists():
            self.log_issue("plugin.json not found")
            return

        with open(plugin_json) as f:
            data = json.load(f)

        required_fields = ["name", "version", "description", "author"]
        for field in required_fields:
            if field not in data:
                self.log_issue(f"plugin.json missing required field: {field}")

        if data.get("name") != "shannon-plugin":
            self.log_issue(f"plugin.json name is '{data.get('name')}', expected 'shannon-plugin'")

        self.log_info(f"Plugin name: {data.get('name')}")
        self.log_info(f"Plugin version: {data.get('version')}")

    def audit_marketplace_json(self):
        """Audit marketplace.json"""
        print("\n📋 Auditing marketplace.json...")
        marketplace_json = self.root / ".claude-plugin" / "marketplace.json"

        if not marketplace_json.exists():
            self.log_issue("marketplace.json not found")
            return

        with open(marketplace_json) as f:
            data = json.load(f)

        if data.get("name") != "shannon-framework":
            self.log_issue(f"marketplace.json name is '{data.get('name')}', expected 'shannon-framework'")

        plugins = data.get("plugins", [])
        if not plugins:
            self.log_issue("No plugins defined in marketplace.json")
        else:
            plugin = plugins[0]
            if plugin.get("name") != "shannon-plugin":
                self.log_issue(f"Plugin name in marketplace is '{plugin.get('name')}', expected 'shannon-plugin'")
            if plugin.get("source") != "./":
                self.log_warning(f"Plugin source is '{plugin.get('source')}', expected './'")

    def audit_commands(self) -> Tuple[List[str], Dict[str, str]]:
        """Audit all command files"""
        print("\n📋 Auditing commands...")
        commands_dir = self.root / "commands"

        if not commands_dir.exists():
            self.log_issue("commands/ directory not found")
            return [], {}

        command_files = list(commands_dir.glob("*.md"))
        command_names = []
        command_contents = {}

        for cmd_file in sorted(command_files):
            cmd_name = cmd_file.stem
            command_names.append(cmd_name)

            with open(cmd_file) as f:
                content = f.read()
                command_contents[cmd_name] = content

            # Check for YAML frontmatter
            frontmatter = self.extract_yaml_frontmatter(content)
            if not frontmatter:
                self.log_warning(f"Command {cmd_name} missing YAML frontmatter")
            else:
                if 'name' not in frontmatter:
                    self.log_warning(f"Command {cmd_name} frontmatter missing 'name' field")
                if 'description' not in frontmatter:
                    self.log_warning(f"Command {cmd_name} frontmatter missing 'description' field")

        self.log_info(f"Found {len(command_files)} commands")
        return command_names, command_contents

    def audit_skills(self) -> Tuple[List[str], Dict[str, str]]:
        """Audit all skill files"""
        print("\n📋 Auditing skills...")
        skills_dir = self.root / "skills"

        if not skills_dir.exists():
            self.log_issue("skills/ directory not found")
            return [], {}

        skill_files = list(skills_dir.glob("*/SKILL.md"))
        skill_names = []
        skill_contents = {}

        for skill_file in sorted(skill_files):
            skill_name = skill_file.parent.name
            skill_names.append(skill_name)

            with open(skill_file) as f:
                content = f.read()
                skill_contents[skill_name] = content

            # Check for YAML frontmatter
            frontmatter = self.extract_yaml_frontmatter(content)
            if not frontmatter:
                self.log_warning(f"Skill {skill_name} missing YAML frontmatter")
            else:
                if 'name' not in frontmatter:
                    self.log_warning(f"Skill {skill_name} frontmatter missing 'name' field")

        self.log_info(f"Found {len(skill_files)} skills")
        return skill_names, skill_contents

    def audit_agents(self) -> Tuple[List[str], Dict[str, str]]:
        """Audit all agent files"""
        print("\n📋 Auditing agents...")
        agents_dir = self.root / "agents"

        if not agents_dir.exists():
            self.log_issue("agents/ directory not found")
            return [], {}

        agent_files = list(agents_dir.glob("*.md"))
        agent_names = []
        agent_contents = {}

        for agent_file in sorted(agent_files):
            agent_name = agent_file.stem
            agent_names.append(agent_name)

            with open(agent_file) as f:
                content = f.read()
                agent_contents[agent_name] = content

            # Check for YAML frontmatter
            frontmatter = self.extract_yaml_frontmatter(content)
            if not frontmatter:
                self.log_warning(f"Agent {agent_name} missing YAML frontmatter")

        self.log_info(f"Found {len(agent_files)} agents")
        return agent_names, agent_contents

    def audit_hooks(self):
        """Audit hooks configuration"""
        print("\n📋 Auditing hooks...")
        hooks_json = self.root / "hooks" / "hooks.json"
        hooks_dir = self.root / "hooks"

        if not hooks_json.exists():
            self.log_warning("hooks/hooks.json not found")
            return

        with open(hooks_json) as f:
            data = json.load(f)

        hooks_config = data.get("hooks", {})
        hook_types = list(hooks_config.keys())

        self.log_info(f"Found {len(hook_types)} hook types: {', '.join(hook_types)}")

        # Check if hook scripts exist
        expected_scripts = {
            "user_prompt_submit.py",
            "precompact.py",
            "post_tool_use.py",
            "stop.py",
            "session_start.sh"
        }

        for script in expected_scripts:
            script_path = hooks_dir / script
            if not script_path.exists():
                self.log_issue(f"Hook script not found: {script}")
            elif not os.access(script_path, os.X_OK):
                self.log_warning(f"Hook script not executable: {script}")

    def audit_cross_references(self, command_contents, skill_names, agent_names):
        """Check cross-references between components"""
        print("\n📋 Auditing cross-references...")

        # Check skill references in commands
        for cmd_name, content in command_contents.items():
            referenced_skills = self.extract_skill_references(content)
            for skill in referenced_skills:
                if skill not in skill_names:
                    self.log_issue(f"Command {cmd_name} references non-existent skill: {skill}")

        # Check agent references in commands
        for cmd_name, content in command_contents.items():
            referenced_agents = self.extract_agent_references(content)
            for agent in referenced_agents:
                if agent not in agent_names:
                    self.log_issue(f"Command {cmd_name} references non-existent agent: {agent}")

    def audit_core_patterns(self):
        """Audit core pattern files"""
        print("\n📋 Auditing core patterns...")
        core_dir = self.root / "core"

        if not core_dir.exists():
            self.log_warning("core/ directory not found")
            return

        core_files = list(core_dir.glob("*.md"))
        self.log_info(f"Found {len(core_files)} core pattern files")

    def run_audit(self):
        """Run complete audit"""
        print("🔍 Starting Shannon Plugin Comprehensive Audit")
        print("=" * 60)

        self.audit_plugin_json()
        self.audit_marketplace_json()

        command_names, command_contents = self.audit_commands()
        skill_names, skill_contents = self.audit_skills()
        agent_names, agent_contents = self.audit_agents()

        self.audit_hooks()
        self.audit_core_patterns()

        self.audit_cross_references(command_contents, skill_names, agent_names)

        # Print results
        print("\n" + "=" * 60)
        print("📊 AUDIT RESULTS")
        print("=" * 60)

        if self.info:
            print("\n✅ Information:")
            for msg in self.info:
                print(f"  {msg}")

        if self.warnings:
            print("\n⚠️  Warnings:")
            for msg in self.warnings:
                print(f"  {msg}")

        if self.issues:
            print("\n❌ Issues:")
            for msg in self.issues:
                print(f"  {msg}")
        else:
            print("\n✅ No critical issues found!")

        print("\n" + "=" * 60)
        print(f"Summary: {len(self.issues)} issues, {len(self.warnings)} warnings")
        print("=" * 60)

        return len(self.issues) == 0

if __name__ == "__main__":
    auditor = PluginAuditor()
    success = auditor.run_audit()
    exit(0 if success else 1)
