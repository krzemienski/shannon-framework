"""
Shannon Skills Framework - Dependency Resolution

The DependencyResolver builds and analyzes skill dependency graphs to determine:
- Valid execution order (topological sort)
- Circular dependency detection
- Parallel execution opportunities
- Missing dependency validation

Uses networkx for efficient graph operations and analysis.

Features:
- Directed acyclic graph (DAG) construction
- Cycle detection with detailed reporting
- Topological sorting for linear execution
- Dependency level grouping for parallel execution
- Missing dependency identification
- Comprehensive validation and error reporting
"""

import logging
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass, field

import networkx as nx

from shannon.skills.models import Skill
from shannon.skills.registry import SkillRegistry, SkillNotFoundError

logger = logging.getLogger(__name__)


class DependencyError(Exception):
    """Base exception for dependency-related errors"""
    pass


class CircularDependencyError(DependencyError):
    """Raised when circular dependencies are detected"""
    pass


class MissingDependencyError(DependencyError):
    """Raised when required dependencies are not available"""
    pass


@dataclass
class ResolvedDependencies:
    """
    Result of dependency resolution containing execution order and grouping.

    Attributes:
        execution_order: Linear list of skill names in dependency-safe order
        parallel_groups: List of skill groups that can execute in parallel
        dependency_levels: Number of dependency levels (depth of graph)
        graph_info: Metadata about the dependency graph
        skill_dependencies: Map of each skill to its direct dependencies
    """
    execution_order: List[str]
    parallel_groups: List[List[str]]
    dependency_levels: int
    graph_info: Dict[str, any]
    skill_dependencies: Dict[str, List[str]] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            'execution_order': self.execution_order,
            'parallel_groups': self.parallel_groups,
            'dependency_levels': self.dependency_levels,
            'graph_info': self.graph_info,
            'skill_dependencies': self.skill_dependencies
        }


