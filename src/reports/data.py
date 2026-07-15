from config.settings import get_settings
import numpy as np
import pandas as pd

class Data:

    def __init__(self):

        self.settings = get_settings()
        
        raw_data = self.loadRawData()
        self.initial_data = self.normalizeData(raw_data)

    def loadRawData(self) -> np.ndarray:
        filename = self.settings.EXPORT_CSV_FILENAME
        assert filename is not None

        return pd.read_csv(filename, delimiter=',', header=None).to_numpy()

    def normalizeData(self, data: np.ndarray) -> np.ndarray:

        numEntities = data.shape[0]
        print(data.shape)
        print(numEntities)
        print(data[:5])
        print()

        # Remove unused columns: "DATE","","DESC","ACCOUNT","CURRENCY","PRICE","",""
        # after should be: "DATE","PRICE"
        removed_columns = np.delete(data, [1, 2, 3, 4, 6, 7], axis=1)
        print(removed_columns.shape)
        print(removed_columns[:5])
        print()

        # Account still is combined need to break it into individual parts
        accounts = data[:, 3]
        longest_account = str(max(accounts, key=len))
        numParts = len(longest_account.split(':'))

        print(longest_account)
        print(numParts)

        accounts_parts = np.zeros((numEntities, numParts), dtype=str)

        normalized = np.hstack((removed_columns, accounts_parts))
        print(normalized.shape)
        print(normalized)

        # Separate each part of the account into the parts of the normalized matrix
        # TODO

        return data
