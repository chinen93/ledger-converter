from abc import ABC, abstractmethod

from src.files.csv import ReadCSV
from src.models.transaction import Transaction


class ConvertionStrategy(ABC):

    @abstractmethod
    def canConvert(self, heading: list[str]) -> bool:
        """
        Returns TRUE if conversion class can convert file.
        """
        raise NotImplementedError

    @abstractmethod
    def convert(
        self,
        heading: list[str],
        csv_reader: ReadCSV,
    ) -> list[Transaction]:
        """
        Conversion of file into transaction list.

        Returns:
        list[Transaction]: All transactions in file
        """
        raise NotImplementedError
