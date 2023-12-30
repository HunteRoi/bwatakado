class CustomerNotFoundError(Exception):
    """Raised when the customer is not found in the database."""

    def __init__(self, customer_phone_number: str):
        self.message = f"Customer with phone number {
            customer_phone_number} does not exist."
        super().__init__(self.message)
