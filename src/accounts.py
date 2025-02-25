import os


ACCOUNTS_FILE = "input/accounts.txt"
DEFAULT_ACCOUNTS_FILE = "input/accounts.txt.example"


class Accounts:
    DEFAULT_BANK = "Bank"
    DEFAULT_EXPENSES = "Expenses"
    DEFAULT_LIABILITY = "Liability"
    DEFAULT_UNKNOWN = "Don't know"

    def __init__(self, accounts_file=ACCOUNTS_FILE):
        self.accountsMap = {}

        currentDir = os.getcwd()
        filename = os.path.join(currentDir, accounts_file)

        if not os.path.isfile(filename):
            filename = os.path.join(currentDir, DEFAULT_ACCOUNTS_FILE)

        with open(filename, "r") as file:
            for line in file:
                line = line.replace("\n", "")
                parts = line.split(":")

                accountType = parts[0]
                identifier = parts[-1]

                if accountType in self.accountsMap:
                    if identifier.upper() not in self.accountsMap[accountType]:
                        self.accountsMap[accountType][identifier.upper()] = line
                else:
                    self.accountsMap[accountType] = {identifier.upper(): line}

        # print(self.accountsMap)

    def getAccount(self, accountType, identifier):
        if accountType in self.accountsMap:
            for accounsMapKey in self.accountsMap[accountType].keys():
                if accounsMapKey in identifier.upper():
                    return self.accountsMap[accountType][accounsMapKey]

        return f"{accountType}:{self.DEFAULT_UNKNOWN}"
