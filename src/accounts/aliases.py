from config.logging import get_logger
from config.settings import get_settings
from src.accounts.loader import AliasesLoader
from src.accounts.lookup import AliasLookup


class AliasManager:
    """
    Accounts Aliases map

    Making it easier to find an account using an aliases.

    Multiple aliases can point to the same account.
    """

    def __init__(self, aliases_file=None):

        self._settings = get_settings()

        if aliases_file is None:
            aliases_file = self._settings.ALIASES_FILE
            assert aliases_file is not None

        aliases = AliasesLoader.load(aliases_file)
        self.lookup = AliasLookup(aliases)

        self.log = get_logger(__name__)

    def hasAlias(self, identifier: str) -> bool:
        """
        Return TRUE if AccountAliases has 'identifier'
        """
        return self.lookup.hasAlias(identifier)

    def getAlias(self, identifier: str) -> str:
        """
        Get alias from 'identifier'

        Returns:
        str: Account or 'identifier' in uppercase
        """
        return self.lookup.getAlias(identifier)
