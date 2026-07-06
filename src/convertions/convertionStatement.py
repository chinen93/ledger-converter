from src.accounts.accounts import AccountsManager
from src.convertions.convertion import ConvertionStrategy, ParsedRow
from src.files.csv import ReadCSV


class StatementConvertion(ConvertionStrategy):

    FIRST_LINE = ["Description", "", "Summary Amt."]
    HEADER = ["Date", "Description", "Amount", "Running Bal."]

    def __init__(self, accounts: AccountsManager):
        super().__init__(accounts, "Checking")

    def canConvert(self, heading: list[str]) -> bool:
        return heading == StatementConvertion.FIRST_LINE

    def move_to_data(self, csv_reader: ReadCSV) -> None:
        csv_reader.moveBeginData(StatementConvertion.HEADER)

    def parse_row(self, row: list[str]) -> ParsedRow:
        return ParsedRow(date=row[0], description=row[1], amount=float(row[2].replace(",", "")))

    def should_skip(self, description: str, value: float, row: list[str]) -> bool:
        return description.startswith("Beginning balance")
