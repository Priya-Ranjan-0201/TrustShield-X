# TruthShield X — National Digital Trust Platform

TruthShield X is a enterprise-grade, multi-tenant digital authenticity and anti-fraud verification platform built for citizens, businesses, and government entities.

---

## Phase 1: Authentication & User Management Service

### Security & Architecture Highlights
- **Password Security**: Argon2id hashing (`time_cost=3`, `memory_cost=65536`, `parallelism=4`).
- **Password Policy**: Minimum 10 characters, at least 1 uppercase, 1 lowercase, 1 digit, 1 special character, checked against top-10k static common password blacklist.
- **Token Security**: Access Token returned in JSON response body (stored in Zustand memory, never localStorage). Refresh Token issued in `HttpOnly`, `Secure`, `SameSite=Strict` cookie (`tsx_refresh_token`).
- **Token Rotation & Theft Detection**: On every `/refresh`, old refresh token JTI is invalidated. If a revoked refresh token is presented, theft is detected: all active sessions for that user ID are instantly invalidated across PostgreSQL and Redis, and an audit alert is logged.
- **Rate Limiting**: Redis-backed sliding window rate limiter (`/login`: 5 attempts/15 mins per IP+Email; `/register`: 3 attempts/hour per IP). Returns HTTP 429 with `Retry-After` header.
- **Audit Logging & Tracing**: Distributed correlation trace ID (`X-Trace-ID`) included on every request/response envelope and logged to `audit_logs` table.
- **Database & Models**: PostgreSQL 16 with SQLAlchemy 2.0 async engine and Alembic migrations. Seeded roles (`CITIZEN`, `BUSINESS`, `GOVERNMENT`, `ADMIN`).
- **Frontend Architecture**: React 19, Vite, TypeScript, Tailwind CSS, Zustand, TanStack Query, React Hook Form + Zod, Axios interceptor handling silent refresh.

---

## Project Structure

```
TrustShield X/
├── backend/
│   └── auth-service/           # FastAPI Auth Microservice
│       ├── alembic/            # Database schema migrations
│       ├── app/
│       │   ├── api/            # API endpoints & dependency injection
│       │   ├── core/           # Security, Argon2id, Redis, Password Policy
│       │   ├── models/         # SQLAlchemy 2.0 Models
│       │   ├── repositories/   # DB Access Layer (Users, Tokens, Audit)
│       │   ├── schemas/        # Pydantic v2 schemas & response envelopes
│       │   └── services/       # AuthService & UserService
│       ├── tests/              # Pytest unit & API integration test suite
│       ├── requirements.txt
│       └── Dockerfile
├── apps/
│   └── web/                    # React 19 Frontend Web Application
│       ├── src/
│       │   ├── components/     # UI components (Button, Input, Card, Alert)
│       │   ├── features/       # Auth (Login, Register, Reset) & Profile pages
│       │   ├── services/       # Axios client with silent refresh interceptor
│       │   └── store/          # Zustand in-memory auth store
│       ├── index.html
│       ├── tailwind.config.js
│       └── Dockerfile
├── docs/                       # Project Specifications & Memory
└── docker-compose.yml          # Container orchestration (PostgreSQL, Redis, FastAPI, Web)
```

---

## Local Development & Setup

### 1. Backend Setup & Test Suite
```bash
cd backend/auth-service
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run Alembic DB Migration (Ensure PostgreSQL & Redis are running)
alembic upgrade head

# Run Test Suite
pytest --cov=app --cov-report=term-missing
```

### 2. Docker Compose Infrastructure Setup
To spin up all services (PostgreSQL 16, Redis 7, Auth Microservice, React Web App):
```bash
docker-compose up --build -d
```

Access Services:
- **Web Frontend**: http://localhost
- **Auth Microservice API Docs**: http://localhost:8000/api/v1/docs
- **Healthcheck Probe**: http://localhost:8000/health
