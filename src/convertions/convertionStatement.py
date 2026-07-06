from src.accounts.accounts import AccountsManager
from src.convertions.convertion import ConvertionStrategy
from src.files.csv import ReadCSV
from src.models.transaction import Transaction


class StatementConvertion(ConvertionStrategy):

    FIRST_LINE = ["Description", "", "Summary Amt."]
    HEADER = ["Date", "Description", "Amount", "Running Bal."]

    def __init__(self, accounts: AccountsManager):
        self.account = accounts

    def canConvert(self, heading: list[str]) -> bool:
        return heading == StatementConvertion.FIRST_LINE

    def convert(
        self,
        heading: list[str],
        csv_reader: ReadCSV,
    ) -> list[Transaction]:

        csv_reader.moveBeginData(StatementConvertion.HEADER)

        transactions = []

        for row in csv_reader:

            date = row[0]
            description = row[1]
            value = float(row[2].replace(",", ""))

            # Transaction to buy something from someone
            if value < 0:
                value = value * -1

                account = self.account.getAccount(
                    AccountsManager.DEFAULT_BANK,
                    "Checking",
                )
                payee = self.account.getAccount(
                    AccountsManager.DEFAULT_EXPENSES,
                    description,
                )

            # Transaction to pay one of my accounts
            else:
                self.value = value
                account = self.account.getAccount(
                    AccountsManager.DEFAULT_LIABILITY,
                    description,
                )
                payee = self.account.getAccount(
                    AccountsManager.DEFAULT_BANK,
                    "Checking",
                )

            if description.startswith("Beginning balance"):
                continue

            transaction = Transaction(date, description, value, payee, account)
            transactions.append(transaction)

        return transactions
