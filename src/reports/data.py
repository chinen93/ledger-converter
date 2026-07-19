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
    
    def _get_price(self, data: np.ndarray) -> np.ndarray:
        assert data.shape[1] == 8
        price = data[:, 5]

        return price.reshape(-1, 1)
    
    def _get_date_parts(self, data:np.ndarray) -> np.ndarray:
        assert data.shape[1] == 8
        numEntities = data.shape[0]

        date_str = data[:, 0]
        date_parts = np.empty((numEntities, 3), dtype=object)

        # Separate each part of the account into the parts of the normalized matrix
        for idx_acc, date in enumerate(date_str):
            parts = date.split('-')

            date_parts[idx_acc, 0] = parts[0]
            date_parts[idx_acc, 1] = parts[1]
            date_parts[idx_acc, 2] = parts[2]

        return date_parts
    

    def _get_accounts_parts(self, data: np.ndarray) -> np.ndarray:
        assert data.shape[1] == 8
        numEntities = data.shape[0]

        # Account still is combined need to break it into individual parts
        accounts = data[:, 3]
        longest_account = str(max(accounts, key=lambda k: len(k.split(":"))))
        numParts = len(longest_account.split(':'))

        numEntities = data.shape[0]
        accounts_parts = np.empty((numEntities, numParts), dtype=object)

        # Separate each part of the account into the parts of the normalized matrix
        for idx_acc, account in enumerate(accounts):
            parts = str(account).split(':')
            for idx_part, part in enumerate(parts):
                accounts_parts[idx_acc][idx_part] = part

        return accounts_parts


    def _normalizeData(self, data: np.ndarray) -> np.ndarray:
        assert data.shape[1] == 8

        date_parts = self._get_date_parts(data)
        price = self._get_price(data)
        accounts_parts = self._get_accounts_parts(data)

        normalized = np.hstack((date_parts, price, accounts_parts))

        return normalized
    
    def load(self) -> None:
        raw_data = self._loadRawData()
        self.initial_data = self._normalizeData(raw_data)


class ManipulateData:

    @classmethod
    def forOverviewReport(cls, data: np.ndarray) -> pd.DataFrame:
        pass

    