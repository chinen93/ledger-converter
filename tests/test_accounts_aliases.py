from src.accounts.aliases import AliasManager
from src.accounts.loader import DEFAULT_ALIASES_FILE
from tests.conf_log_test import BaseTestCase


class TestAccountsAliases(BaseTestCase):

    aliases = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.aliases = AliasManager(DEFAULT_ALIASES_FILE)

    def test_shouldCreateAccountsAliases(self):

        expected = {
            "CREDIT CARD": "CreditCard",
            "CHECK": "Checking",
            "CHECKS": "Checking",
        }

        self.assertListEqual(list(self.aliases.lookup.aliases.keys()), list(expected.keys()))

    def test_shouldGetAccountsAliases(self):

        tests = [
            ("Checking", "CHECKING"),
            ("Credit Card", "CREDITCARD"),
            ("Check", "CHECKING"),
            ("Checks", "CHECKING"),
        ]

        for identifier, expected in tests:
            testString = f"{identifier} to {expected}"
            self.assertEqual(
                self.aliases.getAlias(identifier),
                expected,
                testString,
            )
