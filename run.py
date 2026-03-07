#!/usr/bin/env python3
"""
SIRIO TPV - Ejecutor Simple
Instala lo necesario y ejecuta el backend
"""

import subprocess
import sys
import os

def run(cmd, description=""):
    if description:
        print(f"\n▶ {description}...")
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except:
        return False

print("\n" + "="*60)
print("  SIRIO TPV v0.1 - INICIANDO...")
print("="*60)

# Cambiar a backend
os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))

# Instalar dependencias mínimas
print("\n📦 Instalando dependencias...")
run(f"{sys.executable} -m pip install -q fastapi uvicorn sqlalchemy pydantic 2>/dev/null", 
    "FastAPI, Uvicorn, SQLAlchemy")

# Ejecutar
print("\n" + "="*60)
print("  🚀 SERVIDOR INICIADO")
print("="*60)
print("\n🌐 http://localhost:8000")
print("📍 API Docs: http://localhost:8000/docs")
print("\n" + "-"*60 + "\n")

run(f"{sys.executable} main.py")
