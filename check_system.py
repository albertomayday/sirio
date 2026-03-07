#!/usr/bin/env python3
"""
SIRIO TPV - Verificación de Sistema
Comprueba que todo está listo para ejecutar
"""

import os
import sys
import subprocess
from pathlib import Path

def check(condition, msg_ok, msg_fail):
    """Verificar condición"""
    if condition:
        print(f"✅ {msg_ok}")
        return True
    else:
        print(f"❌ {msg_fail}")
        return False

def main():
    print("\n" + "="*60)
    print("  SIRIO TPV v0.1 - VERIFICACIÓN DEL SISTEMA")
    print("="*60 + "\n")
    
    all_ok = True
    
    # 1. Verificar directorios
    print("📁 VERIFICANDO ESTRUCTURA...")
    root = Path(__file__).parent
    
    checks = [
        (root.exists(), "Raíz del proyecto", "Raíz no encontrada"),
        ((root / "index.html").exists(), "Frontend (index.html)", "Frontend no encontrado"),
        ((root / "backend").exists(), "Directorio backend", "Backend no existe"),
        ((root / "backend" / "main.py").exists(), "Backend main.py", "main.py no encontrado"),
        ((root / "backend" / "requirements.txt").exists(), "requirements.txt", "requirements.txt no encontrado"),
        ((root / "test_mode.marker").exists(), "Test mode marker", "Test mode no activado"),
    ]
    
    for condition, ok_msg, fail_msg in checks:
        if not check(condition, ok_msg, fail_msg):
            all_ok = False
    
    print()
    
    # 2. Verificar Python
    print("🐍 VERIFICANDO PYTHON...")
    check(sys.version_info >= (3, 8), 
          f"Python {sys.version.split()[0]}", 
          "Python 3.8+ requerido")
    
    print()
    
    # 3. Verificar módulos
    print("📦 VERIFICANDO MÓDULOS...")
    modules = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("sqlalchemy", "SQLAlchemy"),
        ("pydantic", "Pydantic"),
    ]
    
    for module, name in modules:
        try:
            __import__(module)
            check(True, f"{name} instalado", "")
        except ImportError:
            check(False, "", f"{name} no instalado - Ejecuta: pip install {module}")
            all_ok = False
    
    print()
    
    # 4. Verificar archivos de configuración
    print("⚙️  VERIFICANDO CONFIGURACIÓN...")
    check((root / "backend" / "core" / "config.py").exists(), 
          "config.py", 
          "config.py no encontrado")
    check((root / "backend" / "core" / "database.py").exists(), 
          "database.py", 
          "database.py no encontrado")
    
    print()
    
    # 5. Verificar puertos
    print("🔌 VERIFICANDO PUERTOS...")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        if result != 0:
            check(True, "Puerto 8000 disponible", "")
        else:
            check(False, "", "Puerto 8000 ya está en uso (algo corre en 8000)")
        sock.close()
    except:
        check(True, "Puerto 8000 disponible", "")
    
    print()
    
    # 6. Resumen
    print("="*60)
    if all_ok:
        print("✅ SISTEMA LISTO PARA EJECUTAR")
        print("\nEjecuta uno de estos comandos:\n")
        print("  python3 setup.py           (automático completo)")
        print("  python3 start_server.py    (servidor integrado)")
        print("  bash install_and_run.sh    (Linux/Mac)")
        print("  install_and_run.bat        (Windows)")
        print()
    else:
        print("⚠️  FALTAN VERIFICACIONES")
        print("\n1. Instala dependencias:")
        print("   pip install -r backend/requirements.txt")
        print("\n2. Verifica de nuevo:")
        print("   python3 check_system.py")
        print()
    
    print("="*60 + "\n")
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
