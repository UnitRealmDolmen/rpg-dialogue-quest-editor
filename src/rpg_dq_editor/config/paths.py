"""Filesystem layout for projects, exports, and logs on Windows."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ProjectPaths:
    """Resolved paths for a single open project."""

    root: Path

    @property
    def project_file(self) -> Path:
        return self.root / "project.rpgq.json"

    @property
    def dialogue_dir(self) -> Path:
        return self.root / "dialogue"

    @property
    def quests_dir(self) -> Path:
        return self.root / "quests"

    @property
    def exports_dir(self) -> Path:
        return self.root / "exports"

    @property
    def backup_dir(self) -> Path:
        return self.root / ".rpgq.bak"

    @classmethod
    def default_appdata(cls) -> Path:
        # %APPDATA%\rpg-dq-editor on Windows; ~/.config fallback elsewhere.
        import os

        appdata = os.environ.get("APPDATA")
        base = Path(appdata) if appdata else Path.home() / ".config"
        return base / "rpg-dq-editor"

    def ensure(self) -> None:
        for d in (self.root, self.dialogue_dir, self.quests_dir, self.exports_dir, self.backup_dir):
            d.mkdir(parents=True, exist_ok=True)