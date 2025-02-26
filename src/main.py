import logging
import logging.config
import os

from src.file import getTransactions, saveTransactions


def setup_logging() -> None:
    """Load logging configuration"""
    currentDir = os.getcwd()
    log_dir = f"{currentDir}/logs"
    config_path = f"{log_dir}/config"

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": f"{log_dir}/ledger_converter.log"},
    )


def main() -> None:
    setup_logging()

    logger = logging.getLogger(__name__)

    logger.info("Program started")

    logger.info("Get Transactions")
    transactions = getTransactions()

    logger.info("Output Transactions in the Right Format")
    saveTransactions(transactions)

    logger.info("Program Ended")
