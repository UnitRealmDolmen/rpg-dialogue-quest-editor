"""Stable id generation. Node ids are prefixed so trees stay scannable."""

from __future__ import annotations

import secrets


def new_node_id(prefix: str = "node") -> str:
    return f"{prefix}_{secrets.token_hex(4)}"


def new_quest_id(prefix: str = "quest") -> str:
    return f"{prefix}_{secrets.token_hex(4)}"