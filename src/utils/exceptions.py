class ServiceError(Exception):
    def __init__(self, message: str = ""):
        self.message = message


class DatabaseInternalError(ServiceError):
    def __init__(self):
        super().__init__(message="Database Internal Error")


class ServiceValidationError(ServiceError):
    pass


class DatabaseNotFoundError(ServiceError):
    pass
