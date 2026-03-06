import json
import logging
from cryptography.fernet import Fernet
from datetime import datetime
import os
from .dongle_manager import DongleManager


logger = logging.getLogger(__name__)


def validar_licencia(license_file: str) -> bool:
    """
    Validate the license file against the security dongle and expiration date.
    
    Args:
        license_file: Path to the encrypted license file
        
    Returns:
        True if license is valid, False otherwise
    """
    # First, check for the dongle
    dongle_manager = DongleManager()
    if not dongle_manager.check_dongle():
        logger.error("Dongle de seguridad no detectado.")
        return False

    try:
        if not os.path.exists(license_file):
            logger.error(f"Archivo de licencia no encontrado: {license_file}")
            return False
        
        # Read encrypted license
        with open(license_file, 'rb') as f:
            encrypted = f.read()
        
        # Get master key from environment or file
        master_key = _obtener_master_key()
        if not master_key:
            logger.error("MASTER_KEY no encontrado en variables de entorno o archivos.")
            return False
        
        # Decrypt license
        try:
            f = Fernet(master_key)
            licencia_json = f.decrypt(encrypted)
            licencia = json.loads(licencia_json)
        except Exception as e:
            logger.error(f"Error descifrando licencia: {e}")
            return False
        
        # Validate required fields
        required_fields = ["dongle_id", "expiracion"]
        if not all(field in licencia for field in required_fields):
            logger.error("Campos requeridos faltantes en licencia")
            return False
        
        # Verify license is bound to connected dongle
        # Note: In test mode, dongle_id might be None
        if licencia.get("dongle_id") and dongle_manager.dongle_id:
            if licencia["dongle_id"] != dongle_manager.dongle_id:
                logger.error("Licencia no vinculada al dongle conectado")
                return False
        
        # Check expiration date
        try:
            fecha_expiracion = datetime.fromisoformat(licencia["expiracion"])
        except Exception as e:
            logger.error(f"Formato de fecha de expiración inválido: {e}")
            return False
        
        if datetime.now() > fecha_expiracion:
            logger.error(f"Licencia expirada desde {fecha_expiracion.isoformat()}")
            return False
        
        # All validations passed
        dias_restantes = (fecha_expiracion - datetime.now()).days
        logger.info(f"Licencia válida. Días restantes: {dias_restantes}")
        return True
        
    except Exception as e:
        logger.error(f"Error validando licencia: {e}")
        return False


def _obtener_master_key() -> bytes:
    """
    Get the master key from environment variable or file system.
    
    Returns:
        Master key bytes, or None if not found
    """
    # Try environment variable first
    master_key = os.getenv("MASTER_KEY")
    if master_key:
        try:
            return master_key.encode() if isinstance(master_key, str) else master_key
        except Exception:
            pass
    
    # Try current directory
    if os.path.exists("master.key"):
        try:
            with open("master.key", "r") as f:
                key_str = f.read().strip()
                return key_str.encode()
        except Exception as e:
            logger.warning(f"Error leyendo master.key en directorio actual: {e}")
    
    # Try parent directory (when running from subdirectory)
    if os.path.exists("../master.key"):
        try:
            with open("../master.key", "r") as f:
                key_str = f.read().strip()
                return key_str.encode()
        except Exception as e:
            logger.warning(f"Error leyendo master.key en directorio padre: {e}")
    
    # Try backend directory
    if os.path.exists("backend/master.key"):
        try:
            with open("backend/master.key", "r") as f:
                key_str = f.read().strip()
                return key_str.encode()
        except Exception as e:
            logger.warning(f"Error leyendo master.key en backend: {e}")
    
    return None

