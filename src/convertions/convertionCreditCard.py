from src.accounts.accounts import AccountsManager
from src.convertions.convertion import ConvertionStrategy, ParsedRow
from src.files.csv import ReadCSV


class CreditCardConvertion(ConvertionStrategy):

    HEADER = ["Posted Date", "Reference Number", "Payee", "Address", "Amount"]

    def __init__(self, accounts: AccountsManager):
        super().__init__(accounts, "CreditCard")

    def canConvert(self, heading: list[str]) -> bool:
        return heading == CreditCardConvertion.HEADER

    def move_to_data(self, csv_reader: ReadCSV) -> None:
        return None

    def parse_row(self, row: list[str]) -> ParsedRow:
        return ParsedRow(date=row[0], description=row[2], amount=float(row[4].replace(",", "")))
