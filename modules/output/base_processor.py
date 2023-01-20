from abc import ABC, abstractmethod


class OutputProcessor(ABC):
    """Interface for the implementation of all classes responsible for
    further processing/output of the information gathered by the
    TCPConnectScanner class."""

    def __init__(self, scanner):
        self.scanner = scanner
        self.scanner.register(self)

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    def initialize(self, *args, **kwargs) -> None:
        ...

    def cleanup(self, *args, **kwargs) -> None:
        ...
