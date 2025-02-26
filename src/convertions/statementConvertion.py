from csv import DictReader

from src.accounts import Accounts
from src.convertions.convertion import Convertion
from src.transaction import Transaction


class StatementConvertion(Convertion):

    FIRST_LINE = ["Description", "", "Summary Amt."]
    HEADER = ["Date", "Description", "Amount", "Running Bal."]

    def __init__(self, accounts: Accounts):
        self.account = accounts

    def canConvert(self, heading: str) -> bool:
        return heading == StatementConvertion.FIRST_LINE

    def convert(
        self,
        heading: str,
        csv_reader: DictReader,
    ) -> list[Transaction]:

        # Move reader cursor until the beginning of data
        row = heading
        while row != StatementConvertion.HEADER:
            row = next(csv_reader)
        row = next(csv_reader)

        transactions = []

        for row in csv_reader:
            date = row[0]
            description = row[1]
            value = float(row[2].replace(",", ""))

            # Transaction to buy something from someone
            if value < 0:
                value = value * -1

                account = self.account.getAccount(
                    Accounts.DEFAULT_BANK,
                    "Checking",
                )
                payee = self.account.getAccount(
                    Accounts.DEFAULT_EXPENSES,
                    description,
                )

            # Transaction to pay one of my accounts
            else:
                self.value = value
                account = self.account.getAccount(
                    Accounts.DEFAULT_LIABILITY,
                    description,
                )
                payee = self.account.getAccount(
                    Accounts.DEFAULT_BANK,
                    "Checking",
                )

            if description.startswith("Beginning balance"):
                continue

            transaction = Transaction(date, description, value, payee, account)
            transactions.append(transaction)

        return transactions
