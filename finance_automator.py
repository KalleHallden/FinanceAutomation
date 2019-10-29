

import csv
import json
import datetime
import re
from models import Transaction, Statement, statement_from_json, transaction_from_json

data = {}
transactions = []
statements = []

try:
    with open('transactions.json') as json_file:
        data = json.load(json_file)
        for info in data["Transactions"]:
            transactions.append(transaction_from_json(info))
except:
    print("Exception")


def getFloat(list_):
    list_ = list_.split(".")
    amount = ""
    for num in list_:
        amount = amount + num
    amount = amount.split(",")
    amount = float(amount[0] + "." + amount[1])
    return amount

with open('export.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("skipped")
        else:
            if len(row) > 0:
                date = datetime.datetime.strptime(row[0], "%Y-%M-%d").date()
                account_num = row[1].split(" ")
                account_num = account_num[len(account_num) - 1]
                name = row[1].replace(account_num, "")
                transaction_amount = getFloat(row[3])
                ending_balance = getFloat(row[4])
                transaction = Transaction(
                    name,
                    transaction_amount,
                    date,
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
        
with open('transactions.json', 'w') as json_file:
    data = {}
    data["Transactions"] = []
    for transfer in transactions:
        data["Transactions"].append(transfer.serialize())
    json.dump(data, json_file, sort_keys=True, indent=4)



    
