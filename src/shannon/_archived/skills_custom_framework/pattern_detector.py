"""Pattern Detection for Dynamic Skill Creation.

Detects patterns in command history and user behavior:
- Repeated command sequences
- Common workflows
- Task patterns
- Optimization opportunities

Part of: Wave 10 - Dynamic Skills & Polish
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
from collections import Counter
import json


@dataclass
class CommandPattern:
    """Detected command pattern."""
    pattern_id: str
    commands: List[str]
    frequency: int
    description: str
    suggested_skill_name: str
    confidence: float = 0.0
    last_seen: str = ""


@dataclass
class WorkflowPattern:
    """Detected workflow pattern."""
    workflow_id: str
    steps: List[Dict[str, Any]]
    frequency: int
    description: str
    optimization_potential: float = 0.0


class PatternDetector:
    """Detects patterns in command history for skill generation.

    Features:
    - Command sequence analysis
    - Workflow pattern detection
    - Frequency analysis
    - Skill suggestions
    """

    def __init__(
        self,
        history_file: Optional[Path] = None,
        min_frequency: int = 3
    ):
        """Initialize pattern detector.

        Args:
            history_file: Path to command history
            min_frequency: Minimum frequency to consider pattern
        """
        self.history_file = history_file
        self.min_frequency = min_frequency
        self.command_history: List[str] = []
        self.detected_patterns: List[CommandPattern] = []

    async def load_history(self):
        """Load command history from file."""
        if not self.history_file or not self.history_file.exists():
            return

        try:
            with open(self.history_file, 'r') as f:
                self.command_history = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error loading history: {e}")

    async def detect_patterns(self) -> List[CommandPattern]:
        """Detect patterns in command history.

        Returns:
            List of detected patterns
        """
        patterns = []

        # Detect 2-command sequences
        sequences_2 = self._find_sequences(length=2)
        for seq, count in sequences_2.items():
            if count >= self.min_frequency:
                pattern = CommandPattern(
                    pattern_id=f"seq2_{len(patterns)}",
                    commands=list(seq),
                    frequency=count,
                    description=f"Sequence: {' → '.join(seq)}",
                    suggested_skill_name=self._suggest_skill_name(seq),
                    confidence=self._calculate_confidence(count, len(self.command_history))
                )
                patterns.append(pattern)

        # Detect 3-command sequences
        sequences_3 = self._find_sequences(length=3)
        for seq, count in sequences_3.items():
            if count >= self.min_frequency:
                pattern = CommandPattern(
                    pattern_id=f"seq3_{len(patterns)}",
                    commands=list(seq),
                    frequency=count,
                    description=f"Sequence: {' → '.join(seq)}",
                    suggested_skill_name=self._suggest_skill_name(seq),
                    confidence=self._calculate_confidence(count, len(self.command_history))
                )
                patterns.append(pattern)

        self.detected_patterns = patterns
        return patterns

    def _find_sequences(self, length: int) -> Counter:
        """Find command sequences of given length.

        Args:
            length: Sequence length

        Returns:
            Counter of sequences
        """
        sequences = Counter()

        for i in range(len(self.command_history) - length + 1):
            seq = tuple(self.command_history[i:i+length])
            sequences[seq] += 1

        return sequences

    def _suggest_skill_name(self, commands: tuple) -> str:
        """Suggest skill name from command sequence.

        Args:
            commands: Command sequence

        Returns:
            Suggested skill name
        """
        # Extract key verbs/actions
        actions = []
        for cmd in commands:
            parts = cmd.split()
            if parts:
                actions.append(parts[0])

        if len(actions) >= 2:
            return f"{'_'.join(actions[:2])}_workflow"
        elif actions:
            return f"{actions[0]}_sequence"
        else:
            return "custom_workflow"

    def _calculate_confidence(self, frequency: int, total: int) -> float:
        """Calculate confidence score for pattern.

        Args:
            frequency: Pattern frequency
            total: Total commands

        Returns:
            Confidence score (0-1)
        """
        if total == 0:
            return 0.0

        # Base confidence on relative frequency
        relative_freq = frequency / total

        # Boost for higher absolute frequency
        freq_boost = min(frequency / 10.0, 0.3)

        return min(relative_freq + freq_boost, 1.0)

    def get_top_patterns(self, n: int = 5) -> List[CommandPattern]:
        """Get top N patterns by frequency.

        Args:
            n: Number of patterns to return

        Returns:
            Top patterns
        """
        sorted_patterns = sorted(
            self.detected_patterns,
            key=lambda p: (p.frequency, p.confidence),
            reverse=True
        )
        return sorted_patterns[:n]

    def export_patterns(self, output_file: Path):
        """Export detected patterns to JSON.

        Args:
            output_file: Output file path
        """
        data = {
            'patterns': [
                {
                    'pattern_id': p.pattern_id,
                    'commands': p.commands,
                    'frequency': p.frequency,
                    'description': p.description,
                    'suggested_skill_name': p.suggested_skill_name,
                    'confidence': p.confidence
                }
                for p in self.detected_patterns
            ],
            'total_commands': len(self.command_history),
            'total_patterns': len(self.detected_patterns)
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
