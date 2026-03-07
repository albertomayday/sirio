#!/usr/bin/env python3
"""
SIRIO TPV - Ejecutor Ultra Simple
"""
import subprocess
import sys

print("\n🚀 SIRIO TPV v0.1\n")

# Instalar si no está
print("📦 Instalando/Verificando dependencias...")
subprocess.run([
    sys.executable, "-m", "pip", "install", "-q",
    "fastapi", "uvicorn", "sqlalchemy", "pydantic"
], check=False)

# Ejecutar
print("✅ Iniciando servidor en http://localhost:8000\n")
subprocess.run([sys.executable, "/workspaces/sirio/backend/main.py"])
