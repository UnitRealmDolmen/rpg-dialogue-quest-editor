"""Quest graph schema: quests hold ordered steps gated by conditions."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from rpg_dq_editor.models.condition import Condition


class QuestStatus(StrEnum):
    DRAFT = "draft"
    REVIEW = "review"
    FINAL = "final"
    DEPRECATED = "deprecated"


class QuestStep(BaseModel):
    step_id: str
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    objective_flag: str
    conditions: list[Condition] = Field(default_factory=list)
    requires_steps: list[str] = Field(default_factory=list)


class Quest(BaseModel):
    quest_id: str
    name: str
    status: QuestStatus = QuestStatus.DRAFT
    steps: list[QuestStep] = Field(default_factory=list)
    reward_flags: list[str] = Field(default_factory=list)
    linked_dialogue_tree: str | None = None

    def step_ids(self) -> set[str]:
        return {s.step_id for s in self.steps}