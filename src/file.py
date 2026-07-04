import csv
import os
from logging import getLogger

from config.settings import get_settings
from src.accounts import Accounts
from src.convertions.convertion import Convertion
from src.convertions.creditCardConvertion import CreditCardConvertion
from src.convertions.statementConvertion import StatementConvertion
from src.transaction import Transaction


class HandleTransactions:

    def __init__(self):
        self._settings = get_settings()
        self.log = getLogger(__name__)

    def _chooseConvertion(
        self,
        converters: list[Convertion],
        csv_reader: csv.DictReader,
    ) -> list[Transaction]:
        """
        Return transactions from csv.

        Choose which converter to use based on the content of the file heading.

        Returns:
        list[Transaction]: transactions as order in the file
        """
        csv_headings = next(csv_reader)

        for converter in converters:
            if converter.canConvert(csv_headings):
                return converter.convert(csv_headings, csv_reader)

        return []

    def _readFile(self, converters: list[Convertion], filename: str) -> list[Transaction]:
        """
        Get transactions from 'filename' using one of the 'converters'

        Returns:
        list[Transaction]: Transactions from the 'filename' or empty
        """

        transactions = []

        self.log.info("=" * 50)
        self.log.info(f"Reading Transactions from: '{filename}'")

        with open(filename, newline="") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
            transactions.extend(self._chooseConvertion(converters, csv_reader))

        return transactions

    def getTransactions(self) -> list[Transaction]:
        """
        Retrieve all transactions from 'config.INPUT_FOLDER' folder

        Returns:
        list[Transaction]: Transactions in ascending date order
        """

        accounts_file = self._settings.ACCOUNTS_FILE
        assert accounts_file is not None

        aliases_files = self._settings.ALIASES_FILE
        assert aliases_files is not None

        accounts = Accounts(accounts_file, aliases_files)
        converters = [StatementConvertion(accounts), CreditCardConvertion(accounts)]
        self.log.debug(
            f"List of Converters: {[obj.__class__.__name__ for obj in converters]}",
        )

        input_folder = self._settings.INPUT_FOLDER
        assert input_folder is not None

        # Getting the current work directory (cwd)
        currentDir = os.getcwd()
        inputDir = currentDir + input_folder

        transactions = []

        for filename in os.listdir(inputDir):
            if filename.endswith(".csv"):
                filename = os.path.join(inputDir, filename)
                transactions.extend(self._readFile(converters, filename))

        transactions.sort(key=lambda x: x.date)

        return transactions

    def saveTransactions(self, transactions: list[Transaction]) -> None:
        """
        Saves 'transactions' to the 'config.OUTPUT_FILENAME'
        """

        output_filename = self._settings.OUTPUT_FILENAME
        assert output_filename is not None

        with open(output_filename, mode="w") as file:
            for transaction in transactions:
                file.write(transaction.exportString())

        self.log.info(f"Wrote Transactions to: '{output_filename}'")
