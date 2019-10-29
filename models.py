import datetime


def statement_from_json(json):
    return Statement(
        json["date"],
        json["buisiness_expenses"],
        json["income"],
        json["ending_balance_month"],
        json["ending_balance_total"],
        json["tax_to_pay"],
        json["withdrew"],
        json["salary"]
    )


def transaction_from_json(json):
    return Transaction(
        json["name"],
        json["amount"],
        json["date"],
        json["account_number"],
        json["ending_balance"]
    )


class Transaction:
    def __init__(self, name, amount, date, account_number, ending_balance):
        self.name = name
        self.amount = amount
        self.date = date
        self.account_number = account_number
        self.ending_balance = ending_balance

    def serialize(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "date": str(self.date),
            "account_number": self.account_number,
            "ending_balance": self.ending_balance
        }


class Statement:
    def __init__(self, date, buisiness_expenses, income, ending_balance_month, ending_balance_total, tax_to_pay, withdrew, salary):
        self.date = date
        self.buisiness_expenses = buisiness_expenses
        self.income = income
        self.ending_balance_month = ending_balance_month
        self.ending_balance_total = ending_balance_total
        self.tax_to_pay = tax_to_pay
        self.withdrew = withdrew
        self.salary = salary

    def serialize(self):
        return {
            "date": str(self.date),
            "buisiness_expenses": self.buisiness_expenses,
            "income": self.income,
            "ending_balance_month": self.ending_balance_month,
            "ending_balance_total": self.ending_balance_total,
            "tax_to_pay": self.tax_to_pay,
            "withdrew": self.withdrew,
            "salary" : self.salary
        }
    def set_ending_balance_month(self):
        self.ending_balance_month = self.income + self.withdrew
    
    last_date = ""
    def create_statement(self, transfer):
        date_day = datetime.datetime.strptime(transfer.date, "%Y-%m-%d").date()
        date_ = date_day.strftime("%Y%m")
        if date_ == self.date:
            if self.last_date == "":
                self.last_date = date_day
            if date_day >= self.last_date:
                self.ending_balance_total = transfer.ending_balance
            names = transfer.name.split(" ")
            transfer_amount = transfer.amount
            for name in names:
                if name.lower() == "sk":
                    # salary kalle
                    self.salary = self.salary + transfer.amount
                    self.tax_to_pay = self.tax_to_pay + \
                        ((transfer.amount / 2) * 3)
                elif name.lower() == "be":
                    # buisiness expense
                    self.buisiness_expenses = self.buisiness_expenses + transfer.amount
                elif name.lower == "e":
                    transfer_amount = 0.0
            if transfer_amount > 0.0:
                self.income = self.income + transfer_amount
            else:
                self.withdrew = self.withdrew + transfer.amount
