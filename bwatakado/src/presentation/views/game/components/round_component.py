import tkinter as tk

from bwatakado.src.presentation.views.game.components.igraphical_component import (
    IGraphicalComponent,
)
from bwatakado.src.presentation.views.game.position import Position


class RoundComponent(IGraphicalComponent):
    """Round component of the game."""

    def __init__(self, position: Position, radius: int, color: str):
        self.position = position
        self.radius = radius
        self.color = color

    @property
    def width(self) -> int:
        return self.radius

    @property
    def height(self) -> int:
        return self.radius

    def draw(self, canvas: tk.Canvas, *options) -> None:
        """Draws the round."""
        canvas.create_oval(
            self.x,
            self.y,
            self.x + self.radius,
            self.y + self.radius,
            fill=self.color,
            outline=self.color,
            tags=options[0],
        )
