# 🚀 DEPLOYMENT SIRIO TPV - VERCEL + RAILWAY

## 📋 ARQUITECTURA

```
┌─────────────────┐         ┌──────────────────┐
│   VERCEL        │         │     RAILWAY      │
│                 │         │                  │
│  Frontend       │────────▶│  FastAPI Backend │
│  (Next.js)      │ API     │  PostgreSQL DB   │
│  Static Files   │  Calls  │  Redis (cache)   │
│  (HTML/CSS/JS)  │         │                  │
└─────────────────┘         └──────────────────┘
```

---

## 📦 FASE 1: PREPARAR FRONTEND PARA VERCEL

Vercel necesita un `package.json` en la raíz con la config correcta.

### Paso 1: Crear Next.js wrapper

```bash
npm install next@latest react react-dom
```

### Paso 2: Crear estructura Next.js

```
frontend/
├── pages/
│   ├── index.js           ← Página principal
│   ├── api/               ← Proxy a API
│   └── _app.js
├── public/                ← Assets estáticos
├── next.config.js
└── package.json
```

---

## 🚂 FASE 2: PREPARAR BACKEND PARA RAILWAY

Railway es perfecto para Full Stack Python + PostgreSQL.

### Paso 1: Crear `railway.json`

```json
{
  "name": "Sirio TPV Backend",
  "description": "FastAPI Backend + PostgreSQL",
  "runtime": "python311",
  "services": [
    {
      "name": "postgres",
      "image": "postgres:16-alpine"
    },
    {
      "name": "backend",
      "runtime": "python311"
    }
  ]
}
```

### Paso 2: Configurar variables de entorno

```
DATABASE_URL=postgresql://user:pass@localhost:5432/sirio
API_URL=https://sirio-api.railway.app
FRONTEND_URL=https://sirio-tpv.vercel.app
DEBUG=false
```

---

## 🎯 OPCIÓN 1: DEPLOYMENT AUTOMÁTICO (Recomendado)

### Cliente: Vercel
1. Conectar GitHub repo a Vercel
2. Deploy automático on push
3. URL: `https://sirio-tpv.vercel.app`

### Backend: Railway
1. Conectar GitHub repo a Railway
2. Deploy automático on push
3. URL: `https://sirio-api.railway.app`
4. PostgreSQL incluido

---

## 🎯 OPCIÓN 2: DEPLOYMENT MANUAL

### Backend a Railway (paso a paso)

```bash
# 1. Login Railway
npm install -g @railway/cli
railway login

# 2. Init proyecto
railway init

# 3. Conectar variables
railway variables set DATABASE_URL=postgresql://...
railway variables set API_KEY=xxx
railway variables set JWT_SECRET=xxx

# 4. Deploy
railway up
```

### Frontend a Vercel (paso a paso)

```bash
# 1. Login Vercel
npm i -g vercel
vercel login

# 2. Deploy
vercel deploy

# 3. Production
vercel --prod
```

---

## 📂 ARCHIVOS A CREAR

### `/frontend/next.config.js`
```javascript
module.exports = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  rewrites: async () => [
    {
      source: '/api/:path*',
      destination: `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`,
    },
  ],
}
```

### `/frontend/pages/api/proxy.js`
```javascript
export default async function handler(req, res) {
  const { path } = req.query;
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  const response = await fetch(`${backendUrl}/api/${path.join('/')}`, {
    method: req.method,
    headers: req.headers,
    body: req.body,
  });
  
  res.status(response.status);
  res.send(await response.text());
}
```

### `/.railway.json`
```json
{
  "build": "pip install -r requirements.txt",
  "start": "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"
}
```

### `/vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://sirio-api.railway.app/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ],
  "env": {
    "NEXT_PUBLIC_API_URL": "@api_url"
  }
}
```

---

## 📋 CHECKLIST DEPLOYMENT

### Vercel
- [ ] Conectar repo a Vercel
- [ ] Configurar ambiente: `main`
- [ ] Variables de entorno en Vercel
- [ ] Dominio personalizado (opcional)
- [ ] SSL/TLS automático

### Railway
- [ ] Crear proyecto en Railway
- [ ] Conectar repo GitHub
- [ ] Crear servicio PostgreSQL
- [ ] Crear servicio Backend (Python)
- [ ] Configurar variables de entorno
- [ ] Health checks
- [ ] Dominio personalizado (opcional)

### Integraciones
- [ ] Frontend conectado a Backend
- [ ] CORS configurado
- [ ] Variables de entorno sincronizadas
- [ ] Logs monitoreados
- [ ] Backups de BD programados

---

## 🔗 URLS POST-DEPLOYMENT

```
Frontend:  https://sirio-tpv.vercel.app
Backend:   https://sirio-api.railway.app
API Docs:  https://sirio-api.railway.app/docs
Database:  PostgreSQL en Railway
```

---

## 📊 COSTOS ESTIMADOS

### Vercel
- Frontend: **Gratis** (hasta 100GB bandwidth/mes)
- Pro: $20/mes (si necesitas más)

### Railway
- PostgreSQL: $5/mes (includes 10GB)
- Backend: Pay-as-you-go (~$0.000011/CPU-second)
- Típico: $10-20/mes

**Total estimado: $15-25/mes**

---

## 🚀 PRÓXIMOS PASOS

1. **Preparar Frontend para Vercel** (5 min)
2. **Preparar Backend para Railway** (5 min)
3. **Deploym Frontend a Vercel** (2 min)
4. **Deploy Backend a Railway** (5 min)
5. **Probar integración** (5 min)

**Tiempo total: ~20 minutos**

---

## ⏭️ QUIERES QUE PROCEDA?

¿Quieres que prepare los archivos y scripts para deploy automático?

```bash
# Se crearía:
✅ frontend/next.config.js
✅ frontend/pages/api/ (proxy routes)
✅ vercel.json (config)
✅ .railway.json (config)
✅ DEPLOYMENT_GUIDE.md (paso a paso visual)
✅ deploy.sh (automático)
```

**Escriba `sí` o `yes` para proceder.**
