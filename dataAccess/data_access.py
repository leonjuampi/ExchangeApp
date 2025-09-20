import json
import os
from decimal import Decimal
import sqlobject as SO
from sqlobject import SQLObjectNotFound

# bd de datos
database = 'mysql://root:123456789@localhost/exchangeApp'
__connection__ = SO.connectionForURI(database)

# usuarios
class Users(SO.SQLObject):
    username = SO.StringCol(length=40, varchar=True)
    password = SO.StringCol(length=100, varchar=True)

# cuentas
class Accounts(SO.SQLObject):
    currency = SO.StringCol(length=10, varchar=True)
    amount = SO.DecimalCol(size=10, precision=2)
    account_user = SO.ForeignKey('Users')

# Inicializa
def initialize_database():
    Users.createTable(ifNotExists=True)
    Accounts.createTable(ifNotExists=True)

def load_users():
    return [{"username": user.username, "password": user.password} for user in Users.select()]

def save_user(user_dict):
    try:
        Users.select(Users.q.username == user_dict["username"]).getOne()
        raise ValueError(f"Usuario '{user_dict['username']}' ya existe")
    except SQLObjectNotFound:
        nuevo_user = Users(username=user_dict["username"], password=user_dict["password"])
        Accounts(currency="ARS", amount=Decimal("0.00"), account_user=nuevo_user.id)


def create_user_account_file(username):
    try:
        user_obj = Users.select(Users.q.username == username).getOne()
    except SQLObjectNotFound:
        return
    try:
        Accounts.select((Accounts.q.currency == "ARS") & (Accounts.q.account_user == user_obj.id)).getOne()
    except SQLObjectNotFound:
        Accounts(currency="ARS", amount=Decimal("0.00"), account_user=user_obj.id)


def load_user_accounts(username):
    try:
        user_obj = Users.select(Users.q.username == username).getOne()
    except SQLObjectNotFound:
        return {"ARS": Decimal("0.00")}

    cuentas = {}
    for acc in Accounts.select(Accounts.q.account_user == user_obj.id):
        cuentas[acc.currency] = acc.amount

    return cuentas


def save_user_accounts(username, accounts_dict):
    try:
        user_obj = Users.select(Users.q.username == username).getOne()
    except SQLObjectNotFound:
        raise ValueError(f"Usuario '{username}' no existe")

    for currency, amount in accounts_dict.items():
        try:
            acc = Accounts.select((Accounts.q.currency == currency) & (Accounts.q.account_user == user_obj.id)).getOne()
            acc.set(amount=amount)
        except SQLObjectNotFound:
            Accounts(currency=currency, amount=amount, account_user=user_obj.id)
