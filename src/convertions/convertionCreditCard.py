from src.accounts.accounts import AccountsManager
from src.convertions.convertion import ConvertionStrategy
from src.files.csv import ReadCSV
from src.models.transaction import Transaction


class CreditCardConvertion(ConvertionStrategy):

    HEADER = ["Posted Date", "Reference Number", "Payee", "Address", "Amount"]

    def __init__(self, accounts: AccountsManager):
        self.account = accounts

    def canConvert(self, heading: list[str]) -> bool:
        return heading == CreditCardConvertion.HEADER

    def convert(
        self,
        heading: list[str],
        csv_reader: ReadCSV,
    ) -> list[Transaction]:
        transactions = []

        for row in csv_reader:
            date = row[0]
            description = row[2]
            value = float(row[4].replace(",", ""))

            # Transaction to buy something from someone
            if value < 0:
                value = value * -1

                account = self.account.getAccount(
                    AccountsManager.DEFAULT_BANK,
                    "CreditCard",
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
                    "CreditCard",
                )

            transaction = Transaction(date, description, value, payee, account)

            transactions.append(transaction)

        return transactions
