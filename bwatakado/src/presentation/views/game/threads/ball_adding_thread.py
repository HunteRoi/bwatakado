from bwatakado.src.presentation.views.game.threads.threaded_action import ThreadedAction


class BallAddingThread(ThreadedAction):
    """Thread responsible for adding balls to the game panel."""

    def __init__(self, game_panel: "GameFrame"):
        self.game_panel = game_panel
        super().__init__()

    def execute(self):
        """Adds a ball to the game panel."""
        with self.game_panel:
            self.game_panel.add_ball()
