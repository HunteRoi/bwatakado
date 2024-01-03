class InvalidPinCodeError(Exception):
    """Raised when the customer PIN code is invalid."""

    def __init__(self, customer_pin_code: str):
        self.message = f"Customer PIN code {customer_pin_code} is invalid."
        super().__init__(self.message)
