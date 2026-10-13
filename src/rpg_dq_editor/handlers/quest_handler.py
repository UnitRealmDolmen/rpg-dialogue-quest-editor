"""Thin UI-facing handlers for quest commands."""

from __future__ import annotations

from typing import Any

from rpg_dq_editor.core.command_bus import CommandBus
from rpg_dq_editor.core.project import EditorProject
from rpg_dq_editor.models.quest import QuestStep
from rpg_dq_editor.services.quest_service import QuestService


def register_quest_handlers(bus: CommandBus, project: EditorProject) -> None:
    def add_step(payload: dict[str, Any]) -> dict[str, str]:
        quest_id = payload["quest_id"]
        svc = QuestService(project.quests[quest_id])
        step = QuestStep(**payload["step"])
        svc.add_step(step)
        return {"step_id": step.step_id}

    def find_cycles(payload: dict[str, Any]) -> list[list[str]]:
        svc = QuestService(project.quests[payload["quest_id"]])
        return svc.dependency_cycles()

    bus.register("quest.add_step", add_step)
    bus.register("quest.find_cycles", find_cycles)