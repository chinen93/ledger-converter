import logging
import os
from pprint import pformat


ALIASES_FILE = "input/accounts_aliases.txt"
DEFAULT_ALIASES_FILE = "input/accounts_aliases.txt.example"


class AccountsAliases:
    def __init__(self, aliases_file: str = ALIASES_FILE):
        self.aliasesMap = {}

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

        logger = logging.getLogger(__name__)
        logger.debug(pformat(self.aliasesMap))

    def getAlias(self, identifier: str) -> str:
        identifier = identifier.upper()
        if identifier in self.aliasesMap:
            return self.aliasesMap[identifier]

        return identifier
