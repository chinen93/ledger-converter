import csv
import os

from config.logging import get_logger
from config.settings import get_settings
from src.accounts.accounts import Accounts
from src.convertions.convertion import ConvertionStrategy
from src.convertions.convertionCreditCard import CreditCardConvertion
from src.convertions.convertionStatement import StatementConvertion
from src.convertions.pipeline import ConvertionPipeline
from src.files.csv import ReadCSV
from src.files.discover import Discover
from src.models.transaction import Transaction


class LedgerConversionWorkflow:

    def __init__(self):
        self._settings = get_settings()
        self.log = get_logger(__name__)

    def _chooseConvertion(
        self,
        converters: list[ConvertionStrategy],
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

    def _readFile(self, converters: list[ConvertionStrategy], filename: str) -> list[Transaction]:
        """
        Get transactions from 'filename' using one of the 'converters'

        Returns:
        list[Transaction]: Transactions from the 'filename' or empty
        """

        transactions = []

        self.log.info(f"Reading Transactions from: '{filename}'")

        with open(filename, newline="") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
            transactions.extend(self._chooseConvertion(converters, csv_reader))

        return transactions

    def loadTransactions(self) -> list[Transaction]:
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

        # convertionPipeline = ConvertionPipeline(accounts)

        converters = [StatementConvertion(accounts), CreditCardConvertion(accounts)]
        self.log.debug(
            f"List of Converters: {[obj.__class__.__name__ for obj in converters]}",
        )

        discover = Discover()
        filenames = discover.discoverFilenames()
        csv_reader = ReadCSV()

        transactions = []
        for filename in filenames:
            
            csv_reader.readFile(filename)
            print(csv_reader.line)
            csv_reader.close()

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