class DependencyResolver:
    """
    Resolves skill dependencies and determines execution order.

    The resolver builds a directed graph of skill dependencies and performs
    comprehensive analysis to enable safe and efficient execution:

    1. Graph Construction: Creates directed edges from dependencies to dependents
    2. Validation: Checks for cycles and missing dependencies
    3. Topological Sort: Determines safe linear execution order
    4. Parallel Grouping: Identifies skills that can run concurrently

    Graph Structure:
        - Nodes: Skill names
        - Edges: dependency -> dependent (A -> B means "B depends on A")
        - DAG: Graph must be acyclic for valid execution

    Example:
        # Skills: A, B (depends on A), C (depends on A), D (depends on B, C)
        resolver = DependencyResolver(registry)

        resolved = resolver.resolve_dependencies([skill_a, skill_b, skill_c, skill_d])

        # Result:
        # execution_order: ['A', 'B', 'C', 'D'] or ['A', 'C', 'B', 'D']
        # parallel_groups: [['A'], ['B', 'C'], ['D']]
        # dependency_levels: 3

    Thread Safety:
        Resolver operations are stateless and thread-safe. Each resolution
        creates a new graph instance.
    """

    def __init__(self, registry: SkillRegistry):
        """
        Initialize the dependency resolver.

        Args:
            registry: SkillRegistry instance for looking up skills
        """
        self.registry = registry
        logger.debug("DependencyResolver initialized")

    def _build_graph(self, skills: List[Skill]) -> nx.DiGraph:
        """
        Build directed dependency graph from skills.

        Creates a directed graph where:
        - Each skill is a node
        - An edge from A to B means "B depends on A" (A must run before B)

        Args:
            skills: List of skills to build graph from

        Returns:
            Directed graph representing dependencies

        Example:
            If skill B has dependencies=['A'], the graph will have:
            - Nodes: A, B
            - Edge: A -> B (A must run before B)
        """
        G = nx.DiGraph()

        # Add all skills as nodes
        for skill in skills:
            G.add_node(skill.name, skill=skill)
            logger.debug(f"Added node: {skill.name}")

        # Add dependency edges
        for skill in skills:
            for dep in skill.dependencies:
                # Edge from dependency to dependent
                # This means dep must execute before skill
                G.add_edge(dep, skill.name)
                logger.debug(f"Added edge: {dep} -> {skill.name}")

        logger.info(f"Built dependency graph: {len(G.nodes)} nodes, {len(G.edges)} edges")
        return G

    def _detect_cycles(self, G: nx.DiGraph) -> List[List[str]]:
        """
        Detect circular dependencies in the graph.

        Args:
            G: Dependency graph to check

        Returns:
            List of cycles (each cycle is a list of skill names)
            Returns empty list if graph is acyclic (no cycles)

        Example:
            If A depends on B, B depends on C, C depends on A:
            Returns [['A', 'B', 'C', 'A']]
        """
        if nx.is_directed_acyclic_graph(G):
            logger.debug("Graph is acyclic (DAG)")
            return []

        cycles = list(nx.simple_cycles(G))
        logger.warning(f"Detected {len(cycles)} circular dependencies")
        return cycles

    def _validate_dependencies_exist(self, skills: List[Skill]) -> List[str]:
        """
        Validate that all dependencies are available in the skill set.

        Args:
            skills: List of skills to validate

        Returns:
            List of missing dependency names (empty if all exist)
        """
        skill_names = {skill.name for skill in skills}
        missing = set()

        for skill in skills:
            for dep in skill.dependencies:
                if dep not in skill_names:
                    missing.add(dep)
                    logger.warning(f"Missing dependency: {dep} (required by {skill.name})")

        return sorted(list(missing))

    def _topological_sort(self, G: nx.DiGraph) -> List[str]:
        """
        Perform topological sort to get linear execution order.

        Returns a valid execution order where all dependencies are
        satisfied (dependencies always come before dependents).

        Args:
            G: Dependency graph (must be a DAG)

        Returns:
            List of skill names in dependency-safe execution order

        Raises:
            nx.NetworkXError: If graph contains cycles

        Note:
            Multiple valid orderings may exist. This returns one valid ordering.
        """
        try:
            order = list(nx.topological_sort(G))
            logger.debug(f"Topological sort order: {order}")
            return order
        except nx.NetworkXError as e:
            logger.error(f"Topological sort failed (graph has cycles): {e}")
            raise

    def _group_by_dependency_level(self, G: nx.DiGraph) -> List[List[str]]:
        """
        Group skills by dependency level for parallel execution.

        Skills in the same group have no dependencies between them and can
        execute concurrently. Groups are ordered by dependency level.

        Uses networkx.topological_generations which efficiently computes
        the minimal number of sequential steps needed to execute all skills.

        Args:
            G: Dependency graph (must be a DAG)

        Returns:
            List of groups, where each group is a list of skill names that
            can execute in parallel. Groups are in dependency order.

        Example:
            Skills: A, B (depends on A), C (depends on A), D (depends on B, C)
            Result: [['A'], ['B', 'C'], ['D']]
            - Level 0: A (no dependencies)
            - Level 1: B and C (both depend only on A, can run in parallel)
            - Level 2: D (depends on B and C)
        """
        generations = nx.topological_generations(G)
        groups = [sorted(list(generation)) for generation in generations]

        logger.info(f"Grouped skills into {len(groups)} dependency levels")
        for i, group in enumerate(groups):
            logger.debug(f"Level {i}: {group} ({len(group)} skills)")

        return groups

    def _get_graph_info(self, G: nx.DiGraph, skills: List[Skill]) -> Dict:
        """
        Extract metadata and statistics about the dependency graph.

        Args:
            G: Dependency graph
            skills: Original skill list

        Returns:
            Dictionary containing graph statistics and analysis
        """
        info = {
            'total_skills': len(G.nodes),
            'total_dependencies': len(G.edges),
            'is_dag': nx.is_directed_acyclic_graph(G),
            'density': nx.density(G),
            'avg_dependencies': sum(len(s.dependencies) for s in skills) / len(skills) if skills else 0,
        }

        # Find skills with no dependencies (entry points)
        entry_points = [node for node in G.nodes if G.in_degree(node) == 0]
        info['entry_points'] = sorted(entry_points)
        info['entry_point_count'] = len(entry_points)

        # Find skills with no dependents (exit points)
        exit_points = [node for node in G.nodes if G.out_degree(node) == 0]
        info['exit_points'] = sorted(exit_points)
        info['exit_point_count'] = len(exit_points)

        # Calculate maximum dependency depth (longest path)
        if nx.is_directed_acyclic_graph(G):
            info['max_depth'] = nx.dag_longest_path_length(G)
        else:
            info['max_depth'] = None

        logger.debug(f"Graph info: {info}")
        return info

    def resolve_dependencies(self, skills: List[Skill]) -> ResolvedDependencies:
        """
        Resolve dependencies and determine execution order.

        This is the main entry point for dependency resolution. It performs:
        1. Dependency validation (missing dependencies)
        2. Graph construction
        3. Cycle detection
        4. Topological sort (linear execution order)
        5. Parallel grouping (concurrent execution opportunities)

        Args:
            skills: List of skills to resolve dependencies for

        Returns:
            ResolvedDependencies containing execution order and grouping

        Raises:
            MissingDependencyError: If any dependencies are missing
            CircularDependencyError: If circular dependencies are detected

        Example:
            resolver = DependencyResolver(registry)
            skills = [skill_a, skill_b, skill_c]
            resolved = resolver.resolve_dependencies(skills)

            # Execute in order
            for skill_name in resolved.execution_order:
                execute_skill(skill_name)

            # Or execute in parallel by group
            for group in resolved.parallel_groups:
                execute_parallel(group)
        """
        logger.info(f"Resolving dependencies for {len(skills)} skills")

        # Validate all dependencies exist
        missing = self._validate_dependencies_exist(skills)
        if missing:
            error_msg = f"Missing dependencies: {', '.join(missing)}"
            logger.error(error_msg)
            raise MissingDependencyError(error_msg)

        # Build dependency graph
        G = self._build_graph(skills)

        # Detect circular dependencies
        cycles = self._detect_cycles(G)
        if cycles:
            cycle_strs = [' -> '.join(cycle + [cycle[0]]) for cycle in cycles]
            error_msg = f"Circular dependencies detected:\n" + '\n'.join(f"  - {c}" for c in cycle_strs)
            logger.error(error_msg)
            raise CircularDependencyError(error_msg)

        # Compute execution order and grouping
        execution_order = self._topological_sort(G)
        parallel_groups = self._group_by_dependency_level(G)

        # Extract graph metadata
        graph_info = self._get_graph_info(G, skills)

        # Build skill dependencies map
        skill_deps = {skill.name: skill.dependencies for skill in skills}

        result = ResolvedDependencies(
            execution_order=execution_order,
            parallel_groups=parallel_groups,
            dependency_levels=len(parallel_groups),
            graph_info=graph_info,
            skill_dependencies=skill_deps
        )

        logger.info(
            f"Resolved dependencies: {len(execution_order)} skills in "
            f"{result.dependency_levels} levels, "
            f"{graph_info['entry_point_count']} entry points"
        )

        return result

    def find_missing_dependencies(self, skills: List[Skill]) -> List[str]:
        """
        Find dependencies that aren't available in the skill set.

        This checks if all required dependencies are present but doesn't
        perform full resolution (no cycle detection or ordering).

        Args:
            skills: List of skills to check

        Returns:
            List of missing dependency names (empty if all exist)

        Example:
            missing = resolver.find_missing_dependencies(skills)
            if missing:
                print(f"Cannot proceed: missing {missing}")
        """
        return self._validate_dependencies_exist(skills)

    def get_execution_order(self, skill_names: List[str]) -> List[str]:
        """
        Get linear execution order for a list of skill names.

        Looks up skills in the registry and resolves dependencies.
        This is a convenience method that combines skill lookup and resolution.

        Args:
            skill_names: Names of skills to order

        Returns:
            List of skill names in dependency-safe execution order

        Raises:
            SkillNotFoundError: If any skill name is not in registry
            MissingDependencyError: If dependencies are missing
            CircularDependencyError: If circular dependencies exist

        Example:
            order = resolver.get_execution_order(['skill_a', 'skill_b'])
            for name in order:
                execute_skill(name)
        """
        logger.debug(f"Getting execution order for: {skill_names}")

        # Look up skills in registry
        skills = []
        for name in skill_names:
            skill = self.registry.get(name)
            if skill is None:
                error_msg = f"Skill not found in registry: {name}"
                logger.error(error_msg)
                raise SkillNotFoundError(error_msg)
            skills.append(skill)

        # Resolve dependencies
        resolved = self.resolve_dependencies(skills)
        return resolved.execution_order

    def get_parallel_groups(self, skill_names: List[str]) -> List[List[str]]:
        """
        Group skills by dependency level for parallel execution.

        Looks up skills in the registry and determines which can run in parallel.
        This is a convenience method that combines skill lookup and grouping.

        Args:
            skill_names: Names of skills to group

        Returns:
            List of groups where each group contains skills that can
            execute in parallel. Groups are in dependency order.

        Raises:
            SkillNotFoundError: If any skill name is not in registry
            MissingDependencyError: If dependencies are missing
            CircularDependencyError: If circular dependencies exist

        Example:
            groups = resolver.get_parallel_groups(['skill_a', 'skill_b', 'skill_c'])
            for group in groups:
                # Execute all skills in group concurrently
                results = await asyncio.gather(*[execute(s) for s in group])
        """
        logger.debug(f"Getting parallel groups for: {skill_names}")

        # Look up skills in registry
        skills = []
        for name in skill_names:
            skill = self.registry.get(name)
            if skill is None:
                error_msg = f"Skill not found in registry: {name}"
                logger.error(error_msg)
                raise SkillNotFoundError(error_msg)
            skills.append(skill)

        # Resolve dependencies
        resolved = self.resolve_dependencies(skills)
        return resolved.parallel_groups

    def analyze_skill_dependencies(self, skill_name: str) -> Dict:
        """
        Analyze dependencies for a specific skill.

        Returns detailed information about a skill's dependencies including
        direct dependencies, transitive dependencies, and dependents.

        Args:
            skill_name: Name of skill to analyze

        Returns:
            Dictionary containing dependency analysis

        Raises:
            SkillNotFoundError: If skill is not in registry

        Example:
            analysis = resolver.analyze_skill_dependencies('skill_b')
            print(f"Direct deps: {analysis['direct_dependencies']}")
            print(f"All deps: {analysis['all_dependencies']}")
            print(f"Used by: {analysis['dependents']}")
        """
        skill = self.registry.get(skill_name)
        if skill is None:
            raise SkillNotFoundError(f"Skill not found: {skill_name}")

        # Get all skills to build complete graph
        all_skills = self.registry.list_all()
        G = self._build_graph(all_skills)

        analysis = {
            'skill_name': skill_name,
            'direct_dependencies': skill.dependencies,
            'dependency_count': len(skill.dependencies),
            'all_dependencies': [],
            'transitive_dependency_count': 0,
            'dependents': [],
            'dependent_count': 0,
            'is_entry_point': G.in_degree(skill_name) == 0,
            'is_exit_point': G.out_degree(skill_name) == 0,
        }

        # Find all transitive dependencies (ancestors in graph)
        if skill_name in G:
            ancestors = nx.ancestors(G, skill_name)
            analysis['all_dependencies'] = sorted(list(ancestors))
            analysis['transitive_dependency_count'] = len(ancestors)

            # Find all dependents (descendants in graph)
            descendants = nx.descendants(G, skill_name)
            analysis['dependents'] = sorted(list(descendants))
            analysis['dependent_count'] = len(descendants)

        logger.debug(f"Analyzed dependencies for '{skill_name}': {analysis}")
        return analysis


__all__ = [
    'DependencyResolver',
    'ResolvedDependencies',
    'DependencyError',
    'CircularDependencyError',
    'MissingDependencyError',
]
