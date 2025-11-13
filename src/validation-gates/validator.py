"""
Shannon Framework v4 - Validation Gate Validator

Performs confidence-based validation at spec/phase/wave levels.
"""

from typing import Dict, List, Optional, Any
from .models import (
    ValidationGate, ValidationGateResult, ValidationIssue,
    ConfidenceScore, GateLevel, GateStatus, ConfidenceLevel
)


class ValidationGateValidator:
    """
    Validates specifications, phases, and waves against confidence thresholds.

    Prevents wrong-direction work by enforcing ≥90% confidence.
    """

    def __init__(self):
        """Initialize validator."""
        self.gates: Dict[str, ValidationGate] = {}

    def register_gate(self, gate: ValidationGate):
        """
        Register a validation gate.

        Args:
            gate: ValidationGate to register
        """
        self.gates[gate.id] = gate

    def validate_specification(
        self,
        specification: Any,
        gate_id: str = "spec_gate"
    ) -> ValidationGateResult:
        """
        Validate specification object.

        Args:
            specification: SpecificationObject to validate
            gate_id: Gate ID to use

        Returns:
            ValidationGateResult
        """
        gate = self.gates.get(gate_id)
        if not gate:
            # Create default gate
            gate = ValidationGate(
                id=gate_id,
                level=GateLevel.SPECIFICATION,
                threshold=0.90
            )

        # Calculate confidence score
        confidence = self._calculate_spec_confidence(specification)

        # Check threshold
        status = GateStatus.PASSED if confidence.overall >= gate.threshold else GateStatus.FAILED

        # Collect issues
        issues = self._validate_spec_completeness(specification, confidence)

        # Generate recommendations
        recommendations = self._generate_spec_recommendations(issues, confidence)

        return ValidationGateResult(
            gate_level=GateLevel.SPECIFICATION,
            gate_id=gate_id,
            status=status,
            confidence_score=confidence,
            threshold=gate.threshold,
            issues=issues,
            recommendations=recommendations
        )

    def validate_phase(
        self,
        phase_result: Any,
        gate_id: str = "phase_gate"
    ) -> ValidationGateResult:
        """
        Validate phase result.

        Args:
            phase_result: PhaseResult to validate
            gate_id: Gate ID to use

        Returns:
            ValidationGateResult
        """
        gate = self.gates.get(gate_id)
        if not gate:
            gate = ValidationGate(
                id=gate_id,
                level=GateLevel.PHASE,
                threshold=0.90
            )

        # Calculate confidence from wave results
        confidence = self._calculate_phase_confidence(phase_result)

        # Check threshold
        status = GateStatus.PASSED if confidence.overall >= gate.threshold else GateStatus.FAILED

        # Collect issues
        issues = self._validate_phase_completeness(phase_result, confidence)

        # Generate recommendations
        recommendations = self._generate_phase_recommendations(issues, confidence)

        return ValidationGateResult(
            gate_level=GateLevel.PHASE,
            gate_id=gate_id,
            status=status,
            confidence_score=confidence,
            threshold=gate.threshold,
            issues=issues,
            recommendations=recommendations
        )

    def validate_wave(
        self,
        wave: Any,
        wave_result: Any,
        gate_id: str = "wave_gate"
    ) -> Dict[str, Any]:
        """
        Validate wave result.

        Args:
            wave: Wave definition
            wave_result: WaveResult to validate
            gate_id: Gate ID to use

        Returns:
            Validation result dictionary
        """
        gate = self.gates.get(gate_id)
        if not gate:
            gate = ValidationGate(
                id=gate_id,
                level=GateLevel.WAVE,
                threshold=wave.confidence_threshold if hasattr(wave, 'confidence_threshold') else 0.90
            )

        # Calculate confidence from task results
        confidence = self._calculate_wave_confidence(wave_result)

        # Check threshold
        passed = confidence.overall >= gate.threshold

        return {
            'confidence': confidence.overall,
            'passed': passed,
            'confidence_level': confidence.confidence_level.value if confidence.confidence_level else None,
        }

    def _calculate_spec_confidence(self, spec: Any) -> ConfidenceScore:
        """
        Calculate confidence score for specification.

        Args:
            spec: SpecificationObject

        Returns:
            ConfidenceScore
        """
        scores = []

        # Completeness: Check if all required fields are present
        completeness = 0.0
        if hasattr(spec, 'title') and spec.title:
            completeness += 0.2
        if hasattr(spec, 'description') and spec.description:
            completeness += 0.2
        if hasattr(spec, 'requirements') and len(spec.requirements) > 0:
            completeness += 0.3
        if hasattr(spec, 'tech_stack') and spec.tech_stack:
            completeness += 0.15
        if hasattr(spec, 'complexity_scores') and spec.complexity_scores:
            completeness += 0.15

        # Clarity: Check if spec is clear (use existing confidence if available)
        clarity = getattr(spec, 'confidence', 0.80)

        # Feasibility: Check technical feasibility
        feasibility = 0.85  # Default assumption
        if hasattr(spec, 'complexity_scores'):
            # Lower feasibility for very high complexity
            overall_complexity = getattr(spec.complexity_scores, 'overall', 0.5)
            if overall_complexity > 0.80:
                feasibility = 0.75
            elif overall_complexity > 0.90:
                feasibility = 0.65

        # Consistency: Check for contradictions
        consistency = 0.90  # Default assumption (would need deeper analysis)

        # Testability: Check if requirements are testable
        testability = 0.85  # Default assumption

        # Calculate overall
        overall = (
            completeness * 0.30 +
            clarity * 0.25 +
            feasibility * 0.20 +
            consistency * 0.15 +
            testability * 0.10
        )

        return ConfidenceScore(
            overall=overall,
            completeness=completeness,
            clarity=clarity,
            feasibility=feasibility,
            consistency=consistency,
            testability=testability
        )

    def _calculate_phase_confidence(self, phase_result: Any) -> ConfidenceScore:
        """
        Calculate confidence score for phase.

        Args:
            phase_result: PhaseResult

        Returns:
            ConfidenceScore
        """
        if not hasattr(phase_result, 'wave_results') or not phase_result.wave_results:
            return ConfidenceScore(overall=0.0)

        # Average wave confidences
        wave_confidences = [
            wr.confidence_score for wr in phase_result.wave_results
            if hasattr(wr, 'confidence_score')
        ]

        if not wave_confidences:
            overall = 0.0
        else:
            overall = sum(wave_confidences) / len(wave_confidences)

        # Calculate component scores
        completeness = 1.0 if hasattr(phase_result, 'status') and phase_result.status else 0.0

        # Check if all waves passed
        all_passed = all(
            hasattr(wr, 'validation_passed') and wr.validation_passed
            for wr in phase_result.wave_results
        )
        clarity = 1.0 if all_passed else 0.7

        return ConfidenceScore(
            overall=overall,
            completeness=completeness,
            clarity=clarity,
            feasibility=overall,
            consistency=overall,
            testability=overall
        )

    def _calculate_wave_confidence(self, wave_result: Any) -> ConfidenceScore:
        """
        Calculate confidence score for wave.

        Args:
            wave_result: WaveResult

        Returns:
            ConfidenceScore
        """
        # Base confidence on success rate
        success_rate = 0.0
        if hasattr(wave_result, 'get_success_rate'):
            success_rate = wave_result.get_success_rate()
        elif hasattr(wave_result, 'total_tasks') and wave_result.total_tasks > 0:
            success_rate = wave_result.completed_tasks / wave_result.total_tasks

        # Use existing confidence if available
        if hasattr(wave_result, 'confidence_score'):
            overall = wave_result.confidence_score
        else:
            overall = success_rate

        return ConfidenceScore(
            overall=overall,
            completeness=success_rate,
            clarity=overall,
            feasibility=overall,
            consistency=overall,
            testability=success_rate
        )

    def _validate_spec_completeness(
        self,
        spec: Any,
        confidence: ConfidenceScore
    ) -> List[ValidationIssue]:
        """Validate specification completeness."""
        issues = []

        if not hasattr(spec, 'title') or not spec.title:
            issues.append(ValidationIssue(
                severity="critical",
                category="completeness",
                description="Specification missing title",
                recommendation="Add a clear title describing the project"
            ))

        if not hasattr(spec, 'requirements') or len(spec.requirements) == 0:
            issues.append(ValidationIssue(
                severity="critical",
                category="completeness",
                description="Specification has no requirements",
                recommendation="Add at least 3-5 functional requirements"
            ))

        if confidence.completeness < 0.70:
            issues.append(ValidationIssue(
                severity="high",
                category="completeness",
                description=f"Specification completeness too low: {confidence.completeness:.1%}",
                recommendation="Add missing sections (tech stack, complexity analysis, etc.)"
            ))

        if confidence.clarity < 0.80:
            issues.append(ValidationIssue(
                severity="medium",
                category="clarity",
                description=f"Specification clarity low: {confidence.clarity:.1%}",
                recommendation="Clarify ambiguous requirements and provide more detail"
            ))

        return issues

    def _validate_phase_completeness(
        self,
        phase_result: Any,
        confidence: ConfidenceScore
    ) -> List[ValidationIssue]:
        """Validate phase completeness."""
        issues = []

        if not hasattr(phase_result, 'wave_results') or not phase_result.wave_results:
            issues.append(ValidationIssue(
                severity="critical",
                category="completeness",
                description="Phase has no wave results",
                recommendation="Execute at least one wave before validating phase"
            ))

        # Check for failed waves
        if hasattr(phase_result, 'wave_results'):
            from ..wave_engine import WaveStatus
            failed_waves = [
                wr for wr in phase_result.wave_results
                if hasattr(wr, 'status') and wr.status == WaveStatus.FAILED
            ]
            if failed_waves:
                issues.append(ValidationIssue(
                    severity="high",
                    category="consistency",
                    description=f"{len(failed_waves)} wave(s) failed",
                    recommendation="Review and fix failed waves before proceeding"
                ))

        return issues

    def _generate_spec_recommendations(
        self,
        issues: List[ValidationIssue],
        confidence: ConfidenceScore
    ) -> List[str]:
        """Generate recommendations for specification."""
        recommendations = []

        # Add recommendations from issues
        for issue in issues:
            if issue.recommendation:
                recommendations.append(issue.recommendation)

        # Add confidence-level recommendations
        if confidence.confidence_level == ConfidenceLevel.CRITICAL:
            recommendations.append("🔴 CRITICAL: Specification needs major revision before proceeding")
        elif confidence.confidence_level == ConfidenceLevel.LOW:
            recommendations.append("🟡 Consider revising specification before implementation")
        elif confidence.confidence_level == ConfidenceLevel.MEDIUM:
            recommendations.append("⚠️  Specification acceptable but could be improved")

        return recommendations

    def _generate_phase_recommendations(
        self,
        issues: List[ValidationIssue],
        confidence: ConfidenceScore
    ) -> List[str]:
        """Generate recommendations for phase."""
        recommendations = []

        for issue in issues:
            if issue.recommendation:
                recommendations.append(issue.recommendation)

        if confidence.overall < 0.90:
            recommendations.append(
                f"Phase confidence {confidence.overall:.1%} below 90% threshold - "
                f"consider re-executing failed waves"
            )

        return recommendations

    def bypass_gate(
        self,
        gate_id: str,
        reason: str
    ) -> ValidationGateResult:
        """
        Bypass validation gate.

        Args:
            gate_id: Gate to bypass
            reason: Reason for bypass

        Returns:
            ValidationGateResult with BYPASSED status
        """
        gate = self.gates.get(gate_id)
        if not gate:
            raise ValueError(f"Gate '{gate_id}' not found")

        if not gate.allow_bypass:
            raise ValueError(f"Gate '{gate_id}' does not allow bypass")

        return ValidationGateResult(
            gate_level=gate.level,
            gate_id=gate_id,
            status=GateStatus.BYPASSED,
            confidence_score=ConfidenceScore(overall=0.0),
            threshold=gate.threshold,
            bypassed_reason=reason
        )
