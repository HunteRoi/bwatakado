import time
from abc import ABC, abstractmethod
from threading import Thread


class ThreadedAction(ABC):
    """Runs an action outside the main thread."""

    def __init__(self, interval: float = 1):
        super().__init__()
        self.is_playing = False
        self.thread = Thread(target=self.run)
        self.interval = interval
        self.start()

    def start(self):
        """Start the thread."""
        self.is_playing = True
        self.thread.start()

    @abstractmethod
    def _execute(self):
        """Action to be executed."""

    def run(self):
        """Run the thread."""
        while self.is_playing:
            self._execute()
            time.sleep(self.interval)

    def stop(self):
        """Stop the thread."""
        self.is_playing = False
        self.thread.join()
