from typing import cast


class Terminal:
    """Current terminal configuration."""

    def __init__(self, admin_password: str):
        self.admin_password = admin_password

    def __eq__(self, __value: object) -> bool:
        __value = cast(Terminal, __value)
        return self.admin_password == __value.admin_password
