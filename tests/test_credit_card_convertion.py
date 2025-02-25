import csv
import os
import unittest
from datetime import datetime

from src.accounts import Accounts
from src.convertions.creditCardConvertion import CreditCardConvertion


CREDIT_CARD_FILENAME = "tests/test_inputs/test_creditCard.csv"
ACCOUNT_CREDIT = "Bank:CreditCard"
PAYEE_DEFAULT = "Expenses:Don't know"
LIABILITY_DEFAULT = "Liability:Don't know"

accounts = Accounts()


class TestCreditCardConvertion(unittest.TestCase):
    currentDir = os.getcwd()
    csv_reader = None
    file = None
    converter = None

    def setUp(self):
        filename = os.path.join(self.currentDir, CREDIT_CARD_FILENAME)
        self.file = open(filename, newline="")
        self.csv_reader = csv.reader(self.file, delimiter=",", quotechar='"')
        self.converter = CreditCardConvertion(accounts)

    def tearDown(self):
        self.file.close()

    def test_shouldConfirmThatCanConvert(self):
        csv_headings = next(self.csv_reader)
        self.assertTrue(self.converter.canConvert(csv_headings))

    def test_shouldChooseCreditCardConversion(self):
        # Read the Headings
        heading = next(self.csv_reader)

        transactions = self.converter.convert(heading, self.csv_reader)

        self.assertEqual(len(transactions), 4)

        self.assertEqual(transactions[0].date, datetime(2025, 2, 20, 0, 0))
        self.assertEqual(transactions[0].description, "ABCDE")
        self.assertEqual(transactions[0].value, 60.00)
        self.assertEqual(transactions[0].payee, PAYEE_DEFAULT)
        self.assertEqual(transactions[0].account, ACCOUNT_CREDIT)

        self.assertEqual(transactions[1].date, datetime(2025, 2, 15, 0, 0))
        self.assertEqual(transactions[1].description, "FGHIJ")
        self.assertEqual(transactions[1].value, 50.50)
        self.assertEqual(transactions[1].payee, ACCOUNT_CREDIT)
        self.assertEqual(transactions[1].account, LIABILITY_DEFAULT)

        self.assertEqual(transactions[2].date, datetime(2025, 2, 10, 0, 0))
        self.assertEqual(transactions[2].description, "KLMNO")
        self.assertEqual(transactions[2].value, 25.50)
        self.assertEqual(transactions[2].payee, PAYEE_DEFAULT)
        self.assertEqual(transactions[2].account, ACCOUNT_CREDIT)

        self.assertEqual(transactions[3].date, datetime(2025, 2, 5, 0, 0))
        self.assertEqual(transactions[3].description, "PQRST, UVXWYZ")
        self.assertEqual(transactions[3].value, 1750.00)
        self.assertEqual(transactions[3].payee, ACCOUNT_CREDIT)
        self.assertEqual(transactions[3].account, LIABILITY_DEFAULT)
