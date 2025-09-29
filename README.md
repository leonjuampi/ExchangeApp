# ExchangeApp 💱

Aplicación de escritorio desarrollada en **Python 3.9 + PyQt6** para simular un sistema de cuentas en distintas monedas.  

---

## 📌 Funcionalidades

- Registro de usuarios con contraseña hasheada.
- Inicio de sesión (login).
- Pantalla principal con:
  - Depósito en ARS.
  - Compra de monedas extranjeras.
  - Venta de monedas.
  - Visualización de saldos.
- Ventanas de diálogo para confirmar operaciones.
- Persistencia en **MySQL** mediante **SQLObject ORM**.

---

## 🗂️ Estructura de carpetas

TP 3RA ETAPA/
│
├── bussiness/ # Lógica de negocio (login, depósitos, compra/venta)
│ └── bussiness_logic.py
│
├── dataAccess/ # Capa de acceso a datos con SQLObject (MySQL)
│ └── data_access.py
│
├── presentation/ # Capa de presentación (UI PyQt6)
│ ├── qt_app.py # Punto de entrada de la app con interfaz gráfica
│ └── screens/ # Archivos .ui compilados a .py con pyuic6
│
├── utils/ # Funciones auxiliares (hash de contraseñas, validaciones, etc.)
│
├── app.py # Versión CLI (consola) del mismo sistema
├── dump.sql # Script SQL inicial (si aplica)
├── requirements.txt # Dependencias del proyecto
└── README.md

---

## ⚙️ Requisitos

- **Python 3.9.x** (probado en 3.9.13)
- **MySQL** en local
- Dependencias listadas en `requirements.txt`

---

## 🚀 Instalación y ejecución

1. **Clonar el repo**
   ```bash
   git clone https://github.com/tuusuario/exchangeapp.git
   cd exchangeapp

2. **Crear entorno virtual**
python -m venv .venv

3. **Activar entorno**
.venv\Scripts\Activate

4. **Instalar Dependencias**
pip install -r requirements.txt

5. **Configurar la base de datos MySQL**
CREATE DATABASE exchangeApp;

5. **Configurar la base de datos MySQL**
Revisar credenciales en dataAccess/data_access.py:
database = 'mysql+pymysql://user:pass@localhost/exchangeApp?charset=utf8mb4'

5. **Configurar la base de datos MySQL**
Importar el dump incluido
bash
mmysql -u root -p ExchangeApp < dump.sql

6. **Configurar la base de datos MySQL**
python -m presentation.qt_app

----

🖥️ Pantallas

Login: ingresar usuario/contraseña o registrarse.

Registro: crear un nuevo usuario.

Principal: menú con botones para depositar, comprar, vender y ver saldos.

Diálogos: ventanas modales para confirmar cada operación.

