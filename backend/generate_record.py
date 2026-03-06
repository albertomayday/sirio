"""Generate Verifactu invoice records"""
import json
import hashlib
from datetime import datetime
from typing import Dict, Any


def generar_registro(
    factura_data: Dict[str, Any],
    dongle_id: str = None
) -> Dict[str, Any]:
    """
    Generate a registry record for Verifactu submission.
    
    Args:
        factura_data: Invoice data dictionary
        dongle_id: Security dongle ID
        
    Returns:
        Dictionary with generated record metadata
    """
    timestamp = datetime.now().isoformat()
    
    # Create a deterministic record ID based on invoice data
    record_hash = hashlib.sha256(
        json.dumps(factura_data, sort_keys=True).encode()
    ).hexdigest()
    
    return {
        "id": record_hash[:16],
        "timestamp": timestamp,
        "factura_id": factura_data.get("id"),
        "hash": record_hash,
        "dongle_id": dongle_id,
        "status": "generated"
    }


def validar_registro(registro: Dict[str, Any]) -> bool:
    """Validate a registry record structure"""
    required_fields = ["id", "timestamp", "factura_id", "hash"]
    return all(field in registro for field in required_fields)
