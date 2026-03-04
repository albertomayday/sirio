import json
from cryptography.fernet import Fernet
from datetime import datetime
import os
from .dongle_manager import DongleManager

def validar_licencia(license_file: str) -> bool:
    # First, check for the dongle
    dongle_manager = DongleManager()
    if not dongle_manager.check_dongle():
        print("Error: Dongle de seguridad no detectado.")
        return False

    try:
        if not os.path.exists(license_file):
            return False
        
        with open(license_file, 'rb') as f:
            encrypted = f.read()
        
        # In a real scenario, the key should be securely managed
        # For this example, we assume a key is available or fetched
        key = os.getenv("MASTER_KEY")
        
        # Check in current directory
        if not key and os.path.exists("master.key"):
            with open("master.key", "r") as kf:
                key = kf.read().strip()
        
        # Check in parent directory (backend root) if running from a subdir
        if not key and os.path.exists("../master.key"):
             with open("../master.key", "r") as kf:
                key = kf.read().strip()

        if not key:
             print("CRITICAL ERROR: MASTER_KEY not found in environment or file system.")
             return False
        f = Fernet(key)
        licencia = json.loads(f.decrypt(encrypted))
        
        # Verify if the license is bound to the dongle ID (optional but recommended)
        if "dongle_id" in licencia and licencia["dongle_id"] != dongle_manager.dongle_id:
             print("Error: La licencia no corresponde al dongle conectado.")
             return False

        if datetime.now() > datetime.fromisoformat(licencia["expiracion"]):
            return False
        
        return True
    except Exception as e:
        print(f"Error validando licencia: {e}")
        return False
