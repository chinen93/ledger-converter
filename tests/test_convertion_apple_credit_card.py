import os
from datetime import datetime

from src.accounts.accounts import AccountsManager
from src.accounts.loader import DEFAULT_ACCOUNTS_FILE, DEFAULT_ALIASES_FILE
from src.convertions.convertionAppleCreditCard import AppleCreditCardConvertion
from src.files.csv import ReadCSV
from tests.conf_log_test import BaseTestCase

CREDIT_CARD_FILENAME = "tests/test_inputs/test_apple_credit_card.csv"
ACCOUNT_CREDIT = "Bank:AppleCard"
PAYEE_DEFAULT = "Expenses:Don't know"
LIABILITY_DEFAULT = "Liability:Don't know"


class TestppleCreditCardCovnertion(BaseTestCase):
    currentDir = os.getcwd()
    csv_reader = None
    file = None
    converter = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.csv_reader = ReadCSV()

        filename = os.path.join(self.currentDir, CREDIT_CARD_FILENAME)
        self.csv_reader.readFile(filename)

        accounts = AccountsManager(DEFAULT_ACCOUNTS_FILE, DEFAULT_ALIASES_FILE)
        self.converter = AppleCreditCardConvertion(accounts)

    def tearDown(self):
        assert self.csv_reader is not None
        self.csv_reader.close()

    def test_shouldConfirmThatCanConvert(self):
        assert self.csv_reader is not None
        assert self.converter is not None

        csv_headings = self.csv_reader.headings
        self.assertTrue(self.converter.canConvert(csv_headings))

    def test_shouldChooseCreditCardConversion(self):
        assert self.csv_reader is not None
        assert self.converter is not None

        transactions = self.converter.convert(self.csv_reader)

        self.assertEqual(len(transactions), 4)

        self.assertEqual(transactions[0].date, datetime(2026, 6, 29, 0, 0))
        self.assertEqual(transactions[0].description, "AAAAA")
        self.assertEqual(transactions[0].value, 600.00)
        self.assertEqual(transactions[0].payee, ACCOUNT_CREDIT)
        self.assertEqual(transactions[0].account, LIABILITY_DEFAULT)

        self.assertEqual(transactions[1].date, datetime(2026, 6, 28, 0, 0))
        self.assertEqual(transactions[1].description, "CCCCC")
        self.assertEqual(transactions[1].value, 100.80)
        self.assertEqual(transactions[1].payee, PAYEE_DEFAULT)
        self.assertEqual(transactions[1].account, ACCOUNT_CREDIT)

        self.assertEqual(transactions[2].date, datetime(2026, 6, 27, 0, 0))
        self.assertEqual(transactions[2].description, "EEEEE")
        self.assertEqual(transactions[2].value, 12.05)
        self.assertEqual(transactions[2].payee, PAYEE_DEFAULT)
        self.assertEqual(transactions[2].account, ACCOUNT_CREDIT)

        self.assertEqual(transactions[3].date, datetime(2026, 6, 26, 0, 0))
        self.assertEqual(transactions[3].description, "GGGGG")
        self.assertEqual(transactions[3].value, 12.27)
        self.assertEqual(transactions[3].payee, PAYEE_DEFAULT)
        self.assertEqual(transactions[3].account, ACCOUNT_CREDIT)
