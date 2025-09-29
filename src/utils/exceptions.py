

class TaskManagerAPIError(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)


class NotFoundDBError(TaskManagerAPIError):
    """Raised when a specific object is not found in the database."""
    pass    

class AlreadyExistError(TaskManagerAPIError):
    """Object already exists in database"""
    pass

class UnauthorizedError(TaskManagerAPIError):
    """Endpoint was accessed without proper authorization."""
    pass