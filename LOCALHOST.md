# 🚀 SIRIO TPV v0.1 - LOCALHOST

## ⚡ EJECUTA AHORA (Desde raíz del proyecto)

```bash
python3 server.py
```

O:

```bash
python3 start.py
```

## ✅ Listo en 30 segundos

Una vez ejecutado:
- 🌐 **Frontend**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs
- 🔌 **API Productos**: http://localhost:8000/api/productos/

## 📊 Lo que verás

### Tab "Mesas"
- 10 mesas (M1-M10)
- Click para abrir comanda

### Tab "Comandas"
- Seleccionar mesa
- Agregar productos (18+ items)
- Númepad integrado
- Confirmar comanda

### Tab "Cobros"
- Seleccionar mesa con cuenta
- Métodos: Efectivo, Tarjeta, Bizum
- VERIFACTu generado automáticamente

### Tab "Usuarios"
- Gestión de cajeros
- Histórico de ventas

## 🎯 Test Rápido

1. Click en **Mesa 1**
2. Click en producto (ej: **Agua 1.5L**)
3. Aumentar cantidad con númepad
4. Click **✓ Confirmar**
5. Click en **Tab Cobros**
6. Seleccionar Mesa 1
7. Click **✓ Cobrar**

¡Listo! Sistema 100% operativo ✨

## 🆘 Si algo falla

```bash
# Verificar sistema
python3 check_system.py

# Instalar dependencias manualmente
pip install fastapi uvicorn sqlalchemy pydantic

# Ver logs del backend
tail -f /workspaces/sirio/backend/tpv.db
```

---

**Versión 0.1 | Localhost Ready ✅**
