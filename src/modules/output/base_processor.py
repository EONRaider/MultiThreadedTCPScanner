from abc import ABC, abstractmethod


class OutputProcessor(ABC):
    """Interface for the implementation of all classes responsible for
    further processing/output of the information gathered by the
    TCPConnect class."""

    def __init__(self, scanner):
        self.scanner = scanner
        self.scanner.register(self)

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """
        Interface for the execution of a main operation by the observer.
        """
        ...

    def startup(self, *args, **kwargs) -> None:
        """
        Performs any operations deemed necessary prior to the first call
        to the update method.
        """
        ...

    def cleanup(self, *args, **kwargs) -> None:
        """
        Performs any operations deemed necessary after to the last call
        to the update method.
        """
        ...
