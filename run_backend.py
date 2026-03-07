#!/usr/bin/env python3
"""
SIRIO TPV - Ejecutor de Backend
Ejecuta el servidor FastAPI de forma simple
"""

import subprocess
import sys

if __name__ == '__main__':
    try:
        # Ejecutar main.py del backend
        exec(open('/workspaces/sirio/backend/main.py').read())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
