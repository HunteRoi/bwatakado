class TicketNotFoundError(Exception):
    """Raised when the ticket is not found in the database."""

    def __init__(self, ticket_code: int):
        self.message = f"Ticket with code {ticket_code} does not exist."
        super().__init__(self.message)
