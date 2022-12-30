
class APIException(BaseException):
    code: int
    message: str

    def __init__(self, code: int = 0, message: str = ''):
        if (code > 0 and len(message) > 0):
            self.code = code
            self.message = message
