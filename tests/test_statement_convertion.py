import csv
import os
import unittest
from datetime import datetime

from src.convertions.statementConvertion import StatementConvertion
from src.transaction import Transaction


STATEMENT_FILENAME = "tests/test_inputs/test_statement.csv"


class TestStatementConvertion(unittest.TestCase):
    currentDir = os.getcwd()
    csv_reader = None
    file = None

    def setUp(self):
        filename = os.path.join(self.currentDir, STATEMENT_FILENAME)
        self.file = open(filename, newline="")
        self.csv_reader = csv.reader(self.file, delimiter=",", quotechar='"')

    def tearDown(self):
        self.file.close()

    def test_shouldConfirmThatCanConvert(self):
        csv_headings = next(self.csv_reader)
        self.assertTrue(StatementConvertion.canConvert(csv_headings))

    def test_shouldChooseStatementConversion(self):
        # Read the Headings
        heading = next(self.csv_reader)

        transactions = StatementConvertion.convert(heading, self.csv_reader)

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
