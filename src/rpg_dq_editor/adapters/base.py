"""Adapter contract every engine writer must satisfy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from rpg_dq_editor.core.project import EditorProject


@dataclass(frozen=True, slots=True)
class ExportResult:
    target: str
    files_written: list[Path]
    warnings: list[str]


class ExportAdapter(Protocol):
    name: str

    def write(self, project: EditorProject, out_dir: Path) -> ExportResult: ...