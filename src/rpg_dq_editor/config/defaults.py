"""Editor-wide defaults. Single source of truth for tunables."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EditorDefaults:
    """Immutable defaults applied when a project is created without overrides."""

    autosave_interval_seconds: int = 90
    max_undo_depth: int = 200
    node_autolayout_spacing: int = 180
    default_locale: str = "en-US"
    export_indent: int = 2
    validate_on_export: bool = True
    recent_projects_limit: int = 12

    def as_dict(self) -> dict[str, object]:
        return {
            "autosave_interval_seconds": self.autosave_interval_seconds,
            "max_undo_depth": self.max_undo_depth,
            "node_autolayout_spacing": self.node_autolayout_spacing,
            "default_locale": self.default_locale,
            "export_indent": self.export_indent,
            "validate_on_export": self.validate_on_export,
            "recent_projects_limit": self.recent_projects_limit,
        }