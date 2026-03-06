"""QR Code generation and digital signing for invoices"""
import qrcode
import json
import logging
from typing import Dict, Any, Optional
from io import BytesIO
from pathlib import Path


logger = logging.getLogger(__name__)


def generar_qr(
    factura: Dict[str, Any],
    output_path: Optional[str] = None,
    size: int = 10,
    border: int = 2
) -> Optional[bytes]:
    """
    Generate a QR code for invoice consultation.
    
    Args:
        factura: Invoice data dictionary
        output_path: Optional path to save QR code image
        size: QR code size (pixels per box)
        border: Border size in boxes
        
    Returns:
        QR code image bytes, or None if error
    """
    try:
        # Create QR data from invoice essentials
        qr_data = {
            "id": factura.get("id"),
            "total": str(factura.get("total", 0)),
            "fecha": factura.get("fecha"),
            "emisor_nif": factura.get("emisor_nif"),
            "receptor_nif": factura.get("receptor_nif", "CONSUMIDOR"),
            "csv": factura.get("csv"),  # Código Seguro de Verificación
        }
        
        # Convert to JSON string (compact)
        qr_text = json.dumps(qr_data, separators=(',', ':'))
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,  # Auto-detect if needed
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
            box_size=size,
            border=border,
        )
        qr.add_data(qr_text)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to file if path provided
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            img.save(output_file, format='PNG')
            logger.info(f"QR guardado en: {output_path}")
        
        # Also return as bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()
    
    except Exception as e:
        logger.error(f"Error generando QR: {e}")
        return None


def firmar_digital(
    registro: Dict[str, Any],
    private_key: Optional[bytes] = None
) -> Dict[str, Any]:
    """
    Apply digital signature to registry according to Verifactu requirements.
    
    Args:
        registro: Registry record to sign
        private_key: Optional private key for signing (base64 encoded)
        
    Returns:
        Dictionary with signature metadata
    """
    import hashlib
    from datetime import datetime
    
    try:
        # Create a deterministic string from the registry
        registry_str = json.dumps(
            {k: v for k, v in registro.items() if k not in ["firma", "firma_timestamp"]},
            sort_keys=True,
            separators=(',', ':')
        )
        
        # Generate signature hash
        signature_hash = hashlib.sha256(registry_str.encode()).hexdigest()
        
        # In a real scenario, this would use RSA or ECDSA signing
        # For now, we simulate with hash-based signature
        
        firma_metadata = {
            "algoritmo": "SHA256",
            "timestamp": datetime.now().isoformat(),
            "firma": signature_hash,
            "tipo": "DIGITAL_SIMULATED",  # Mark as simulated for non-production
            "estado": "firmado"
        }
        
        return firma_metadata
    
    except Exception as e:
        logger.error(f"Error firmando digitalmente: {e}")
        return {
            "estado": "error",
            "error": str(e)
        }


def validar_firma(
    registro: Dict[str, Any],
    firma_metadata: Dict[str, Any]
) -> bool:
    """
    Validate digital signature of a registry.
    
    Args:
        registro: Registry record to validate
        firma_metadata: Signature metadata to verify against
        
    Returns:
        True if signature is valid
    """
    import hashlib
    
    try:
        # Recreate the registry string for verification
        registry_str = json.dumps(
            {k: v for k, v in registro.items() if k not in ["firma", "firma_timestamp"]},
            sort_keys=True,
            separators=(',', ':')
        )
        
        # Recalculate the hash
        expected_hash = hashlib.sha256(registry_str.encode()).hexdigest()
        
        # Compare with provided signature
        return expected_hash == firma_metadata.get("firma")
    
    except Exception as e:
        logger.error(f"Error validando firma: {e}")
        return False

