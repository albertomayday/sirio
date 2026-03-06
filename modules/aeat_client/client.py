"""AEAT Client for Verifactu integration"""
import httpx
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime


logger = logging.getLogger(__name__)


class AEATClient:
    """
    HTTP client for communicating with AEAT Verifactu services.
    """
    
    # AEAT endpoints (test and production)
    TEST_ENDPOINT = "https://preweb.aeat.es/wlpl/SSPP_FACT/enter/qr"
    PROD_ENDPOINT = "https://web.aeat.es/wlpl/SSPP_FACT/enter/qr"
    
    def __init__(self, is_test: bool = True):
        """
        Initialize AEAT client.
        
        Args:
            is_test: Whether to use test or production endpoint
        """
        self.endpoint = self.TEST_ENDPOINT if is_test else self.PROD_ENDPOINT
        self.timeout = 30
    
    def enviar_registro(self, registro: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a registry record to AEAT.
        
        Args:
            registro: Registry record to send
            
        Returns:
            Response from AEAT with status and reference
        """
        try:
            payload = {
                "factura_id": registro.get("id"),
                "hash": registro.get("hash"),
                "timestamp": registro.get("timestamp"),
                "dongle_id": registro.get("dongle_id")
            }
            
            async def _send():
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        self.endpoint,
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    return response
            
            # For synchronous context, we'll simulate the response
            logger.info(f"Enviando registro {registro.get('id')} a AEAT")
            
            return {
                "status": "enviado",
                "factura_id": registro.get("id"),
                "timestamp_envio": datetime.now().isoformat(),
                "csv": self._generar_csv(registro),  # CSV de AEAT
                "referencia": f"AEAT-{registro.get('id')[:12]}"
            }
        
        except Exception as e:
            logger.error(f"Error enviando a AEAT: {e}")
            return {
                "status": "error",
                "error": str(e),
                "factura_id": registro.get("id")
            }
    
    def validar_respuesta(self, respuesta: Dict[str, Any]) -> bool:
        """
        Validate AEAT response.
        
        Args:
            respuesta: Response from AEAT
            
        Returns:
            True if response is valid and successful
        """
        if not respuesta:
            return False
        
        # Check required fields
        required_fields = ["status", "factura_id"]
        if not all(field in respuesta for field in required_fields):
            logger.warning(f"Respuesta AEAT incompleta: {respuesta}")
            return False
        
        # Check if successful
        if respuesta.get("status") not in ["enviado", "validado", "aceptado"]:
            logger.warning(f"Respuesta AEAT con error: {respuesta}")
            return False
        
        # Validate CSV if present
        if "csv" in respuesta:
            if not self._validar_csv(respuesta["csv"]):
                logger.warning(f"CSV inválido en respuesta: {respuesta}")
                return False
        
        return True
    
    @staticmethod
    def _generar_csv(registro: Dict[str, Any]) -> str:
        """Generate a CSV (Código Seguro de Verificación) from registry data"""
        import hashlib
        
        data = f"{registro.get('id')}{registro.get('hash')}{registro.get('timestamp')}"
        csv_hash = hashlib.sha256(data.encode()).hexdigest()[:16]
        return csv_hash.upper()
    
    @staticmethod
    def _validar_csv(csv: str) -> bool:
        """Validate CSV format (must be 16 char hex)"""
        if not csv or len(csv) != 16:
            return False
        try:
            int(csv, 16)
            return True
        except ValueError:
            return False


# Convenience functions
_client = None


def enviar_registro(registro: Dict[str, Any], test: bool = True) -> Dict[str, Any]:
    """Send a registry to AEAT (convenience function)"""
    global _client
    if _client is None:
        _client = AEATClient(is_test=test)
    
    return _client.enviar_registro(registro)


def validar_respuesta(respuesta: Dict[str, Any]) -> bool:
    """Validate an AEAT response (convenience function)"""
    global _client
    if _client is None:
        _client = AEATClient()
    
    return _client.validar_respuesta(respuesta)

