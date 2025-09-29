import sys, builtins
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QMessageBox, QTableWidgetItem
)
from PyQt6.QtGui import QDoubleValidator


from presentation.screens.login_iu import Ui_Login as UiLogin  
from presentation.screens.registro_ui import Ui_MainWindow as UiRegistro
from presentation.screens.principal_ui import Ui_Form as UiPrincipal
from presentation.screens.deposito_dialog_ui import Ui_Dialog as UiDeposito
from presentation.screens.comprar_dialog_ui import Ui_Dialog as UiComprar
from presentation.screens.vender_dialog_ui import Ui_Dialog as UiVender


from dataAccess.data_access import initialize_database, load_user_accounts
from bussiness.bussiness_logic import (
    login_user, create_user, deposit, buy_currency, sell_currency
)


# ---------- Diálogos ----------
class DepositoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = UiDeposito()
        self.ui.setupUi(self)
        self.ui.txtArs.setPlaceholderText("Monto en ARS (ej: 1000.50)")
        self.ui.txtArs.clear()
        self.ui.txtArs.setValidator(QDoubleValidator(0.0, 10**12, 2, self))

    def get_amount(self):
        if self.exec() == QDialog.DialogCode.Accepted:
            return self.ui.txtArs.text().strip()
        return None

class ComprarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = UiComprar()
        self.ui.setupUi(self)
        self.ui.txtMonedaComprar.setPlaceholderText("Moneda a comprar (USD/EUR/BRL/...)")
        self.ui.txtMontoComprar.setPlaceholderText("Monto ARS a convertir")
        self.ui.txtMontoComprar.setValidator(QDoubleValidator(0.0, 10**12, 2, self))
        self.ui.txtMonedaComprar.clear()
        self.ui.txtMontoComprar.clear()

    def get_values(self):
        if self.exec() == QDialog.DialogCode.Accepted:
            moneda = self.ui.txtMonedaComprar.text().strip().upper()
            monto = self.ui.txtMontoComprar.text().strip()
            return moneda, monto
        return None, None

class VenderDialog(QDialog):
    def __init__(self, balances: dict, parent=None):
        super().__init__(parent)
        self.ui = UiVender()
        self.ui.setupUi(self)

        self.ui.btnOkCancelVender.accepted.connect(self.accept)
        self.ui.btnOkCancelVender.rejected.connect(self.reject)

        self.ui.txtMonedaVender.setPlaceholderText("Moneda a vender (USD/EUR/...)")
        self.ui.txtMontoVender.setPlaceholderText("Monto a vender (en esa moneda)")
        self.ui.txtMontoVender.setValidator(QDoubleValidator(0.0, 10**12, 6, self))
        self.ui.txtMonedaVender.clear()
        self.ui.txtMontoVender.clear()


    def get_values(self):
        if self.exec() == QDialog.DialogCode.Accepted:
            moneda = self.ui.txtMonedaVender.text().strip().upper()
            monto = self.ui.txtMontoVender.text().strip()
            return moneda, monto
        return None, None

# ---------- Ventanas ----------
class LoginView(QWidget):
    def __init__(self, on_login_ok, on_go_register):
        super().__init__()
        self.ui = UiLogin()
        self.ui.setupUi(self)
        self.on_login_ok = on_login_ok
        self.on_go_register = on_go_register


        self.ui.txtPass.setEchoMode(self.ui.txtPass.EchoMode.Password)

        self.ui.btnLogin.clicked.connect(self.handle_login)
        self.ui.btnRegister.clicked.connect(self.on_go_register)

    def handle_login(self):
        u = self.ui.txtUser.text().strip().lower()
        p = self.ui.txtPass.text()
        if not u or not p:
            QMessageBox.warning(self, "Atención", "Completá usuario y contraseña.")
            return
        if login_user(u, p):
            self.on_login_ok(u)
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")

class RegistroView(QMainWindow):
    def __init__(self, on_registered):
        super().__init__()
        self.ui = UiRegistro()
        self.ui.setupUi(self)
        self.on_registered = on_registered


        self.ui.txtPass.setEchoMode(self.ui.txtPass.EchoMode.Password)
        self.ui.txtPass_2.setEchoMode(self.ui.txtPass_2.EchoMode.Password)

        self.ui.btnRegister.clicked.connect(self.handle_register)

    def handle_register(self):
        u = self.ui.txtUser.text().strip().lower()
        p1 = self.ui.txtPass.text()
        p2 = self.ui.txtPass_2.text()
        ok, msg = create_user(u, p1, p2)
        (QMessageBox.information if ok else QMessageBox.critical)(self, "Registro", msg)
        if ok:
            self.on_registered()
            self.close()

