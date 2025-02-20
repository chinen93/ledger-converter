import csv
import os

from src.transaction import Transaction

STATEMENT_FILE_HEADER = "Description,,Summary Amt.".split(',')
CREDIT_CARD_FILE_HEADER = "Posted Date,Reference Number,Payee,Address,Amount".split(',')

def _convertStatement(csv_reader):

    # Jump statement information
    for _ in range(5):
        next(csv_reader)
    
    csv_headings = next(csv_reader)
    # print(csv_headings)

    transactions = []

    for row in csv_reader:
        # print(', '.join(row))
        
        # ['Date', 'Description', 'Amount', 'Running Bal.']
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

def _convertCredit(csv_reader):
    transactions = []

    for row in csv_reader:
        # print(', '.join(row))

        # ['Posted Date', 'Reference Number', 'Payee', 'Address', 'Amount']
        date = row[0]
        description = row[2]
        value = row[4]
        account = Transaction.ACCOUNT_CREDIT

        transaction = Transaction(date, description, value, account)
        # print(transaction.toString())
        transactions.append(transaction)

    return transactions

def _readFile(filename):
    transactions = []

    print(f"Reading Transactions from: '{filename}'")

    with open(filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        csv_headings = next(csv_reader)

        if csv_headings== STATEMENT_FILE_HEADER:
            print("Statement file")
            transactions.extend(_convertStatement(csv_reader))
        if csv_headings == CREDIT_CARD_FILE_HEADER:
            print("Credit Card file")
            # print(csv_headings)
            transactions.extend(_convertCredit(csv_reader))

    return transactions

def getTransactions():
    # Getting the current work directory (cwd)
    currentDir = os.getcwd()

    transactions = []

    for r, _, f in os.walk(currentDir):
        for file in f:
            if file.endswith(".csv"):
                filename = os.path.join(r, file)
                transactions.extend(_readFile(filename))

    transactions.sort(key=lambda x: x.date)

    return transactions

def saveTransactions(transactions):

    filename = "output.txt"
    with open(filename, mode="w") as file:
        for transaction in transactions:
            file.write(transaction.exportString())

    print(f"Wrote Transactions to: '{filename}'")

    
