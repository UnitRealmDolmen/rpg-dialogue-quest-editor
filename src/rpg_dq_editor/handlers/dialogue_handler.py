"""Thin UI-facing handlers for dialogue commands. No business logic here."""

from __future__ import annotations

from typing import Any

from rpg_dq_editor.core.command_bus import CommandBus
from rpg_dq_editor.core.project import EditorProject
from rpg_dq_editor.models.dialogue import DialogueNode
from rpg_dq_editor.services.dialogue_service import DialogueService


def register_dialogue_handlers(bus: CommandBus, project: EditorProject) -> None:
    def add_node(payload: dict[str, Any]) -> dict[str, str]:
        tree_id = payload["tree_id"]
        svc = DialogueService(project.dialogue_trees[tree_id])
        node = DialogueNode(**payload["node"])
        svc.add_node(node)
        return {"node_id": node.node_id}

    def list_orphans(payload: dict[str, Any]) -> list[str]:
        svc = DialogueService(project.dialogue_trees[payload["tree_id"]])
        return svc.orphan_nodes()

    bus.register("dialogue.add_node", add_node)
    bus.register("dialogue.list_orphans", list_orphans)