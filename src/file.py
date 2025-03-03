import csv
import logging
import os

from src.accounts import Accounts
from src.config import ACCOUNTS_FILE, ALIASES_FILE, INPUT_FOLDER, OUTPUT_FILENAME
from src.convertions.convertion import Convertion
from src.convertions.creditCardConvertion import CreditCardConvertion
from src.convertions.statementConvertion import StatementConvertion
from src.transaction import Transaction


logging = logging.getLogger(__name__)


def _chooseConvertion(
    converters: list[Convertion],
    csv_reader: csv.DictReader,
) -> list[Transaction]:
    csv_headings = next(csv_reader)

    for converter in converters:
        if converter.canConvert(csv_headings):
            return converter.convert(csv_headings, csv_reader)


def _readFile(converters: list[Convertion], filename: str) -> list[Transaction]:
    transactions = []

    logging.info(f"Reading Transactions from: '{filename}'")

    with open(filename, newline="") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        transactions.extend(_chooseConvertion(converters, csv_reader))

    return transactions


def getTransactions() -> list[Transaction]:

    accounts = Accounts(ACCOUNTS_FILE, ALIASES_FILE)
    converters = [StatementConvertion(accounts), CreditCardConvertion(accounts)]
    logging.debug(
        f"List of Converters: {[obj.__class__.__name__ for obj in converters]}",
    )

    # Getting the current work directory (cwd)
    currentDir = os.getcwd()
    inputDir = currentDir + INPUT_FOLDER

    transactions = []

    for filename in os.listdir(inputDir):
        if filename.endswith(".csv"):
            filename = os.path.join(inputDir, filename)
            transactions.extend(_readFile(converters, filename))

    transactions.sort(key=lambda x: x.date)

    return transactions


def saveTransactions(transactions: list[Transaction]) -> None:

    with open(OUTPUT_FILENAME, mode="w") as file:
        for transaction in transactions:
            file.write(transaction.exportString())

    logging.info(f"Wrote Transactions to: '{OUTPUT_FILENAME}'")
