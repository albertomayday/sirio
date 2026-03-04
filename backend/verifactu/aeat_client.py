import requests
from core.models import RegistroVERIFACTU
from core.database import SessionLocal
from datetime import datetime

def enviar_aeat(registro_id: int):
    # Use a new session for the background task
    db = SessionLocal()
    try:
        registro = db.query(RegistroVERIFACTU).filter(RegistroVERIFACTU.id == registro_id).first()
        if not registro:
            print(f"Error: Registro {registro_id} no encontrado para envío AEAT.")
            return False

        # Simulate sending to AEAT
        print(f"Enviando registro {registro.id} a AEAT...")
        # In a real scenario, this would make a SOAP/REST request to AEAT
        
        # Simulate network delay
        import time
        time.sleep(1)
        
        registro.estado_envio = "enviado"
        registro.csv_aeat = "CSV_SIMULADO_12345"
        registro.fecha_envio = datetime.utcnow()
        
        db.commit()
        print(f"Registro {registro.id} enviado correctamente.")
        return True
    except Exception as e:
        print(f"Error enviando a AEAT: {e}")
        db.rollback()
        return False
    finally:
        db.close()
