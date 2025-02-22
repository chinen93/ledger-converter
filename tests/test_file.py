import csv
import os
import unittest
from datetime import datetime

from src.file import _chooseConvertion
from src.transaction import Transaction


STATEMENT_FILENAME = "tests/test_inputs/test_statement.csv"
CREDIT_CARD_FILENAME = "tests/test_inputs/test_creditCard.csv"


class TestFile(unittest.TestCase):
    currentDir = os.getcwd()

    def test_shouldChooseStatementConversion(self):

        transactions = []

        filename = os.path.join(self.currentDir, STATEMENT_FILENAME)
        with open(filename, newline="") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
            transactions.extend(_chooseConvertion(csv_reader))

        self.assertEqual(len(transactions), 3)

        self.assertEqual(transactions[0].date, datetime(2025, 2, 13, 0, 0))
        self.assertEqual(transactions[0].description, "ABCDEFGH")
        self.assertEqual(transactions[0].value, 1200.00)
        self.assertEqual(transactions[0].account, Transaction.LIABILITY_DEFAULT)
        self.assertEqual(transactions[0].payee, Transaction.ACCOUNT_CHECKING)

        self.assertEqual(transactions[1].date, datetime(2025, 2, 16, 0, 0))
        self.assertEqual(transactions[1].description, "IJKLMNOP,123")
        self.assertEqual(transactions[1].value, 1234.56)
        self.assertEqual(transactions[1].account, Transaction.ACCOUNT_CHECKING)
        self.assertEqual(transactions[1].payee, Transaction.PAYEE_DEFAULT)

        self.assertEqual(transactions[2].date, datetime(2025, 2, 20, 0, 0))
        self.assertEqual(transactions[2].description, "QRSTUVXW")
        self.assertEqual(transactions[2].value, 200.00)
        self.assertEqual(transactions[2].account, Transaction.LIABILITY_DEFAULT)
        self.assertEqual(transactions[2].payee, Transaction.ACCOUNT_CHECKING)

    def test_shouldChooseCreditCardConversion(self):

        transactions = []

        filename = os.path.join(self.currentDir, CREDIT_CARD_FILENAME)
        with open(filename, newline="") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
            transactions.extend(_chooseConvertion(csv_reader))

        self.assertEqual(len(transactions), 4)

        self.assertEqual(transactions[0].date, datetime(2025, 2, 20, 0, 0))
        self.assertEqual(transactions[0].description, "ABCDE")
        self.assertEqual(transactions[0].value, 60.00)
        self.assertEqual(transactions[0].account, Transaction.ACCOUNT_CREDIT)
        self.assertEqual(transactions[0].payee, Transaction.PAYEE_DEFAULT)

        self.assertEqual(transactions[1].date, datetime(2025, 2, 15, 0, 0))
        self.assertEqual(transactions[1].description, "FGHIJ")
        self.assertEqual(transactions[1].value, 50.50)
        self.assertEqual(transactions[1].account, Transaction.LIABILITY_DEFAULT)
        self.assertEqual(transactions[1].payee, Transaction.ACCOUNT_CREDIT)

        self.assertEqual(transactions[2].date, datetime(2025, 2, 10, 0, 0))
        self.assertEqual(transactions[2].description, "KLMNO")
        self.assertEqual(transactions[2].value, 25.50)
        self.assertEqual(transactions[2].account, Transaction.ACCOUNT_CREDIT)
        self.assertEqual(transactions[2].payee, Transaction.PAYEE_DEFAULT)

        self.assertEqual(transactions[3].date, datetime(2025, 2, 5, 0, 0))
        self.assertEqual(transactions[3].description, "PQRST, UVXWYZ")
        self.assertEqual(transactions[3].value, 1750.00)
        self.assertEqual(transactions[3].account, Transaction.LIABILITY_DEFAULT)
        self.assertEqual(transactions[3].payee, Transaction.ACCOUNT_CREDIT)
