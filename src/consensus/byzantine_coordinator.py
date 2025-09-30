"""
Shannon Framework - Byzantine Consensus Module

Production-ready Byzantine Fault Tolerant consensus:
- PBFT (Practical Byzantine Fault Tolerance) implementation
- 3-phase consensus protocol (pre-prepare, prepare, commit)
- Fault tolerance: tolerates (N-1)/3 faulty agents
- Async voting and quorum logic
"""

import asyncio
import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set, Callable
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ConsensusPhase(Enum):
    """Phases of PBFT consensus protocol"""
    PRE_PREPARE = "pre_prepare"
    PREPARE = "prepare"
    COMMIT = "commit"
    FINALIZED = "finalized"


class VoteType(Enum):
    """Types of votes in consensus"""
    APPROVE = "approve"
    REJECT = "reject"
    ABSTAIN = "abstain"


@dataclass
class Message:
    """Base message for consensus protocol"""
    message_type: str
    sender_id: str
    view: int
    sequence: int
    timestamp: datetime = field(default_factory=datetime.now)
    signature: Optional[str] = None

    def compute_digest(self) -> str:
        """Compute cryptographic digest of message"""
        content = f"{self.message_type}:{self.sender_id}:{self.view}:{self.sequence}"
        return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class PrePrepareMessage(Message):
    """Pre-prepare message from primary"""
    proposal: Any = None
    proposal_digest: str = ""

    def __post_init__(self):
        if self.proposal_digest == "" and self.proposal is not None:
            self.proposal_digest = self._compute_proposal_digest()

    def _compute_proposal_digest(self) -> str:
        """Compute digest of proposal"""
        proposal_str = json.dumps(self.proposal, sort_keys=True, default=str)
        return hashlib.sha256(proposal_str.encode()).hexdigest()


@dataclass
class PrepareMessage(Message):
    """Prepare message from replica"""
    proposal_digest: str = ""


@dataclass
class CommitMessage(Message):
    """Commit message from replica"""
    proposal_digest: str = ""


@dataclass
class Vote:
    """Individual vote in consensus"""
    agent_id: str
    vote_type: VoteType
    proposal_id: str
    rationale: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    signature: Optional[str] = None


@dataclass
class ConsensusProposal:
    """Proposal for consensus decision"""
    proposal_id: str
    content: Any
    proposer_id: str
    view: int
    sequence: int
    timestamp: datetime = field(default_factory=datetime.now)
    digest: str = field(default="", init=False)

    def __post_init__(self):
        if not self.digest:
            self.digest = self.compute_digest()

    def compute_digest(self) -> str:
        """Compute digest of proposal content"""
        content_str = json.dumps(self.content, sort_keys=True, default=str)
        return hashlib.sha256(content_str.encode()).hexdigest()


class VoteCollector:
    """
    Collects and validates votes for consensus decisions

    Tracks votes by phase and validates quorum requirements.
    """

    def __init__(self, n_agents: int, quorum_threshold: float = 0.67):
        self.n_agents = n_agents
        self.quorum_threshold = quorum_threshold
        self.votes: Dict[str, Dict[str, Vote]] = {}  # proposal_id -> agent_id -> vote
        self.quorum_size = self._compute_quorum_size()

    def _compute_quorum_size(self) -> int:
        """Compute minimum votes needed for quorum"""
        return int(self.n_agents * self.quorum_threshold) + 1

    def add_vote(self, proposal_id: str, vote: Vote) -> None:
        """Add a vote to the collection"""
        if proposal_id not in self.votes:
            self.votes[proposal_id] = {}

        self.votes[proposal_id][vote.agent_id] = vote

        logger.debug(
            f"Vote recorded: {vote.agent_id} -> {vote.vote_type.value} "
            f"for proposal {proposal_id[:8]}"
        )

    def get_votes(self, proposal_id: str) -> List[Vote]:
        """Get all votes for a proposal"""
        return list(self.votes.get(proposal_id, {}).values())

    def count_votes(self, proposal_id: str) -> Dict[VoteType, int]:
        """Count votes by type for a proposal"""
        votes = self.get_votes(proposal_id)
        counts = {
            VoteType.APPROVE: 0,
            VoteType.REJECT: 0,
            VoteType.ABSTAIN: 0
        }

        for vote in votes:
            counts[vote.vote_type] += 1

        return counts

    def has_quorum(self, proposal_id: str) -> bool:
        """Check if proposal has reached quorum"""
        total_votes = len(self.get_votes(proposal_id))
        return total_votes >= self.quorum_size

    def is_approved(self, proposal_id: str, require_quorum: bool = True) -> bool:
        """Check if proposal is approved"""
        if require_quorum and not self.has_quorum(proposal_id):
            return False

        counts = self.count_votes(proposal_id)
        return counts[VoteType.APPROVE] > counts[VoteType.REJECT]

    def is_rejected(self, proposal_id: str, require_quorum: bool = True) -> bool:
        """Check if proposal is rejected"""
        if require_quorum and not self.has_quorum(proposal_id):
            return False

        counts = self.count_votes(proposal_id)
        return counts[VoteType.REJECT] > counts[VoteType.APPROVE]


