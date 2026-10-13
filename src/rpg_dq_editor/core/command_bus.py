"""Thin command bus. Handlers register callables, UI dispatches by name."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol


class EditorCommand(Protocol):
    name: str

    def execute(self, payload: dict[str, Any]) -> Any: ...


@dataclass(slots=True)
class CommandBus:
    _handlers: dict[str, Callable[[dict[str, Any]], Any]] = field(default_factory=dict)

    def register(self, name: str, fn: Callable[[dict[str, Any]], Any]) -> None:
        if name in self._handlers:
            raise ValueError(f"command already registered: {name}")
        self._handlers[name] = fn

    def dispatch(self, name: str, payload: dict[str, Any] | None = None) -> Any:
        try:
            fn = self._handlers[name]
        except KeyError as exc:
            raise KeyError(f"unknown command: {name}") from exc
        return fn(payload or {})