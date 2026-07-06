from config.logging import get_logger
from src.accounts.accounts import AccountsManager
from src.convertions.convertion import ConvertionStrategy
from src.convertions.convertionCreditCard import CreditCardConvertion
from src.convertions.convertionStatement import StatementConvertion
from src.files.csv import ReadCSV
from src.models.transaction import Transaction


class ConvertionPipeline:

    STRATEGIES = (StatementConvertion, CreditCardConvertion)

    def __init__(self, accounts: AccountsManager):
        self.log = get_logger(__name__)
        self.strategies: list[ConvertionStrategy] = [
            strategy_class(accounts) for strategy_class in self.STRATEGIES
        ]

        self.log.debug(
            f"List of Converters: {[obj.__class__.__name__ for obj in self.strategies]}",
        )

    def convert(self, csv_reader: ReadCSV) -> list[Transaction]:

        transactions: list[Transaction] = []

        csv_headings = csv_reader.headings

        for converter in self.strategies:
            if converter.canConvert(csv_headings):
                return converter.convert(csv_reader)

        return transactions
