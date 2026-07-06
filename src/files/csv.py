import csv

from config.logging import get_logger


class ReadCSV:

    def __init__(self):
        self.log = get_logger(__name__)

    def readFile(self, filename: str) -> None:
        self.log.info(f"Reading Transactions from: '{filename}'")

        self.filename = filename
        self._csvfile = open(filename, newline="")
        self.reader = csv.reader(self._csvfile, delimiter=",", quotechar='"')

        # Read First Line
        self.headings = next(self.reader)

    def moveBeginData(self, header: list[str]) -> None:
        row = next(self.reader)

        while row != header:
            row = next(self.reader)

        row = next(self.reader)

    def __iter__(self):
        for row in self.reader:
            yield row

    def close(self) -> None:
        self._csvfile.close()
