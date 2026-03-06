#!/bin/bash

# ============================================================================
# 🚀 SIRIO TPV - VERCEL DEPLOYMENT SCRIPT
# ============================================================================

set -e

cat << 'EOF'

╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║          🎉 SIRIO TPV v1.0.0 - DEPLOYMENT A VERCEL 🎉                ║
║                                                                        ║
║                Full Stack en Vercel con Postgres                      ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝

Este script realizará los siguientes pasos:

  [1/5] Instalar Vercel CLI
  [2/5] Configurar Vercel Postgres
  [3/5] Instalar dependencias de frontend
  [4/5] Build del proyecto
  [5/5] Desplegar a Vercel (PROD)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Requisitos previos:
  ✓ Node.js 18+ instalado
  ✓ Cuenta en Vercel (https://vercel.com)
  ✓ GitHub repo conectado a Vercel

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF

read -p "¿Deseas continuar? (s/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Cancelado"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "[1/5] Instalando Vercel CLI..."
echo "════════════════════════════════════════════════════════════════════"

npm install -g vercel@latest

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "[2/5] Verificando autenticación con Vercel..."
echo "════════════════════════════════════════════════════════════════════"

if ! vercel whoami > /dev/null 2>&1; then
    echo ""
    echo "⚠️  No estás autenticado en Vercel"
    echo ""
    echo "Ejecuta: vercel login"
    echo ""
    echo "Luego vuelve a ejecutar este script"
    exit 1
fi

echo "✅ Autenticación OK"

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "[3/5] Instalando dependencias de frontend..."
echo "════════════════════════════════════════════════════════════════════"

cd frontend
npm install

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "[4/5] Compilando proyecto..."
echo "════════════════════════════════════════════════════════════════════"

npm run build

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "[5/5] Desplegando a Vercel (PRODUCCIÓN)..."
echo "════════════════════════════════════════════════════════════════════"

echo ""
echo "    ⚠️  PASO IMPORTANTE:"
echo ""
echo "    Durante el deployment, Vercel te pedirá:"
echo ""
echo "    1. Confirmar el nombre del proyecto"
echo "       → Recomendado: 'sirio-tpv'"
echo ""
echo "    2. Seleccionar directorio de raíz"
echo "       → Selecciona: ./frontend"
echo ""
echo "    3. Configurar variables de entorno"
echo "       → Se hace automáticamente"
echo ""
echo ""

vercel --prod

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "✅ DEPLOYMENT COMPLETADO"
echo "════════════════════════════════════════════════════════════════════"

echo ""
echo "🎉 ¡Sirio TPV está en vivo en Vercel!"
echo ""
echo "Próximos pasos:"
echo ""
echo "1. Accede al dashboard:"
echo "   vercel dashboard"
echo ""
echo "2. Agregar Postgres a tu proyecto:"
echo "   • Ve a: https://vercel.com/dashboard"
echo "   • Proyecto: sirio-tpv"
echo "   • Storage → Create Database → Postgres"
echo ""
echo "3. Inicializar la base de datos:"
echo "   • Copiar SQL de: ./scripts/init-database.sql"
echo "   • Ejecutar en Vercel Postgres Console"
echo ""
echo "4. Tu aplicación está en:"
echo "   https://sirio-tpv.vercel.app"
echo ""
echo "5. API disponible en:"
echo "   https://sirio-tpv.vercel.app/api/health"
echo ""

cd ..

echo ""
read -p "¿Quieres abrir el dashboard en el navegador? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    vercel dashboard
fi

echo ""
echo "✨ ¡Listo!"
