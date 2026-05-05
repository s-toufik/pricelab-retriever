from abc import ABC, abstractmethod

class Configuration(ABC):

    @abstractmethod
    def load(self) -> object:
        pass