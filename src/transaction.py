import datetime


class Transaction:

    def __init__(self, date, description, value, payee, account):

        format = "%m/%d/%Y"
        datetime_str = datetime.datetime.strptime(date, format)

        self.date = datetime_str
        self.description = description
        self.value = value
        self.payee = payee
        self.account = account

    def exportString(self):
        return (
            f'{self.date.strftime("%Y-%m-%d")}       {self.description}\n'
            f"    {self.payee}                            ${self.value}\n"
            f"    {self.account}\n\n"
        )

    def toString(self):
        return (
            f"{self.date} - "
            f"{self.description} - "
            f"{self.value} - "
            f"{self.payee} - "
            f"{self.account}"
        )
