class RequestError(Exception):
    """Exception raised for request errors.

    Attributes:
        message -- Explanation of the error.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
