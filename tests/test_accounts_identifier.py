import unittest

from src.accountsAliases import DEFAULT_ALIASES_FILE, AccountsAliases


class TestAccountsAliases(unittest.TestCase):

    aliases = None

    def setUp(self):
        self.aliases = AccountsAliases(DEFAULT_ALIASES_FILE)

    def test_shouldCreateAccountsAliases(self):

        expected = {
            "CREDIT CARD": "CreditCard",
            "CHECK": "Checking",
            "CHECKS": "Checking",
        }

        self.assertDictEqual(self.aliases.aliases, expected)

        wrong_file_accounts = AccountsAliases("INVALID_FILE")
        self.assertDictEqual(wrong_file_accounts.aliases, expected)

    def test_shouldGetAccountsAliases(self):

        tests = [
            ("Checking", "CHECKING"),
            ("Credit Card", "CreditCard"),
            ("Check", "Checking"),
            ("Checks", "Checking"),
        ]

        for identifier, expected in tests:
            testString = f"{identifier} to {expected}"
            self.assertEqual(
                self.aliases.getAlias(identifier),
                expected,
                testString,
            )
