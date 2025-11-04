"""
Shannon Framework v4 - Specification Validator

Validates specifications for structural correctness and semantic completeness.
"""

import jsonschema
from typing import List, Dict, Any, Optional
from .models import SpecificationObject, Requirement


class ValidationError:
    """Represents a validation error."""

    def __init__(self, field: str, message: str, severity: str = "error"):
        self.field = field
        self.message = message
        self.severity = severity  # error, warning, info

    def __repr__(self):
        return f"ValidationError({self.field}: {self.message} [{self.severity}])"


class SpecificationValidator:
    """Validates specification objects."""

    def __init__(self):
        self.schema = self._load_schema()

    def validate(self, spec: SpecificationObject) -> List[ValidationError]:
        """
        Validate specification object.

        Args:
            spec: SpecificationObject to validate

        Returns:
            List of ValidationError objects (empty if valid)
        """
        errors = []

        # Structural validation
        errors.extend(self._validate_structure(spec))

        # Semantic validation
        errors.extend(self._validate_semantics(spec))

        # Completeness validation
        errors.extend(self._validate_completeness(spec))

        # Consistency validation
        errors.extend(self._validate_consistency(spec))

        return errors

    def _validate_structure(self, spec: SpecificationObject) -> List[ValidationError]:
        """Validate structural correctness."""
        errors = []

        # Required fields
        if not spec.title or spec.title == "Untitled Specification":
            errors.append(ValidationError("title", "Specification must have a meaningful title", "warning"))

        if not spec.description:
            errors.append(ValidationError("description", "Specification must have a description", "error"))

        if not spec.requirements:
            errors.append(ValidationError("requirements", "Specification must have at least one requirement", "warning"))

        # Domain percentages validation
        if spec.domain_percentages:
            if not spec.domain_percentages.validate():
                errors.append(ValidationError(
                    "domain_percentages",
                    "Domain percentages must sum to 100%",
                    "error"
                ))

        # Complexity scores validation
        if spec.complexity_scores:
            for dimension, score in spec.complexity_scores.to_dict().items():
                if not 0.0 <= score <= 1.0:
                    errors.append(ValidationError(
                        f"complexity_scores.{dimension}",
                        f"Complexity score must be between 0.0 and 1.0 (got {score})",
                        "error"
                    ))

        return errors

    def _validate_semantics(self, spec: SpecificationObject) -> List[ValidationError]:
        """Validate semantic correctness."""
        errors = []

        # Check for conflicting requirements
        conflicts = self._detect_requirement_conflicts(spec.requirements)
        for conflict in conflicts:
            errors.append(ValidationError(
                "requirements",
                f"Potential conflict between requirements: {conflict}",
                "warning"
            ))

        # Check tech stack coherence
        if spec.tech_stack:
            incoherence = self._detect_tech_stack_incoherence(spec.tech_stack)
            if incoherence:
                errors.append(ValidationError(
                    "tech_stack",
                    f"Potentially incompatible technologies: {incoherence}",
                    "warning"
                ))

        return errors

    def _validate_completeness(self, spec: SpecificationObject) -> List[ValidationError]:
        """Validate specification completeness."""
        errors = []

        # Check confidence score
        if spec.confidence > 0 and spec.confidence < 0.90:
            errors.append(ValidationError(
                "confidence",
                f"Low confidence score ({spec.confidence:.2f} < 0.90). Specification may be incomplete.",
                "warning"
            ))

        # Check for missing critical information
        if not spec.tech_stack.languages and not spec.tech_stack.frameworks:
            errors.append(ValidationError(
                "tech_stack",
                "No languages or frameworks specified. Tech stack is incomplete.",
                "warning"
            ))

        # Check requirement priorities
        if spec.requirements:
            high_priority_count = sum(1 for r in spec.requirements if r.priority == 'high')
            if high_priority_count == 0:
                errors.append(ValidationError(
                    "requirements",
                    "No high-priority requirements defined. Consider prioritizing critical features.",
                    "info"
                ))

        return errors

    def _validate_consistency(self, spec: SpecificationObject) -> List[ValidationError]:
        """Validate internal consistency."""
        errors = []

        # Check requirement dependencies are valid
        all_req_ids = {req.id for req in spec.requirements}
        for req in spec.requirements:
            for dep_id in req.dependencies:
                if dep_id not in all_req_ids:
                    errors.append(ValidationError(
                        f"requirements.{req.id}",
                        f"Dependency '{dep_id}' does not exist",
                        "error"
                    ))

        # Check circular dependencies
        circular_deps = self._detect_circular_dependencies(spec.requirements)
        if circular_deps:
            errors.append(ValidationError(
                "requirements",
                f"Circular dependency detected: {' -> '.join(circular_deps)}",
                "error"
            ))

        return errors

    def _detect_requirement_conflicts(self, requirements: List[Requirement]) -> List[str]:
        """Detect potentially conflicting requirements."""
        conflicts = []

        # Simple keyword-based conflict detection
        conflict_keywords = [
            ("real-time", "batch"),
            ("synchronous", "asynchronous"),
            ("sql", "nosql"),  # Not always a conflict but worth noting
        ]

        for i, req1 in enumerate(requirements):
            for j, req2 in enumerate(requirements[i + 1:], i + 1):
                req1_lower = req1.text.lower()
                req2_lower = req2.text.lower()

                for keyword1, keyword2 in conflict_keywords:
                    if keyword1 in req1_lower and keyword2 in req2_lower:
                        conflicts.append(f"{req1.id} ({keyword1}) vs {req2.id} ({keyword2})")

        return conflicts

    def _detect_tech_stack_incoherence(self, tech_stack) -> Optional[str]:
        """Detect potentially incompatible technologies."""
        # Simple checks for common incompatibilities
        frameworks = [f.lower() for f in tech_stack.frameworks]

        # Multiple competing frontend frameworks
        frontend_frameworks = ['react', 'vue', 'angular']
        found_frontend = [f for f in frontend_frameworks if f in frameworks]
        if len(found_frontend) > 1:
            return f"Multiple frontend frameworks: {', '.join(found_frontend)}"

        # Multiple competing backend frameworks
        backend_frameworks = ['express', 'fastapi', 'django', 'flask', 'spring']
        found_backend = [f for f in backend_frameworks if f in frameworks]
        if len(found_backend) > 1:
            return f"Multiple backend frameworks: {', '.join(found_backend)}"

        return None

    def _detect_circular_dependencies(self, requirements: List[Requirement]) -> Optional[List[str]]:
        """Detect circular dependencies in requirements."""
        # Build dependency graph
        graph = {req.id: req.dependencies for req in requirements}

        # DFS to detect cycles
        visited = set()
        rec_stack = set()

        def has_cycle(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    cycle = has_cycle(neighbor, path.copy())
                    if cycle:
                        return cycle
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    return path[cycle_start:] + [neighbor]

            rec_stack.remove(node)
            return None

        for req_id in graph:
            if req_id not in visited:
                cycle = has_cycle(req_id, [])
                if cycle:
                    return cycle

        return None

    def _load_schema(self) -> Dict[str, Any]:
        """Load JSON schema for specification validation."""
        # JSON Schema for SpecificationObject
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["title", "description"],
            "properties": {
                "title": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200
                },
                "description": {
                    "type": "string",
                    "minLength": 10
                },
                "requirements": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "text"],
                        "properties": {
                            "id": {"type": "string"},
                            "text": {"type": "string"},
                            "priority": {"enum": ["high", "medium", "low"]},
                            "category": {"enum": ["functional", "non-functional", "technical"]},
                        }
                    }
                },
                "tech_stack": {
                    "type": "object",
                    "properties": {
                        "languages": {"type": "array", "items": {"type": "string"}},
                        "frameworks": {"type": "array", "items": {"type": "string"}},
                        "databases": {"type": "array", "items": {"type": "string"}},
                        "infrastructure": {"type": "array", "items": {"type": "string"}},
                    }
                },
                "confidence": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0
                }
            }
        }
