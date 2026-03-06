#!/bin/bash
# Validador de estructura y configuración del repositorio Sirio

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                   VALIDADOR ESTRUCTURA SIRIO                        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"

passed=0
failed=0
warnings=0

check_file() {
    local file=$1
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
        ((passed++))
        return 0
    else
        echo -e "${RED}✗${NC} $file (NO ENCONTRADO)"
        ((failed++))
        return 1
    fi
}

check_dir() {
    local dir=$1
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $dir/"
        ((passed++))
        return 0
    else
        echo -e "${RED}✗${NC} $dir/ (NO ENCONTRADO)"
        ((failed++))
        return 1
    fi
}

check_import() {
    local file=$1
    local import_name=$2
    if grep -q "$import_name" "$file"; then
        echo -e "${GREEN}✓${NC} $file: $import_name"
        ((passed++))
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $file: $import_name (NO ENCONTRADO)"
        ((warnings++))
        return 1
    fi
}

echo -e "\n${BLUE}▶ Verificando estructura de directorios${NC}"
check_dir "backend"
check_dir "backend/api"
check_dir "backend/api/routes"
check_dir "backend/core"
check_dir "backend/verifactu"
check_dir "backend/licensing"
check_dir "frontend"
check_dir "modules"
check_dir "modules/aeat_client"
check_dir "modules/factura_utils"

echo -e "\n${BLUE}▶ Verificando archivos __init__.py${NC}"
check_file "backend/api/__init__.py"
check_file "backend/api/routes/__init__.py"
check_file "backend/core/__init__.py"
check_file "backend/verifactu/__init__.py"
check_file "backend/licensing/__init__.py"
check_file "modules/__init__.py"
check_file "modules/aeat_client/__init__.py"
check_file "modules/factura_utils/__init__.py"
check_file "openclaw/__init__.py"
check_file "openclaw/src/__init__.py"

echo -e "\n${BLUE}▶ Verificando módulos principales${NC}"
check_file "backend/main.py"
check_file "backend/generate_record.py"
check_file "backend/hash_chain.py"
check_file "backend/store_immutable.py"
check_file "modules/aeat_client/client.py"
check_file "modules/factura_utils/qr_sign.py"

echo -e "\n${BLUE}▶ Verificando configuración${NC}"
check_file "backend/requirements.txt"
check_file "backend/Dockerfile"
check_file "backend/.env.example"
check_file "backend/core/config.py"
check_file "docker-compose.yml"
check_file ".env.example"
check_file "frontend/nginx.conf"

echo -e "\n${BLUE}▶ Verificando sintaxis Python${NC}"
for file in backend/main.py backend/generate_record.py backend/hash_chain.py backend/store_immutable.py; do
    if python3 -m py_compile "$file" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $file (Sintaxis OK)"
        ((passed++))
    else
        echo -e "${RED}✗${NC} $file (Error de sintaxis)"
        ((failed++))
    fi
done

echo -e "\n${BLUE}▶ Verificando contenido de archivos críticos${NC}"

# Check for duplicate dependencies
if grep -q "^cryptography$" backend/requirements.txt && \
   grep -c "^cryptography" backend/requirements.txt | grep -q "^1$"; then
    echo -e "${GREEN}✓${NC} requirements.txt: Sin duplicidades de cryptography"
    ((passed++))
else
    echo -e "${RED}✗${NC} requirements.txt: Posible duplicidad o versión faltante"
    ((failed++))
fi

# Check for pyusb in requirements
if grep -q "pyusb" backend/requirements.txt; then
    echo -e "${GREEN}✓${NC} requirements.txt: pyusb incluido"
    ((passed++))
else
    echo -e "${YELLOW}⚠${NC} requirements.txt: pyusb no encontrado (opcional)"
    ((warnings++))
fi

# Check for IVA calculation fix in tpv.py
if grep -q "tasa_iva = Decimal" backend/api/routes/tpv.py; then
    echo -e "${GREEN}✓${NC} tpv.py: Cálculo de IVA corregido"
    ((passed++))
else
    echo -e "${RED}✗${NC} tpv.py: Cálculo de IVA no actualizado"
    ((failed++))
fi

# Check for logging in validator.py
if grep -q "logger.error" backend/licensing/validator.py; then
    echo -e "${GREEN}✓${NC} validator.py: Logging implementado"
    ((passed++))
else
    echo -e "${RED}✗${NC} validator.py: Logging no encontrado"
    ((failed++))
fi

# Check Dockerfile
if grep -q "WORKDIR /app/backend" backend/Dockerfile; then
    echo -e "${GREEN}✓${NC} Dockerfile: WORKDIR configurado correctamente"
    ((passed++))
else
    echo -e "${RED}✗${NC} Dockerfile: WORKDIR no configurado"
    ((failed++))
fi

# Check docker-compose
if grep -q "depends_on:" docker-compose.yml && \
   grep -q "postgres" docker-compose.yml; then
    echo -e "${GREEN}✓${NC} docker-compose.yml: Servicios configurados"
    ((passed++))
else
    echo -e "${RED}✗${NC} docker-compose.yml: Configuración incompleta"
    ((failed++))
fi

echo -e "\n${BLUE}▶ Verificando importaciones en módulos${NC}"
if python3 -c "import sys; sys.path.insert(0, 'backend'); from core import config" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} core: Imports funcionales"
    ((passed++))
else
    echo -e "${RED}✗${NC} core: Error en imports"
    ((failed++))
fi

if python3 -c "import sys; sys.path.insert(0, 'backend'); from api import routes" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} api.routes: Imports funcionales"
    ((passed++))
else
    echo -e "${RED}✗${NC} api.routes: Error en imports"
    ((failed++))
fi

# Summary
echo -e "\n${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                         RESUMEN VALIDACIÓN                          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo -e "${GREEN}Verificaciones pasadas:${NC}    ${passed}"
echo -e "${RED}Verificaciones fallidas:${NC}   ${failed}"
echo -e "${YELLOW}Advertencias:${NC}             ${warnings}"

total=$((passed + failed + warnings))
echo -e "\n${BLUE}Total: ${total} verificaciones${NC}"

if [ $failed -eq 0 ]; then
    echo -e "\n${GREEN}✅ ¡Refactorización completada exitosamente!${NC}"
    echo -e "\n${YELLOW}Próximos pasos:${NC}"
    echo "1. Copiar .env.example a .env"
    echo "2. Editar variables de entorno si es necesario"
    echo "3. Ejecutar: docker-compose up --build"
    echo "4. Acceder a: http://localhost"
    exit 0
else
    echo -e "\n${RED}❌ Se encontraron ${failed} error(es). Por favor, revisar.${NC}"
    exit 1
fi
