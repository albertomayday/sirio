@echo off
REM =====================================================
REM SIRIO TPV x64 - Build to EXE
REM Convierte la aplicación Python a ejecutable .exe
REM =====================================================

setlocal enabledelayedexpansion

echo.
echo ======================================================
echo SIRIO TPV x64 - Build to Executable
echo ======================================================
echo.

cd /d "%~dp0"

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado
    echo Descarga desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python encontrado

REM Instalar PyInstaller si no existe
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando PyInstaller...
    python -m pip install --quiet pyinstaller
)

REM Limpiar builds anteriores
if exist dist rmdir /s /q dist >nul 2>&1
if exist build rmdir /s /q build >nul 2>&1

echo [INFO] Compilando ejecutable...
echo.

REM Crear ejecutable
pyinstaller ^
    --onefile ^
    --windowed ^
    --icon=frontend/icon.ico ^
    --name "Sirio-TPV" ^
    --add-data "frontend:frontend" ^
    --add-data "backend:backend" ^
    --add-data "modules:modules" ^
    --collect-all fastapi ^
    --collect-all uvicorn ^
    --collect-all sqlalchemy ^
    --collect-all pydantic ^
    launcher\sirio_launcher.py

if errorlevel 1 (
    echo [ERROR] Fallo la compilacion
    pause
    exit /b 1
)

echo.
echo ======================================================
echo [OK] Ejecutable creado en: dist\Sirio-TPV.exe
echo ======================================================
echo.

REM Crear archivo de informacion del release
(
    echo {
    echo   "name": "Sirio TPV x64",
    echo   "version": "1.0.0",
    echo   "executable": "Sirio-TPV.exe",
    echo   "architecture": "x64",
    echo   "platform": "Windows",
    echo   "status": "OPERATIVO"
    echo }
) > dist\release.json

echo [INFO] Release info generado
echo.
echo Distribuir el archivo: dist\Sirio-TPV.exe
echo.
pause
