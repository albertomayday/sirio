from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.models import RegistroVERIFACTU

router = APIRouter()

@router.get("/registros")
def listar_registros(db: Session = Depends(get_db)):
    return db.query(RegistroVERIFACTU).all()

@router.get("/registros/{id}/pdf")
def descargar_pdf(id: int, db: Session = Depends(get_db)):
    # Implement PDF generation logic here
    pass

@router.post("/sincronizar")
def sincronizar_pendientes(db: Session = Depends(get_db)):
    # Implement synchronization logic here
    pass
