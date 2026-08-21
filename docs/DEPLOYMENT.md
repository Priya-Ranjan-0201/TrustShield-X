# TRUTHSHIELD X — PRODUCTION DEPLOYMENT GUIDE

**Release:** `REL-4.0.0-PROD-CERTIFIED`  
**Build Hash:** `sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069`  

---

## 1. Prerequisites

- Python 3.13+ with `uv` package manager
- Node.js 20+ (for Frontend UI build)
- PostgreSQL 16 with continuous WAL archiving
- Redis 7.2 Cluster with tenant key isolation

---

## 2. Production Startup

```bash
# 1. Clone & Navigate
cd "TrustShield X"

# 2. Start Infrastructure via Docker Compose
docker-compose up -d postgres redis

# 3. Apply Reversible Database Migrations (42 revisions)
cd backend/auth-service
uv run alembic upgrade head

# 4. Launch Production API Server
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# 5. Build & Serve Production Frontend
cd ../../frontend
npm install
npm run build
```
