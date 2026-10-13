"""Adapter registry. Adding a format == one entry here."""

from __future__ import annotations

from rpg_dq_editor.adapters.base import ExportAdapter
from rpg_dq_editor.adapters.json_adapter import JsonAdapter
from rpg_dq_editor.adapters.ink_adapter import InkAdapter
from rpg_dq_editor.adapters.csv_adapter import CsvAdapter

ADAPTERS: dict[str, ExportAdapter] = {
    "json": JsonAdapter(),
    "ink": InkAdapter(),
    "csv": CsvAdapter(),
}


def get_adapter(target: str) -> ExportAdapter:
    try:
        return ADAPTERS[target]
    except KeyError as exc:
        raise KeyError(f"unknown export target: {target}") from exc