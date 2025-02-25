import unittest

from src.transaction import Transaction


TEST_DATE = "02/21/2025"
TEST_DESCRIPTION = "TEST DESCRIPTION"
TEST_PAYEE = "Expenses:Don't know"
TEST_ACCOUNT = "Bank:Checking"


class TestTransaction(unittest.TestCase):

    def test_shouldCreatePurchaseTransaction(self):

        values = [
            (123.45, 123.45),
            (-1234.56, -1234.56),
        ]

        for value, exp_value in values:
            transaction = Transaction(
                date=TEST_DATE,
                description=TEST_DESCRIPTION,
                value=value,
                payee=TEST_PAYEE,
                account=TEST_ACCOUNT,
            )

            expected = (
                f"2025-02-21       {TEST_DESCRIPTION}\n"
                f"    {TEST_PAYEE}                            ${exp_value}\n"  # noqa: E501 (Long Line)
                f"    {TEST_ACCOUNT}\n\n"
            )

            self.assertEqual(
                transaction.exportString(),
                expected,
                f"Value={value}",
            )
