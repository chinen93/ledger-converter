from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.accounts.accounts import AccountsManager
from src.files.csv import ReadCSV
from src.models.transaction import Transaction


@dataclass
class ParsedRow:
    date: str
    description: str
    amount: float


class ConvertionStrategy(ABC):

    def __init__(self, accounts: AccountsManager, bank_account: str):
        self.accounts = accounts
        self.bank_account = bank_account

    @abstractmethod
    def canConvert(self, heading: list[str]) -> bool:
        """
        Returns TRUE if conversion class can convert file.
        """
        raise NotImplementedError

    @abstractmethod
    def move_to_data(self, csv_reader: ReadCSV) -> None:
        """Move the CSV reader to the first transaction row."""
        raise NotImplementedError

    @abstractmethod
    def parse_row(self, row: list[str]) -> ParsedRow:
        """Extract date, description and amount from a CSV row."""
        raise NotImplementedError

    def should_skip(self, description: str, value: float, row: list[str]) -> bool:
        """Allow a converter to ignore certain rows."""
        return False

    def convert(
        self,
        csv_reader: ReadCSV,
    ) -> list[Transaction]:
        """
        Conversion of file into transaction list.

        Returns:
        list[Transaction]: All transactions in file
        """
        self.move_to_data(csv_reader)

        transactions: list[Transaction] = []

        for row in csv_reader:
            parsedRow = self.parse_row(row)

            if self.should_skip(parsedRow.description, parsedRow.amount, row):
                continue

            transactions.append(
                self.build_transaction(parsedRow.date, parsedRow.description, parsedRow.amount)
            )

        return transactions

    def build_transaction(self, date: str, description: str, value: float) -> Transaction:
        normalized_value = abs(value)
        payee, account = self._get_accounts(description, value)

        return Transaction(date, description, normalized_value, payee, account)

    def _get_accounts(self, description: str, value: float) -> tuple[str, str]:

        if value < 0:
            payee = self.accounts.getAccount(
                AccountsManager.DEFAULT_EXPENSES,
                description,
            )
            account = self.accounts.getAccount(
                AccountsManager.DEFAULT_BANK,
                self.bank_account,
            )
            return (payee, account)

        payee = self.accounts.getAccount(
            AccountsManager.DEFAULT_BANK,
            self.bank_account,
        )
        account = self.accounts.getAccount(
            AccountsManager.DEFAULT_LIABILITY,
            description,
        )
        return (payee, account)
