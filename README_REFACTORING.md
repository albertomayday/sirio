# 🚀 SIRIO - TPV Verifactu operativo

Sistema de punto de venta (TPV) táctil para hostelería con cumplimiento automático **VERI*FACTU** mediante integración con AEAT.

## ⚡ Inicio Rápido

### Requisitos Previos
- Docker y Docker Compose
- Git
- (Opcional) Python 3.11+ para desarrollo local

### Instalación y Ejecución

#### Opción 1: Con Docker (Recomendado)

```bash
# Clonar repositorio
git clone <repo-url>
cd sirio

# Copiar configuración de ejemplo
cp .env.example .env

# Iniciar servicios
docker-compose up --build

# Acceder a la aplicación
# Frontend:  http://localhost
# API Docs:  http://localhost/docs
# Backend:   http://localhost:8000
```

#### Opción 2: Desarrollo Local

```bash
# Instalar dependencias
cd backend
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Ejecutar backend
bash run_backend.sh
```

## 📁 Estructura del Proyecto

```
sirio/
├── backend/               # FastAPI Backend
│   ├── api/              # Rutas API
│   │   └── routes/
│   │       ├── tpv.py           # Operaciones TPV
│   │       ├── verifactu.py      # Integración Verifactu
│   │       ├── productos.py      # Gestión productos
│   │       └── reportes.py       # Reportes y auditoría
│   ├── core/             # Módulos centrales
│   │   ├── config.py     # Configuración
│   │   ├── database.py   # Conexión BD
│   │   ├── models.py     # Modelos SQLAlchemy
│   │   └── init_db.py    # Inicialización BD
│   ├── verifactu/        # Integración Verifactu
│   │   ├── aeat_client.py        # Cliente AEAT
│   │   ├── registro.py           # Registro Verifactu
│   │   └── xml_generator.py      # Generador XML
│   ├── licensing/        # Sistema de licenciamiento
│   │   ├── dongle_manager.py     # Gestor dongle USB
│   │   └── validator.py          # Validador licencia
│   ├── requirements.txt  # Dependencias Python
│   ├── main.py          # Punto de entrada
│   ├── Dockerfile       # Dockerfile optimizado
│   └── run_backend.sh   # Script arranque local
│
├── frontend/             # SPA React
│   ├── index.html       # HTML principal
│   ├── static/          # Assets compilados
│   └── nginx.conf       # Configuración Nginx
│
├── modules/             # Módulos compartidos
│   ├── aeat_client/     # Cliente AEAT refactorizado
│   └── factura_utils/   # Utilidades facturación
│
├── agents/              # Agentes OpenClaw
│   ├── openclaw_agent.js       # Agente JavaScript
│   ├── openclaw_agent.py       # Agente Python
│   └── workflow_verifactu_final.yaml  # Workflow orquestación
│
├── docker-compose.yml   # Orquestación servicios
├── .env.example         # Variables de entorno
└── README.md           # Este archivo
```

## 🔧 Características Implementadas

### ✅ Backend Operativo
- [x] API REST completa con FastAPI
- [x] Cálculo correcto de IVA por línea de producto
- [x] Integración Verifactu con AEAT
- [x] Generación QR y firma digital
- [x] Almacenamiento inmutable de registros
- [x] Cadena de hash para integridad
- [x] Validación de licencias
- [x] Sistema de logging completo

### ✅ Database
- [x] PostgreSQL configurado en Docker
- [x] Modelos SQLAlchemy para:
  - Productos
  - Sesiones/cajas
  - Tickets/facturas
  - Registros Verifactu
  - Mesas

### ✅ DevOps
- [x] Dockerfile optimizado
- [x] docker-compose.yml con 3 servicios
- [x] Health checks automáticos
- [x] Variables de entorno centralizadas
- [x] Volúmenes persistentes para datos

### ✅ Seguridad
- [x] Soporte dongle USB (simulado con archivo para desarrollo)
- [x] Encriptación Fernet para licencias
- [x] Credenciales no hardcodeadas
- [x] Validación de configuración en startup

## 📊 API Endpoints

### TPV
```
POST /api/tpv/sesion/abrir              # Abrir caja
POST /api/tpv/sesion/cerrar             # Cerrar caja
POST /api/tpv/tickets                   # Crear ticket/factura
GET  /api/tpv/mesas                     # Listar mesas
```

### Verifactu
```
POST /api/verifactu/registrar           # Registrar factura
GET  /api/verifactu/estado/{id}         # Consultar estado
GET  /api/verifactu/csv/{id}            # Obtener CSV
```

### Productos
```
GET    /api/productos                   # Listar productos
POST   /api/productos                   # Crear producto
PUT    /api/productos/{id}              # Actualizar
DELETE /api/productos/{id}              # Eliminar
```

### Reportes
```
GET /api/reportes/ventas                # Reporte ventas
GET /api/reportes/auditoria             # Log auditoría
GET /api/reportes/resumen               # Resumen diario
```

## 🔐 Variables de Entorno

```bash
# Database
DATABASE_URL=postgresql://tpv:password@db:5432/tpv

# Security
DONGLE_REQUIRED=false          # false para desarrollo
MASTER_KEY_REPO=               # Repo key privado (opcional)

# Application
DEBUG=false
LOG_LEVEL=INFO

# AEAT
AEAT_TEST_MODE=true            # true para pruebas
```

Ver `.env.example` para la lista completa.

## 🧪 Testing

```bash
# Test modo
touch backend/test_mode.marker

# Ejecutar tests
cd backend
pytest tests/

# Validar importaciones
python -c "from api.routes import tpv; print('✓ Imports OK')"
```

## 🐛 Troubleshooting

### Puerto 8000 en uso
```bash
docker-compose down
docker-compose up -d
```

### Base de datos no responde
```bash
# Verificar estado
docker-compose ps
docker-compose logs db

# Recrear BD
docker-compose down -v
docker-compose up
```

### Certificado dongle no válido
- Verificar archivo `backend/dongle.key` existe
- Ver logs: `docker-compose logs backend`
- En desarrollo, asegurar `DONGLE_REQUIRED=false` en `.env`

## 📝 Cambios Principales Realizados

### Refactorización Completada

1. **Estructura de paquetes**: Agregados `__init__.py` en todos los módulos Python
2. **Dependencias**: `requirements.txt` actualizado con versiones pinned y sin duplicidades
3. **Módulos faltantes**: 
   - `generate_record.py` - Generación de registros
   - `hash_chain.py` - Cadena de integridad
   - `store_immutable.py` - Almacenamiento inmutable
4. **AEAT Client**: Implementación real con soporte HTTP
5. **QR y Firma**: Funciones operativas con `qrcode` y `signxml`
6. **Cálculo de IVA**: Lógica corregida por línea de producto
7. **Validación**: Errores descriptivos y logging mejorado
8. **Docker**: Dockerfile y docker-compose optimizados
9. **Configuración**: Sistema `.env` centralizado

## 🚀 Deploy en Producción

```bash
# Usar certificados reales
# Configurar DONGLE_REQUIRED=true
# Usar AEAT_TEST_MODE=false
# Configurar DATABASE_URL con BD externa
# Usar HTTPS en Nginx
# Configurar backups automáticos

docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 📞 Soporte

Para reportar problemas o sugerencias:
1. Ver logs: `docker-compose logs -f`
2. Revisar documentación API: http://localhost/docs
3. Verificar conectividad: `docker-compose ps`

## 📄 Licencia

Protegido por derechos de autor. Requiere dongle de seguridad para producción.

---

**Estado**: ✅ Operativo y listo para desarrollo
**Última actualización**: 2026-03-06
