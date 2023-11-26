import tkinter as tk

from bwatakado.src.presentation.views.constants import TRAP_RADIUS
from bwatakado.src.presentation.views.game.components.round_component import (
    RoundComponent,
)
from bwatakado.src.presentation.views.game.position import Position


class Trap(RoundComponent):
    """Trap component of the game"""

    @staticmethod
    def generate_default_traps(width: int, height: int) -> list["Trap"]:
        """Generate traps for the game."""
        default_point = 12

        top_left_corner_trap = Trap(Position(default_point, default_point), TRAP_RADIUS)
        top_right_corner_trap = Trap(
            Position(width - TRAP_RADIUS - default_point, default_point), TRAP_RADIUS
        )
        bottom_left_corner_trap = Trap(
            Position(default_point, height - TRAP_RADIUS - default_point), TRAP_RADIUS
        )
        bottom_right_corner_trap = Trap(
            Position(
                width - TRAP_RADIUS - default_point,
                height - TRAP_RADIUS - default_point,
            ),
            TRAP_RADIUS,
        )

        return [
            top_left_corner_trap,
            top_right_corner_trap,
            bottom_left_corner_trap,
            bottom_right_corner_trap,
        ]

    def __init__(self, position: Position, radius: int, color: str = "#000000"):
        """Initializes the trap."""
        super().__init__(position, radius, color)

    def draw(self, canvas: tk.Canvas, *options) -> None:
        """Draws the trap."""
        super().draw(canvas, "trap")
