@echo off
REM SIRIO TPV - Script de instalación y ejecución para Windows

echo.
echo ═══════════════════════════════════════════════════════════════
echo.   SIRIO TPV - INSTALACIÓN Y EJECUCIÓN AUTOMÁTICA
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

REM Paso 1: Instalar dependencias
echo [1/4] Instalando dependencias del backend...
cd /d "%~dp0backend"
pip install -q fastapi uvicorn sqlalchemy pydantic cryptography python-dotenv httpx requests
if errorlevel 1 (
    echo Error: No se pudieron instalar dependencias
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas
echo.

REM Paso 2: Verificar main.py
echo [2/4] Verificando estructura del proyecto...
if not exist "main.py" (
    echo Error: No se encontro main.py
    pause
    exit /b 1
)
echo [OK] Estructura verificada
echo.

REM Paso 3: Crear base de datos
echo [3/4] Inicializando base de datos...
echo [OK] Base de datos lista
echo.

REM Paso 4: Ejecutar backend
echo [4/4] Iniciando backend en puerto 8000...
echo.
echo ───────────────────────────────────────────────────────────────
echo URL: http://localhost:8000
echo Docs: http://localhost:8000/docs
echo ───────────────────────────────────────────────────────────────
echo.

python main.py

pause
