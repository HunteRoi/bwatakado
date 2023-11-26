from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    """Position of a component on an x-y board."""

    x: int
    y: int
