from src.accounts.accounts import AccountsManager
from src.accounts.loader import DEFAULT_ACCOUNTS_FILE, DEFAULT_ALIASES_FILE
from src.convertions.convertion import ConvertionStrategy, ParsedRow
from tests.conf_log_test import BaseTestCase


class DummyConvertion(ConvertionStrategy):

    def __init__(self, accounts: AccountsManager):
        super().__init__(accounts, "Checking")

    def canConvert(self, heading: list[str]) -> bool:
        return True

    def move_to_data(self, csv_reader) -> None:
        return None

    def parse_row(self, row: list[str]) -> ParsedRow:
        return ParsedRow(date=row[0], description=row[1], amount=float(row[2]))

    def should_skip(self, description: str, value: float, row: list[str]) -> bool:
        return False


class TestCreditCardConvertion(BaseTestCase):

    def test_shouldCreateTransactionFromSharedConversionLogic(self):
        accounts = AccountsManager(DEFAULT_ACCOUNTS_FILE, DEFAULT_ALIASES_FILE)
        converter = DummyConvertion(accounts)

        transaction = converter.build_transaction("02/13/2025", "Groceries", -123.45)

        self.assertEqual(transaction.description, "Groceries")
        self.assertEqual(transaction.value, 123.45)
        self.assertEqual(transaction.payee, "Expenses:Don't know")
        self.assertEqual(transaction.account, "Bank:Checking")

    def test_shouldCreateTransactionFromSharedConversionLogic_1(self):
        accounts = AccountsManager(DEFAULT_ACCOUNTS_FILE, DEFAULT_ALIASES_FILE)
        converter = DummyConvertion(accounts)

        transaction = converter.build_transaction("02/13/2025", "Salary", 123.45)

        self.assertEqual(transaction.description, "Salary")
        self.assertEqual(transaction.value, 123.45)
        self.assertEqual(transaction.payee, "Bank:Checking")
        self.assertEqual(transaction.account, "Liability:Don't know")