class PrincipalView(QWidget):
    def __init__(self, username, on_logout):
        super().__init__()
        self.user = username
        self.on_logout = on_logout
        self.ui = UiPrincipal()
        self.ui.setupUi(self)


        self.ui.Welcome.setText(f"Bienvenido!  {self.user}")


        self.ui.tableSaldos.setColumnCount(2)
        self.ui.tableSaldos.setHorizontalHeaderLabels(["Moneda", "Saldo disponible"])
        self.ui.tableSaldos.setEditTriggers(self.ui.tableSaldos.EditTrigger.NoEditTriggers)
        self.ui.tableSaldos.setSelectionBehavior(self.ui.tableSaldos.SelectionBehavior.SelectRows)

        # Conexiones
        self.ui.btnLogout.clicked.connect(self.on_logout)
        self.ui.btnIngresarPesos.clicked.connect(self.handle_deposit)
        self.ui.btnComprar.clicked.connect(self.handle_buy)
        self.ui.btnVender.clicked.connect(self.handle_sell)

        self.refresh_balances()

    def refresh_balances(self):
        balances = load_user_accounts(self.user)
        items = list(balances.items())
        self.ui.tableSaldos.setRowCount(len(items))
        for i, (cur, amt) in enumerate(items):
            self.ui.tableSaldos.setItem(i, 0, QTableWidgetItem(str(cur)))
            try:
                val = f"{float(amt):.6f}"
            except Exception:
                val = str(amt)
            self.ui.tableSaldos.setItem(i, 1, QTableWidgetItem(val))


    def handle_deposit(self):
        dlg = DepositoDialog(self)
        amount = dlg.get_amount()
        if not amount:
            return
        ok, msg = deposit(self.user, amount)
        (QMessageBox.information if ok else QMessageBox.critical)(self, "Depósito", msg)
        self.refresh_balances()

    def handle_buy(self):
        dlg = ComprarDialog(self)
        currency, amount_ars = dlg.get_values()
        if not currency or not amount_ars:
            return

        r = QMessageBox.question(
            self, "Confirmar",
            f"¿Convertir ARS {amount_ars} a {currency}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if r != QMessageBox.StandardButton.Yes:
            return

        # el buy_currency pide input() para confirmar; respondemos "s" para que funque
        real_input = builtins.input
        builtins.input = lambda prompt="": "s"
        try:
            ok, msg = buy_currency(self.user, currency, amount_ars)
        finally:
            builtins.input = real_input

        (QMessageBox.information if ok else QMessageBox.critical)(self, "Compra", msg)
        self.refresh_balances()

    def handle_sell(self):
        balances = load_user_accounts(self.user)
        dlg = VenderDialog(balances, self)
        currency, amount = dlg.get_values()
        if not currency or not amount:
            return

        r = QMessageBox.question(
            self, "Confirmar",
            f"¿Vender {amount} {currency} a ARS?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if r != QMessageBox.StandardButton.Yes:
            return

        # el sell_currency pide 3 input(): moneda, monto, confirmación
        real_input = builtins.input
        inputs = iter([currency, amount, "s"])
        builtins.input = lambda prompt="": next(inputs)
        try:
            ok, msg = sell_currency(self.user)
        finally:
            builtins.input = real_input

        (QMessageBox.information if ok else QMessageBox.critical)(self, "Venta", msg)
        self.refresh_balances()


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ExchangeApp")

        self.login = LoginView(self.on_login_ok, self.open_register)
        self.setCentralWidget(self.login)
        self.principal = None
        self.registro = None

    def on_login_ok(self, username):
        self.principal = PrincipalView(username, on_logout=self.back_to_login)
        self.setCentralWidget(self.principal)
        self.resize(900, 600)

    def open_register(self):
        self.registro = RegistroView(on_registered=self.back_to_login)
        self.registro.show()

    def back_to_login(self):
        self.login = LoginView(self.on_login_ok, self.open_register)
        self.setCentralWidget(self.login)
        self.resize(500, 360)

def main():
    initialize_database()
    app = QApplication(sys.argv)
    w = App()
    w.resize(500, 360)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
