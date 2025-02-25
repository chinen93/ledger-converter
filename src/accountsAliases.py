import os


ALIASES_FILE = "input/accounts_aliases.txt"
DEFAULT_ALIASES_FILE = "input/accounts_aliases.txt.example"


class AccountsAliases:
    def __init__(self, aliases_file=ALIASES_FILE):
        self.aliases = {}

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

                self.aliases[identifier] = alias

    def getAlias(self, identifier):
        identifier = identifier.upper()
        if identifier in self.aliases:
            return self.aliases[identifier]

        return identifier
