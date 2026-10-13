"""Flat CSV export for localization pipelines: node_id, speaker, line."""

from __future__ import annotations

import csv
from pathlib import Path

from rpg_dq_editor.adapters.base import ExportResult
from rpg_dq_editor.core.project import EditorProject


class CsvAdapter:
    name = "csv"

    def write(self, project: EditorProject, out_dir: Path) -> ExportResult:
        path = out_dir / "dialogue_lines.csv"
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["tree_id", "node_id", "speaker_id", "emotion", "line"])
            for tree in project.dialogue_trees.values():
                for nid, node in tree.nodes.items():
                    writer.writerow([tree.tree_id, nid, node.speaker_id, node.emotion, node.line])
        return ExportResult(self.name, [path], [])