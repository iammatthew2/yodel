from __future__ import annotations

from typing import Protocol, Tuple

Color = Tuple[int, int, int]


class BoardInterface(Protocol):
    width: int
    height: int

    def clear(self) -> None: ...
    def draw_pixel(self, x: int, y: int, color: Color) -> None: ...
    def draw_text(self, x: int, y: int, text: str, color: Color) -> None: ...
    def show(self) -> None: ...
