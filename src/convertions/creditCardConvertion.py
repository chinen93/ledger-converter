from src.convertions.convertion import Convertion
from src.transaction import Transaction


class CreditCardConvertion(Convertion):

    HEADER = ["Posted Date", "Reference Number", "Payee", "Address", "Amount"]

    def canConvert(heading):
        return heading == CreditCardConvertion.HEADER

    def convert(heading, csv_reader):
        transactions = []

        for row in csv_reader:
            date = row[0]
            description = row[2]
            value = row[4]
            account = Transaction.ACCOUNT_CREDIT

            transaction = Transaction(date, description, value, account)

            transactions.append(transaction)

        return transactions
