"""Business logic for quest graphs: step ordering, cycle detection."""

from __future__ import annotations

from rpg_dq_editor.models.quest import Quest, QuestStep


class QuestService:
    def __init__(self, quest: Quest) -> None:
        self._quest = quest

    def add_step(self, step: QuestStep) -> None:
        if step.step_id in self._quest.step_ids():
            raise ValueError(f"duplicate step_id: {step.step_id}")
        self._quest.steps.append(step)

    def dependency_cycles(self) -> list[list[str]]:
        """Return every cyclic requires_steps chain. Empty list == DAG."""
        graph = {s.step_id: list(s.requires_steps) for s in self._quest.steps}
        cycles: list[list[str]] = []
        visiting: list[str] = []
        done: set[str] = set()

        def walk(node: str) -> None:
            if node in done:
                return
            if node in visiting:
                cycles.append(visiting[visiting.index(node):] + [node])
                return
            visiting.append(node)
            for dep in graph.get(node, []):
                walk(dep)
            visiting.pop()
            done.add(node)

        for step_id in graph:
            walk(step_id)
        return cycles

    def unresolved_deps(self) -> dict[str, list[str]]:
        known = self._quest.step_ids()
        return {
            s.step_id: [d for d in s.requires_steps if d not in known]
            for s in self._quest.steps
            if any(d not in known for d in s.requires_steps)
        }