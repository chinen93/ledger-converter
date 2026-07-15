from config.logging import setup_logging, get_logger
from src.workflows import LedgerConversionWorkflow

def mainConverter() -> None:
    """
    Main Converter program function
    """
    setup_logging(testing=False)

    log = get_logger(__name__)
    log.info("Converter Program Started")

    workflow = LedgerConversionWorkflow()

    log.info("Get Transactions")
    transactions = workflow.loadTransactions()

    log.info("Output Transactions in the Right Format")
    workflow.saveTransactions(transactions)

    log.info("Program Ended")

def mainReports() -> None:
    """
    Main Reports program function
    """
    setup_logging(testing=False)

    log = get_logger(__name__)
    log.info("Report Program Started")

    log.info("Program Ended")