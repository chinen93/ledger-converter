import logging
import os
from pprint import pformat

from src.config import ALIASES_FILE


DEFAULT_ALIASES_FILE = "input/config/accounts_aliases.txt.example"


class AccountsAliases:
    """
    Accounts Aliases map

    Making it easier to find an account using an aliases.

    Multiple aliases can point to the same account.
    """

    def _load_file(self, aliases_file) -> None:
        """
        Loads 'aliases_file' into a map

        Account:Alias

        So when an alias is found the correct account is sent to the transaction
        """
        currentDir = os.getcwd()
        filename = os.path.join(currentDir, aliases_file)

        if not os.path.isfile(filename):
            filename = os.path.join(currentDir, DEFAULT_ALIASES_FILE)

        with open(filename, "r") as file:
            for line in file:
                line = line.replace("\n", "")
                parts = line.split(":")

                identifier = parts[0].strip().upper()
                alias = parts[1].strip()

                self.aliasesMap[identifier] = alias

    def __init__(self, aliases_file: str = ALIASES_FILE):
        self.aliasesMap = {}

        self._load_file(aliases_file)

        logger = logging.getLogger(__name__)
        logger.debug(pformat(self.aliasesMap))

    def getAlias(self, identifier: str) -> str:
        """
        Get alias from 'identifier'

        Returns:
        str: Account or 'identifier'
        """
        identifier = identifier.upper()
        if identifier in self.aliasesMap:
            return self.aliasesMap[identifier]

        return identifier
