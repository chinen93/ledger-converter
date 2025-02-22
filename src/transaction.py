import datetime


class Transaction:

    ACCOUNT_CHECKING = "Bank:Checking"
    ACCOUNT_CREDIT = "Bank:CreditCard"
    PAYEE_DEFAULT = "Expenses:Don't know"
    LIABILITY_DEFAULT = "Liability:Don't know"

    def __init__(self, date, description, value, account, payee=PAYEE_DEFAULT):

        format = "%m/%d/%Y"
        datetime_str = datetime.datetime.strptime(date, format)

        self.date = datetime_str
        self.description = description

        value = float(value.replace(",", ""))
        # Transaction to buy something from someone
        if value < 0:
            self.value = value * -1
            self.account = account
            self.payee = payee

        # Transaction to pay one of my accounts
        else:
            self.value = value
            self.account = self.LIABILITY_DEFAULT
            self.payee = account

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
