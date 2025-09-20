from getpass import getpass
from bussiness.bussiness_logic import login_user, create_user, deposit, buy_currency, sell_currency, show_balances
from dataAccess.data_access import initialize_database



def main():
    while True:
        # while true xq sigue apareciendo hasta qe salga. 
        print("\n--- MENU ---")
        print("1 -> Crear usuario")
        print("2 -> Ingresar")
        print("3 -> Salir")
        opcion = input("Por favor ingrese una opcion: ")
        initialize_database()

        if opcion == "1":
            
            username = input("Por favor ingrese nombre de usuario: ").lower()
            password = getpass("Por favor ingrese su contraseña: ")
            confirm_password = getpass("Repita la contraseña: ")
            
            ok, mensaje = create_user(username, password, confirm_password)
            if ok:
                print(f"✅ {mensaje}")
            else:
                print(f"❌ {mensaje}")    

        elif opcion == "2":
            username = input("Por favor ingrese nombre de usuario: ").lower()
            password = getpass("Por favor ingrese su contraseña: ")
            if login_user(username, password):
                print("✅ Inicio de sesión exitoso")
                menu_usuario(username)
            else:
                print("❌ Usuario o contraseña incorrectos")

        elif opcion == "3":
            print("👋 Saliendo del sistema...")
            break

        else:
            print("⚠️ Opcion invalida")


def menu_usuario(username):
    while True:
        print(f"\n--- Bienvenido {username} En que te puedo ayudar hoy??---")
        print("1 -> Ingresar pesos (ARS)")
        print("2 -> Comprar moneda extranjera")
        print("3 -> Vender moneda extranjera")
        print("4 -> Mostrar saldos")
        print("5 -> Cerrar sesión")
        print("---------------------")
        print()
        initialize_database()

        opcion = input("Elegí una opción: ")

        if opcion == "1":
            monto = input("Monto a depositar (ARS): ")
            ok, msg = deposit(username, monto)
            print(msg)

        elif opcion == "2":
            moneda = input("Moneda a comprar (por ejemplo, USD o EUR): ").upper()
            monto = input("Monto en ARS a convertir: ")
            ok, msg = buy_currency(username, moneda, monto)
            print(msg)

        elif opcion == "3":
            ok, msg = sell_currency(username)
            print(msg)

        elif opcion == "4":
            show_balances(username)

        elif opcion == "5":
            print("Cerrando sesión...")
            break

        else:
            print("Opción inválida.")


if __name__ == '__main__':
    main()

