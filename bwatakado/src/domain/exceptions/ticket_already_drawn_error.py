class TicketAlreadyDrawnError(Exception):
    """Exception raised when a ticket is drawn twice."""

    def __init__(self, ticket_code: str) -> None:
        super().__init__(f"Ticket {ticket_code} already drawn.")
