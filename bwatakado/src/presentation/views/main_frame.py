from tkinter import Frame, Tk

from bwatakado.src.presentation.views.constants import APP_WIDTH, APP_HEIGHT
from bwatakado.src.presentation.views.game.game_frame import GameFrame
from bwatakado.src.presentation.views.menu import Menu


class MainFrame(Frame):
    """Main Frame of the application."""

    def __init__(self, root: Tk):
        """Initialize the MainFrame."""
        super().__init__(root)

        self.menu = None
        self.root = root
        self.root.title("Bwatakado")
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.resizable(False, False)

        self.create_widgets()

        self.pack()
        self.current_panel = GameFrame(self, APP_WIDTH, APP_HEIGHT)
        self.pack()

    def create_widgets(self):
        """Create the widgets of the MainFrame."""
        self.menu = Menu(self)
        self.root.config(menu=self.menu)

    def destroy(self):
        """Destroy the MainFrame."""
        self.current_panel.destroy()
