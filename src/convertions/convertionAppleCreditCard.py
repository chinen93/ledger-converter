from src.accounts.accounts import AccountsManager
from src.convertions.convertion import ConvertionStrategy, ParsedRow
from src.files.csv import ReadCSV


class AppleCreditCardConvertion(ConvertionStrategy):

    HEADER = [
        "Transaction Date",
        "Clearing Date",
        "Description",
        "Merchant",
        "Category",
        "Type",
        "Amount (USD)",
        "Purchased By",
    ]

    def __init__(self, accounts: AccountsManager):
        super().__init__(accounts, "AppleCard")

    def canConvert(self, heading: list[str]) -> bool:
        return heading == AppleCreditCardConvertion.HEADER

    def move_to_data(self, csv_reader: ReadCSV) -> None:
        return None

    def parse_row(self, row: list[str]) -> ParsedRow:
        return ParsedRow(date=row[0], description=row[2], amount=float(row[6].replace(",", "")))
