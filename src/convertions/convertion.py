from abc import ABC, abstractmethod
from csv import DictReader

from src.transaction import Transaction


class Convertion(ABC):

    @abstractmethod
    def canConvert(self, heading: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def convert(
        self,
        heading: str,
        csv_reading: DictReader,
    ) -> list[Transaction]:
        raise NotImplementedError
