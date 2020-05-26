class ActionNotSupportedException(BaseException):
    DEFAULT_EXCEPTION_MESSAGE = "Action not supported for this corpus"

    def __init__(self, message=DEFAULT_EXCEPTION_MESSAGE):
        self.message = message
