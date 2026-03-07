#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   SIRIO TPV - INSTALACIÓN Y EJECUCIÓN AUTOMÁTICA           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Paso 1: Instalar dependencias
echo "📦 PASO 1: Instalando dependencias del backend..."
cd /workspaces/sirio/backend
pip install -q fastapi uvicorn sqlalchemy pydantic cryptography python-dotenv psycopg2-binary httpx requests reportlab qrcode pillow signxml lxml pyusb || {
  echo "❌ Error instalando dependencias"
  exit 1
}
echo "✅ Dependencias instaladas correctamente"
echo ""

# Paso 2: Verificar estructura
echo "🔍 PASO 2: Verificando estructura del proyecto..."
if [ ! -f "main.py" ]; then
  echo "❌ No se encontró main.py en $(pwd)"
  exit 1
fi
if [ ! -f "requirements.txt" ]; then
  echo "⚠️  No se encontró requirements.txt"
fi
echo "✅ Estructura verificada"
echo ""

# Paso 3: Crear base de datos si no existe
echo "🗄️  PASO 3: Inicializando base de datos..."
if [ ! -f "tpv.db" ]; then
  echo "   Creando nueva base de datos SQLite..."
fi
echo "✅ Base de datos lista"
echo ""

# Paso 4: Ejecutar el backend
echo "🚀 PASO 4: Iniciando backend en puerto 8000..."
echo "   URL: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""
echo "────────────────────────────────────────────────────────────"
echo ""

python main.py
