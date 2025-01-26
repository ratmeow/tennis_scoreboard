class ServiceError(Exception):
    def __init__(self, message: str = ""):
        self.message = message


class DatabaseNotFoundError(ServiceError):
    pass

class UniqueError(ServiceError):
    pass

class WinnerAlreadyExists(ServiceError):
    pass