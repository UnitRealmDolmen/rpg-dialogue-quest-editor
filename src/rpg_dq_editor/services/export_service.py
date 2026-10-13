"""Export orchestration. Picks an adapter and writes to disk."""

from __future__ import annotations

from pathlib import Path

from rpg_dq_editor.adapters.base import ExportAdapter, ExportResult
from rpg_dq_editor.adapters.registry import get_adapter
from rpg_dq_editor.core.project import EditorProject


class ExportService:
    def __init__(self, project: EditorProject) -> None:
        self._project = project

    def available_targets(self) -> list[str]:
        from rpg_dq_editor.adapters.registry import ADAPTERS

        return sorted(ADAPTERS)

    def export(self, target: str, out_dir: Path) -> ExportResult:
        adapter: ExportAdapter = get_adapter(target)
        out_dir.mkdir(parents=True, exist_ok=True)
        return adapter.write(self._project, out_dir)