import logging
import os
from pprint import pformat

from src.accountsAliases import DEFAULT_ALIASES_FILE, AccountsAliases


DEFAULT_ACCOUNTS_FILE = "input/config/accounts.txt.example"


class Accounts:
    DEFAULT_BANK = "Bank"
    DEFAULT_EXPENSES = "Expenses"
    DEFAULT_LIABILITY = "Liability"
    DEFAULT_UNKNOWN = "Don't know"

    def _load_file(self, accounts_file: str) -> None:
        """
        Loads 'accounts_file' into data structure.

        Data structure format:

        "Bank":{
            "CHECKING": "Bank:Checking",
            "CREDITCARD": "Bank:CreditCard"
        }
        """
        currentDir = os.getcwd()
        filename = os.path.join(currentDir, accounts_file)

        if not os.path.isfile(filename):
            filename = os.path.join(currentDir, DEFAULT_ACCOUNTS_FILE)

        with open(filename, "r") as file:
            for line in file:
                line = line.replace("\n", "")
                parts = line.split(":")

                accountType = parts[0]
                identifier = parts[-1].upper()

                if accountType in self.accountsMap:
                    if identifier not in self.accountsMap[accountType]:
                        self.accountsMap[accountType][identifier] = line
                else:
                    self.accountsMap[accountType] = {identifier: line}

    def __init__(
        self,
        accounts_file: str = DEFAULT_ACCOUNTS_FILE,
        aliases_file: str = DEFAULT_ALIASES_FILE,
    ):
        self.accountsMap = {}
        self.aliases = AccountsAliases(aliases_file)

        self._load_file(accounts_file)

        logger = logging.getLogger(__name__)
        logger.debug(pformat(self.accountsMap))

    def getAccount(self, accountType: str, identifier: str) -> str:
        """
        Get account.

        Account Type normally is: Assets, Expenses, Liability, etc...

        Identifier represents the account itself in Ledger.

        If no account is found a default identifier is used.

        Returns:
        str: Account identifier
        """
        if accountType in self.accountsMap:
            identifier_parts = identifier.split(" ")
            while len(identifier_parts) > 0:
                identifier_small = " ".join(identifier_parts).upper()

                if identifier_small in self.aliases.aliasesMap.keys():
                    aliasIdentifier = self.aliases.getAlias(identifier_small).upper()
                    return self.accountsMap[accountType][aliasIdentifier]

                if identifier_small in self.accountsMap[accountType].keys():
                    return self.accountsMap[accountType][identifier_small]

                identifier_parts.pop()

        return f"{accountType}:{self.DEFAULT_UNKNOWN}"
