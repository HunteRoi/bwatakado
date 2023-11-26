import tkinter as tk

from bwatakado.src.presentation.views.game.components.igraphical_component import (
    IGraphicalComponent,
)
from bwatakado.src.presentation.views.game.position import Position


class Wall(IGraphicalComponent):
    """Barrier component of the game."""

    @staticmethod
    def generate_default_walls(width: int, height: int) -> list["Wall"]:
        """Default walls for the game."""
        default_size = 10
        default_point = 0

        top_wall = Wall(Position(default_point, default_point), width, default_size)
        bottom_wall = Wall(Position(default_point, default_point), default_size, height)
        left_wall = Wall(Position(width - default_size, default_point), width, height)
        right_wall = Wall(Position(default_point, height - default_size), width, height)

        return [top_wall, bottom_wall, left_wall, right_wall]

    def __init__(
        self, position: Position, width: int, height: int, color: str = "#808080"
    ):
        self.position = position
        self.color = color
        self._width = width
        self._height = height

    def draw(self, canvas: tk.Canvas, *_) -> None:
        """Draws the wall."""
        canvas.create_rectangle(
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height,
            fill=self.color,
            outline=self.color,
        )

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height
