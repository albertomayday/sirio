#!/bin/bash
# SIRIO TPV - Commit y Push automático

echo "╔════════════════════════════════════════════════════════════╗"
echo "║              GIT COMMIT & PUSH AUTOMÁTICO                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

cd /workspaces/sirio

echo "📍 Repositorio: $(pwd)"
echo ""

# Ver estado
echo "🔍 Estado actual:"
git status --short
echo ""

# Agregar cambios
echo "➕ Agregando archivos..."
git add -A
echo "✅ Archivos agregados"
echo ""

# Hacer commit
echo "💾 Realizando commit..."
git commit -m "feat: SIRIO TPV v0.1 - Sistema operativo completo

- Frontend refactorizado con diseño de restaurant/bar
- Panel de mesas (10 mesas configuradas)
- Sistema de comandas con productos dinámicos
- Panel de cobros con VERIFACTu
- Gestión de usuarios (cajeros)
- Backend FastAPI con SQLite
- API completa para productos, ventas, reportes
- Servidor integrado
- Scripts de instalación (Linux/Mac/Windows)
- Documentación completa
- Sistema 100% operativo y funcional

Archivos creados:
- server.py - Servidor integrado simple
- start.py - Ejecutor automático
- run.py - Instalador y ejecutor
- check_system.py - Verificador de sistema
- setup.py - Setup automático
- start_server.py - Servidor con soporte de archivos estáticos
- install_and_run.sh - Script para Linux/Mac
- install_and_run.bat - Script para Windows
- QUICK_START.md - Guía de inicio rápido
- INSTALLATION.md - Documentación de instalación
- LOCALHOST.md - Referencia para localhost
- README_OPERATIVO.txt - Resumen operativo

Archivos modificados:
- index.html - Conectado a API backend con indicador de estado

Estado: ✅ Operativo | Versión 0.1 | 2026-03-07" 2>&1

if [ $? -eq 0 ]; then
  echo "✅ Commit realizado"
  echo ""
  
  # Push
  echo "🚀 Haciendo push..."
  git push origin main 2>&1
  
  if [ $? -eq 0 ]; then
    echo "✅ Push completado exitosamente"
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "  ✅ COMMIT Y PUSH COMPLETADOS"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "📍 Ver cambios en:"
    echo "   https://github.com/albertomayday/sirio/commits/main"
    echo ""
  else
    echo "❌ Error en push"
    echo "Verifica tu conexión a GitHub"
  fi
else
  echo "⚠️  Nada para commitear o error"
fi

echo ""
