class PortScannerException(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code


class HostnameResolutionError(PortScannerException):
    def __init__(self, message: str, code: int = 1):
        super().__init__(message, code)
