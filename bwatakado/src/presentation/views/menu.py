from tkinter import Menu as TkMenu


class Menu(TkMenu):
    """Menu of the application."""

    def __init__(self, root: "MainFrame"):
        """Initialize the Menu."""
        super().__init__(root)
        self.settings_menu_item = None
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets of the Menu."""
        self.settings_menu_item = TkMenu(self, tearoff=0)
        self.settings_menu_item.add_command(label="Quitter", command=self.root.quit)

        self.add_cascade(label="Paramètres", menu=self.settings_menu_item)
