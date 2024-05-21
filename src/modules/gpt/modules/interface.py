from abc import ABC, abstractmethod
from typing import Callable, Dict


class AIQueryInterface(ABC):

    @abstractmethod
    def generate(self):
        """
        Generates a dictionary with keys 'result' and 'amount'.

        Returns:
            dict: A dictionary with:
                - 'result' (str): A string result.
                - 'amount' (float): A float amount.
        """
        pass

    @abstractmethod
    def calc(self):
        pass

    @abstractmethod
    def get_result(self):
        pass
