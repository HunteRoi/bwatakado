import tkinter as tk
from abc import ABC, abstractmethod

from bwatakado.src.presentation.views.game.position import Position


class IGraphicalComponent(ABC):
    """Interface for a graphical component."""

    @property
    def position(self) -> Position:
        """Returns the position of the round."""
        return self._position

    @position.setter
    def position(self, position: Position) -> None:
        """Sets the position of the round."""
        self._position = position

    @property
    def x(self) -> int:
        """Returns the x coordinate of the component."""
        return self.position.x

    @property
    def y(self) -> int:
        """Returns the y coordinate of the component."""
        return self.position.y

    @property
    @abstractmethod
    def width(self) -> int:
        """Returns the width of the component."""

    @property
    @abstractmethod
    def height(self) -> int:
        """Returns the height of the component."""

    @abstractmethod
    def draw(self, canvas: tk.Canvas, *args) -> None:
        """Draws the component."""
