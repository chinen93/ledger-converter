from src.file import getTransactions, saveTransactions


def main():
    print("====== Get Transactions")
    transactions = getTransactions()

    print("====== Output Transactions in the Right Format")
    saveTransactions(transactions)
