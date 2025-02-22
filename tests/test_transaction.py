import unittest

from src.transaction import Transaction


TEST_DATE = "02/21/2025"
TEST_DESCRIPTION = "TEST DESCRIPTION"


class TestTransaction(unittest.TestCase):

    def test_shouldCreatePurchaseTransaction(self):

        values = [
            ("-123.45", 123.45),
            ("-1,234.56", 1234.56),
            ("-1234.56", 1234.56),
        ]

        for value, exp_value in values:
            transaction = Transaction(
                date=TEST_DATE,
                description=TEST_DESCRIPTION,
                value=value,
                account=Transaction.ACCOUNT_CHECKING,
                payee=Transaction.PAYEE_DEFAULT,
            )

            expected = (
                f"2025-02-21       TEST DESCRIPTION\n"
                f"    Expenses:Don't know                            ${exp_value}\n"  # noqa: E501 (Long Line)
                f"    Bank:Checking\n\n"
            )

            self.assertEqual(
                transaction.exportString(),
                expected,
                f"Value={value}",
            )

    def test_shouldCreatePaymentAccountTransaction(self):
        values = [
            ("123.45", 123.45),
            ("1,234.56", 1234.56),
            ("1234.56", 1234.56),
        ]

        for value, exp_value in values:
            transaction = Transaction(
                date=TEST_DATE,
                description=TEST_DESCRIPTION,
                value=value,
                account=Transaction.ACCOUNT_CHECKING,
                payee=Transaction.PAYEE_DEFAULT,
            )

            expected = (
                f"2025-02-21       TEST DESCRIPTION\n"
                f"    Bank:Checking                            ${exp_value}\n"
                f"    Liability:Don't know\n\n"
            )

            self.assertEqual(
                transaction.exportString(),
                expected,
                f"Value={value}",
            )
