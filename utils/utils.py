import bcrypt
import re
from decimal import Decimal
import requests
from typing import Optional



def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def validate_password(password):
    if len(password) < 10:
        return False, "La contraseña debe tener al menos 10 caracteres."
    if not re.search(r"[A-Z]", password):
        return False, "La contraseña debe contener al menos una letra mayuscula."
    if not re.search(r"[0-9]", password):
        return False, "La contraseña debe contener al menos un numero."
    if not re.search(r"[!@#$%^&*(),.?\":{}|+<>]", password):
        return False, "La contraseña debe contener al menos un caracter especial."
    return True, ""

def get_conversion_rate(base: str, target: str) -> Optional[Decimal]:
    try:
        response = requests.get(
            "https://api.currencyfreaks.com/latest",
            params={
                "apikey": "99534bc875524e02b3d0476b8bce4c6c", 
                "symbols": f"{base},{target}"
            }
        )
        data = response.json()
        rate_base = Decimal(data["rates"][base])
        rate_target = Decimal(data["rates"][target])
        return rate_target / rate_base
    except Exception as e:
        print(f"Error al obtener cotización: {e}")
        return None 