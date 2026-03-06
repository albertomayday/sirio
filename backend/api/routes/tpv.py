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
    """
    Create a new ticket with lines and automatic Verifactu registration.
    Correctly handles VAT calculation per line item.
    """
    from core.models import Producto
    
    # 1. Calculate totals with correct VAT per line
    lineas_procesadas = []
    subtotal_total = Decimal(0)
    iva_total = Decimal(0)
    
    for linea in ticket.lineas:
        # Get product to retrieve VAT rate
        producto = db.query(Producto).filter(Producto.id == linea.producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {linea.producto_id} no encontrado")
        
        # Calculate line totals
        linea_total = linea.precio * linea.cantidad
        tasa_iva = Decimal(producto.iva) / Decimal(100)
        
        # Correct calculation: subtotal = total / (1 + tasa_iva)
        linea_subtotal = linea_total / (1 + tasa_iva)
        linea_iva = linea_total - linea_subtotal
        
        lineas_procesadas.append({
            "producto_id": linea.producto_id,
            "nombre": linea.nombre,
            "cantidad": linea.cantidad,
            "precio_unitario": float(linea.precio),
            "tasa_iva": producto.iva,
            "subtotal": float(linea_subtotal),
            "iva": float(linea_iva),
            "total": float(linea_total)
        })
        
        subtotal_total += linea_subtotal
        iva_total += linea_iva
    
    total = subtotal_total + iva_total
    
    # 2. Create ticket
    nuevo_ticket = Ticket(
        numero=f"T-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        sesion_id=ticket.sesion_id,
        lineas=lineas_procesadas,
        subtotal=subtotal_total,
        iva=iva_total,
        total=total,
        tipo=ticket.tipo,
        estado="emitido"
    )
    db.add(nuevo_ticket)
    db.commit()
    db.refresh(nuevo_ticket)
    
    # 3. Verifactu integration
    if ticket.tipo == "factura":
        try:
            registro = crear_registro_verifactu(nuevo_ticket, db)
            db.commit()
            
            # 4. Send to AEAT in background
            background_tasks.add_task(enviar_aeat, registro.id)
        except Exception as e:
            print(f"Error Verifactu: {e}")
            # Don't fail the ticket creation if Verifactu fails
            # but log it for monitoring
            
    return nuevo_ticket

@router.get("/mesas")
def listar_mesas(db: Session = Depends(get_db)):
    return db.query(Mesa).all()
