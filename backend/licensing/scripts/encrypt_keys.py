from cryptography.fernet import Fernet
import json
import os

def generar_licencia(cliente_id: str, expiracion: str, key: bytes):
    licencia = {
        "cliente_id": cliente_id,
        "expiracion": expiracion,
        "features": ["tpv", "verifactu", "reportes"],
        "max_tickets_dia": 500
    }
    
    f = Fernet(key)
    encrypted = f.encrypt(json.dumps(licencia).encode())
    
    with open(f"{cliente_id}.lic", "wb") as f:
        f.write(encrypted)
    
    print(f"Licencia generada para {cliente_id}")

if __name__ == "__main__":
    key = Fernet.generate_key()
    print(f"Master Key: {key.decode()}")
    generar_licencia("cliente_demo", "2025-12-31", key)
