#!/usr/bin/env python3
"""
Deep Shannon Plugin Audit - Comprehensive Cross-Reference Verification
"""

import re
from pathlib import Path
from collections import defaultdict

class DeepAuditor:
    def __init__(self, root_dir="."):
        self.root = Path(root_dir)
        self.issues = []
        self.warnings = []

    def get_all_skills(self):
        """Get list of all skill names"""
        skills_dir = self.root / "skills"
        if not skills_dir.exists():
            return []
        return [d.name for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]

    def get_all_agents(self):
        """Get list of all agent names"""
        agents_dir = self.root / "agents"
        if not agents_dir.exists():
            return []
        return [f.stem for f in agents_dir.glob("*.md")]

    def get_all_commands(self):
        """Get list of all command names"""
        commands_dir = self.root / "commands"
        if not commands_dir.exists():
            return []
        return [f.stem for f in commands_dir.glob("*.md")]

    def check_skill_references_in_file(self, filepath, valid_skills):
        """Check skill references in a single file"""
        with open(filepath) as f:
            content = f.read()

        # Pattern 1: Skill tool invocations
        skill_tool_pattern = r'Skill\s*\(\s*skill\s*=\s*["\']([^"\']+)["\']\s*\)'
        matches = re.finditer(skill_tool_pattern, content, re.MULTILINE)
        for match in matches:
            skill_name = match.group(1)
            if skill_name not in valid_skills:
                self.issues.append(f"{filepath.name}: References non-existent skill '{skill_name}' via Skill tool")

        # Pattern 2: Slash command style references
        slash_pattern = r'/shannon-plugin:([a-z-]+)'
        matches = re.finditer(slash_pattern, content)
        for match in matches:
            skill_name = match.group(1)
            # Check if it's a skill (skills use hyphens, commands use sh_ prefix)
            if '-' in skill_name and not skill_name.startswith('sh_') and skill_name not in valid_skills:
                # Could be a skill reference
                if skill_name not in self.get_all_commands():
                    self.warnings.append(f"{filepath.name}: References '{skill_name}' which is neither a skill nor command")

        # Pattern 3: @skill references (documentation style)
        at_skill_pattern = r'@skill\s+([a-z-]+)'
        matches = re.finditer(at_skill_pattern, content)
        for match in matches:
            skill_name = match.group(1)
            if skill_name not in valid_skills:
                self.warnings.append(f"{filepath.name}: Documentation references non-existent skill '{skill_name}'")

        # Pattern 4: skills/ directory references
        skills_path_pattern = r'skills/([a-z-]+)/'
        matches = re.finditer(skills_path_pattern, content)
        for match in matches:
            skill_name = match.group(1)
            if skill_name not in valid_skills:
                self.issues.append(f"{filepath.name}: References non-existent skill path 'skills/{skill_name}/'")

    def check_agent_references_in_file(self, filepath, valid_agents):
        """Check agent references in a single file"""
        with open(filepath) as f:
            content = f.read()

        # Pattern 1: Task tool with subagent_type
        agent_pattern = r'Task\s*\([^)]*subagent_type\s*=\s*["\']([A-Z_]+)["\']\s*[^)]*\)'
        matches = re.finditer(agent_pattern, content, re.DOTALL)
        for match in matches:
            agent_name = match.group(1)
            if agent_name not in valid_agents:
                self.issues.append(f"{filepath.name}: References non-existent agent '{agent_name}' via Task tool")

        # Pattern 2: Agent file path references
        agent_path_pattern = r'agents/([A-Z_]+)\.md'
        matches = re.finditer(agent_path_pattern, content)
        for match in matches:
            agent_name = match.group(1)
            if agent_name not in valid_agents:
                self.issues.append(f"{filepath.name}: References non-existent agent file 'agents/{agent_name}.md'")

    def check_command_references_in_file(self, filepath, valid_commands):
        """Check command references in a single file"""
        with open(filepath) as f:
            content = f.read()

        # Pattern: /command_name or /shannon-plugin:command_name
        command_patterns = [
            r'/(sh_[a-z_]+)',
            r'/shannon-plugin:(sh_[a-z_]+)',
            r'/shannon_prime',
            r'/shannon-plugin:shannon_prime'
        ]

        for pattern in command_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                cmd_name = match.group(1) if match.lastindex else 'shannon_prime'
                if cmd_name not in valid_commands:
                    self.warnings.append(f"{filepath.name}: References non-existent command '{cmd_name}'")

    def check_mcp_references(self):
        """Check if MCP references are consistent"""
        print("\n📋 Checking MCP references...")

        # Common MCP names that should be referenced
        expected_mcps = ['serena', 'sequential-thinking', 'puppeteer', 'context7']

        # Check if skills/mcp-discovery exists and has proper mapping
        mcp_skill = self.root / "skills" / "mcp-discovery"
        if not mcp_skill.exists():
            self.warnings.append("mcp-discovery skill not found")
            return

        # Check for domain-mcp-matrix.json
        matrix_file = mcp_skill / "mappings" / "domain-mcp-matrix.json"
        if not matrix_file.exists():
            self.warnings.append("MCP domain matrix file not found at skills/mcp-discovery/mappings/domain-mcp-matrix.json")

    def check_readme_consistency(self):
        """Check if README matches actual component counts"""
        print("\n📋 Checking README consistency...")

        readme = self.root / "README.md"
        if not readme.exists():
            self.warnings.append("README.md not found")
            return

        with open(readme) as f:
            content = f.read()

        actual_counts = {
            'commands': len(self.get_all_commands()),
            'skills': len(self.get_all_skills()),
            'agents': len(self.get_all_agents())
        }

        # Look for count references in README
        # Common patterns: "14 commands", "17 skills", "24 agents"
        for component, count in actual_counts.items():
            # Check if README mentions the correct count
            patterns = [
                rf'\b{count}\s+{component}\b',
                rf'{component}\s*\(\s*{count}\s*\)',
                rf'{count}\s+total\s+{component}',
            ]

            found = False
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    found = True
                    break

            if not found:
                self.warnings.append(f"README may not mention correct {component} count ({count})")

    def run_deep_audit(self):
        """Run comprehensive deep audit"""
        print("🔍 Starting Deep Cross-Reference Audit")
        print("=" * 60)

        valid_skills = self.get_all_skills()
        valid_agents = self.get_all_agents()
        valid_commands = self.get_all_commands()

        print(f"\n✓ Found {len(valid_commands)} commands")
        print(f"✓ Found {len(valid_skills)} skills")
        print(f"✓ Found {len(valid_agents)} agents")

        # Check commands for skill/agent references
        print("\n📋 Checking command files for references...")
        commands_dir = self.root / "commands"
        for cmd_file in commands_dir.glob("*.md"):
            self.check_skill_references_in_file(cmd_file, valid_skills)
            self.check_agent_references_in_file(cmd_file, valid_agents)

        # Check skills for skill/agent references
        print("\n📋 Checking skill files for references...")
        for skill_name in valid_skills:
            skill_file = self.root / "skills" / skill_name / "SKILL.md"
            if skill_file.exists():
                self.check_skill_references_in_file(skill_file, valid_skills)
                self.check_agent_references_in_file(skill_file, valid_agents)

        # Check agents for skill/agent references
        print("\n📋 Checking agent files for references...")
        agents_dir = self.root / "agents"
        for agent_file in agents_dir.glob("*.md"):
            self.check_skill_references_in_file(agent_file, valid_skills)
            self.check_agent_references_in_file(agent_file, valid_agents)

        # Check README
        print("\n📋 Checking README for command references...")
        readme = self.root / "README.md"
        if readme.exists():
            self.check_command_references_in_file(readme, valid_commands)

        # Additional checks
        self.check_mcp_references()
        self.check_readme_consistency()

        # Print results
        print("\n" + "=" * 60)
        print("📊 DEEP AUDIT RESULTS")
        print("=" * 60)

        if self.issues:
            print("\n❌ Critical Issues:")
            for issue in self.issues:
                print(f"  {issue}")
        else:
            print("\n✅ No critical issues found!")

        if self.warnings:
            print("\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  {warning}")
        else:
            print("\n✅ No warnings!")

        print("\n" + "=" * 60)
        print(f"Summary: {len(self.issues)} critical issues, {len(self.warnings)} warnings")
        print("=" * 60)

        return len(self.issues) == 0

if __name__ == "__main__":
    auditor = DeepAuditor()
    success = auditor.run_deep_audit()
    exit(0 if success else 1)
