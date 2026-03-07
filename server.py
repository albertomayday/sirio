#!/usr/bin/env python3
"""
SIRIO TPV - Servidor Simple Integrado
Ejecuta todo en uno sin complicaciones
"""

import sys
import os
from pathlib import Path

# Setup path
root = Path(__file__).parent
backend = root / 'backend'
sys.path.insert(0, str(backend))
os.chdir(backend)

print("\n" + "="*70)
print(" " * 15 + "🚀 SIRIO TPV v0.1 - SERVIDOR INICIANDO")
print("="*70)

# Intentar importar o instalar
try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse
    from fastapi.staticfiles import StaticFiles
except ImportError:
    print("\n📦 Instalando dependencias...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", 
                   "fastapi>=0.104.1", "uvicorn[standard]>=0.24.0", 
                   "sqlalchemy>=2.0.23", "pydantic>=2.5.0"], check=False)
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse
    from fastapi.staticfiles import StaticFiles

# Importar rutas
try:
    from core.database import engine, Base
    from api.routes import tpv, productos, verifactu, reportes
except ImportError as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)

# Crear app
app = FastAPI(title="SIRIO TPV v0.1")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas API
app.include_router(tpv.router, prefix="/api/tpv", tags=["TPV"])
app.include_router(verifactu.router, prefix="/api/verifactu", tags=["Verifactu"])
app.include_router(productos.router, prefix="/api/productos", tags=["Productos"])
app.include_router(reportes.router, prefix="/api/reportes", tags=["Reportes"])

# Frontend
frontend_path = root / "index.html"

@app.get("/")
async def root():
    if frontend_path.exists():
        return FileResponse(str(frontend_path), media_type="text/html")
    return {"message": "SIRIO TPV API v0.1", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "ok", "service": "SIRIO TPV", "version": "0.1"}

if __name__ == "__main__":
    import uvicorn
    
    # Crear BD
    Base.metadata.create_all(bind=engine)
    
    # Mostrar info
    print("\n✅ Dependencias correctas")
    print("✅ Base de datos lista")
    print("\n📍 Frontend:        http://localhost:8000")
    print("📍 API:             http://localhost:8000/api")
    print("📍 Documentación:   http://localhost:8000/docs")
    print("\n" + "-"*70 + "\n")
    
    # Ejecutar
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
