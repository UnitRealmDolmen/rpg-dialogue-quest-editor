"""Ink (.ink) writer for dialogue trees. Quests are skipped with a warning."""

from __future__ import annotations

from pathlib import Path

from rpg_dq_editor.adapters.base import ExportResult
from rpg_dq_editor.core.project import EditorProject


class InkAdapter:
    name = "ink"

    def write(self, project: EditorProject, out_dir: Path) -> ExportResult:
        written: list[Path] = []
        warnings: list[str] = []
        for tree in project.dialogue_trees.values():
            lines: list[str] = [f"// tree: {tree.name}", f"=== {tree.tree_id} ==="]
            for nid, node in tree.nodes.items():
                lines.append(f"=== {nid} ===")
                lines.append(f"{node.speaker_id}: {node.line}")
                for opt in node.options:
                    lines.append(f"* [{opt.text}] -> {opt.target_node_id or 'DONE'}")
                lines.append("")
            path = out_dir / f"{tree.tree_id}.ink"
            path.write_text("\n".join(lines), encoding="utf-8")
            written.append(path)
        if project.quests:
            warnings.append("ink adapter does not emit quests; use json or csv")
        return ExportResult(self.name, written, warnings)