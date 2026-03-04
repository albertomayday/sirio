from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.models import Ticket, Sesion
from datetime import date

router = APIRouter()

from sqlalchemy import func

@router.get("/ventas")
def reporte_ventas(fecha_desde: date, fecha_hasta: date, db: Session = Depends(get_db)):
    ventas = db.query(Ticket).filter(
        func.date(Ticket.fecha) >= fecha_desde,
        func.date(Ticket.fecha) <= fecha_hasta
    ).all()
    
    total_ventas = sum(t.total for t in ventas if t.total)
    return {
        "periodo": {"desde": fecha_desde, "hasta": fecha_hasta},
        "total_ventas": float(total_ventas),
        "cantidad_tickets": len(ventas),
        "tickets": ventas
    }

@router.get("/productos-top")
def productos_mas_vendidos(db: Session = Depends(get_db)):
    # This is a simplified implementation. In a real scenario, we would aggregate from ticket lines.
    # Since lines are stored as JSON, complex aggregation might be tricky in SQL directly depending on DB.
    # Here we fetch all tickets and aggregate in Python for simplicity, or use a more normalized schema.
    tickets = db.query(Ticket).all()
    product_counts = {}
    
    for ticket in tickets:
        if ticket.lineas:
            for linea in ticket.lineas:
                pid = linea.get('id')
                qty = linea.get('cantidad', 1)
                if pid:
                    product_counts[pid] = product_counts.get(pid, 0) + qty
    
    sorted_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)
    return [{"producto_id": pid, "cantidad": qty} for pid, qty in sorted_products[:10]]

@router.get("/arqueo/{sesion_id}")
def arqueo_caja(sesion_id: int, db: Session = Depends(get_db)):
    sesion = db.query(Sesion).filter(Sesion.id == sesion_id).first()
    if not sesion:
        return {"error": "Sesion no encontrada"}
    
    tickets_sesion = db.query(Ticket).filter(Ticket.sesion_id == sesion_id).all()
    total_efectivo = sum(t.total for t in tickets_sesion if t.tipo == 'efectivo') # Assuming 'tipo' or payment method logic
    total_tarjeta = sum(t.total for t in tickets_sesion if t.tipo == 'tarjeta')
    
    return {
        "sesion": sesion,
        "resumen": {
            "total_ventas": float(sum(t.total for t in tickets_sesion if t.total)),
            "total_efectivo": float(total_efectivo),
            "total_tarjeta": float(total_tarjeta),
            "cantidad_tickets": len(tickets_sesion)
        }
    }
