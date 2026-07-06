import os

from config.logging import get_logger
from config.settings import get_settings


class Discover:

    def __init__(self):
        self._settings = get_settings()
        self.log = get_logger(__name__)

        input_folder = self._settings.INPUT_FOLDER
        assert input_folder is not None

        # Getting the current work directory (cwd)
        currentDir = os.getcwd()
        self.input_folder = currentDir + input_folder

    def discoverFilenames(self) -> list[str]:
        filenames: list[str] = []

        for filename in os.listdir(self.input_folder):
            if filename.endswith(".csv"):
                filename = os.path.join(self.input_folder, filename)
                filenames.append(filename)

        self.log.info(f"Found {len(filenames)} files to convert")
        return filenames
