from tkinter import Tk

from bwatakado.src.presentation.views.main_frame import MainFrame


def main():
    """Main function of the application."""

    root = Tk()
    app = MainFrame(root)
    app.mainloop()


if __name__ == "__main__":
    main()
