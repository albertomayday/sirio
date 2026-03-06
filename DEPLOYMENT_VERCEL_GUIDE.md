# 🚀 SIRIO TPV - GUÍA DE DEPLOYMENT A VERCEL

## 📋 ARQUITECTURA

```
Vercel (Todo en un lugar)
├── Frontend (Next.js)
│   ├── Pages
│   ├── Static Assets
│   └── API Routes (Serverless)
│
├── Database (Vercel Postgres)
│   ├── Transactions
│   ├── Products
│   ├── Users
│   ├── Invoices
│   └── Audit Logs
│
└── Environment Vars
    └── POSTGRES_PRISMA_URL
    └── API_KEYS
    └── JWT_SECRET
```

---

## 🎯 PASO 1: Preparativos Previos

### Requisitos
- ✅ Node.js 18+ instalado
- ✅ Cuenta en Vercel (https://vercel.com)  
- ✅ GitHub repo del proyecto
- ✅ 15 minutos libres

### Instalaciones

```bash
# Instalar Vercel CLI global
npm install -g vercel@latest

# Verificar instalación
vercel --version
```

---

## 🎯 PASO 2: Autenticación en Vercel

```bash
# Login en Vercel
vercel login

# Verificar
vercel whoami
```

Te pedirá:
1. Email de tu cuenta Vercel
2. Verificación por email
3. Confirmar desde el navegador

✅ Una vez completado, verás tu email.

---

## 🎯 PASO 3: Configuración del Proyecto

### Opción A: Deployment Automático (RECOMENDADO)

```bash
# Desde la raíz del proyecto
bash deploy-vercel.sh
```

El script realizará:
1. ✅ Instalar dependencias
2. ✅ Compilar proyecto
3. ✅ Desplegar a Vercel (PROD)

### Opción B: Deployment Manual

```bash
cd frontend
npm install
npm run build
vercel --prod
```

---

## 🎯 PASO 4: Configurar Vercel Postgres

### Desde el Dashboard Vercel

1. Ve a: https://vercel.com/dashboard
2. Selecciona tu proyecto `sirio-tpv`
3. Tab: **Storage** → **Create Database**
4. Selecciona: **Postgres**
5. Configura:
   - Nombre: `sirio-db`
   - Región: Tu región (ej: Madrid)
   - Confirmar

✅ Vercel creará automáticamente las variables de entorno:
- `POSTGRES_PRISMA_URL`
- `POSTGRES_URL_NON_POOLING`

---

## 🎯 PASO 5: Inicializar Base de Datos

### Método 1: Desde Vercel Console (Recomendado)

1. Dashboard → Storage → sirio-db
2. Tab: **Postgres** → **Console**
3. Copiar todo el contenido de `scripts/init-database.sql`
4. Pegar en la consola
5. Ejecutar

### Método 2: Desde Script Python

```bash
python3 scripts/init-db-vercel.py
```

### Verificar Creación

```bash
# Query de test
vercel env list
```

---

## 🎯 PASO 6: Variables de Entorno

### Automático (hecho por Vercel)

Vercel añade automáticamente:
- `POSTGRES_PRISMA_URL` ← Database URL  
- `POSTGRES_URL_NON_POOLING` ← Backup URL

### Manual (si es necesario)

Dashboard → Settings → Environment Variables

Añadir:
```
NEXT_PUBLIC_API_URL = https://sirio-tpv.vercel.app/api
JWT_SECRET = your-secret-key-here
API_KEY = your-api-key-here
DEBUG = false
```

---

## 🎯 PASO 7: Verificar Deployment

### URLs Importante

```
Frontend:       https://sirio-tpv.vercel.app
API Health:     https://sirio-tpv.vercel.app/api/health
API Docs:       https://sirio-tpv.vercel.app/api-docs
Database Stats: https://vercel.com/dashboard (Storage)
```

### Health Check

```bash
# Debe devolver 200 OK
curl https://sirio-tpv.vercel.app/api/health

# Respuesta esperada:
# {"status":"healthy","timestamp":"...","version":"1.0.0"}
```

### API Test

```bash
# Crear transacción de prueba
curl -X POST https://sirio-tpv.vercel.app/api/tpv \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"name": "Cerveza", "quantity": 1, "price": 3.5}
    ],
    "payment_method": "card"
  }'
```

---

## 📊 MONITOREO POST-DEPLOYMENT

### Logs en Vivo

```bash
# Ver logs de deployment
vercel logs https://sirio-tpv.vercel.app

# Con filtro
vercel logs https://sirio-tpv.vercel.app --follow
```

### Dashboard Vercel

https://vercel.com/dashboard/sirio-tpv

Monitorea:
- ✅ Deployments
- ✅ Performance
- ✅ Error rates
- ✅ Database connections
- ✅ API usage

---

## 🐛 TROUBLESHOOTING

### Error: "Build failed"

```bash
# Solución 1: Limpiar caché
vercel env pull
npm run build

# Solución 2: Verificar path
# Asegurar que next.config.js está en frontend/

# Solución 3: Verificar Node version
node --version  # Debe ser 18+
```

### Error: "Database connection refused"

```bash
# Verificar variables de entorno
vercel env list

# Reiniciar deployment
vercel redeploy
```

### Error: "CORS policy"

✅ Ya configurado en `frontend/next.config.js`

Verificar headers:
```bash
curl -I https://sirio-tpv.vercel.app/api/health
```

### Funciones Lentas (>10s)

```bash
# Aumentar timeout en vercel.json
"functions": {
  "pages/api/**": {
    "maxDuration": 60  # Aumentar de 10 a 60
  }
}
```

---

## 🎊 RESULTADO FINAL

### ✅ Checklist

- [ ] Frontend activo en Vercel
- [ ] API routes funcionando
- [ ] Postgres conectado
- [ ] Base de datos inicializada
- [ ] Health check pasando
- [ ] CORS configurado
- [ ] Variables de entorno OK
- [ ] SSL/TLS automático ✅
- [ ] Dominio personalizado (opcional)

### URL Final

```
🎉 https://sirio-tpv.vercel.app 🎉
```

---

## 📈 PRÓXIMOS PASOS

### Día 1 (Hoy)
- [x] Desplegar a Vercel
- [x] Inicializar BD
- [x] Verificar health check

### Semana 1
- [ ] Probar transacciones de prueba
- [ ] Verificar integridad de datos
- [ ] Configurar dominio personalizado (opcional)

### Mes 1
- [ ] Implementar JWT
- [ ] Añadir tests
- [ ] Monitoring con Sentry/DataDog
- [ ] Backup automático de BD

### Roadmap
- [ ] CI/CD con GitHub Actions
- [ ] WebhooksAPM (performance)
- [ ] Rate limiting
- [ ] Analytics

---

## 💰 COSTOS

### Vercel
- **Pagos-por-uso:**
  - Bandwidth: $0.50/GB (incluye 100GB gratis)
  - Compute: $0.00001667/second (primera 3000 horas gratis)
  - Típico: **$0-10/mes**

### Vercel Postgres
- **Incluido en proyecto:**
  - Storage: 256 MB
  - Costo: $5/mes (primera BD)
  - **Total: $5/mes**

### Pro Plan (opcional)
- $20/mes
- 3000 GB bandwidth
- Más colaboradores
- Soporte prioritario

**Costo estimado: $5-25/mes**

---

## 🔗 REFERENCIAS

- Vercel Docs: https://vercel.com/docs
- Next.js Docs: https://nextjs.org/docs
- Vercel Postgres: https://vercel.com/docs/storage/vercel-postgres
- Vercel CLI: https://vercel.com/docs/cli

---

## 📞 SOPORTE

### Si algo falla

1. Revisar logs: `vercel logs`
2. Comprobar BD: Dashboard Storage
3. Limpiar caché: `vercel env pull`
4. Reimplementar: `vercel redeploy`

### Más ayuda

- Docs: https://vercel.com/support
- Community: https://github.com/vercel/next.js/discussions

---

## ✨ ¡LISTO!

Tu Sirio TPV está en la nube:

```
🎉 https://sirio-tpv.vercel.app 🎉
```

**Comparte tu URL de Vercel con tu equipo y ¡a usar!**

---

**Versión:** 1.0.0  
**Platform:** Vercel + Next.js + Postgres  
**Status:** ✅ PRODUCCIÓN-READY

---

Generado: 2026-03-06
