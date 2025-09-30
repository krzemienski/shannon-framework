"""
Evidence collection for production validation.

Collects execution evidence, timestamps, operations, and parallelism proof.
"""

import asyncio
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class OperationEvidence:
    """Evidence for a single operation"""
    operation_id: str
    operation_type: str
    start_time: float
    end_time: float
    duration_seconds: float
    success: bool
    agent_id: Optional[str] = None
    output_files: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            'operation_id': self.operation_id,
            'operation_type': self.operation_type,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration_seconds': self.duration_seconds,
            'success': self.success,
            'agent_id': self.agent_id,
            'output_files': self.output_files,
            'metadata': self.metadata
        }


@dataclass
class ParallelismEvidence:
    """Evidence of parallel execution"""
    concurrent_operations: List[tuple[str, str]]  # (op_id, op_id) pairs
    time_overlap_seconds: float
    parallelism_detected: bool
    proof: str

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            'concurrent_operations': self.concurrent_operations,
            'time_overlap_seconds': self.time_overlap_seconds,
            'parallelism_detected': self.parallelism_detected,
            'proof': self.proof
        }


@dataclass
class ExecutionEvidence:
    """Complete execution evidence"""
    execution_id: str
    start_time: float
    end_time: float
    total_duration_seconds: float
    operations: List[OperationEvidence]
    parallelism: Optional[ParallelismEvidence]
    files_created: List[str]
    files_modified: List[str]
    success: bool
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            'execution_id': self.execution_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'total_duration_seconds': self.total_duration_seconds,
            'operations': [op.to_dict() for op in self.operations],
            'parallelism': self.parallelism.to_dict() if self.parallelism else None,
            'files_created': self.files_created,
            'files_modified': self.files_modified,
            'success': self.success,
            'errors': self.errors
        }

    def save_to_file(self, path: Path):
        """Save evidence to JSON file"""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        logger.info(f"Evidence saved to {path}")


class EvidenceCollector:
    """
    Collects and analyzes execution evidence.

    Tracks operations, timestamps, file changes, and parallelism.
    """

    def __init__(self, execution_id: str):
        """
        Initialize evidence collector.

        Args:
            execution_id: Unique execution identifier
        """
        self.execution_id = execution_id
        self.start_time = time.time()
        self.end_time: Optional[float] = None

        self._operations: List[OperationEvidence] = []
        self._files_before: Set[Path] = set()
        self._files_after: Set[Path] = set()
        self._active_operations: Dict[str, float] = {}

        logger.info(f"EvidenceCollector initialized: {execution_id}")

    def snapshot_files(self, directory: Path):
        """
        Take snapshot of files in directory.

        Args:
            directory: Directory to snapshot
        """
        if not directory.exists():
            return

        files = set()
        for path in directory.rglob('*'):
            if path.is_file():
                files.add(path)

        if not self._files_before:
            self._files_before = files
            logger.info(f"Initial snapshot: {len(files)} files")
        else:
            self._files_after = files
            logger.info(f"Final snapshot: {len(files)} files")

    def start_operation(self, operation_id: str, operation_type: str, agent_id: Optional[str] = None):
        """
        Record operation start.

        Args:
            operation_id: Unique operation identifier
            operation_type: Type of operation
            agent_id: Optional agent identifier
        """
        start_time = time.time()
        self._active_operations[operation_id] = start_time
        logger.info(f"Operation started: {operation_id} ({operation_type})")

    def end_operation(self, operation_id: str, success: bool, output_files: Optional[List[str]] = None,
                     metadata: Optional[Dict[str, Any]] = None):
        """
        Record operation completion.

        Args:
            operation_id: Operation identifier
            success: Whether operation succeeded
            output_files: Optional list of output files
            metadata: Optional metadata dictionary
        """
        if operation_id not in self._active_operations:
            logger.warning(f"Operation {operation_id} not found in active operations")
            return

        start_time = self._active_operations.pop(operation_id)
        end_time = time.time()
        duration = end_time - start_time

        evidence = OperationEvidence(
            operation_id=operation_id,
            operation_type="unknown",
            start_time=start_time,
            end_time=end_time,
            duration_seconds=duration,
            success=success,
            output_files=output_files or [],
            metadata=metadata or {}
        )

        self._operations.append(evidence)
        logger.info(f"Operation completed: {operation_id} (success={success}, duration={duration:.3f}s)")

    def detect_parallelism(self) -> Optional[ParallelismEvidence]:
        """
        Detect parallel execution from operation timestamps.

        Returns:
            ParallelismEvidence if parallelism detected, None otherwise
        """
        if len(self._operations) < 2:
            return None

        concurrent_pairs = []
        max_overlap = 0.0

        for i, op1 in enumerate(self._operations):
            for op2 in self._operations[i+1:]:
                # Check if operations overlapped in time
                overlap_start = max(op1.start_time, op2.start_time)
                overlap_end = min(op1.end_time, op2.end_time)
                overlap = overlap_end - overlap_start

                if overlap > 0.001:  # 1ms minimum overlap
                    concurrent_pairs.append((op1.operation_id, op2.operation_id))
                    max_overlap = max(max_overlap, overlap)

        if concurrent_pairs:
            proof = (f"Detected {len(concurrent_pairs)} concurrent operation pairs "
                    f"with max overlap {max_overlap:.3f}s")

            return ParallelismEvidence(
                concurrent_operations=concurrent_pairs,
                time_overlap_seconds=max_overlap,
                parallelism_detected=True,
                proof=proof
            )

        return None

    def finalize(self, success: bool, errors: Optional[List[str]] = None) -> ExecutionEvidence:
        """
        Finalize evidence collection.

        Args:
            success: Whether execution succeeded
            errors: Optional error messages

        Returns:
            ExecutionEvidence with complete evidence
        """
        self.end_time = time.time()
        total_duration = self.end_time - self.start_time

        # Detect file changes
        files_created = [str(f) for f in (self._files_after - self._files_before)]
        files_modified = []  # Would need timestamps to detect modifications

        # Detect parallelism
        parallelism = self.detect_parallelism()

        evidence = ExecutionEvidence(
            execution_id=self.execution_id,
            start_time=self.start_time,
            end_time=self.end_time,
            total_duration_seconds=total_duration,
            operations=self._operations,
            parallelism=parallelism,
            files_created=files_created,
            files_modified=files_modified,
            success=success,
            errors=errors or []
        )

        logger.info(f"Evidence finalized: {self.execution_id} (success={success}, "
                   f"duration={total_duration:.3f}s, operations={len(self._operations)})")

        return evidence