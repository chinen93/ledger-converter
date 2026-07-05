

from csv import DictReader
import csv
from io import TextIOWrapper

from config.logging import get_logger


class ReadCSV():

    def __init__(self):
        self.log = get_logger(__name__)
        self.filename: str
        self.reader: DictReader
        self.line: str
        self._csvfile: TextIOWrapper

    def readFile(self, filename: str) -> None:
        print(filename)
        self.log.info(f"Reading Transactions from: '{filename}'")

        self._csvfile = open(filename, newline="")
        self.reader = csv.DictReader(self._csvfile, delimiter=",", quotechar='"')

        row = next(self.reader)
        self.line = str(row)

    def moveBeginData(self, header: list[str]) -> None:
        row = next(self.reader)

        while row != header:
            row = next(self.reader)

        row = next(self.reader)

    def __iter__(self):
        yield next(self.reader)

    def close(self) -> None:
        self._csvfile.close()