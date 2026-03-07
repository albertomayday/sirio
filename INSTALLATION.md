# 🚀 SIRIO TPV v0.1 - GUÍA DE INSTALACIÓN Y USO

## ⚡ Inicio Rápido (3 pasos)

### OPCIÓN 1: Script Automático (Recomendado)

#### Linux/Mac:
```bash
cd /workspaces/sirio
bash install_and_run.sh
```

#### Windows:
```cmd
cd C:\workspaces\sirio
install_and_run.bat
```

#### Python (Todas las plataformas):
```bash
cd /workspaces/sirio
python3 setup.py
```

---

## 📋 Instalación Manual

Si prefieres instalar paso a paso:

### Paso 1: Instalar dependencias

```bash
cd /workspaces/sirio/backend
pip install -r requirements.txt
```

O instalar mínimo requerido:
```bash
pip install fastapi uvicorn sqlalchemy pydantic cryptography
```

### Paso 2: Ejecutar backend

```bash
python main.py
```

O con uvicorn en modo desarrollo:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Paso 3: Acceder al frontend

Abre en tu navegador:
- **Frontend**: `http://localhost:8000` (si está servido) o `file:///workspaces/sirio/index.html`
- **API Docs**: `http://localhost:8000/docs`

---

## ✅ Verificación de Instalación

### 1. Verificar que pip está actualizado
```bash
python3 -m pip --version
```

### 2. Verificar FastAPI está instalado
```bash
python3 -c "import fastapi; print(fastapi.__version__)"
```

### 3. Probar conexión a API
```bash
curl http://localhost:8000/api/productos/
```

---

## 📊 Estructura del Proyecto

```
/workspaces/sirio/
├── index.html                  ← Frontend (TPV Mesas)
├── backend/
│   ├── main.py                 ← Servidor FastAPI
│   ├── requirements.txt         ← Dependencias
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── models.py
│   ├── api/
│   │   ├── routes/
│   │   │   ├── tpv.py         ← Puntos de venta
│   │   │   ├── productos.py   ← Gestión de productos
│   │   │   ├── verifactu.py   ← VERIFACTu (fiscalidad)
│   │   │   └── reportes.py    ← Reportes
│   ├── licensing/              ← Sistema de licencias
│   └── verifactu/              ← Módulo VERIFACTu
├── setup.py                    ← Setup automático
├── install_and_run.sh          ← Script Linux/Mac
└── install_and_run.bat         ← Script Windows
```

---

## 🔧 Configuración

### Variables de Entorno

Crear archivo `.env` en `/workspaces/sirio/backend/`:

```env
# Base de datos (SQLite por defecto)
DATABASE_URL=sqlite:///./tpv.db

# Modo desarrollo
DEBUG=true
DONGLE_REQUIRED=false

# Logging
LOG_LEVEL=INFO
```

---

## 🌐 Endpoints de API

### Productos
- `GET /api/productos/` - Listar todos los productos
- `POST /api/productos/` - Crear producto
- `GET /api/productos/{id}` - Obtener producto
- `PUT /api/productos/{id}` - Actualizar producto
- `DELETE /api/productos/{id}` - Eliminar producto

### Ventas (TPV)
- `POST /api/tpv/venta` - Registrar venta
- `GET /api/tpv/ventas` - Listar ventas
- `GET /api/tpv/reportes` - Reportes

### VERIFACTu
- `POST /api/verifactu/registro` - Registrar en VERIFACTu
- `GET /api/verifactu/estado/{hash}` - Verificar estado

---

## 🎨 Frontend

El `index.html` incluye:

✅ **Interfaz de Mesas**
- Vista general de mesas del local
- Estados: Libre, Ocupada, Cuenta pedida

✅ **Panel de Comandas**
- Selector de mesas
- Catálogo de productos
- Númer pad para cantidades y descuentos
- Ticket en tiempo real

✅ **Panel de Cobros**
- Lista de mesas pendientes
- Métodos de pago (Efectivo, Tarjeta, Bizum)
- Integración con VERIFACTu

✅ **Gestión de Usuarios**
- Activación/desactivación de cajeros
- Histórico de ventas
- Estadísticas por usuario

---

## 🔒 Modo Test

Para ejecutar SIN dongle físico:

Crear archivo `/workspaces/sirio/test_mode.marker`:
```
TEST MODE ACTIVE
```

O variable de entorno:
```bash
export DONGLE_REQUIRED=false
```

---

## ❓ Troubleshooting

### Error: "ModuleNotFoundError: No module named 'fastapi'"

**Solución:**
```bash
pip install fastapi uvicorn
```

### Error: "Database connection failed"

**Solución:** Verificar `DATABASE_URL` en `.env` o use SQLite (por defecto)

### Error: "Port 8000 already in use"

**Solución:** Cambiar puerto en `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Cambiar puerto
```

### Frontend no carga productos

**Verificar:**
1. Backend está corriendo en http://localhost:8000
2. API está respondiendo: `curl http://localhost:8000/api/productos/`
3. Revisar consola del navegador (F12 > Console)

---

## 📞 Soporte

Para más información, revisar:
- `README.md` - Documentación principal
- `backend/requirements.txt` - Dependencias
- Código fuente en `backend/main.py`

---

**Versión:** 0.1  
**Fecha:** 2026-03-07  
**Estado:** ✅ Operativo
