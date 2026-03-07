#!/usr/bin/env python3
"""
SIRIO TPV - Servidor Integrado
Sirve el frontend (index.html) y el backend (API) en un único servidor
"""

import sys
import os
import asyncio
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

# Cambiar al directorio del backend
os.chdir(backend_path)

try:
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse
    from fastapi.middleware.cors import CORSMiddleware
except ImportError:
    print("❌ Error: FastAPI no está instalado")
    print("\nInstala las dependencias con:")
    print("  pip install fastapi uvicorn sqlalchemy pydantic")
    sys.exit(1)

# Importar rutas del backend
try:
    from core.database import engine, Base
    from api.routes import tpv, productos, verifactu, reportes
    from core.config import settings
except ImportError as e:
    print(f"❌ Error importando módulos del backend: {e}")
    sys.exit(1)

# Crear aplicación con soporte de archivos estáticos
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

# Servir archivos estáticos del frontend
frontend_path = Path(__file__).parent
static_files_config = {
    "html": str(frontend_path),
    "css": str(frontend_path / "frontend" / "static") if (frontend_path / "frontend" / "static").exists() else str(frontend_path),
}

app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

@app.get("/")
async def root():
    """Servir index.html en la raíz"""
    index_file = frontend_path / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "SIRIO TPV API v0.1"}

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok", "service": "SIRIO TPV", "version": "0.1"}

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("  🚀 SIRIO TPV v0.1 - Servidor Integrado")
    print("="*60)
    print("\n📍 Frontend:  http://localhost:8000")
    print("📍 API:       http://localhost:8000/api")
    print("📍 Docs:      http://localhost:8000/docs")
    print("📍 Health:    http://localhost:8000/health")
    print("\n" + "-"*60 + "\n")
    
    # Crear tablas de BD
    Base.metadata.create_all(bind=engine)
    
    # Ejecutar servidor
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
