class TicketsNotFoundError(Exception):
    """Exception raised when no tickets are found."""

    def __init__(self, ticket_codes: list[str] = None):
        self.message = (
            f"Tickets with codes {ticket_codes} do not exist."
            if ticket_codes is not None
            else "Unknown tickets"
        )
        super().__init__(self.message)
