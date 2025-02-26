import logging
import os
from pprint import pformat

from src.accountsAliases import DEFAULT_ALIASES_FILE, AccountsAliases


ACCOUNTS_FILE = "input/accounts.txt"
DEFAULT_ACCOUNTS_FILE = "input/accounts.txt.example"


class Accounts:
    DEFAULT_BANK = "Bank"
    DEFAULT_EXPENSES = "Expenses"
    DEFAULT_LIABILITY = "Liability"
    DEFAULT_UNKNOWN = "Don't know"

    def __init__(
        self,
        accounts_file: str = DEFAULT_ACCOUNTS_FILE,
        aliases_file: str = DEFAULT_ALIASES_FILE,
    ):
        self.accountsMap = {}
        self.aliases = AccountsAliases(aliases_file)

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

        logger = logging.getLogger(__name__)
        logger.debug(pformat(self.accountsMap))

    def getAccount(self, accountType: str, identifier: str) -> str:
        if accountType in self.accountsMap:

            for aliasKey in self.aliases.aliasesMap.keys():
                if aliasKey in identifier.upper():
                    aliasIdentifier = self.aliases.getAlias(aliasKey).upper()
                    return self.accountsMap[accountType][aliasIdentifier]

            for accounsMapKey in self.accountsMap[accountType].keys():
                if accounsMapKey in identifier.upper():
                    return self.accountsMap[accountType][accounsMapKey]

        return f"{accountType}:{self.DEFAULT_UNKNOWN}"
