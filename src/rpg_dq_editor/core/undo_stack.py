"""Bounded undo/redo stack. Oldest entries are dropped past capacity."""

from __future__ import annotations

from collections import deque
from typing import Callable, Generic, TypeVar

T = TypeVar("T")

Apply = Callable[[T], None]
Revert = Callable[[T], None]


class UndoStack(Generic[T]):
    def __init__(self, capacity: int = 200) -> None:
        self._capacity = capacity
        self._undo: deque[tuple[Apply, Revert]] = deque()
        self._redo: deque[tuple[Apply, Revert]] = deque()

    def push(self, apply_fn: Apply, revert_fn: Revert) -> None:
        self._undo.append((apply_fn, revert_fn))
        if len(self._undo) > self._capacity:
            self._undo.popleft()
        self._redo.clear()

    def undo(self, target: T) -> bool:
        if not self._undo:
            return False
        apply_fn, revert_fn = self._undo.pop()
        revert_fn(target)
        self._redo.append((apply_fn, revert_fn))
        return True

    def redo(self, target: T) -> bool:
        if not self._redo:
            return False
        apply_fn, revert_fn = self._redo.pop()
        apply_fn(target)
        self._undo.append((apply_fn, revert_fn))
        return True