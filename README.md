# Simulation POC: React + FastAPI Auth

Este proyecto es una Prueba de Concepto (POC) que implementa un sistema básico de autenticación (Login/Signup) utilizando **React** en el frontend y **FastAPI** en el backend, con **SQLite** como base de datos.

## 🚀 Requisitos Previos

- **Python 3.8+**
- **Node.js 18+**
- **npm** o **yarn**

---

## 🛠️ Configuración del Backend (FastAPI)

El backend utiliza un ambiente virtual para gestionar las dependencias de forma aislada.

1.  **Navega al directorio del backend:**
    ```bash
    cd backend
    ```

2.  **Crea un ambiente virtual (si no existe):**
    ```bash
    python -m venv venv
    ```

3.  **Activa el ambiente virtual:**
    - En **Windows**:
      ```powershell
      .\venv\Scripts\Activate.ps1
      ```
    - En **macOS/Linux**:
      ```bash
      source venv/bin/activate
      ```

4.  **Configura las variables de entorno:**
    Copia el archivo de ejemplo y ajusta las variables si es necesario:
    ```bash
    cp .env.example .env
    ```

5.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

6.  **Ejecuta el servidor:**
    ```bash
    python -m uvicorn main:app --reload
    ```
    El servidor estará disponible en `http://localhost:8000`.

---

## 💻 Configuración del Frontend (React + Vite)

1.  **Navega al directorio del frontend:**
    ```bash
    cd ./frontend
    ```

2.  **Configura las variables de entorno:**
    Copia el archivo de ejemplo (ajusta `VITE_API_URL` si tu backend corre en otro puerto):
    ```bash
    cp .env.example .env
    ```

3.  **Instala las dependencias:**
    ```bash
    npm install
    ```

4.  **Ejecuta el servidor de desarrollo:**
    ```bash
    npm run dev
    ```
    El frontend estará disponible en `http://localhost:5173`.

---

## 🎨 Características

- **Diseño Premium**: Interfaz moderna con efecto "Glassmorphism" y modo oscuro.
- **Seguridad**: Autenticación basada en JWT y hashing de contraseñas con bcrypt.
- **Base de Datos**: SQLite integrada (no requiere configuración de base de datos externa).
- **Iconos**: Lucide React para una mejor experiencia visual.

---

## 📄 Estructura del Proyecto

```text
simulation-poc/
├── backend/            # Lógica de FastAPI, modelos y auth.db
│   ├── venv/           # Ambiente virtual de Python
│   ├── main.py         # Punto de entrada de la API
│   └── ...
├── frontend/           # Aplicación React (Vite)
│   ├── src/            # Componentes y servicios
│   └── ...
└── README.md           # Estas instrucciones
```
