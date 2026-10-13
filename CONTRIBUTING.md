# Contributing to rpg-dialogue-quest-editor

Thanks for wanting to help build the dialogue and quest editor. This repo is a
Windows-first desktop tool for authoring RPG dialogue trees and quest graphs,
then exporting them into engine-consumable formats. Contributions of new
format adapters, validators, and UI panels are always welcome.

## Ground rules

- **Python 3.12+** is required. We target CPython only.
- Every new feature ships with tests under `tests/`.
- Keep the service layer pure: no `tkinter` / `PySide6` imports inside
  `src/rpg_dq_editor/services/`. UI talks to services, services talk to models.
- New export formats go through `services/export_service.py` + a writer in
  `adapters/`. Do not bolt format logic into the UI.

## Layout

```
src/rpg_dq_editor/
  app/          entry + bootstrap
  core/         project, undo, command bus
  handlers/     thin UI-facing request handlers
  services/     business logic (dialogue, quest, export, validation)
  models/       dataclasses for nodes, quests, conditions
  adapters/     engine format adapters (json, ink, yarn, csv)
  utils/        ids, logging, text helpers
  config/       defaults + paths
  ui/           panel widgets (thin, no business logic)
```

## Workflow

1. Fork, branch as `feat/<thing>` or `fix/<thing>`.
2. `python -m venv .venv && .venv\Scripts\activate`
3. `pip install -e .[dev]`
4. `pytest -q`
5. Open a PR. Describe the *authoring workflow* it improves, not just the diff.

## Style

- `ruff` + `black`, line length 100.
- Type hints on every public function. `mypy --strict` on `services/` and `models/`.
- Naming: dialogue nodes are `DialogueNode`, quest steps are `QuestStep`. Do
  not invent synonyms — the schema is shared with the export adapters.

## Reporting issues

Include the project file (`.rpgq.json`), editor version, and the exact export
target. A dialogue tree that renders wrong in one engine but not another is
the most useful bug report you can file.