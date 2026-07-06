from config.logging import get_logger

from src.accounts.entities import Accounts, Aliases
from src.models.account import Account


class AccountsLookup:

    DEFAULT_UNKNOWN = "Don't know"

    def __init__(self, accounts: Accounts, aliasLookup: AliasLookup):
        self.accounts = accounts
        self.aliases = aliasLookup
        self.log = get_logger(__name__)

    def hasAccount(self, accountType: str, identifier: str) -> bool:
        """
        Return TRUE if account map has 'accountType' and 'identifier'
        """
        acc = Account(accountType, identifier)

        return acc.key() in self.accounts.accounts.keys()

    def getAccount(self, accountType: str, identifier: str) -> str:
        """
        Get account.

        Account Type normally is: Assets, Expenses, Liability, etc...

        Identifier represents the account itself in Ledger.

        If no account is found a default identifier is used.

        Returns:
        str: Account identifier
        """

        if self.accounts.hasAccountType(accountType):

            identifier_parts = identifier.split(" ")
            while len(identifier_parts) > 0:
                id_substring = " ".join(identifier_parts).upper()

                if self.aliases.hasAlias(id_substring):
                    aliasIdentifier = self.aliases.getAlias(id_substring)
                    value = self.accounts.get(accountType, aliasIdentifier)
                    if value is not None:
                        return str(value.text)

                if self.hasAccount(accountType, id_substring):
                    value = self.accounts.get(accountType, id_substring)
                    if value is not None:
                        return str(value.text)

                identifier_parts.pop()

        # When DEFAULT_UNKOWN is used I need to save it and possibly add an ALIAS for it
        self.log.debug(identifier)
        return f"{accountType}:{self.DEFAULT_UNKNOWN}"


class AliasLookup:

    def __init__(self, aliases: Aliases):
        self.aliases = aliases

    def hasAlias(self, identifier: str) -> bool:
        """
        Return TRUE if AccountAliases has 'identifier'
        """
        return identifier in self.aliases.keys()

    def getAlias(self, identifier: str) -> str:
        """
        Get alias from 'identifier'

        Returns:
        str: Account or 'identifier' in uppercase
        """
        identifier = identifier.upper()

        alias = self.aliases.get(identifier)
        if alias is not None:
            return alias.value.upper()

        return identifier
