from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from api.routes import tpv, verifactu, productos, reportes
import sys
import os

# Import licensing modules
sys.path.append(os.path.dirname(__file__))
from licensing.dongle_manager import DongleManager
from licensing.validator import validar_licencia

from core.config import settings

# Check for dongle and license on startup
if settings.DONGLE_REQUIRED:
    dongle_manager = DongleManager()
    if not dongle_manager.check_dongle():
        print("CRITICAL ERROR: Security Dongle not found. System cannot start.")
        sys.exit(1)

    if not validar_licencia("license.key"):
        print("CRITICAL ERROR: Invalid or missing license. System cannot start.")
        sys.exit(1)
else:
    print("WARNING: Running in TEST MODE. Dongle check bypassed.")

Base.metadata.create_all(bind=engine)

# Initialize DB with sample data
from core.init_db import init_db
try:
    init_db()
except Exception as e:
    print(f"Error initializing DB: {e}")

app = FastAPI(title="TPV Verifactu")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tpv.router, prefix="/api/tpv", tags=["TPV"])
app.include_router(verifactu.router, prefix="/api/verifactu", tags=["Verifactu"])
app.include_router(productos.router, prefix="/api/productos", tags=["Productos"])
app.include_router(reportes.router, prefix="/api/reportes", tags=["Reportes"])

@app.get("/")
def read_root():
    return {"message": "TPV Verifactu API"}

if __name__ == "__main__":
    import uvicorn
    host = "0.0.0.0" if not settings.DONGLE_REQUIRED else "127.0.0.1"
    uvicorn.run(app, host=host, port=8000)
