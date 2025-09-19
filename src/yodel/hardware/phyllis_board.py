from __future__ import annotations

"""Adapter to reuse phyllis_bot hardware driver.

Implementation TODO:
- Import underlying matrix driver module from phyllis_bot (path / packaging TBD).
- Provide same interface as BoardInterface.
"""

from .board_interface import BoardInterface, Color

class PhyllisBoard(BoardInterface):
    def __init__(self) -> None:
        # TODO: initialize underlying matrix from reused code
        self.width = 64
        self.height = 16
        self._driver = None  # placeholder

    def clear(self) -> None:  # pragma: no cover
        # TODO: delegate to driver
        pass

    def draw_pixel(self, x: int, y: int, color: Color) -> None:  # pragma: no cover
        # TODO: set pixel via driver
        pass

    def draw_text(self, x: int, y: int, text: str, color: Color) -> None:  # pragma: no cover
        # TODO: render text using existing font routines
        pass

    def show(self) -> None:  # pragma: no cover
        # TODO: flush / swap buffer
        pass
