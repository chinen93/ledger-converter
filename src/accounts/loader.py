import os

from src.accounts.entities import Accounts, Aliases
from src.models.account import Account, Alias

DEFAULT_ACCOUNTS_FILE = "input/config/accounts.txt.example"
DEFAULT_ALIASES_FILE = "input/config/accounts_aliases.txt.example"


class AccountLoader:

    @classmethod
    def load(cls, accounts_file: str) -> Accounts:
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

        accounts = Accounts()

        with open(filename, "r") as file:
            for line in file:
                line = line.replace("\n", "")
                parts = line.split(":")

                accountType = parts[0]
                identifier = parts[-1].upper()

                account = Account(accountType, identifier, line)
                accounts.add(account)

        return accounts


class AliasesLoader:

    @classmethod
    def load(cls, aliases_file) -> Aliases:
        """
        Loads 'aliases_file' into a map

        Account:Alias

        So when an alias is found the correct account is sent to the transaction
        """
        currentDir = os.getcwd()
        filename = os.path.join(currentDir, aliases_file)

        if not os.path.isfile(filename):
            filename = os.path.join(currentDir, DEFAULT_ALIASES_FILE)

        aliases = Aliases()

        with open(filename, "r") as file:
            for line in file:
                line = line.replace("\n", "")
                parts = line.split(":")

                identifier = parts[0].strip().upper()
                value = parts[1].strip()

                alias = Alias(identifier, value)

                aliases.add(alias)

        return aliases
