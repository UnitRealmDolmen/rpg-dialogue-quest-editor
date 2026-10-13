"""Editor logger. Writes to stderr + rotating file under the appdata dir."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from rpg_dq_editor.config.paths import ProjectPaths

_CONFIGURED = False


def get_logger(name: str) -> logging.Logger:
    global _CONFIGURED
    logger = logging.getLogger(name)
    if not _CONFIGURED:
        log_dir = ProjectPaths.default_appdata() / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(
            log_dir / "editor.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8"
        )
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        root = logging.getLogger("rpg_dq_editor")
        root.setLevel(logging.INFO)
        root.addHandler(handler)
        _CONFIGURED = True
    return logger