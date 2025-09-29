# ExchangeApp 💱
---

## 🚀 Requisitos

- **Python 3.9.x** (probado en 3.9.13)
- **MySQL** en local
- Dependencias listadas en `requirements.txt`

---

## ⚙️ Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/leonjuampi/exchangeapp.git
cd exchangeapp
```
2. **Crear y activar entorno virtual**

```bash
python -m venv .venv
.venv\Scripts\activate   
```
3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

## 🛢️ Base de datos

1. **Crear la base de datos**
```bash
CREATE DATABASE exchangeApp;
```

2. **Importar el dump incluido**
```bash
mmysql -u root -p ExchangeApp < dump.sql
```

3. **Verificar credenciales en**
```bash
dataAccess/data_access.py:
```

**Por defecto:**
```bash
'mysql+pymysql://user:pass@localhost/exchangeApp?charset=utf8mb4'
```

## ▶️ Ejecución
```bash
python -m presentation.qt_app
```

## 🖥️ Pantallas
- Login: ingresar usuario/contraseña o registrarse.
- Registro: crear un nuevo usuario.
- Principal: menú con botones para depositar, comprar, vender y ver saldos.
- Diálogos: ventanas modales para confirmar cada operación.

## 📂 Estructura del proyecto
```bash
.
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
```

## ✅ Funcionalidades

- Registro de usuarios con contraseña hasheada.
- Inicio de sesión (login).
- Pantalla principal con:
  - Depósito en ARS.
  - Compra de monedas extranjeras.
  - Venta de monedas.
  - Visualización de saldos.
- Ventanas de diálogo para confirmar operaciones.
- Persistencia en **MySQL** mediante **SQLObject ORM**.



