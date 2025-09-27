from http import HTTPStatus


class CustomException(Exception):
    def __init__(self, status_code: int, code: str, message: str) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)


class ExceptionWhenCreatingCallSessionRecord(CustomException):
    def __init__(self) -> None:
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = "Error when creating a record about CallSession."
        self.code = "Error when creating a record about CallSession."


class ExceptionWhenCreatingProcessingLogRecord(CustomException):
    def __init__(self) -> None:
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = "Error when creating a record about ProcessingLog."
        self.code = "Error when creating a record about ProcessingLog."


class ExceptionWhenUpdatingProcessingLogRecord(CustomException):
    def __init__(self) -> None:
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = "Error when updating a record about ProcessingLog."
        self.code = "Error when updating a record about ProcessingLog."


class ExceptionWhenUpdatingCallSessionRecord(CustomException):
    def __init__(self) -> None:
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = "Error when updating a record about CallSession."
        self.code = "Error when updating a record about CallSession."


class ExceptionCallSessionNotFound(CustomException):
    def __init__(self) -> None:
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = "Error when receiving an CallSession by session_id."
        self.code = "Error when receiving an CallSession by session_id."


class ExceptionWhenDownloadAudio(CustomException):
    def __init__(self, message: str) -> None:
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = f"Failed to download audio: {message}"
        self.code = f"Failed to download audio: {message}"


class ExceptionTranscriptionAPI(CustomException):
    def __init__(self, message: str) -> None:
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = f"Error: {message}"
        self.code = f"Error: {message}"


class ExceptionOpenAiFailed(CustomException):
    def __init__(self, message: str) -> None:
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = f"Error: {message}"
        self.code = f"Error: {message}"

class ExceptionProcessingCallSession(CustomException):
    def __init__(self, message: str) -> None:
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = f"Error: {message}"
        self.code = f"Error: {message}"


class ExceptionCallSessionStatusWhenGetting(CustomException):
    def __init__(self, message: str) -> None:
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = f"Error: Call session status - {message}"
        self.code = f"Error: Call session status - {message}"
