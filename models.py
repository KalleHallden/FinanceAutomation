import datetime

def statement_from_json(json):
        return Statement(
            datetime.datetime.strptime(json["date"], "%Y-%M-%d").date(),
            json["buisiness_expenses"],
            json["income"],
            json["ending_balance_month"],
            json["ending_balance_total"],
            json["tax_to_pay"]
        )
def transaction_from_json(json):
        return Transaction(
            json["name"],
            json["amount"],
            datetime.datetime.strptime(json["date"], "%Y-%M-%d").date(),
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
            "name" : self.name,
            "amount" : self.amount,
            "date" : str(self.date),
            "account_number" : self.account_number,
            "ending_balance" : self.ending_balance
        }

class Statement:
    def __init__(self, date, buisiness_expenses, income, ending_balance_month, ending_balance_total, tax_to_pay):
        self.date = date
        self.buisiness_expenses = buisiness_expenses
        self.income = income
        self.ending_balance_month = ending_balance_month
        self.ending_balance_total = ending_balance_total
        self.tax_to_pay = tax_to_pay
    
    def serialize(self):
        return {
            "date" : str(self.date),
            "buisiness_expenses" : self.buisiness_expenses,
            "income" : self.income,
            "ending_balance_month" : self.ending_balance_month,
            "ending_balance_total" : self.ending_balance_total,
            "tax_to_pay" : self.tax_to_pay
        }