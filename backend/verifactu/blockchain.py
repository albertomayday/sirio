import hashlib

def calcular_hash_sha256(contenido: str, hash_anterior: str) -> str:
    """
    Calcula el hash SHA-256 encadenado.
    El contenido debe ser la representación canónica del registro.
    """
    data = f"{contenido}{hash_anterior}".encode('utf-8')
    return hashlib.sha256(data).hexdigest()
