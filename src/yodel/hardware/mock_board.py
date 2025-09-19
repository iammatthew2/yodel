from __future__ import annotations

from .board_interface import BoardInterface, Color

class MockBoard(BoardInterface):
    def __init__(self, width: int = 32, height: int = 8) -> None:
        self.width = width
        self.height = height
        self._buffer = [[(0,0,0) for _ in range(width)] for _ in range(height)]

    def clear(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self._buffer[y][x] = (0,0,0)

    def draw_pixel(self, x: int, y: int, color: Color) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self._buffer[y][x] = color

    def draw_text(self, x: int, y: int, text: str, color: Color) -> None:
        # Placeholder: just print text positionally
        print(f"[MOCK TEXT] ({x},{y}) {text} {color}")

    def show(self) -> None:
        # Simple ASCII visualization
        rows = []
        for row in self._buffer:
            rows.append(''.join('#' if px != (0,0,0) else '.' for px in row))
        print('\n'.join(rows))
