from typing import Optional


class Account:

    def __init__(self, accountType: str, identifier: str, text: Optional[str] = None):

        self.accountType = accountType
        self.identifier = identifier
        self.text = text

    def key(self) -> str:
        return f"{self.accountType}:{self.identifier}"

    def __lt__(self, other: object):

        if not isinstance(other, Account):
            return NotImplemented

        assert self.text is not None
        assert other.text is not None

        mine = len(self.text.split(":"))
        theirs = len(other.text.split(":"))

        return mine < theirs

    def __eq__(self, other: object):

        if not isinstance(other, Account):
            return NotImplemented

        assert self.text is not None
        assert other.text is not None

        mine = len(self.text.split(":"))
        theirs = len(other.text.split(":"))

        return mine < theirs and self.key() == other.key()


class Alias:
    def __init__(self, identifier: str, value: str):
        self.identifier = identifier
        self.value = value
