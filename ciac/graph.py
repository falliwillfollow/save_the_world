from __future__ import annotations

from collections import defaultdict, deque
from typing import Any


class DependencyCycleError(ValueError):
    pass


def pattern_dependencies(pattern: dict[str, Any]) -> list[str]:
    return [
        dep["id"]
        for dep in pattern.get("dependencies", [])
        if dep.get("kind") == "pattern"
    ]


def dependency_order(patterns_by_id: dict[str, dict[str, Any]], selected_ids: list[str]) -> list[str]:
    selected = list(dict.fromkeys(selected_ids))
    selected_set = set(selected)
    indegree = {pattern_id: 0 for pattern_id in selected}
    dependents: dict[str, list[str]] = defaultdict(list)

    for pattern_id in selected:
        pattern = patterns_by_id[pattern_id]
        for dependency_id in pattern_dependencies(pattern):
            if dependency_id in selected_set:
                indegree[pattern_id] += 1
                dependents[dependency_id].append(pattern_id)

    queue = deque(sorted([pattern_id for pattern_id, degree in indegree.items() if degree == 0]))
    ordered: list[str] = []
    while queue:
        pattern_id = queue.popleft()
        ordered.append(pattern_id)
        for dependent in sorted(dependents[pattern_id]):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                queue.append(dependent)

    if len(ordered) != len(selected):
        cycle_members = sorted(pattern_id for pattern_id, degree in indegree.items() if degree > 0)
        raise DependencyCycleError(f"Dependency cycle among selected patterns: {', '.join(cycle_members)}")
    return ordered

