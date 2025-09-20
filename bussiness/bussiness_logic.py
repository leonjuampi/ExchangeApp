from dataAccess.data_access import load_users, save_user, create_user_account_file, load_user_accounts, save_user_accounts
from utils.utils import hash_password, check_password,validate_password, validate_password, get_conversion_rate
from decimal import Decimal
import time
import os



def create_user(username, password, confirm_password):
    users = load_users()

    if password != confirm_password:
        return False, "Las contraseñas no coinciden."
    
    ok, mensaje = validate_password(password)
    if not ok:
        return False, mensaje
    
    if username == "" :
        return False, "El nombre de usuario no puede estar vacío."

    for user in users:
        if user['username'] == username:
            return False, "El usuario ya existe."

    hashed_pw = hash_password(password)
    users.append({"username": username, "password": hashed_pw})
    save_user({"username": username, "password": hashed_pw})

    create_user_account_file(username)
    return True, "Usuario creado correctamente."


def login_user(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username:
            return check_password(password, user['password'])
    return False

def deposit(username, amount_str):
    try:
        amount = Decimal(amount_str)
        if amount <= 0:
            return False, "El deposito debe ser mayor a 0."
    except:
        return False, "Monto inválido."

    accounts = load_user_accounts(username)
    if "ARS" not in accounts:
        return False, "Cuenta no encontrada."

    accounts["ARS"] += amount
    save_user_accounts(username, accounts)
    return True, f"Se depositaron ARS {amount:.2f} correctamente."


def buy_currency(username, currency, amount_str):
    try:
        amount = Decimal(amount_str)
        if amount <= 0:
            return False, "El monto a comprar debe ser mayor a 0."
    except:
        return False, "Monto inválido."

    accounts = load_user_accounts(username)
    if "ARS" not in accounts:
        return False, "Cuenta no encontrada."

    accounts = load_user_accounts(username)
    ars_balance = accounts.get("ARS", Decimal("0.00"))

    rate_ars = get_conversion_rate("USD", "ARS")
    rate_target = get_conversion_rate("USD", currency)

    if rate_ars is None or rate_target is None:
        return False, "No se pudo obtener la cotización."

    # Convertir ARS a moneda destino
    conversion = (amount * rate_target) / rate_ars

    if ars_balance < amount:
        return False, "Fondos insuficientes."

    print(f"Se van a convertir ARS {amount:.2f} a {currency} --> {conversion:.2f}")
    confirm = input("¿Confirmar operación? (s/n): ").lower()
    start_time = time.time()
    if confirm != "s" or (time.time() - start_time > 120):
        return False, "Operación cancelada por tiempo o negación."

    accounts["ARS"] -= amount
    accounts[currency] = accounts.get(currency, Decimal("0.00")) + conversion
    save_user_accounts(username, accounts)
    return True, f"Compra realizada: {conversion:.2f} {currency}"

def sell_currency(username):
    accounts = load_user_accounts(username)
    
    # Mostrar monedas extranjeras disponibles
    foreign_currencies = {k: v for k, v in accounts.items() if k != "ARS" and v > 0}
    
    if not foreign_currencies:
        print("No tenés monedas extranjeras para vender.")
        return False, "Sin fondos en divisas."

    print("Monedas extranjeras disponibles para vender:")
    for moneda, saldo in foreign_currencies.items():
        print(f"- {moneda}: {saldo:.4f}")

    currency = input("Moneda a vender (por ejemplo, USD o EUR): ").upper()
    
    if currency not in foreign_currencies:
        return False, "No tenés saldo en esa moneda para vender."

    amount_str = input(f"Monto a vender ({currency}): ")
    
    try:
        amount = Decimal(amount_str)
        if amount <= 0:
            return False, "El monto debe ser mayor que cero."
    except:
        return False, "Monto inválido."

    currency_balance = accounts.get(currency, Decimal("0.00"))
    if currency_balance < amount:
        return False, "Fondos insuficientes en la moneda."

    rate_ars = get_conversion_rate("USD", "ARS")
    rate_currency = get_conversion_rate("USD", currency)

    if rate_ars is None or rate_currency is None:
        return False, "No se pudo obtener la cotización."

    ars_equiv = (amount * rate_ars) / rate_currency

    print(f"Se van a vender {amount:.2f} {currency} y recibir ARS --> {ars_equiv:.2f}")
    confirm = input("¿Confirmar operación? (s/n): ").lower()
    start_time = time.time()
    if confirm != "s" or (time.time() - start_time > 120):
        return False, "Operación cancelada por tiempo o negación."

    accounts[currency] -= amount
    accounts["ARS"] = accounts.get("ARS", Decimal("0.00")) + ars_equiv
    save_user_accounts(username, accounts)
    return True, f"Venta realizada: +ARS {ars_equiv:.2f}"

def show_balances(username):
    accounts = load_user_accounts(username)
    print("\n--- SALDOS ---")
    for currency, amount in accounts.items():
        print(f"{currency}: {amount:.2f}")    