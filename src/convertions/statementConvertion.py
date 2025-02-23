from src.convertions.convertion import Convertion
from src.transaction import Transaction


class StatementConvertion(Convertion):

    FIRST_LINE = ["Description", "", "Summary Amt."]
    HEADER = ["Date", "Description", "Amount", "Running Bal."]

    def canConvert(heading):
        return heading == StatementConvertion.FIRST_LINE

    def convert(heading, csv_reader):
        # Move reader cursor until the beginning of data
        row = heading
        while row != StatementConvertion.HEADER:
            row = next(csv_reader)
        row = next(csv_reader)

        transactions = []

        for row in csv_reader:
            date = row[0]
            description = row[1]
            value = row[2]
            account = Transaction.ACCOUNT_CHECKING

            if description.startswith("Beginning balance"):
                continue

            transaction = Transaction(date, description, value, account)
            # print(transaction.toString())
            transactions.append(transaction)

        return transactions
