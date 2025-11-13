#!/usr/bin/env python3
"""
Shannon v5.0 Complete System Validation
Validates: formats, references, dependencies, integration
"""

import os, sys, json, re
from pathlib import Path
from typing import List, Dict, Set

class ShannonValidator:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir)
        self.issues = []
        self.skills = set()
        self.commands = set()
        self.agents = set()

    def validate_all(self):
        """Run all validations"""
        print("🔍 Shannon v5.0 Complete System Validation\n")

        self.validate_plugin_config()
        self.validate_commands()
        self.validate_skills()
        self.validate_command_skill_mappings()
        self.validate_skill_dependencies()

        self.report_results()

    def validate_plugin_config(self):
        """Validate plugin configuration files"""
        print("📦 Validating plugin configuration...")

        # Check plugin.json
        plugin_file = self.root / ".claude-plugin/plugin.json"
        try:
            with open(plugin_file) as f:
                plugin = json.load(f)
                if plugin.get("name") != "shannon":
                    self.issues.append(f"plugin.json name should be 'shannon', got '{plugin.get('name')}'")
                if not plugin.get("version"):
                    self.issues.append("plugin.json missing version")
        except Exception as e:
            self.issues.append(f"plugin.json error: {e}")

        # Check marketplace.json
        market_file = self.root / ".claude-plugin/marketplace.json"
        try:
            with open(market_file) as f:
                market = json.load(f)
                plugins = market.get("plugins", [])
                if not any(p.get("name") == "shannon" for p in plugins):
                    self.issues.append("marketplace.json doesn't list 'shannon' plugin")
        except Exception as e:
            self.issues.append(f"marketplace.json error: {e}")

        print(f"   {'✅' if not self.issues else '❌'} Plugin config\n")

    def validate_commands(self):
        """Validate all command files"""
        print("🎯 Validating commands...")

        for cmd_file in (self.root / "commands").glob("*.md"):
            name = cmd_file.stem
            self.commands.add(name)

            content = cmd_file.read_text()

            # Check frontmatter
            if not content.startswith("---"):
                self.issues.append(f"{cmd_file.name}: Missing frontmatter")
                continue

            # Extract frontmatter
            parts = content.split("---", 2)
            if len(parts) < 3:
                self.issues.append(f"{cmd_file.name}: Malformed frontmatter")
                continue

            frontmatter = parts[1]

            # Check name field matches filename
            if f"name: {name}" not in frontmatter:
                self.issues.append(f"{cmd_file.name}: name field '{name}' doesn't match filename")

            # Check required fields
            if "description:" not in frontmatter:
                self.issues.append(f"{cmd_file.name}: Missing description")
            if "usage:" not in frontmatter:
                self.issues.append(f"{cmd_file.name}: Missing usage")

        print(f"   {'✅' if len([i for i in self.issues if 'commands' in i]) == 0 else '❌'} {len(self.commands)} commands\n")

    def validate_skills(self):
        """Validate all skill files"""
        print("📚 Validating skills...")

        for skill_dir in (self.root / "skills").iterdir():
            if not skill_dir.is_dir():
                continue

            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                self.issues.append(f"{skill_dir.name}: Missing SKILL.md")
                continue

            self.skills.add(skill_dir.name)

            content = skill_file.read_text()

            # Check frontmatter
            if not content.startswith("---"):
                self.issues.append(f"{skill_dir.name}/SKILL.md: Missing frontmatter")
                continue

            # Extract frontmatter
            parts = content.split("---", 2)
            if len(parts) < 3:
                self.issues.append(f"{skill_dir.name}/SKILL.md: Malformed frontmatter")
                continue

            frontmatter = parts[1]

            # Check name matches directory
            if f"name: {skill_dir.name}" not in frontmatter:
                self.issues.append(f"{skill_dir.name}/SKILL.md: name doesn't match directory")

            # Check required fields
            if "description:" not in frontmatter:
                self.issues.append(f"{skill_dir.name}/SKILL.md: Missing description")

        print(f"   {'✅' if len([i for i in self.issues if 'SKILL.md' in i]) == 0 else '❌'} {len(self.skills)} skills\n")

    def validate_command_skill_mappings(self):
        """Verify commands reference existing skills"""
        print("🔗 Validating command→skill mappings...")

        for cmd_file in (self.root / "commands").glob("*.md"):
            content = cmd_file.read_text()

            # Extract @skill references
            skill_refs = re.findall(r'@skill ([a-z-]+)', content)

            for skill_name in skill_refs:
                if skill_name not in self.skills:
                    self.issues.append(f"{cmd_file.name} references non-existent skill: {skill_name}")

        mapping_issues = [i for i in self.issues if 'references non-existent' in i]
        print(f"   {'✅' if len(mapping_issues) == 0 else '❌'} Command-skill mappings\n")

    def validate_skill_dependencies(self):
        """Verify skill dependencies exist"""
        print("🔄 Validating skill dependencies...")

        for skill_dir in (self.root / "skills").iterdir():
            if not skill_dir.is_dir():
                continue

            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue

            content = skill_file.read_text()

            # Extract dependencies
            if "required-sub-skills:" in content:
                # Simple extraction (not full YAML parse)
                lines = content.split("\n")
                in_deps = False
                for line in lines:
                    if "required-sub-skills:" in line:
                        in_deps = True
                        continue
                    if in_deps and line.strip().startswith("- "):
                        dep = line.strip().replace("- ", "").strip()
                        if dep and dep not in self.skills:
                            self.issues.append(f"{skill_dir.name}: requires non-existent skill '{dep}'")
                    elif in_deps and not line.strip().startswith("- "):
                        in_deps = False

        dep_issues = [i for i in self.issues if 'requires non-existent' in i]
        print(f"   {'✅' if len(dep_issues) == 0 else '❌'} Skill dependencies\n")

    def report_results(self):
        """Report validation results"""
        print("=" * 60)
        print(f"\n📊 VALIDATION RESULTS\n")
        print(f"   Commands: {len(self.commands)}")
        print(f"   Skills: {len(self.skills)}")
        print(f"   Issues: {len(self.issues)}\n")

        if self.issues:
            print("❌ ISSUES FOUND:\n")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")
            print("\n")
            sys.exit(1)
        else:
            print("✅ ALL VALIDATIONS PASSED\n")
            print("Shannon v5.0 is properly configured.\n")
            sys.exit(0)

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    validator = ShannonValidator(root)
    validator.validate_all()
