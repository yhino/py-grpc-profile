from abc import ABCMeta, abstractmethod
from typing import Callable, Dict


class Adapter(metaclass=ABCMeta):
    @abstractmethod
    def run(
        self, behavior: Callable, request_or_iterator, servicer_context, metadata: Dict
    ):
        pass
