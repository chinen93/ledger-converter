from typing import Optional

from src.models.account import Account, Alias


class Aliases:
    def __init__(self):
        self.aliases: dict[str, Alias] = {}  # type: ignore

    def add(self, alias: Alias) -> None:
        self.aliases[alias.identifier] = alias

    def get(self, identifier: str) -> Optional[Alias]:
        return self.aliases.get(identifier)

    def keys(self) -> list[str]:
        return list(self.aliases.keys())


class Accounts:
    def __init__(self):
        self.accounts: dict[str, Account] = {}  # type: ignore
        self.accountTypes: set[str] = set()  # type: ignore

    def add(self, acc: Account) -> None:

        self.accountTypes.add(acc.accountType)

        key = acc.key()
        if key not in self.accounts:
            self.accounts[key] = acc
        else:
            if acc < self.accounts[key]:
                self.accounts[key] = acc

    def keys(self) -> list[str]:
        return list(self.accounts.keys())

    def get(self, accountType: str, identifier: str) -> Optional[Account]:
        acc = Account(accountType, identifier)

        return self.accounts.get(acc.key())

    def hasAccountType(self, accountType: str) -> bool:
        return accountType in self.accountTypes
