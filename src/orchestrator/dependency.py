"""
Shannon Framework v4 - Dependency Graph

Dependency resolution for agent orchestration.
"""

from typing import List, Set, Dict, Optional
from .models import AgentTask, OrchestrationPlan


class CircularDependencyError(Exception):
    """Raised when circular dependency is detected."""
    pass


class DependencyResolver:
    """Resolves task dependencies for orchestration."""

    def __init__(self, plan: OrchestrationPlan):
        """
        Initialize resolver with orchestration plan.

        Args:
            plan: Orchestration plan with tasks
        """
        self.plan = plan
        self.task_map = {task.id: task for task in plan.tasks}
        self.dependency_graph = self._build_graph()

    def _build_graph(self) -> Dict[str, Set[str]]:
        """
        Build dependency graph.

        Returns:
            Dictionary mapping task ID to set of dependency IDs
        """
        graph = {}
        for task in self.plan.tasks:
            graph[task.id] = set(task.dependencies)
        return graph

    def validate(self) -> List[str]:
        """
        Validate dependency graph.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check for missing dependencies
        for task_id, deps in self.dependency_graph.items():
            for dep_id in deps:
                if dep_id not in self.task_map:
                    errors.append(
                        f"Task '{task_id}' depends on non-existent task '{dep_id}'"
                    )

        # Check for circular dependencies
        try:
            self.topological_sort()
        except CircularDependencyError as e:
            errors.append(str(e))

        return errors

    def topological_sort(self) -> List[str]:
        """
        Perform topological sort to get execution order.

        Returns:
            List of task IDs in dependency order

        Raises:
            CircularDependencyError: If circular dependency detected
        """
        # Kahn's algorithm
        in_degree = {task_id: 0 for task_id in self.task_map}

        # Calculate in-degrees
        for task_id, deps in self.dependency_graph.items():
            for dep_id in deps:
                if dep_id in in_degree:
                    in_degree[dep_id] += 1

        # Find tasks with no dependencies
        queue = [task_id for task_id, degree in in_degree.items() if degree == 0]
        sorted_tasks = []

        while queue:
            # Get task with priority (if using priority strategy)
            task_id = queue.pop(0)
            sorted_tasks.append(task_id)

            # Reduce in-degree for dependent tasks
            for other_id, deps in self.dependency_graph.items():
                if task_id in deps:
                    in_degree[other_id] -= 1
                    if in_degree[other_id] == 0:
                        queue.append(other_id)

        # Check if all tasks were sorted
        if len(sorted_tasks) != len(self.task_map):
            # Find the cycle
            remaining = set(self.task_map.keys()) - set(sorted_tasks)
            cycle = self._find_cycle(remaining)
            raise CircularDependencyError(
                f"Circular dependency detected: {' -> '.join(cycle)}"
            )

        return sorted_tasks

    def _find_cycle(self, remaining: Set[str]) -> List[str]:
        """
        Find a cycle in the dependency graph.

        Args:
            remaining: Set of remaining task IDs

        Returns:
            List of task IDs forming a cycle
        """
        visited = set()
        rec_stack = set()
        path = []

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for dep in self.dependency_graph.get(node, []):
                if dep not in visited:
                    if dfs(dep):
                        return True
                elif dep in rec_stack:
                    # Found cycle
                    cycle_start = path.index(dep)
                    return path[cycle_start:] + [dep]

            path.pop()
            rec_stack.remove(node)
            return False

        for task_id in remaining:
            if task_id not in visited:
                result = dfs(task_id)
                if result:
                    return result

        return []

    def get_execution_waves(self) -> List[List[str]]:
        """
        Get execution waves (groups of tasks that can run in parallel).

        Returns:
            List of waves, where each wave is a list of task IDs
        """
        waves = []
        completed = set()

        while len(completed) < len(self.task_map):
            # Get tasks ready to execute
            wave = []
            for task_id, deps in self.dependency_graph.items():
                if task_id not in completed and all(d in completed for d in deps):
                    wave.append(task_id)

            if not wave:
                # This shouldn't happen if validation passed
                raise CircularDependencyError("Unable to resolve dependencies")

            waves.append(wave)
            completed.update(wave)

        return waves

    def get_parallel_groups(self, max_parallel: int = 8) -> List[List[str]]:
        """
        Get execution groups respecting max parallel limit.

        Args:
            max_parallel: Maximum tasks per group

        Returns:
            List of groups, each with <= max_parallel tasks
        """
        waves = self.get_execution_waves()
        groups = []

        for wave in waves:
            # Split wave into groups if needed
            for i in range(0, len(wave), max_parallel):
                groups.append(wave[i:i + max_parallel])

        return groups

    def get_critical_path(self) -> List[str]:
        """
        Get critical path (longest dependency chain).

        Returns:
            List of task IDs on critical path
        """
        # Calculate longest path to each task
        distances = {task_id: 0 for task_id in self.task_map}
        predecessors = {task_id: None for task_id in self.task_map}

        # Process in topological order
        sorted_tasks = self.topological_sort()

        for task_id in sorted_tasks:
            for dep_id in self.dependency_graph[task_id]:
                if distances[dep_id] + 1 > distances[task_id]:
                    distances[task_id] = distances[dep_id] + 1
                    predecessors[task_id] = dep_id

        # Find task with maximum distance
        max_task = max(distances, key=distances.get)

        # Reconstruct path
        path = []
        current = max_task
        while current is not None:
            path.append(current)
            current = predecessors[current]

        path.reverse()
        return path

    def get_dependencies_for(self, task_id: str) -> Set[str]:
        """
        Get all dependencies for a task (direct and transitive).

        Args:
            task_id: Task ID

        Returns:
            Set of all dependency task IDs
        """
        if task_id not in self.task_map:
            return set()

        all_deps = set()
        to_process = list(self.dependency_graph[task_id])

        while to_process:
            dep_id = to_process.pop(0)
            if dep_id not in all_deps:
                all_deps.add(dep_id)
                to_process.extend(self.dependency_graph.get(dep_id, []))

        return all_deps

    def get_dependents_of(self, task_id: str) -> Set[str]:
        """
        Get all tasks that depend on this task.

        Args:
            task_id: Task ID

        Returns:
            Set of dependent task IDs
        """
        dependents = set()
        for other_id, deps in self.dependency_graph.items():
            if task_id in deps:
                dependents.add(other_id)
        return dependents

    def can_run_parallel(self, task_ids: List[str]) -> bool:
        """
        Check if tasks can run in parallel (no dependencies between them).

        Args:
            task_ids: List of task IDs to check

        Returns:
            True if all tasks are independent
        """
        task_set = set(task_ids)

        for task_id in task_ids:
            deps = self.get_dependencies_for(task_id)
            if deps & task_set:
                return False

        return True
