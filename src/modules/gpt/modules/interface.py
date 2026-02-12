from abc import ABC, abstractmethod
from typing import Callable, Dict


class AIQueryInterface(ABC):

    @abstractmethod
    def generate(self):
        """
        Executes request to the provider and stores raw result on the instance.
        """
        pass

    @abstractmethod
    def calc(self):
        pass

    @abstractmethod
    def get_result(self):
        pass
