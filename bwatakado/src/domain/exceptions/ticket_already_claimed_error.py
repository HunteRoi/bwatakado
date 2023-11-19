class TicketAlreadyClaimedError(Exception):
    """Exception raised when trying to add a ticket that has already been claimed to a customer's list of tickets."""

    def __init__(self, ticket_id: str):
        super().__init__(f"Ticket {ticket_id} already claimed.")
