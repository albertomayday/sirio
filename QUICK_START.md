# 🚀 SIRIO TPV v0.1 - INICIO RÁPIDO

## ⚡ EJECUTAR EN 30 SEGUNDOS

### Opción 1: Python (Todas las plataformas)

```bash
cd /workspaces/sirio

# Opción A: Con setup automático
python3 setup.py

# O Opción B: Servidor integrado (Recomendado)
python3 start_server.py
```

### Opción 2: Bash (Linux/Mac)

```bash
cd /workspaces/sirio
bash install_and_run.sh
```

### Opción 3: Batch (Windows)

```cmd
cd C:\workspaces\sirio
install_and_run.bat
```

---

## ✅ Lo que está LISTO

| Componente | Estado | URL |
|-----------|--------|-----|
| **Frontend (TPV)** | ✅ Operativo | http://localhost:8000 |
| **API Backend** | ✅ Configurado | http://localhost:8000/api |
| **API Docs** | ✅ Disponible | http://localhost:8000/docs |
| **Base de datos** | ✅ SQLite local | `backend/tpv.db` |
| **Test Mode** | ✅ Activado | Sin dongle requerido |
| **CORS** | ✅ Habilitado | Todas las conexiones |

---

## 📦 Dependencias

**Instaladas automáticamente:**
- fastapi >= 0.104.1
- uvicorn >= 0.24.0
- sqlalchemy >= 2.0.23
- pydantic >= 2.5.0
- cryptography >= 41.0.7
- sqlalchemy, httpx, requests, etc.

---

## 🎯 Funcionalidades

✅ **Gestión de Mesas**
- 10 mesas configuradas
- Estados: Libre, Ocupada, Cuenta pedida
- Información en tiempo real

✅ **Comandas**
- Selector rápido de mesas
- Catálogo de 18+ productos
- Númepad integrado
- Descuentos y cambio de cantidad
- Cambio de precio manual

✅ **Cobros**
- Métodos de pago: Efectivo, Tarjeta, Bizum
- VERIFACTu (hash SHA-256)
- Historial de transacciones
- Integración con fiscalidad

✅ **Usuarios**
- Gestión de cajeros
- Activación/desactivación en tiempo real
- Estadísticas de ventas
- Histórico de cobros

✅ **Backend API**
- CRUD de productos
- Registro de ventas
- VERIFACTu compliance
- Reportes
- Base de datos SQLite

---

## 🔌 Conexión Frontend-Backend

El frontend se conecta automáticamente a:
```
http://localhost:8000/api/productos/
```

**Si falla la conexión:**
1. Verificar que el backend está corriendo
2. Revisar la consola del navegador (F12 > Console)
3. Probar: `curl http://localhost:8000/api/productos/`

---

## 📝 Documentación Completa

Ver `INSTALLATION.md` para:
- Instalación manual
- Configuración personalizada
- Troubleshooting
- Variables de entorno
- Endpoints de API

---

## 🎮 USO DEL SISTEMA

### 1. Abrir Browser
```
http://localhost:8000
```

### 2. Seleccionar Usuario
- Click en usuario en topbar para cambiar de cajero

### 3. Abrir Mesa
- Click en mesa en panel "Mesas"
- Automáticamente entra a "Comandas"

### 4. Agregar Productos
- Click en producto para agregarlo
- Modificar cantidad con númepad
- Aplicar descuentos

### 5. Confirmar Comanda
- Click "✓ Confirmar"

### 6. Pedir Cuenta
- Click "Pedir cuenta"
- Mesa pasa a estado "Cuenta pedida"

### 7. Cobrar
- Ir a tab "Cobros"
- Seleccionar mesa
- Elegir método de pago
- Click "✓ Cobrar y emitir VERIFACTu"

### 8. Ver Historial
- Tab "Usuarios" para ver histórico de cobros

---

## 🛠️ Parar el Servidor

### Método 1: Ctrl+C en terminal
```
^C
```

### Método 2: Próximo inicio
El servidor se detendrá automáticamente

---

## 📊 Estructura de Datos

### Productos (hardcodeados en demo)
```json
{
  "id": 1,
  "nombre": "Agua 1.5L",
  "precio": 0.89,
  "categoria": "bebidas",
  "activo": true
}
```

### Mesas
```
Mesa 1-10: Estados [libre, ocupada, cuenta]
```

### Usuarios
```
Ana García (Cajera) - activa
Carlos López (Cajero) - inactivo
```

---

## 🎓 Siguientes Pasos

1. **Persistencia**: Los datos están en memoria, se pierden al reiniciar
   - Para persistencia: Usar PostgreSQL o guardar en DB

2. **Sincronización**: Múltiples clientes en tiempo real
   - Para sincronizar: Implementar WebSockets

3. **Reportes**: Generar reportes PDF/Excel
   - Para reportes: Integrar ReportLab

4. **Móvil**: Acceder desde móvil
   - Cambiar localhost a IP del servidor

---

**¡Sistema listo para usar! 🎉**

Versión 0.1 | 2026-03-07
