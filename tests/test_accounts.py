from src.accounts.accounts import AccountsManager
from src.accounts.loader import DEFAULT_ACCOUNTS_FILE, DEFAULT_ALIASES_FILE
from tests.conf_log_test import BaseTestCase


class TestAccounts(BaseTestCase):

    accounts = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.accounts = AccountsManager(
            accounts_file=DEFAULT_ACCOUNTS_FILE,
            aliases_file=DEFAULT_ALIASES_FILE,
        )

    def test_shouldCreateAccounts(self):

        expected = {
            "Bank:CHECKING": "Bank:Checking",
            "Bank:CREDITCARD": "Bank:CreditCard",
            "Liability:TEST": "Liability:Test",
        }

        self.assertListEqual(list(self.accounts.lookup.accounts.keys()), list(expected.keys()))
        for expectedKey, expectedValue in expected.items():
            keySplit = expectedKey.split(":")
            value = self.accounts.getAccount(keySplit[0], keySplit[1])
            self.assertEqual(value, expectedValue)

    def test_shouldGetAccounts(self):

        tests = [
            ("Bank", "Checking", "Bank:Checking"),
            ("Bank", "CHECKING", "Bank:Checking"),
            ("Bank", "Check", "Bank:Checking"),
            ("Bank", "CHECK", "Bank:Checking"),
            ("Bank", "CreditCard", "Bank:CreditCard"),
            ("Bank", "CreditCard ABC DEF", "Bank:CreditCard"),
            ("Bank", "CREDITCARD", "Bank:CreditCard"),
            ("Bank", "ANYTHING", "Bank:Don't know"),
            ("Expenses", "ANYTHING", "Expenses:Don't know"),
            ("Liability", "ANYTHING", "Liability:Don't know"),
        ]

        for accountType, identifier, expected in tests:
            testString = f"{accountType}, {identifier} to {expected}"
            self.assertEqual(
                self.accounts.getAccount(accountType, identifier),
                expected,
                testString,
            )
