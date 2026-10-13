"""In-memory project state: dialogue trees + quests + dirty tracking."""

from __future__ import annotations

from dataclasses import dataclass, field

from rpg_dq_editor.models.dialogue import DialogueTree
from rpg_dq_editor.models.quest import Quest


@dataclass
class EditorProject:
    project_id: str
    name: str
    dialogue_trees: dict[str, DialogueTree] = field(default_factory=dict)
    quests: dict[str, Quest] = field(default_factory=dict)
    dirty: bool = False

    def add_tree(self, tree: DialogueTree) -> None:
        self.dialogue_trees[tree.tree_id] = tree
        self.dirty = True

    def add_quest(self, quest: Quest) -> None:
        self.quests[quest.quest_id] = quest
        self.dirty = True

    def mark_clean(self) -> None:
        self.dirty = False

    def summary(self) -> str:
        return (
            f"{self.name}: {len(self.dialogue_trees)} dialogue trees, "
            f"{len(self.quests)} quests"
        )