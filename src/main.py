from logging import getLogger

from config.logging import setup_logging
from src.file import HandleTransactions


def main() -> None:
    """
    Main program function
    """
    setup_logging(testing=False)    

    log = getLogger(__name__)
    log.info("Program started")

    handleTransactions = HandleTransactions()

    log.info("Get Transactions")
    transactions = handleTransactions.getTransactions()

    log.info("Output Transactions in the Right Format")
    handleTransactions.saveTransactions(transactions)

    log.info("Program Ended")
