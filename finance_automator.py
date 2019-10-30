

import csv
import json
import datetime
import re
from models import Transaction, Statement, statement_from_json, transaction_from_json
from datetime import date

data = {}
transactions = []
statements = []

try:
    with open('transactions.json') as json_file:
        data = json.load(json_file)
        for info in data["Transactions"]:
            transactions.append(transaction_from_json(info))
    with open('statements.json') as json_file:
        data = json.load(json_file)
        for info in data["Statements"]:
            statements.append(statement_from_json(info))
except:
    print("Exception")


def getFloat(list_):
    try:
        list_ = list_.split(".")
        amount = ""
        for num in list_:
            amount = amount + num
        amount = amount.split(",")
        amount = float(amount[0] + "." + amount[1])
        return amount
    except:
        return 0.0

with open('exports/export.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("skipped")
        else:
            if len(row) > 0:
                date_ = row[0]
                account_num = row[1].split(" ")
                account_num = account_num[len(account_num) - 1]
                name = row[1].replace(account_num, "")
                transaction_amount = getFloat(row[3])
                ending_balance = getFloat(row[4])
                transaction = Transaction(
                    name,
                    transaction_amount,
                    date_,
                    account_num,
                    ending_balance
                )
                exists = False
                for transfer in transactions:
                    if transfer.date == transaction.date:
                        if transfer.name == transaction.name:
                            if transfer.amount == transaction.amount:
                                exists = True
                if exists != True:
                    transactions.append(transaction)
        line_count = line_count + 1

states = []

with open('transactions.json', 'w') as json_file:
    data = {}
    data["Transactions"] = []
    for transfer in transactions: 
        date_day = datetime.datetime.strptime(transfer.date, "%Y-%m-%d").date().strftime("%Y%m")
        statement = Statement(date_day, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        data["Transactions"].append(transfer.serialize())
        exists = False
        for stat_ in states:
            if stat_.date == date_day:
                statement = stat_
        
        statement.create_statement(transfer)
        statement.set_ending_balance_month()
        for state in states:
            if state.date == statement.date:
                exists = True
        
        if not exists:
            states.append(statement)
            
                

    json.dump(data, json_file, sort_keys=True, indent=4)

# statements = states

statements = sorted(
    states,
    key=lambda x: datetime.datetime.strptime(x.date, '%Y%m').date(), reverse=True
)
        
with open('statements.json', 'w') as json_file:
    data = {}
    data["Statements"] = []
    for stat_ in statements:
        data["Statements"].append(stat_.serialize())
    json.dump(data, json_file, sort_keys=True, indent=4)

total_income = 0.0
total_expenses = 0.0
total_taxes = 0.0
taxes_paid = 0.0
salary_taken = 0.0
total_withdrawls = 0.0

for stat_ in statements:
    total_income = total_income + stat_.income
    total_expenses = total_expenses + stat_.buisiness_expenses 
    salary_taken = salary_taken + stat_.salary
    taxes_paid = taxes_paid + stat_.tax_paid
    total_withdrawls = total_withdrawls + stat_.withdrew

total_taxes = (salary_taken / 2) * 3 - taxes_paid
# print(str(total_withdrawls) + " - " + str(taxes_paid) + " = " + str(total_withdrawls - taxes_paid)) 
total_withdrawls = total_withdrawls - taxes_paid
total_net_income = (total_income + total_expenses) + salary_taken + (total_taxes)
potential_salary = (total_net_income + taxes_paid) * 0.4

print("\n"*3)
print("Total income: " + str(total_income))
print("Total NET income: " + str(total_net_income))
print("Total expenses: " + str(total_expenses))
print("Total tax to pay: " + str(total_taxes))
print("Potential salary: " + str(potential_salary))
print("Salary taken: " + str(salary_taken))
print("Total withdrawls: " + str(total_withdrawls))
print("\n"*3)



    
