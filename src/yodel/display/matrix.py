from __future__ import annotations

"""Matrix display abstraction wrapping rgbmatrix if present.

Goals:
- Provide simple scroll API for game messages.
- Allow running on non-hardware systems (falls back to stdout).
"""
from dataclasses import dataclass
from typing import Optional
import importlib
import time


class DisplayUnavailable(RuntimeError):
    pass


@dataclass
class ScrollConfig:
    speed_seconds: float = 0.01
    brightness: float = 0.5  # 0..1 scaling of text color
    color: tuple[int, int, int] = (255, 255, 0)
    font_path: str = "fonts/spleen-16x32.bdf"
    baseline_offset: int = 23  # tune vs font size
    rotate_180: bool = True


class MatrixDisplay:
    def __init__(self, rows: int = 32, cols: int = 64, config: Optional[ScrollConfig] = None) -> None:
        self.config = config or ScrollConfig()
        self._hw = None
        self.rows = rows
        self.cols = cols
        self._load_driver()

    def _load_driver(self) -> None:
        try:
            rgbmatrix = importlib.import_module("rgbmatrix")
        except ImportError:
            return  # fallback to stdout mode
        options = rgbmatrix.RGBMatrixOptions()
        options.rows = self.rows
        options.cols = self.cols
        if self.config.rotate_180:
            options.pixel_mapper_config = "Rotate:180"
        self._hw = rgbmatrix.RGBMatrix(options=options)
        self._graphics = rgbmatrix.graphics

    def available(self) -> bool:
        return self._hw is not None

    def scroll_once(self, text: str) -> None:
        if not self.available():
            print(f"[DISPLAY:FALLBACK] {text}")
            return
        graphics = self._graphics
        font = graphics.Font()
        font.LoadFont(self.config.font_path)
        color_scaled = tuple(int(c * self.config.brightness) for c in self.config.color)
        text_color = graphics.Color(*color_scaled)
        canvas = self._hw.CreateFrameCanvas()
        pos = canvas.width
        while True:
            canvas.Clear()
            length = graphics.DrawText(canvas, font, pos, self.config.baseline_offset, text_color, text)
            pos -= 1
            if pos + length < 0:
                break
            time.sleep(self.config.speed_seconds)
            canvas = self._hw.SwapOnVSync(canvas)

    def show_static(self, text: str, x: int = 0, y: int = 0) -> None:
        if not self.available():
            print(f"[DISPLAY:FALLBACK:STATIC] ({x},{y}) {text}")
            return
        graphics = self._graphics
        font = graphics.Font()
        font.LoadFont(self.config.font_path)
        color_scaled = tuple(int(c * self.config.brightness) for c in self.config.color)
        text_color = graphics.Color(*color_scaled)
        canvas = self._hw.CreateFrameCanvas()
        canvas.Clear()
        graphics.DrawText(canvas, font, x, y or self.config.baseline_offset, text_color, text)
        self._hw.SwapOnVSync(canvas)
