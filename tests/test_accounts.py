import unittest

from src.accounts import DEFAULT_ACCOUNTS_FILE, Accounts
from src.accountsAliases import DEFAULT_ALIASES_FILE


class TestAccounts(unittest.TestCase):

    accounts = None

    def setUp(self):
        self.accounts = Accounts(
            accounts_file=DEFAULT_ACCOUNTS_FILE,
            aliases_file=DEFAULT_ALIASES_FILE,
        )

    def test_shouldCreateAccounts(self):

        expected = {
            "Bank": {
                "CHECKING": "Bank:Checking",
                "CREDITCARD": "Bank:CreditCard",
            },
            "Liability": {"TEST": "Liability:Test"},
        }

        self.assertDictEqual(self.accounts.accountsMap, expected)

        wrong_file_accounts = Accounts("INVALID_FILE")
        self.assertDictEqual(wrong_file_accounts.accountsMap, expected)

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
