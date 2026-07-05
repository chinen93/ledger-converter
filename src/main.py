from config.logging import setup_logging, get_logger
from src.file import HandleTransactions


def main() -> None:
    """
    Main program function
    """
    setup_logging(testing=False)

    log = get_logger(__name__)
    log.info("Program started")

    handleTransactions = HandleTransactions()

    log.info("Get Transactions")
    transactions = handleTransactions.getTransactions()

    log.info("Output Transactions in the Right Format")
    handleTransactions.saveTransactions(transactions)

    log.info("Program Ended")
