import csv
import os

from src.accounts import ACCOUNTS_FILE, Accounts
from src.accountsAliases import ALIASES_FILE
from src.convertions.creditCardConvertion import CreditCardConvertion
from src.convertions.statementConvertion import StatementConvertion


accounts = Accounts(ACCOUNTS_FILE, ALIASES_FILE)


def _chooseConvertion(csv_reader):
    csv_headings = next(csv_reader)

    converters = [StatementConvertion(accounts), CreditCardConvertion(accounts)]

    for converter in converters:
        if converter.canConvert(csv_headings):
            return converter.convert(csv_headings, csv_reader)


def _readFile(filename):
    transactions = []

    print(f"Reading Transactions from: '{filename}'")

    with open(filename, newline="") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        transactions.extend(_chooseConvertion(csv_reader))

    return transactions


def getTransactions():
    # Getting the current work directory (cwd)
    currentDir = os.getcwd()
    inputDir = currentDir + "/input/"

    transactions = []

    for filename in os.listdir(inputDir):
        if filename.endswith(".csv"):
            filename = os.path.join(inputDir, filename)
            transactions.extend(_readFile(filename))

    transactions.sort(key=lambda x: x.date)

    return transactions


def saveTransactions(transactions):

    filename = "output.txt"
    with open(filename, mode="w") as file:
        for transaction in transactions:
            file.write(transaction.exportString())

    print(f"Wrote Transactions to: '{filename}'")
