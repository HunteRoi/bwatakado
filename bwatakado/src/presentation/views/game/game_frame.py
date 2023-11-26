import threading
from random import randrange as random
from tkinter import Canvas

from bwatakado.src.presentation.views.constants import APP_WIDTH, APP_HEIGHT
from bwatakado.src.presentation.views.game.components.ball import Ball
from bwatakado.src.presentation.views.game.components.trap import Trap
from bwatakado.src.presentation.views.game.components.wall import Wall
from bwatakado.src.presentation.views.game.position import Position
from bwatakado.src.presentation.views.game.threads.ball_adding_thread import (
    BallAddingThread,
)
from bwatakado.src.presentation.views.game.threads.ball_removing_thread import (
    BallRemovingThread,
)
from bwatakado.src.presentation.views.game.threads.threaded_action import ThreadedAction


class GameFrame(Canvas):
    """Game frame running threads before showing ticket drawing screen."""

    def __init__(
        self, root: "MainFrame", width: int = APP_WIDTH, height: int = APP_HEIGHT
    ):
        """Initialize the game frame."""
        super().__init__(root)

        self.root = root
        self.max_positions = Position(width - 10, height - 10)
        self.balls_lock = threading.Lock()
        self.balls: list[Ball] = []
        self.walls: list[Wall] = Wall.generate_default_walls(width, height)
        self.traps: list[Trap] = Trap.generate_default_traps(width, height)

        self.pack()
        self.configure(background="white", width=width, height=height)
        self.threads: dict[str, ThreadedAction] = {
            "add": BallAddingThread(self),
            "remove": BallRemovingThread(self),
        }

        self.draw_walls()
        self.draw_traps()
        self.is_playing = True

        self.root.after(0, self.animate)

    def add_ball(self):
        """Adds ball to the game frame."""
        if len(self.balls) < 10:
            self.balls.append(
                Ball(
                    Position(
                        random(self.max_positions.x), random(self.max_positions.y)
                    ),
                    random(10, stop=20),
                    f"#{random(0, 0xFFFFFF):06x}",
                    Position(random(1, 5), random(1, 5)),
                )
            )

    def remove_trapped_balls(self):
        """Removes trapped balls from the game frame."""
        for ball in self.balls:
            if ball.is_trapped:
                self.balls.remove(ball)

    def draw_walls(self):
        """Draws walls."""
        for wall in self.walls:
            wall.draw(self)

    def draw_traps(self):
        """Draws traps."""
        for trap in self.traps:
            trap.draw(self)

    def __enter__(self):
        """Critical section lock enter for balls list."""
        self.balls_lock.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Critical section lock exit for balls list."""
        self.balls_lock.release()

    def animate(self):
        """Animates ball movements."""
        while self.is_playing:
            self.update()
            if self.threads.get("remove").is_playing:
                self.delete("ball")

                with self:
                    for ball in self.balls:
                        ball.draw(self, self.walls, self.traps)

    def destroy(self):
        """Destroys the game frame."""
        self.is_playing = False
        for thread in self.threads.values():
            thread.stop()
