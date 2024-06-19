# Created by NaveenPiedy at 6/19/2024 7:21 AM
from grpc import StatusCode


class CustomError(Exception):
    def __init__(self, message, code=StatusCode.UNKNOWN):
        super().__init__(message)
        self.message = message
        self.code = code


class NotFoundError(CustomError):
    def __init__(self, message="Resource not found"):
        super().__init__(message, StatusCode.NOT_FOUND)


class UnauthorizedError(CustomError):
    def __init__(self, message="Unauthorized access"):
        super().__init__(message, StatusCode.UNAUTHENTICATED)


class InternalServerError(CustomError):
    def __init__(self, message="Internal server error"):
        super().__init__(message, StatusCode.INTERNAL)
