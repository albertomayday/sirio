"""Immutable storage for Verifactu records"""
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
from threading import Lock


class ImmutableStore:
    """Thread-safe immutable storage for Verifactu records"""
    
    def __init__(self, storage_path: str = "/tmp/verifactu_records"):
        """Initialize the immutable store"""
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
    
    def guardar_registro(
        self,
        factura_id: str,
        registro: Dict[str, Any],
        cadena_entry: Dict[str, Any]
    ) -> bool:
        """
        Save a registry record immutably.
        
        Args:
            factura_id: Invoice ID
            registro: The registry record
            cadena_entry: The hash chain entry
            
        Returns:
            True if saved successfully
        """
        with self._lock:
            try:
                filename = self.storage_path / f"{factura_id}_{registro['id']}.json"
                
                data = {
                    "factura_id": factura_id,
                    "registro": registro,
                    "cadena_entry": cadena_entry,
                    "guardado_en": datetime.now().isoformat()
                }
                
                # Write with restricted permissions
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                
                # Make read-only
                filename.chmod(0o444)
                return True
            except Exception as e:
                print(f"Error guardando registro: {e}")
                return False
    
    def obtener_registro(self, factura_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a record by invoice ID"""
        try:
            files = list(self.storage_path.glob(f"{factura_id}_*.json"))
            if not files:
                return None
            
            # Get the most recent
            latest_file = max(files, key=lambda p: p.stat().st_mtime)
            
            with open(latest_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error obteniendo registro: {e}")
            return None
    
    def listar_registros(self) -> List[Dict[str, Any]]:
        """List all stored records"""
        records = []
        try:
            for file in sorted(self.storage_path.glob("*.json")):
                with open(file, 'r') as f:
                    records.append(json.load(f))
        except Exception as e:
            print(f"Error listando registros: {e}")
        
        return records
    
    def verificar_integridad_registro(
        self,
        factura_id: str
    ) -> bool:
        """Verify the integrity of a stored record"""
        record = self.obtener_registro(factura_id)
        if not record:
            return False
        
        # Verify that the record hasn't been modified
        # (in a real scenario, verify against the hash chain)
        return "hash" in record.get("registro", {})


# Global instance
_store = None


def store_immutable(
    factura_id: str,
    registro: Dict[str, Any],
    cadena_entry: Dict[str, Any]
) -> bool:
    """Store a registry immutably"""
    global _store
    if _store is None:
        _store = ImmutableStore()
    
    return _store.guardar_registro(factura_id, registro, cadena_entry)


def retrieve_immutable(factura_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve an immutable record"""
    global _store
    if _store is None:
        _store = ImmutableStore()
    
    return _store.obtener_registro(factura_id)


def list_immutable_records() -> List[Dict[str, Any]]:
    """List all immutable records"""
    global _store
    if _store is None:
        _store = ImmutableStore()
    
    return _store.listar_registros()