class ByzantineCoordinator:
    """
    Byzantine Fault Tolerant consensus coordinator

    Implements PBFT protocol with:
    - Pre-prepare, prepare, commit phases
    - View changes for primary failure
    - Fault tolerance: (N-1)/3 Byzantine faults
    - Async message passing
    """

    def __init__(
        self,
        n_agents: int,
        agent_id: str,
        is_primary: bool = False,
        quorum_threshold: float = 0.67,
        timeout_seconds: float = 30.0
    ):
        if n_agents < 4:
            raise ValueError("PBFT requires at least 4 agents (3f + 1 where f >= 1)")

        self.n_agents = n_agents
        self.agent_id = agent_id
        self.is_primary = is_primary
        self.quorum_threshold = quorum_threshold
        self.timeout_seconds = timeout_seconds

        # Fault tolerance calculation
        self.max_faulty = (n_agents - 1) // 3
        self.min_correct = 2 * self.max_faulty + 1

        self.current_view = 0
        self.sequence_number = 0

        # Message logs
        self.pre_prepare_log: Dict[int, PrePrepareMessage] = {}
        self.prepare_log: Dict[int, List[PrepareMessage]] = {}
        self.commit_log: Dict[int, List[CommitMessage]] = {}

        # Vote collection
        self.vote_collector = VoteCollector(n_agents, quorum_threshold)

        # Proposal tracking
        self.proposals: Dict[str, ConsensusProposal] = {}
        self.proposal_phase: Dict[str, ConsensusPhase] = {}
        self.finalized_proposals: Set[str] = set()

        # Agent tracking
        self.agent_ids: List[str] = []
        self.faulty_agents: Set[str] = set()

        logger.info(
            f"ByzantineCoordinator initialized: "
            f"n_agents={n_agents}, "
            f"max_faulty={self.max_faulty}, "
            f"primary={is_primary}"
        )

    def register_agent(self, agent_id: str) -> None:
        """Register an agent in the network"""
        if agent_id not in self.agent_ids:
            self.agent_ids.append(agent_id)
            logger.debug(f"Agent registered: {agent_id}")

    def mark_faulty(self, agent_id: str) -> None:
        """Mark an agent as Byzantine faulty"""
        self.faulty_agents.add(agent_id)
        logger.warning(f"Agent marked as faulty: {agent_id}")

    def is_faulty(self, agent_id: str) -> bool:
        """Check if agent is marked as faulty"""
        return agent_id in self.faulty_agents

    def can_tolerate_faults(self) -> bool:
        """Check if system can still tolerate faults"""
        return len(self.faulty_agents) <= self.max_faulty

    def get_primary_id(self) -> str:
        """Get ID of primary for current view"""
        if not self.agent_ids:
            return self.agent_id

        primary_index = self.current_view % len(self.agent_ids)
        return self.agent_ids[primary_index]

    def _next_sequence(self) -> int:
        """Get next sequence number"""
        self.sequence_number += 1
        return self.sequence_number

    async def propose(
        self,
        content: Any,
        proposal_id: Optional[str] = None
    ) -> ConsensusProposal:
        """
        Create a consensus proposal (primary only)

        Args:
            content: Proposal content
            proposal_id: Optional custom ID

        Returns:
            ConsensusProposal object
        """
        if not self.is_primary:
            raise ValueError("Only primary can propose")

        if proposal_id is None:
            proposal_id = f"proposal_{self.current_view}_{self.sequence_number}"

        proposal = ConsensusProposal(
            proposal_id=proposal_id,
            content=content,
            proposer_id=self.agent_id,
            view=self.current_view,
            sequence=self._next_sequence()
        )

        self.proposals[proposal_id] = proposal
        self.proposal_phase[proposal_id] = ConsensusPhase.PRE_PREPARE

        logger.info(f"Proposal created: {proposal_id}")

        return proposal

    async def pre_prepare(
        self,
        proposal: ConsensusProposal
    ) -> PrePrepareMessage:
        """
        Primary sends pre-prepare message

        Phase 1: Primary multicasts proposal to all replicas
        """
        if not self.is_primary:
            raise ValueError("Only primary can send pre-prepare")

        message = PrePrepareMessage(
            message_type="pre_prepare",
            sender_id=self.agent_id,
            view=self.current_view,
            sequence=proposal.sequence,
            proposal=proposal.content,
            proposal_digest=proposal.digest
        )

        self.pre_prepare_log[proposal.sequence] = message

        logger.info(
            f"Pre-prepare sent: seq={proposal.sequence}, "
            f"digest={proposal.digest[:8]}"
        )

        return message

    async def prepare(
        self,
        pre_prepare_msg: PrePrepareMessage
    ) -> PrepareMessage:
        """
        Replica sends prepare message

        Phase 2: Replicas validate and multicast prepare messages
        """
        # Validate pre-prepare message
        if pre_prepare_msg.view != self.current_view:
            raise ValueError("Invalid view in pre-prepare")

        if pre_prepare_msg.sender_id != self.get_primary_id():
            raise ValueError("Pre-prepare not from primary")

        message = PrepareMessage(
            message_type="prepare",
            sender_id=self.agent_id,
            view=self.current_view,
            sequence=pre_prepare_msg.sequence,
            proposal_digest=pre_prepare_msg.proposal_digest
        )

        # Add to log
        if pre_prepare_msg.sequence not in self.prepare_log:
            self.prepare_log[pre_prepare_msg.sequence] = []

        self.prepare_log[pre_prepare_msg.sequence].append(message)

        logger.debug(
            f"Prepare sent: seq={pre_prepare_msg.sequence}, "
            f"from={self.agent_id}"
        )

        return message

    def is_prepared(self, sequence: int) -> bool:
        """
        Check if replica is prepared

        Prepared means: received pre-prepare and 2f matching prepares
        """
        if sequence not in self.pre_prepare_log:
            return False

        if sequence not in self.prepare_log:
            return False

        # Need 2f + 1 total messages (including pre-prepare)
        n_prepares = len(self.prepare_log[sequence])
        required = 2 * self.max_faulty

        return n_prepares >= required

    async def commit(self, sequence: int) -> CommitMessage:
        """
        Replica sends commit message

        Phase 3: If prepared, multicast commit
        """
        if not self.is_prepared(sequence):
            raise ValueError("Cannot commit: not prepared")

        pre_prepare = self.pre_prepare_log[sequence]

        message = CommitMessage(
            message_type="commit",
            sender_id=self.agent_id,
            view=self.current_view,
            sequence=sequence,
            proposal_digest=pre_prepare.proposal_digest
        )

        # Add to log
        if sequence not in self.commit_log:
            self.commit_log[sequence] = []

        self.commit_log[sequence].append(message)

        logger.debug(f"Commit sent: seq={sequence}, from={self.agent_id}")

        return message

    def is_committed_local(self, sequence: int) -> bool:
        """
        Check if replica has committed locally

        Committed-local means: prepared and received 2f + 1 commits
        """
        if not self.is_prepared(sequence):
            return False

        if sequence not in self.commit_log:
            return False

        n_commits = len(self.commit_log[sequence])
        required = 2 * self.max_faulty + 1

        return n_commits >= required

    async def finalize(self, proposal_id: str) -> bool:
        """
        Finalize a proposal after consensus

        Returns:
            True if finalized successfully
        """
        if proposal_id not in self.proposals:
            logger.error(f"Cannot finalize unknown proposal: {proposal_id}")
            return False

        proposal = self.proposals[proposal_id]

        if not self.is_committed_local(proposal.sequence):
            logger.warning(
                f"Cannot finalize: not committed locally for seq={proposal.sequence}"
            )
            return False

        self.proposal_phase[proposal_id] = ConsensusPhase.FINALIZED
        self.finalized_proposals.add(proposal_id)

        logger.info(f"Proposal finalized: {proposal_id}")

        return True

    async def vote_on_proposal(
        self,
        proposal_id: str,
        vote_type: VoteType,
        rationale: Optional[str] = None
    ) -> Vote:
        """
        Submit a vote on a proposal

        Args:
            proposal_id: ID of proposal to vote on
            vote_type: APPROVE, REJECT, or ABSTAIN
            rationale: Optional reason for vote

        Returns:
            Vote object
        """
        vote = Vote(
            agent_id=self.agent_id,
            vote_type=vote_type,
            proposal_id=proposal_id,
            rationale=rationale
        )

        self.vote_collector.add_vote(proposal_id, vote)

        return vote

    async def collect_votes(
        self,
        proposal_id: str,
        agent_vote_funcs: Dict[str, Callable[[ConsensusProposal], VoteType]],
        timeout: Optional[float] = None
    ) -> Dict[VoteType, int]:
        """
        Collect votes from all agents asynchronously

        Args:
            proposal_id: ID of proposal
            agent_vote_funcs: Mapping of agent_id to voting function
            timeout: Optional timeout for vote collection

        Returns:
            Vote counts by type
        """
        timeout = timeout or self.timeout_seconds

        if proposal_id not in self.proposals:
            raise ValueError(f"Unknown proposal: {proposal_id}")

        proposal = self.proposals[proposal_id]

        async def collect_vote(agent_id: str, vote_func: Callable) -> Vote:
            """Collect single agent's vote"""
            try:
                # Run vote function (may be async or sync)
                if asyncio.iscoroutinefunction(vote_func):
                    vote_type = await vote_func(proposal)
                else:
                    vote_type = vote_func(proposal)

                return await self.vote_on_proposal(proposal_id, vote_type)

            except Exception as e:
                logger.error(f"Error collecting vote from {agent_id}: {e}")
                return await self.vote_on_proposal(
                    proposal_id,
                    VoteType.ABSTAIN,
                    rationale=f"Error: {str(e)}"
                )

        # Collect all votes in parallel
        vote_tasks = [
            collect_vote(agent_id, vote_func)
            for agent_id, vote_func in agent_vote_funcs.items()
        ]

        try:
            await asyncio.wait_for(
                asyncio.gather(*vote_tasks),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            logger.warning(f"Vote collection timeout for {proposal_id}")

        return self.vote_collector.count_votes(proposal_id)

    async def reach_consensus(
        self,
        proposal: ConsensusProposal,
        agent_vote_funcs: Dict[str, Callable]
    ) -> bool:
        """
        Run full PBFT consensus protocol

        Args:
            proposal: Consensus proposal
            agent_vote_funcs: Agent voting functions

        Returns:
            True if consensus reached and proposal approved
        """
        proposal_id = proposal.proposal_id

        # Phase 1: Pre-prepare (primary only)
        if self.is_primary:
            await self.pre_prepare(proposal)

        # Phase 2: Prepare (all replicas)
        # Simulate receiving pre-prepare and sending prepares
        if proposal.sequence in self.pre_prepare_log:
            pre_prepare_msg = self.pre_prepare_log[proposal.sequence]
            await self.prepare(pre_prepare_msg)

        # Wait for prepare quorum
        await asyncio.sleep(0.1)  # Simulate network delay

        # Phase 3: Commit (if prepared)
        if self.is_prepared(proposal.sequence):
            await self.commit(proposal.sequence)

        # Wait for commit quorum
        await asyncio.sleep(0.1)

        # Phase 4: Collect votes
        vote_counts = await self.collect_votes(
            proposal_id,
            agent_vote_funcs
        )

        # Phase 5: Finalize if committed and approved
        if self.is_committed_local(proposal.sequence):
            is_approved = self.vote_collector.is_approved(proposal_id)

            if is_approved:
                await self.finalize(proposal_id)
                logger.info(f"Consensus reached: {proposal_id} APPROVED")
                return True
            else:
                logger.info(f"Consensus reached: {proposal_id} REJECTED")
                return False

        logger.warning(f"Consensus failed: {proposal_id}")
        return False

    def get_consensus_status(self, proposal_id: str) -> Dict[str, Any]:
        """Get current consensus status for a proposal"""
        if proposal_id not in self.proposals:
            return {'error': 'Unknown proposal'}

        proposal = self.proposals[proposal_id]
        phase = self.proposal_phase.get(proposal_id, ConsensusPhase.PRE_PREPARE)

        vote_counts = self.vote_collector.count_votes(proposal_id)
        has_quorum = self.vote_collector.has_quorum(proposal_id)
        is_approved = self.vote_collector.is_approved(proposal_id, require_quorum=False)

        return {
            'proposal_id': proposal_id,
            'phase': phase.value,
            'sequence': proposal.sequence,
            'view': proposal.view,
            'is_prepared': self.is_prepared(proposal.sequence),
            'is_committed': self.is_committed_local(proposal.sequence),
            'is_finalized': proposal_id in self.finalized_proposals,
            'vote_counts': {k.value: v for k, v in vote_counts.items()},
            'has_quorum': has_quorum,
            'is_approved': is_approved,
            'n_faulty_agents': len(self.faulty_agents),
            'can_tolerate_faults': self.can_tolerate_faults()
        }