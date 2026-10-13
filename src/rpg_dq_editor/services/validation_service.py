"""Cross-asset validation run before export."""

from __future__ import annotations

from dataclasses import dataclass

from rpg_dq_editor.core.project import EditorProject
from rpg_dq_editor.services.dialogue_service import DialogueService
from rpg_dq_editor.services.quest_service import QuestService


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    severity: str  # "error" | "warning"
    scope: str
    message: str


class ValidationService:
    def __init__(self, project: EditorProject) -> None:
        self._project = project

    def run(self) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for tree in self._project.dialogue_trees.values():
            svc = DialogueService(tree)
            for orphan in svc.orphan_nodes():
                issues.append(ValidationIssue("warning", tree.tree_id, f"orphan node: {orphan}"))
            for dead in svc.dead_ends():
                issues.append(ValidationIssue("warning", tree.tree_id, f"dead-end node: {dead}"))
        for quest in self._project.quests.values():
            qsvc = QuestService(quest)
            for cycle in qsvc.dependency_cycles():
                issues.append(
                    ValidationIssue("error", quest.quest_id, "dependency cycle: " + " -> ".join(cycle))
                )
            for step_id, missing in qsvc.unresolved_deps().items():
                issues.append(
                    ValidationIssue(
                        "error", quest.quest_id, f"step {step_id} missing deps: {missing}"
                    )
                )
        return issues