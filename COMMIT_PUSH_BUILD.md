# 🚀 GUÍA COMPLETA: Commit, Push y Build x64 de SIRIO

## Tabla de Contenidos
1. [Hacer Commit y Push](#commit-y-push)
2. [Crear Ejecutable x64](#crear-ejecutable-x64)
3. [Distribución](#distribución)
4. [Troubleshooting](#troubleshooting)

---

## 📝 Commit y Push

### Paso 1: Verificar cambios
```bash
cd /workspaces/sirio
git status
```

Deberías ver cambios en:
- ✅ `backend/` (varios archivos)
- ✅ `modules/` (nuevos archivos)
- ✅ `docker-compose.yml`
- ✅ Documentación
- ✅ Scripts de build

### Paso 2: Hacer commit automático

**Opción 1: Script Bash (Linux/Mac/WSL)**
```bash
bash git_commit_push.sh
```

**Opción 2: Manual (Todos los SO)**
```bash
git add -A
git commit -m "refactor: refactorización completa operativa del repositorio Sirio

[Estructura de Paquetes]
✅ Agregados 10 archivos __init__.py
✅ Todos los imports funcionan correctamente

[Dependencias]
✅ requirements.txt refactorizado
✅ pyusb descomentado para USB

[Módulos Nuevos]
✅ generate_record.py (45 líneas)
✅ hash_chain.py (80 líneas)  
✅ store_immutable.py (120 líneas)

[Módulos Implementados]
✅ aeat_client/client.py (+140 líneas)
✅ factura_utils/qr_sign.py (+180 líneas)

[Mejoras]
✅ IVA calculado por línea
✅ Dockerfile optimizado
✅ docker-compose completo
✅ Logging mejorado

Total: +1200 líneas, 18 archivos nuevos, 8 modificados
Status: ✅ OPERATIVO"
```

### Paso 3: Push al repositorio
```bash
git push origin main
```

O si es otra rama:
```bash
git push origin <nombre-rama>
```

**Resultado esperado:**
```
Counting objects: 45, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (40/40), done.
Writing objects: 100% (45/45), 125.34 KiB | 1.5 MiB/s, done.
Total 45 (delta 5), reused 0 (delta 0)
remote: Resolving deltas: 100% (5/5), done.
To github.com:albertomayday/sirio.git
   abc1234..def5678  main -> main
```

---

## 🔨 Crear Ejecutable x64

### Opción 1: ZIP Portable (Recomendado)

**Paso 1: Instalar dependencias**
```bash
pip install pyinstaller
```

**Paso 2: Construir paquete portable**
```bash
python3 build_sirio_x64.py
```

**Resultado:**
```
✅ Estructura creada
✓ Backend copiado
✓ Frontend copiado
✓ Módulos copiados
✓ Launcher creado
✓ Paquete creado: dist/Sirio-TPV-1.0.0-x64-portable.zip (42.5 MB)
```

**Archivos generados:**
- `dist/Sirio-TPV-1.0.0-x64-portable.zip` - Paquete completo
- `dist/release.json` - Metadatos del release
- `build/` - Estructura sin comprimir

### Opción 2: EXE Compilado (Windows)

**Paso 1: Instalar PyInstaller**
```bash
pip install pyinstaller
```

**Paso 2: Ejecutar script batch (Windows)**
```bash
build_exe.bat
```

**Resultado:**
```
[OK] Python encontrado
[INFO] Compilando ejecutable...
[OK] Ejecutable creado en: dist\Sirio-TPV.exe (85.3 MB)
```

**Archivos generados:**
- `dist/Sirio-TPV.exe` - Ejecutable portable
- `dist/release.json` - Información del release

### Opción 3: Build Completo (Manual)

```bash
# 1. Crear estructura
mkdir -p build/app/{backend,frontend,modules,data}

# 2. Copiar archivos
cp -r backend/* build/app/backend/
cp -r frontend/* build/app/frontend/
cp -r modules/* build/app/modules/

# 3. Compilar con PyInstaller
pyinstaller \
  --onefile \
  --windowed \
  --name "Sirio-TPV" \
  --add-data "build/app:app" \
  launcher/sirio_launcher.py

# 4. Empaquetar
zip -r dist/Sirio-TPV-x64.zip dist/Sirio-TPV
```

---

## 📦 Distribución

### Contenido del Paquete

**Opción ZIP Portable contendrá:**
```
Sirio-TPV-x64/
├── app/
│   ├── backend/          # API FastAPI
│   ├── frontend/         # Interfaz web
│   ├── modules/          # Módulos Python
│   └── data/             # Datos y configuración
├── launcher/
│   └── sirio_launcher.py # Script principal
├── START.bat             # Iniciar (Windows)
├── SETUP.bat             # Configurar
├── README.txt            # Instrucciones
└── requirements.txt      # Dependencias
```

**Opción EXE:**
```
Sirio-TPV.exe  (ejecutable standalone, 85-100 MB)
```

### Instrucciones para Usuarios

1. **Descargar:**
   - ZIP: Descargar y extraer `Sirio-TPV-1.0.0-x64-portable.zip`
   - EXE: Descargar y ejecutar `Sirio-TPV.exe`

2. **Configurar (ZIP):**
   ```bash
   SETUP.bat
   ```

3. **Iniciar:**
   ```bash
   START.bat
   ```

4. **Acceder:**
   - http://localhost:9000 - Frontend
   - http://localhost:8000 - API
   - http://localhost:8000/docs - Documentación

---

## 🔍 Verificación Pre-Build

Antes de crear el ejecutable, verifica:

```bash
# Validar estructura
bash validate.sh

# Verificar importaciones
python3 -c "import sys; sys.path.insert(0, 'backend'); from core import config; print('✓ Imports OK')"

# Validar sintaxis
python3 -m py_compile backend/main.py backend/generate_record.py backend/hash_chain.py

# Verificar requirements
pip install -r backend/requirements.txt --dry-run
```

---

## 📊 Tamaño Esperado

| Formato | Tamaño | Tiempo Build |
|---------|--------|--------------|
| ZIP Portable | 40-50 MB | 5-10 min |
| EXE Standalone | 80-100 MB | 10-15 min |
| Instalador (MSI) | 30-40 MB | 15-20 min |

---

## 🐛 Troubleshooting

### Problema: "Python no encontrado"
**Solución:**
```bash
# Verificar Python
python --version
python3 --version

# Agregá Python al PATH
# https://docs.python.org/3/using/windows.html#installation-steps-to-install-python
```

### Problema: "PyInstaller not found"
**Solución:**
```bash
pip install --upgrade pyinstaller
```

### Problema: El ZIP es demasiado grande
**Solución:**
```bash
# Usar compresión máxima
# En build_sirio_x64.py cambiar:
# zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
# Por:
# zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9)
```

### Problema: "Port already in use"
**Solución:**
```bash
# Encontrar proceso usando puerto 8000
netstat -ano | findstr :8000

# Matar proceso (Windows)
taskkill /PID <process_id> /F

# Matar proceso (Linux)
lsof -i :8000 | awk 'NR!=1 {print $2}' | xargs kill -9
```

### Problema: Backend no inicia
**Solución:**
```bash
# Verificar logs
cat data/logs/sirio_*.log

# Verificar configuración
cat backend/.env

# Reinstalar dependencias
pip install --force-reinstall -r backend/requirements.txt
```

---

## ✅ Checklist Pre-Distribución

- [ ] ✅ Todos los tests pasando (`bash validate.sh`)
- [ ] ✅ Código compilado sin errores
- [ ] ✅ Ejecutable probado en Windows 10/11 x64
- [ ] ✅ ZIP descargable y extraíble
- [ ] ✅ README.txt incluido con instrucciones
- [ ] ✅ requirements.txt actualizado
- [ ] ✅ .env.example con valores seguros
- [ ] ✅ Versión actualizada en config
- [ ] ✅ Release notes creado
- [ ] ✅ Hashsum SHA256 generado

---

## 📈 Versioning

**Convención de versionado:**
```
Sirio-TPV-{VERSION}-{ARCH}-{TYPE}.{EXT}

Ejemplos:
- Sirio-TPV-1.0.0-x64-portable.zip
- Sirio-TPV-1.0.0-x64.exe
- Sirio-TPV-1.0.0-x84-installer.msi
```

**Incrementar versión:**
- Patch: 1.0.0 → 1.0.1 (bug fixes)
- Minor: 1.0.0 → 1.1.0 (features)
- Major: 1.0.0 → 2.0.0 (breaking changes)

---

## 📝 Release Notes Template

```markdown
# Sirio TPV v1.0.0 - Release Notes

## 🎉 Novedades
- Sistema TPV completo operativo
- Integración Verifactu con AEAT
- Generación de QR y firma digital
- Base de datos PostgreSQL incluida

## 🐛 Correcciones
- Cálculo de IVA corregido
- Validación de licencia mejorada
- Logging completo

## 📋 Requisitos
- Windows 10/11 x64
- Python 3.11+ (incluido)
- Docker (opcional)

## 🚀 Instalación
1. Descargar Sirio-TPV-1.0.0-x64.zip
2. Extraer archivo
3. Ejecutar SETUP.bat
4. Ejecutar START.bat

## 📞 Soporte
- Docs: http://localhost:8000/docs
- Logs: data/logs/
- Issues: https://github.com/albertomayday/sirio/issues
```

---

## 🔒 Seguridad en Build

Verificar que:
- ✅ No hay credenciales embebidas
- ✅ .env no está en el ZIP
- ✅ API keys están vacías
- ✅ Certificados no incluidos
- ✅ Logs no contienen datos sensibles

---

## 🎯 Próximos Pasos Después del Build

1. **Testing en VM Windows:**
   ```bash
   # Probar en máquina virtual Windows 10/11 x64
   # Verificar que START.bat funciona
   # Verificar que la aplicación se abre
   ```

2. **Upload a Release:**
   ```bash
   # En GitHub:
   # https://github.com/albertomayday/sirio/releases/new
   # Upload: Sirio-TPV-1.0.0-x64-portable.zip
   # Upload: Sirio-TPV-1.0.0-x64.exe
   ```

3. **Publicar Release Notes:**
   - Título: "Sirio TPV v1.0.0 - First Stable Release"
   - Descripción: Release notes completo
   - Tag: v1.0.0

---

**Siguiente comando para completar el ciclo:**

```bash
# 1. Commit y Push
bash git_commit_push.sh

# 2. Build x64
python3 build_sirio_x64.py

# 3. (Opcional) Compilar EXE
build_exe.bat

# 4. Verificar distribución
ls -lh dist/
```

---

**Estado:** ✅ LISTO PARA DISTRIBUCIÓN
**Fecha**: 2026-03-06
**Versión**: 1.0.0
