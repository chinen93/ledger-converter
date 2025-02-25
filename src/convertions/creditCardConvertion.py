from src.accounts import Accounts
from src.convertions.convertion import Convertion
from src.transaction import Transaction


class CreditCardConvertion(Convertion):

    HEADER = ["Posted Date", "Reference Number", "Payee", "Address", "Amount"]

    def __init__(self, accounts):
        self.account = accounts

    def canConvert(self, heading):
        return heading == CreditCardConvertion.HEADER

    def convert(self, heading, csv_reader):
        transactions = []

        for row in csv_reader:
            date = row[0]
            description = row[2]
            value = float(row[4].replace(",", ""))

            # Transaction to buy something from someone
            if value < 0:
                value = value * -1

                account = self.account.getAccount(
                    Accounts.DEFAULT_BANK,
                    "CreditCards",
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
                    "CreditCards",
                )

            transaction = Transaction(date, description, value, payee, account)

            transactions.append(transaction)

        return transactions
