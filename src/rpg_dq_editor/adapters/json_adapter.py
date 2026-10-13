"""Canonical JSON export. Round-trips the full project schema."""

from __future__ import annotations

import json
from pathlib import Path

from rpg_dq_editor.adapters.base import ExportResult
from rpg_dq_editor.core.project import EditorProject


class JsonAdapter:
    name = "json"

    def write(self, project: EditorProject, out_dir: Path) -> ExportResult:
        payload = {
            "project_id": project.project_id,
            "name": project.name,
            "dialogue_trees": {
                tid: tree.model_dump(mode="json") for tid, tree in project.dialogue_trees.items()
            },
            "quests": {qid: q.model_dump(mode="json") for qid, q in project.quests.items()},
        }
        path = out_dir / "project.export.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return ExportResult(self.name, [path], [])