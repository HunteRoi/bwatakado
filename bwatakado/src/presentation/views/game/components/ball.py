import tkinter as tk

from bwatakado.src.presentation.views.game.components.igraphical_component import (
    IGraphicalComponent,
)
from bwatakado.src.presentation.views.game.components.round_component import (
    RoundComponent,
)
from bwatakado.src.presentation.views.game.position import Position


class Ball(RoundComponent):
    """Ball component of the game."""

    def __init__(self, position: Position, radius: int, color: str, speed: Position):
        """Initializes the ball."""
        super().__init__(position, radius, color)
        self.direction = speed
        self.is_trapped = False
        self.has_previously_collided = False

    def has_collided_with(self, other: IGraphicalComponent) -> bool:
        """Checks if the ball has collided with another component."""
        return self.has_collided_on_x(other) or self.has_collided_on_y(other)

    def has_collided_on_x(self, other: IGraphicalComponent) -> bool:
        """Checks if the ball has collided with another component on the x axis."""
        left_side_collision = (
            other.x - self.radius <= self.x <= other.x + other.width
            and other.y <= self.y <= other.y + other.height
        )
        right_side_collision = (
            other.x <= self.x <= other.x + other.width + self.radius
            and other.y <= self.y <= other.y + other.height
        )
        return left_side_collision or right_side_collision

    def has_collided_on_y(self, other: IGraphicalComponent) -> bool:
        """Checks if the ball has collided with another component on the y axis."""
        top_side_collision = (
            other.x <= self.x <= other.x + other.width
            and other.y <= self.y <= other.y + other.height + self.radius
        )
        bottom_side_collision = (
            other.x <= self.x <= other.x + other.width
            and other.y - self.radius <= self.y <= other.y + other.height
        )
        return top_side_collision or bottom_side_collision

    def draw(self, canvas: tk.Canvas, *options: list[IGraphicalComponent]) -> None:
        """Draws the ball."""
        walls, traps = options
        has_collided = False

        for wall in walls:
            if self.has_collided_with(wall):
                has_collided = True
                if self.has_collided_on_x(wall):
                    self.direction = Position(-self.direction.x, self.direction.y)
                if self.has_collided_on_y(wall):
                    self.direction = Position(self.direction.x, -self.direction.y)

        if has_collided:
            if self.has_previously_collided:
                self.is_trapped = True
        self.has_previously_collided = has_collided

        for trap in traps:
            if self.has_collided_with(trap):
                self.is_trapped = True
                break

        self.position = Position(self.x + self.direction.x, self.y + self.direction.y)

        canvas.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            fill=self.color,
            outline=self.color,
            tags="ball",
        )
