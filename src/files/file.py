from config.logging import get_logger
from config.settings import get_settings
from src.accounts.accounts import Accounts
from src.convertions.pipeline import ConvertionPipeline
from src.files.csv import ReadCSV
from src.files.discover import Discover
from src.models.transaction import Transaction


class LedgerConversionWorkflow:

    def __init__(self):
        self._settings = get_settings()
        self.log = get_logger(__name__)

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
        convertionPipeline = ConvertionPipeline(accounts)

        discover = Discover()
        filenames = discover.discoverFilenames()
        csv_reader = ReadCSV()

        transactions = []
        for filename in filenames:

            csv_reader.readFile(filename)
            transactions.extend(convertionPipeline.convert(csv_reader))
            csv_reader.close()

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
