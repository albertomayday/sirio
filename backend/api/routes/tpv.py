from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from core.database import get_db
from core.models import Sesion, Ticket, Mesa
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from verifactu.registro import crear_registro_verifactu
from verifactu.aeat_client import enviar_aeat

router = APIRouter()

class LineaTicket(BaseModel):
    producto_id: int
    cantidad: int
    precio: Decimal
    nombre: str

class TicketCreate(BaseModel):
    sesion_id: int
    lineas: List[LineaTicket]
    tipo: str

@router.post("/sesion/abrir")
def abrir_caja(efectivo_inicial: Decimal, usuario: str, db: Session = Depends(get_db)):
    sesion = Sesion(usuario=usuario, efectivo_inicial=efectivo_inicial, estado="abierta")
    db.add(sesion)
    db.commit()
    db.refresh(sesion)
    return sesion

@router.post("/sesion/cerrar")
def cerrar_caja(sesion_id: int, efectivo_final: Decimal, db: Session = Depends(get_db)):
    sesion = db.query(Sesion).filter(Sesion.id == sesion_id).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesion no encontrada")
    sesion.cierre = datetime.utcnow()
    sesion.efectivo_final = efectivo_final
    sesion.estado = "cerrada"
    db.commit()
    return sesion



@router.post("/tickets")
def crear_ticket(ticket: TicketCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. Crear ticket
    total = sum(l.precio * l.cantidad for l in ticket.lineas)
    subtotal = total / Decimal(1.21) # Assuming 21% VAT for simplicity
    iva = total - subtotal
    
    nuevo_ticket = Ticket(
        numero=f"T-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        sesion_id=ticket.sesion_id,
        lineas=[l.dict() for l in ticket.lineas],
        subtotal=subtotal,
        iva=iva,
        total=total,
        tipo=ticket.tipo,
        estado="emitido"
    )
    db.add(nuevo_ticket)
    db.commit()
    db.refresh(nuevo_ticket)
    
    # 2. Verifactu integration
    if ticket.tipo == "factura":
        try:
            registro = crear_registro_verifactu(nuevo_ticket, db)
            # nuevo_ticket.registro_id = registro.id # Removed due to circular dependency fix
            db.commit()
            
            # 3. Send to AEAT in background
            background_tasks.add_task(enviar_aeat, registro.id)
        except Exception as e:
            print(f"Error Verifactu: {e}")
            
    return nuevo_ticket

@router.get("/mesas")
def listar_mesas(db: Session = Depends(get_db)):
    return db.query(Mesa).all()
