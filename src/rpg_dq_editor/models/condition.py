"""Condition predicates used by dialogue options and quest step gating."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class ConditionKind(StrEnum):
    FLAG_SET = "flag_set"
    FLAG_CLEAR = "flag_clear"
    ITEM_HELD = "item_held"
    LEVEL_AT_LEAST = "level_at_least"
    QUEST_COMPLETE = "quest_complete"
    SCRIPT = "script"


class Condition(BaseModel):
    """A single gating predicate. `script` conditions stay opaque strings."""

    kind: ConditionKind
    key: str = Field(..., min_length=1, max_length=128)
    value: str | int | bool | None = None
    script_body: str | None = Field(default=None, max_length=4096)

    def describe(self) -> str:
        if self.kind is ConditionKind.SCRIPT:
            return f"script({self.key})"
        if self.value is None:
            return f"{self.kind.value}:{self.key}"
        return f"{self.kind.value}:{self.key}={self.value}"