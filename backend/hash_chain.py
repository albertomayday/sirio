"""Hash chain implementation for record linking"""
import hashlib
from typing import Dict, Any, List
from datetime import datetime


class HashChain:
    """Implements a hash chain for linking Verifactu records"""
    
    def __init__(self):
        """Initialize the hash chain"""
        self.chain: List[Dict[str, Any]] = []
        self.previous_hash = "0" * 64  # Initial hash (all zeros)
    
    def agregar_a_cadena(
        self,
        registro: Dict[str, Any],
        factura_id: str
    ) -> Dict[str, Any]:
        """
        Add a record to the hash chain.
        
        Args:
            registro: The registry record to add
            factura_id: Invoice ID for linking
            
        Returns:
            The chain entry with hash references
        """
        # Create entry linking to previous record
        entry_content = f"{self.previous_hash}{registro['hash']}{factura_id}"
        current_hash = hashlib.sha256(entry_content.encode()).hexdigest()
        
        entry = {
            "index": len(self.chain),
            "timestamp": datetime.now().isoformat(),
            "factura_id": factura_id,
            "record_hash": registro['hash'],
            "previous_hash": self.previous_hash,
            "chain_hash": current_hash
        }
        
        self.chain.append(entry)
        self.previous_hash = current_hash
        
        return entry
    
    def verificar_integridad(self) -> bool:
        """Verify the integrity of the entire chain"""
        if not self.chain:
            return True
        
        previous_hash = "0" * 64
        for entry in self.chain:
            entry_content = (
                f"{entry['previous_hash']}{entry['record_hash']}"
                f"{entry['factura_id']}"
            )
            calculated_hash = hashlib.sha256(entry_content.encode()).hexdigest()
            
            if calculated_hash != entry['chain_hash']:
                return False
            
            previous_hash = entry['chain_hash']
        
        return True
    
    def obtener_ultimo_hash(self) -> str:
        """Get the hash of the last chain entry"""
        return self.previous_hash if self.chain else "0" * 64
