"""Thin UI-facing handler for export + validation commands."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from rpg_dq_editor.core.command_bus import CommandBus
from rpg_dq_editor.core.project import EditorProject
from rpg_dq_editor.services.export_service import ExportService
from rpg_dq_editor.services.validation_service import ValidationService


def register_export_handlers(bus: CommandBus, project: EditorProject) -> None:
    def validate_project(_: dict[str, Any]) -> list[dict[str, str]]:
        return [
            {"severity": i.severity, "scope": i.scope, "message": i.message}
            for i in ValidationService(project).run()
        ]

    def export_project(payload: dict[str, Any]) -> dict[str, Any]:
        svc = ExportService(project)
        result = svc.export(payload["target"], Path(payload["out_dir"]))
        return {
            "target": result.target,
            "files": [str(p) for p in result.files_written],
            "warnings": result.warnings,
        }

    bus.register("export.validate", validate_project)
    bus.register("export.run", export_project)