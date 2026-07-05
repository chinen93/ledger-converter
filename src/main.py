from config.logging import setup_logging, get_logger
from src.files.file import LedgerConversionWorkflow


def main() -> None:
    """
    Main program function
    """
    setup_logging(testing=False)

    log = get_logger(__name__)
    log.info("Program started")

    workflow = LedgerConversionWorkflow()

    log.info("Get Transactions")
    transactions = workflow.loadTransactions()

    log.info("Output Transactions in the Right Format")
    workflow.saveTransactions(transactions)

    log.info("Program Ended")
