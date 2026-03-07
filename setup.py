#!/usr/bin/env python3
"""
SIRIO TPV - Setup e Inicialización Automática
Instala todas las dependencias y ejecuta el backend
"""

import subprocess
import sys
import os
import platform

def print_header(msg):
    print("\n" + "═" * 60)
    print(f"  {msg}")
    print("═" * 60 + "\n")

def run_command(cmd, description):
    """Ejecutar comando y verificar resultado"""
    print(f"▶ {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, shell=True)
        print(f"✅ {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"   {e.stderr}")
        return False

def main():
    print_header("SIRIO TPV v0.1 - SETUP AUTOMÁTICO")
    
    # Paso 1: Verificar Python
    print(f"📌 Sistema: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version}")
    
    # Paso 2: Backend path
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    if not os.path.exists(backend_path):
        print(f"\n❌ Error: No se encontró directorio backend en {backend_path}")
        sys.exit(1)
    
    print(f"📁 Ruta backend: {backend_path}")
    os.chdir(backend_path)
    
    # Paso 3: Instalar dependencias
    print_header("PASO 1: Instalando dependencias")
    deps = [
        'fastapi>=0.104.1',
        'uvicorn[standard]>=0.24.0',
        'sqlalchemy>=2.0.23',
        'pydantic>=2.5.0',
        'cryptography>=41.0.7',
        'python-dotenv>=1.0.0',
        'httpx>=0.25.1',
        'requests>=2.31.0',
    ]
    
    for dep in deps:
        cmd = f"{sys.executable} -m pip install -q {dep}"
        if not run_command(cmd, f"Instalando {dep.split('>=')[0]}"):
            print(f"⚠️  Continuando con siguientes dependencias...")
    
    # Paso 4: Crear base de datos
    print_header("PASO 2: Inicializando base de datos")
    if os.path.exists('tpv.db'):
        print("✅ Base de datos existente detectada")
    else:
        print("ℹ️  La base de datos se creará al iniciar el servidor")
    
    # Paso 5: Ejecutar backend
    print_header("PASO 3: Iniciando backend")
    print("📍 Server: http://localhost:8000")
    print("📍 API: http://localhost:8000/api")
    print("📍 Docs: http://localhost:8000/docs (Swagger UI)")
    print("📍 Frontend: http://localhost:8000/index.html (o abre frontend/index.html)")
    print("\n" + "─" * 60 + "\n")
    
    # Ejecutar main.py
    try:
        cmd = f"{sys.executable} main.py"
        print(f"Ejecutando: {cmd}\n")
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print("\n\n⏹️  Servidor detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error ejecutando backend: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
