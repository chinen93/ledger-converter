from datetime import datetime
from typing import Optional

from config.settings import get_settings
import numpy as np
import pandas as pd

class Data:

    def __init__(self):
        self.settings = get_settings()
        self.initial_data: Optional[np.ndarray] = None

    def _loadRawData(self) -> np.ndarray:
        filename = self.settings.EXPORT_CSV_FILENAME
        assert filename is not None

        readData = pd.read_csv(filename, delimiter=',', header=None)
        readData.iloc[:, 0] = pd.to_datetime(readData.iloc[:, 0],  errors='coerce').astype(str)
        value = readData.fillna('')

        assert pd.api.types.is_string_dtype(value.iloc[:, 0])
        assert pd.api.types.is_string_dtype(value.iloc[:, 1])
        assert pd.api.types.is_string_dtype(value.iloc[:, 2])
        assert pd.api.types.is_string_dtype(value.iloc[:, 3])
        assert pd.api.types.is_string_dtype(value.iloc[:, 4])
        assert pd.api.types.is_any_real_numeric_dtype(value.iloc[:, 5])
        assert pd.api.types.is_string_dtype(value.iloc[:, 6])
        assert pd.api.types.is_string_dtype(value.iloc[:, 7])
        
        return value.to_numpy()

    def _normalizeData(self, data: np.ndarray) -> np.ndarray:

        assert data.shape[1] == 8

        # Remove unused columns: "DATE","","DESC","ACCOUNT","CURRENCY","PRICE","",""
        # after should be: "DATE","PRICE"
        removed_columns = np.delete(data, [1, 2, 3, 4, 6, 7], axis=1)

        # Account still is combined need to break it into individual parts
        accounts = data[:, 3]
        longest_account = str(max(accounts, key=lambda k: len(k.split(":"))))
        numParts = len(longest_account.split(':'))

        numEntities = data.shape[0]
        accounts_parts = np.zeros((numEntities, numParts), dtype=str)

        normalized = np.hstack((removed_columns, accounts_parts))

        # Separate each part of the account into the parts of the normalized matrix
        for idx_acc, account in enumerate(accounts):
            parts = str(account).split(':')
            for idx_part, part in enumerate(parts):
                normalized[idx_acc][2 + idx_part] = part

        return normalized
    
    def load(self) -> None:
        raw_data = self._loadRawData()
        self.initial_data = self._normalizeData(raw_data)

