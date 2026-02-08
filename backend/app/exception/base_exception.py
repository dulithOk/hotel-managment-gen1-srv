class BaseAppException(Exception):
    def __init__(self, message: str, status: int = 500):
        self.message = message
        self.status = status

    def __str__(self):
        return f"{self.message} | Status: {self.status}"
