from config.logging import get_logger
from src.accounts.aliases import AliasManager
from src.accounts.loader import AccountLoader
from src.accounts.lookup import AccountsLookup


class AccountsManager:

    DEFAULT_BANK = "Bank"
    DEFAULT_EXPENSES = "Expenses"
    DEFAULT_LIABILITY = "Liability"

    def __init__(
        self,
        accounts_file: str,
        aliases_file: str,
    ):
        self.log = get_logger(__name__)

        self.aliasesManager = AliasManager(aliases_file)

        accounts = AccountLoader.load(accounts_file)
        self.lookup = AccountsLookup(accounts, self.aliasesManager.lookup)

    def hasAccount(self, accountType: str, identifier: str) -> bool:
        """
        Return TRUE if account map has 'accountType' and 'identifier'
        """
        return self.lookup.hasAccount(accountType, identifier)

    def getAccount(self, accountType: str, identifier: str) -> str:
        """
        Get account.

        Account Type normally is: Assets, Expenses, Liability, etc...

        Identifier represents the account itself in Ledger.

        If no account is found a default identifier is used.

        Returns:
        str: Account identifier
        """
        return self.lookup.getAccount(accountType, identifier)
