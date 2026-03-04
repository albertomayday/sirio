from core.models import Ticket, RegistroVERIFACTU
from .blockchain import calcular_hash_sha256
from sqlalchemy.orm import Session
from sqlalchemy import desc

def crear_registro_verifactu(ticket: Ticket, db: Session) -> RegistroVERIFACTU:
    # Retrieve the last registered VeriFactu record to chain the hash
    ultimo = db.query(RegistroVERIFACTU).order_by(desc(RegistroVERIFACTU.id)).first()
    hash_anterior = ultimo.hash_actual if ultimo else "0" * 64
    
    # Simplified XML construction for demonstration
    xml = f"<Registro><Ticket>{ticket.numero}</Ticket><HashAnterior>{hash_anterior}</HashAnterior></Registro>"
    
    hash_actual = calcular_hash_sha256(xml, hash_anterior)
    
    # Simplified signature and QR generation
    firma = "firma_simulada"
    qr_data = f"https://verifactu.gob.es/verify?hash={hash_actual}"
    
    registro = RegistroVERIFACTU(
        ticket_id=ticket.id,
        hash_anterior=hash_anterior,
        hash_actual=hash_actual,
        xml_registro=xml,
        firma_xades=firma,
        qr_data=qr_data,
        estado_envio="pendiente"
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)
    
    return registro
