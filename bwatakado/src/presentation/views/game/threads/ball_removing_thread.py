from bwatakado.src.presentation.views.game.threads.threaded_action import ThreadedAction


class BallRemovingThread(ThreadedAction):
    """Thread responsible for removing balls to the game panel when dy and dx are 0."""

    def __init__(self, game_panel: "GameFrame"):
        self.game_panel = game_panel
        super().__init__(0.1)

    def execute(self):
        """Removes trapped balls from the game panel."""
        with self.game_panel:
            self.game_panel.remove_trapped_balls()
