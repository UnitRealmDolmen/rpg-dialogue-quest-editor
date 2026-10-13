"""Dialogue tree schema shared by the editor UI and every export adapter."""

from __future__ import annotations

from pydantic import BaseModel, Field

from rpg_dq_editor.models.condition import Condition


class DialogueOption(BaseModel):
    """One selectable branch leading out of a node."""

    option_id: str
    text: str = Field(..., min_length=1, max_length=512)
    target_node_id: str | None = None
    conditions: list[Condition] = Field(default_factory=list)
    once_only: bool = False


class DialogueNode(BaseModel):
    """A single line of spoken dialogue plus its outgoing branches."""

    node_id: str
    speaker_id: str
    line: str = Field(..., min_length=1, max_length=2048)
    emotion: str = "neutral"
    options: list[DialogueOption] = Field(default_factory=list)
    script_on_enter: str | None = None
    canonical_locale: str = "en-US"


class DialogueTree(BaseModel):
    """A named dialogue asset: a set of nodes keyed by id."""

    tree_id: str
    name: str
    root_node_id: str
    nodes: dict[str, DialogueNode] = Field(default_factory=dict)

    def reachable_ids(self) -> set[str]:
        seen: set[str] = set()
        stack = [self.root_node_id]
        while stack:
            nid = stack.pop()
            if nid in seen or nid not in self.nodes:
                continue
            seen.add(nid)
            for opt in self.nodes[nid].options:
                if opt.target_node_id:
                    stack.append(opt.target_node_id)
        return seen