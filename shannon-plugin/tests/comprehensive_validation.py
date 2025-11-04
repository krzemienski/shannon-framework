#!/usr/bin/env python3
"""
Comprehensive Shannon V4 Integration Validation
Validates all components are properly integrated
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

class ShannonValidator:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.commands_dir = self.base_dir / "shannon-plugin" / "commands"
        self.agents_dir = self.base_dir / "shannon-plugin" / "agents"
        self.skills_dir = self.base_dir / "shannon-plugin" / "skills"
        self.docs_dir = self.base_dir / "docs"

        self.results = {
            "commands": {},
            "agents": {},
            "skills": {},
            "documentation": {},
            "errors": [],
            "warnings": []
        }

    def extract_frontmatter(self, content: str) -> Dict:
        """Extract YAML frontmatter from markdown content"""
        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {}

        fm_text = match.group(1)
        frontmatter = {}

        # Simple YAML parsing (handles our specific case)
        current_key = None
        current_list = []

        for line in fm_text.split('\n'):
            line = line.strip()
            if not line:
                continue

            if ':' in line and not line.startswith('-'):
                if current_key and current_list:
                    frontmatter[current_key] = current_list
                    current_list = []

                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                if value:
                    frontmatter[key] = value
                else:
                    current_key = key
            elif line.startswith('-'):
                item = line[1:].strip()
                current_list.append(item)

        if current_key and current_list:
            frontmatter[current_key] = current_list

        return frontmatter

    def extract_skill_references(self, content: str) -> List[str]:
        """Extract @skill references from command content"""
        pattern = r'@skill\s+([a-z-]+)'
        matches = re.findall(pattern, content, re.IGNORECASE)
        return list(set(matches))  # Remove duplicates

    def get_all_skills(self) -> Dict[str, Path]:
        """Get all available skills"""
        skills = {}
        if self.skills_dir.exists():
            for skill_dir in self.skills_dir.iterdir():
                if skill_dir.is_dir():
                    skill_file = skill_dir / "SKILL.md"
                    if skill_file.exists():
                        skills[skill_dir.name] = skill_file
        return skills

    def validate_commands(self) -> Dict:
        """Test 1: Validate all command files and their skill references"""
        print("TEST 1: Command → Skill Reference Validation")
        print("=" * 60)

        all_skills = self.get_all_skills()
        skill_names = set(all_skills.keys())

        command_results = {}
        broken_references = []

        if not self.commands_dir.exists():
            self.results["errors"].append("Commands directory not found")
            return command_results

        for cmd_file in sorted(self.commands_dir.glob("*.md")):
            cmd_name = cmd_file.stem
            print(f"\nValidating: {cmd_name}")

            try:
                content = cmd_file.read_text()
                skill_refs = self.extract_skill_references(content)

                result = {
                    "file": str(cmd_file),
                    "skill_references": skill_refs,
                    "valid_references": [],
                    "broken_references": []
                }

                for skill_ref in skill_refs:
                    if skill_ref in skill_names:
                        result["valid_references"].append(skill_ref)
                        print(f"  ✓ @skill {skill_ref}")
                    else:
                        result["broken_references"].append(skill_ref)
                        broken_references.append({
                            "command": cmd_name,
                            "skill": skill_ref
                        })
                        print(f"  ✗ @skill {skill_ref} - MISSING")
                        self.results["errors"].append(
                            f"Command {cmd_name} references missing skill: {skill_ref}"
                        )

                command_results[cmd_name] = result

            except Exception as e:
                error_msg = f"Error reading command {cmd_name}: {e}"
                self.results["errors"].append(error_msg)
                print(f"  ERROR: {e}")

        self.results["commands"] = command_results
        return command_results

    def validate_agents(self) -> Dict:
        """Test 2: Validate all agent definitions"""
        print("\n\nTEST 2: Agent Definition Validation")
        print("=" * 60)

        all_skills = self.get_all_skills()
        skill_names = set(all_skills.keys())

        agent_results = {}

        if not self.agents_dir.exists():
            self.results["errors"].append("Agents directory not found")
            return agent_results

        for agent_file in sorted(self.agents_dir.glob("*.md")):
            agent_name = agent_file.stem
            print(f"\nValidating: {agent_name}")

            try:
                content = agent_file.read_text()
                frontmatter = self.extract_frontmatter(content)

                result = {
                    "file": str(agent_file),
                    "has_frontmatter": bool(frontmatter),
                    "has_sitrep": "sitrep" in content.lower(),
                    "has_serena": "serena" in content.lower(),
                    "activated_by": frontmatter.get("activated-by", ""),
                    "activated_by_valid": False
                }

                # Check frontmatter
                if frontmatter:
                    print(f"  ✓ Has frontmatter")
                else:
                    print(f"  ✗ Missing frontmatter")
                    self.results["warnings"].append(
                        f"Agent {agent_name} missing frontmatter"
                    )

                # Check SITREP protocol
                if result["has_sitrep"]:
                    print(f"  ✓ Mentions SITREP protocol")
                else:
                    print(f"  ⚠ No SITREP protocol mention")
                    self.results["warnings"].append(
                        f"Agent {agent_name} doesn't mention SITREP protocol"
                    )

                # Check Serena MCP
                if result["has_serena"]:
                    print(f"  ✓ Mentions Serena MCP")
                else:
                    print(f"  ⚠ No Serena MCP mention")
                    self.results["warnings"].append(
                        f"Agent {agent_name} doesn't mention Serena MCP"
                    )

                # Check activated-by skill
                if result["activated_by"]:
                    if result["activated_by"] in skill_names:
                        result["activated_by_valid"] = True
                        print(f"  ✓ activated-by: {result['activated_by']}")
                    else:
                        print(f"  ✗ activated-by: {result['activated_by']} - MISSING")
                        self.results["errors"].append(
                            f"Agent {agent_name} activated by missing skill: {result['activated_by']}"
                        )
                else:
                    print(f"  ⚠ No activated-by field")

                agent_results[agent_name] = result

            except Exception as e:
                error_msg = f"Error reading agent {agent_name}: {e}"
                self.results["errors"].append(error_msg)
                print(f"  ERROR: {e}")

        self.results["agents"] = agent_results
        return agent_results

    def validate_skills(self) -> Dict:
        """Test 3: Validate skill dependencies"""
        print("\n\nTEST 3: Skill → Sub-Skill Validation")
        print("=" * 60)

        all_skills = self.get_all_skills()
        skill_names = set(all_skills.keys())

        skill_results = {}
        dependency_graph = defaultdict(list)

        for skill_name, skill_file in sorted(all_skills.items()):
            print(f"\nValidating: {skill_name}")

            try:
                content = skill_file.read_text()
                frontmatter = self.extract_frontmatter(content)

                required_sub_skills = frontmatter.get("required-sub-skills", [])
                if isinstance(required_sub_skills, str):
                    required_sub_skills = [required_sub_skills] if required_sub_skills else []

                result = {
                    "file": str(skill_file),
                    "required_sub_skills": required_sub_skills,
                    "valid_dependencies": [],
                    "missing_dependencies": []
                }

                for sub_skill in required_sub_skills:
                    if sub_skill in skill_names:
                        result["valid_dependencies"].append(sub_skill)
                        dependency_graph[skill_name].append(sub_skill)
                        print(f"  ✓ requires: {sub_skill}")
                    else:
                        result["missing_dependencies"].append(sub_skill)
                        print(f"  ✗ requires: {sub_skill} - MISSING")
                        self.results["errors"].append(
                            f"Skill {skill_name} requires missing sub-skill: {sub_skill}"
                        )

                if not required_sub_skills:
                    print(f"  ℹ No sub-skill dependencies")

                skill_results[skill_name] = result

            except Exception as e:
                error_msg = f"Error reading skill {skill_name}: {e}"
                self.results["errors"].append(error_msg)
                print(f"  ERROR: {e}")

        # Check for circular dependencies
        print("\n\nChecking for circular dependencies...")
        circular = self.detect_circular_dependencies(dependency_graph)
        if circular:
            for cycle in circular:
                cycle_str = " → ".join(cycle)
                print(f"  ✗ Circular dependency: {cycle_str}")
                self.results["errors"].append(f"Circular dependency: {cycle_str}")
        else:
            print("  ✓ No circular dependencies detected")

        self.results["skills"] = skill_results
        self.results["dependency_graph"] = dict(dependency_graph)

        return skill_results

    def detect_circular_dependencies(self, graph: Dict[str, List[str]]) -> List[List[str]]:
        """Detect circular dependencies in skill graph"""
        cycles = []
        visited = set()
        rec_stack = set()

        def visit(node, path):
            if node in rec_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return

            if node in visited:
                return

            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get(node, []):
                visit(neighbor, path + [node])

            rec_stack.remove(node)

        for node in graph:
            if node not in visited:
                visit(node, [])

        return cycles

    def validate_documentation(self) -> Dict:
        """Test 4: Validate documentation cross-references"""
        print("\n\nTEST 4: Documentation Cross-Reference Check")
        print("=" * 60)

        all_skills = self.get_all_skills()
        skill_names = set(all_skills.keys())

        all_commands = set(f.stem for f in self.commands_dir.glob("*.md"))

        doc_results = {}

        if not self.docs_dir.exists():
            print("  ⚠ No docs/ directory found")
            return doc_results

        for doc_file in sorted(self.docs_dir.rglob("*.md")):
            doc_name = str(doc_file.relative_to(self.docs_dir))
            print(f"\nValidating: {doc_name}")

            try:
                content = doc_file.read_text()

                # Find skill references
                skill_refs = self.extract_skill_references(content)

                # Find command references (looking for /sh_ or /sc_ patterns)
                cmd_pattern = r'/(sh_[a-z_]+|sc_[a-z_]+)'
                cmd_refs = re.findall(cmd_pattern, content)

                # Find file path references
                path_pattern = r'`([a-zA-Z0-9_/-]+\.[a-zA-Z0-9]+)`'
                path_refs = re.findall(path_pattern, content)

                result = {
                    "file": str(doc_file),
                    "skill_references": skill_refs,
                    "command_references": cmd_refs,
                    "path_references": path_refs,
                    "invalid_skills": [],
                    "invalid_commands": [],
                    "invalid_paths": []
                }

                # Validate skill references
                for skill_ref in skill_refs:
                    if skill_ref not in skill_names:
                        result["invalid_skills"].append(skill_ref)
                        print(f"  ✗ Invalid skill reference: {skill_ref}")
                        self.results["warnings"].append(
                            f"Doc {doc_name} references missing skill: {skill_ref}"
                        )

                # Validate command references
                for cmd_ref in cmd_refs:
                    if cmd_ref not in all_commands:
                        result["invalid_commands"].append(cmd_ref)
                        print(f"  ✗ Invalid command reference: {cmd_ref}")
                        self.results["warnings"].append(
                            f"Doc {doc_name} references missing command: {cmd_ref}"
                        )

                # Validate file paths (check if they exist in repo)
                for path_ref in path_refs:
                    full_path = self.base_dir / path_ref
                    if not full_path.exists():
                        result["invalid_paths"].append(path_ref)
                        # This is just a warning as docs may reference external files

                if not (result["invalid_skills"] or result["invalid_commands"] or result["invalid_paths"]):
                    print(f"  ✓ All references valid")

                doc_results[doc_name] = result

            except Exception as e:
                error_msg = f"Error reading doc {doc_name}: {e}"
                self.results["warnings"].append(error_msg)
                print(f"  ERROR: {e}")

        self.results["documentation"] = doc_results
        return doc_results

    def calculate_health_score(self) -> Dict:
        """Calculate overall integration health score"""
        total_checks = 0
        passed_checks = 0

        # Command validation
        for cmd_result in self.results["commands"].values():
            total_checks += len(cmd_result["skill_references"])
            passed_checks += len(cmd_result["valid_references"])

        # Agent validation
        for agent_result in self.results["agents"].values():
            # Frontmatter check
            total_checks += 1
            if agent_result["has_frontmatter"]:
                passed_checks += 1

            # activated-by check
            if agent_result["activated_by"]:
                total_checks += 1
                if agent_result["activated_by_valid"]:
                    passed_checks += 1

        # Skill validation
        for skill_result in self.results["skills"].values():
            total_checks += len(skill_result["required_sub_skills"])
            passed_checks += len(skill_result["valid_dependencies"])

        # Calculate score
        if total_checks == 0:
            score = 0
        else:
            score = (passed_checks / total_checks) * 100

        return {
            "score": round(score, 2),
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": total_checks - passed_checks,
            "error_count": len(self.results["errors"]),
            "warning_count": len(self.results["warnings"])
        }

    def generate_report(self) -> str:
        """Generate comprehensive validation report"""
        health = self.calculate_health_score()

        report = []
        report.append("# Shannon V4 Comprehensive Integration Validation Results")
        report.append("")
        report.append(f"**Generated:** {Path.cwd()}")
        report.append(f"**Base Directory:** {self.base_dir}")
        report.append("")

        # Health Score
        report.append("## Overall Integration Health")
        report.append("")
        report.append(f"**Health Score:** {health['score']}%")
        report.append("")
        report.append(f"- Total Checks: {health['total_checks']}")
        report.append(f"- Passed: {health['passed_checks']}")
        report.append(f"- Failed: {health['failed_checks']}")
        report.append(f"- Errors: {health['error_count']}")
        report.append(f"- Warnings: {health['warning_count']}")
        report.append("")

        # Status indicator
        if health['score'] >= 95:
            report.append("**Status:** ✅ EXCELLENT - System is well integrated")
        elif health['score'] >= 80:
            report.append("**Status:** ✓ GOOD - Minor issues need attention")
        elif health['score'] >= 60:
            report.append("**Status:** ⚠ FAIR - Several issues need fixing")
        else:
            report.append("**Status:** ✗ POOR - Critical issues require immediate attention")
        report.append("")

        # Test 1: Commands
        report.append("## Test 1: Command → Skill Reference Validation")
        report.append("")
        report.append(f"**Total Commands:** {len(self.results['commands'])}")
        report.append("")

        broken_refs = []
        for cmd_name, cmd_result in sorted(self.results["commands"].items()):
            if cmd_result["broken_references"]:
                broken_refs.append((cmd_name, cmd_result["broken_references"]))

        if broken_refs:
            report.append("### Broken References")
            report.append("")
            for cmd_name, refs in broken_refs:
                report.append(f"- **{cmd_name}**")
                for ref in refs:
                    report.append(f"  - Missing skill: `{ref}`")
            report.append("")
        else:
            report.append("✅ All skill references are valid")
            report.append("")

        # Test 2: Agents
        report.append("## Test 2: Agent Definition Validation")
        report.append("")
        report.append(f"**Total Agents:** {len(self.results['agents'])}")
        report.append("")

        agent_issues = []
        for agent_name, agent_result in sorted(self.results["agents"].items()):
            issues = []
            if not agent_result["has_frontmatter"]:
                issues.append("Missing frontmatter")
            if not agent_result["has_sitrep"]:
                issues.append("No SITREP mention")
            if not agent_result["has_serena"]:
                issues.append("No Serena MCP mention")
            if agent_result["activated_by"] and not agent_result["activated_by_valid"]:
                issues.append(f"Invalid activated-by: {agent_result['activated_by']}")

            if issues:
                agent_issues.append((agent_name, issues))

        if agent_issues:
            report.append("### Agent Issues")
            report.append("")
            for agent_name, issues in agent_issues:
                report.append(f"- **{agent_name}**")
                for issue in issues:
                    report.append(f"  - {issue}")
            report.append("")
        else:
            report.append("✅ All agents properly configured")
            report.append("")

        # Test 3: Skills
        report.append("## Test 3: Skill → Sub-Skill Validation")
        report.append("")
        report.append(f"**Total Skills:** {len(self.results['skills'])}")
        report.append("")

        # Dependency graph
        if self.results.get("dependency_graph"):
            report.append("### Dependency Graph")
            report.append("")
            report.append("```")
            for skill, deps in sorted(self.results["dependency_graph"].items()):
                if deps:
                    report.append(f"{skill}:")
                    for dep in deps:
                        report.append(f"  → {dep}")
            report.append("```")
            report.append("")

        # Missing dependencies
        missing_deps = []
        for skill_name, skill_result in sorted(self.results["skills"].items()):
            if skill_result["missing_dependencies"]:
                missing_deps.append((skill_name, skill_result["missing_dependencies"]))

        if missing_deps:
            report.append("### Missing Dependencies")
            report.append("")
            for skill_name, deps in missing_deps:
                report.append(f"- **{skill_name}**")
                for dep in deps:
                    report.append(f"  - Missing sub-skill: `{dep}`")
            report.append("")
        else:
            report.append("✅ All sub-skill dependencies exist")
            report.append("")

        # Test 4: Documentation
        report.append("## Test 4: Documentation Cross-Reference Check")
        report.append("")
        report.append(f"**Total Documentation Files:** {len(self.results['documentation'])}")
        report.append("")

        doc_issues = []
        for doc_name, doc_result in sorted(self.results["documentation"].items()):
            issues = []
            if doc_result["invalid_skills"]:
                issues.append(f"Invalid skills: {', '.join(doc_result['invalid_skills'])}")
            if doc_result["invalid_commands"]:
                issues.append(f"Invalid commands: {', '.join(doc_result['invalid_commands'])}")

            if issues:
                doc_issues.append((doc_name, issues))

        if doc_issues:
            report.append("### Documentation Issues")
            report.append("")
            for doc_name, issues in doc_issues:
                report.append(f"- **{doc_name}**")
                for issue in issues:
                    report.append(f"  - {issue}")
            report.append("")
        else:
            report.append("✅ All documentation references are valid")
            report.append("")

        # Errors
        if self.results["errors"]:
            report.append("## Critical Errors Requiring Fixes")
            report.append("")
            for i, error in enumerate(self.results["errors"], 1):
                report.append(f"{i}. {error}")
            report.append("")

        # Warnings
        if self.results["warnings"]:
            report.append("## Warnings")
            report.append("")
            for i, warning in enumerate(self.results["warnings"], 1):
                report.append(f"{i}. {warning}")
            report.append("")

        # Summary
        report.append("## Summary")
        report.append("")

        if health['score'] >= 95:
            report.append("Shannon V4 integration is excellent. The system is well integrated with minimal issues.")
        elif health['score'] >= 80:
            report.append("Shannon V4 integration is good. Address the minor issues identified above.")
        elif health['score'] >= 60:
            report.append("Shannon V4 integration is fair. Several issues need to be addressed for optimal functionality.")
        else:
            report.append("Shannon V4 integration has critical issues. Immediate action required to fix broken references and dependencies.")

        report.append("")
        report.append("---")
        report.append("")
        report.append("**Next Steps:**")
        report.append("")

        if self.results["errors"]:
            report.append("1. Fix all critical errors listed above")
            report.append("2. Re-run validation to verify fixes")

        if self.results["warnings"]:
            report.append("3. Review and address warnings")

        if health['score'] >= 95:
            report.append("- System is ready for production use")

        return "\n".join(report)

    def run_all_validations(self):
        """Run all validation tests"""
        print("Shannon V4 Comprehensive Integration Validation")
        print("=" * 60)
        print()

        self.validate_commands()
        self.validate_agents()
        self.validate_skills()
        self.validate_documentation()

        print("\n\n" + "=" * 60)
        print("Validation Complete")
        print("=" * 60)

        return self.generate_report()

def main():
    import sys

    base_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    validator = ShannonValidator(base_dir)
    report = validator.run_all_validations()

    # Save report
    output_file = Path(base_dir) / "shannon-plugin" / "tests" / "COMPREHENSIVE_VALIDATION_RESULTS.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(report)

    print(f"\n\nReport saved to: {output_file}")
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    # Print summary
    health = validator.calculate_health_score()
    print(f"\nHealth Score: {health['score']}%")
    print(f"Errors: {health['error_count']}")
    print(f"Warnings: {health['warning_count']}")

    if health['error_count'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
