# TruthShield X
## AI Development Rules & Engineering Standards
### Document: 03-Rules.md
**Version:** 1.0 (Unified Master)  
**Status:** Approved Mandatory Technical Standard  
**Target Audience:** Core Engineering Team, System Architects, QA Engineers, AI Assistants (Antigravity, Cursor, Windsurf, Claude Code, Copilot)

---

# Purpose

This document establishes the mandatory engineering standards, coding conventions, architectural constraints, security policies, AI model governance rules, testing requirements, documentation standards, and DevOps practices for **TruthShield X**.

Every human engineer, contributor, and AI coding assistant working on this project must strictly comply with these rules.

---

# Rule Hierarchy & Priority

When two guidelines or implementation choices appear to conflict, decision resolution follows this strict priority order:

1. **Security & Zero-Trust Compliance** (Protects user data, credentials, and system integrity)
2. **Architecture & Service Boundaries** (Maintains microservices separation and API contracts)
3. **Data Integrity & Privacy** (Ensures DPDP compliance, transactional consistency, and non-corruption)
4. **Performance & SLA Targets** (Meets response latency and system scalability targets)
5. **Code Maintainability & Clean Code** (Improves readability, modularity, and testability)
6. **UI/UX Aesthetics & Animation** (Delivers a modern, accessible interface)

---

# Table of Contents

1. General Development Rules (G-001 – G-010)
2. Architecture & Service Boundary Rules (A-001 – A-008)
3. Frontend Engineering Rules (F-001 – F-012)
4. Backend Microservice Rules (B-001 – B-010)
5. AI Development & Model Lifecycle Rules (AI-001 – AI-010)
6. Database & Migration Rules (DB-001 – DB-008)
7. API Design & Versioning Rules (API-001 – API-008)
8. Zero-Trust Security & Privacy Rules (SEC-001 – SEC-012)
9. Structured Logging & Telemetry Rules (LOG-001 – LOG-008)
10. Standardized Error Handling Rules (ERR-001 – ERR-008)
11. Git Workflow & Conventional Commits (GIT-001 – GIT-006)
12. Testing & AI Benchmark Rules (TEST-001 – TEST-008)
13. Documentation & Memory Maintenance (DOC-001 – DOC-006)
14. DevOps, Container & Infrastructure Rules (OPS-001 – OPS-008)
15. UI/UX Design System Rules (UI-001 – UI-008)
16. AI Coding Assistant Directives (AGENT-001 – AGENT-010)
17. Definition of Done (DoD) & Single Source of Truth

---

# 1. General Development Rules

- **G-001 (No Duplicate Logic):** Never duplicate business or parsing logic across modules. Abstract shared routines into `@truthshield/shared` or microservice common utilities.
- **G-002 (Modularity & Single Responsibility):** Every class, function, or module must perform exactly one function. Keep functions short (<50 lines) and files focused (<300 lines).
- **G-003 (Zero Hardcoded Secrets):** Never commit API keys, tokens, DB credentials, or private keys to source control. Enforce loading via `.env` or HashiCorp Vault.
- **G-004 (Input Validation):** Validate every external input (API payloads, uploaded file headers, query params) at the system boundary before executing logic.
- **G-005 (Zero-Trust Input Sanitization):** Treat all user inputs as untrusted. Sanitize strings against SQL injection, XSS, Path Traversal, and Command Injection.
- **G-006 (Dependency Injection):** Use Dependency Injection (DI) for database sessions, API clients, and service repositories to enable seamless unit testing.
- **G-007 (Composition over Inheritance):** Prefer object composition and modular mixins over deep class inheritance hierarchies.
- **G-008 (Strict Typing):** Enforce strict typing across Python (Pydantic / Type Hints) and TypeScript (`noImplicitAny: true`). Explicitly define return types.
- **G-009 (Mandatory Unit Tests):** Every new service method or utility function must be accompanied by corresponding unit tests before PR approval.
- **G-010 (No Dead or Commented Code):** Never commit commented-out production code, scratch files, or unused imports to main branches.

---

# 2. Architecture & Service Boundary Rules

- **A-001 (Database Isolation):** Frontend client applications (Web, Mobile, Extension) must NEVER access backend databases directly.
- **A-002 (Single Entry Gateway):** All external client communications must pass strictly through the central API Gateway.
- **A-003 (Microservice Data Sovereignty):** No microservice may directly read or write to another microservice's database. Inter-service data exchange occurs exclusively via REST, gRPC, or RabbitMQ events.
- **A-004 (Asynchronous Execution):** Long-running tasks (>2 seconds, e.g., Video Deepfake processing, APK dynamic analysis) must execute asynchronously using Celery/RabbitMQ task queues.
- **A-005 (AI Gateway Abstraction):** All AI models must be isolated behind the central AI Gateway. Client and backend services must never call deep learning models directly.
- **A-006 (Mandatory Health Endpoints):** Every backend microservice and AI model container must expose standardized `/healthz` (liveness) and `/readyz` (readiness) HTTP endpoints.
- **A-007 (Stateless Microservices):** Microservices must remain stateless. Shared state must be persisted in Redis or database stores to allow instant horizontal scaling.
- **A-008 (Circuit Breaker Protection):** External API integrations (e.g., WHOIS lookup, Google Safe Browsing) must implement circuit breakers to prevent cascading service failures.

---

# 3. Frontend Engineering Rules (React 19 + TypeScript + Vite)

- **F-001 (Functional Components Only):** Class components are strictly forbidden. Use modern React 19 functional components with hooks.
- **F-002 (Feature-Based Structure):** Organize pages and feature domain components inside `src/features/<feature-name>/`.
- **F-003 (Reusable Component Isolation):** Atomic, domain-agnostic UI elements (buttons, inputs, modals) belong exclusively in `src/components/`.
- **F-004 (Hook & Service Abstraction):** Never invoke `fetch()` or `axios` directly inside JSX components. Abstract API calls into React Query hooks inside `src/services/` or `src/hooks/`.
- **F-005 (Zero Business Logic in JSX):** JSX must remain clean and presentation-focused. Complex calculations or filtering logic belong in custom hooks or utility functions.
- **F-006 (Server State via TanStack Query):** Manage all server fetching, caching, synchronization, and polling using TanStack Query.
- **F-007 (Client State via Zustand):** Use Zustand for lightweight global client state (e.g., active user session, theme, active modal).
- **F-008 (Form Validation):** Every form must use React Hook Form paired with Zod schemas for strict schema validation.
- **F-009 (Component Line Limit):** Keep UI components under ~300 lines. Split complex views into sub-components.
- **F-010 (Accessibility Standards):** All UI elements must include appropriate ARIA attributes, semantic HTML tags, and support keyboard navigation (WCAG 2.1 AA).
- **F-011 (Dark Mode First):** Build and style all views using dark mode as the default primary theme.
- **F-012 (Type Safety):** Prohibit the use of `any` or `ts-ignore`. Explicitly declare prop types and component interfaces.

```typescript
// Exemplary React Component Pattern (F-004, F-005, F-008)
import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { scanUrlSchema, ScanUrlInput } from './scan.schema';
import { useScanUrl } from '@/services/useScanService';

export const UrlScanForm: React.FC = () => {
  const { mutate: scanUrl, isPending } = useScanUrl();
  const { register, handleSubmit, formState: { errors } } = useForm<ScanUrlInput>({
    resolver: zodResolver(scanUrlSchema),
  });

  const onSubmit = (data: ScanUrlInput) => {
    scanUrl(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <input
        {...register('url')}
        placeholder="Enter URL to scan..."
        className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-md text-white"
        aria-label="URL Input"
      />
      {errors.url && <p className="text-red-400 text-sm">{errors.url.message}</p>}
      <button
        type="submit"
        disabled={isPending}
        className="w-full py-2 bg-cyan-600 hover:bg-cyan-500 rounded-md font-semibold text-white transition-all"
      >
        {isPending ? 'Analyzing Website...' : 'Inspect Website'}
      </button>
    </form>
  );
};
```

---

# 4. Backend Microservice Rules (FastAPI + Python 3.12)

- **B-001 (Controller-Service-Repository Pattern):** Enforce strict separation of layers:
  - `routers/`: Route declarations and HTTP status codes only.
  - `services/`: Core business logic and rules.
  - `repositories/`: Database queries and ORM operations.
- **B-002 (Pydantic Schemas):** Enforce strict input validation using Pydantic schemas for all request bodies, path parameters, and query strings.
- **B-003 (Standard API Envelope):** Every API endpoint must return a uniform JSON response envelope:

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": {},
  "meta": {
    "traceId": "req_9f82a1...",
    "timestamp": "2026-08-04T14:45:00Z"
  }
}
```

- **B-004 (Asynchronous Endpoints):** Use `async def` for IO-bound endpoints (database queries, network calls, file storage).
- **B-005 (Explicit Exception Middleware):** Catch exceptions globally via custom FastAPI middleware and return standardized error envelopes (never raw 500 stack traces).
- **B-006 (Database Session Management):** Always use dependency injection (`Depends(get_db)`) for database sessions; guarantee session cleanup via `yield`.
- **B-007 (SQLAlchemy 2.0 Syntax):** Use modern SQLAlchemy 2.0 select statements (`select(User).where(...)`). Legacy 1.x query methods are prohibited.
- **B-008 (Background Worker Isolation):** Offload long-running tasks to Celery workers using explicit queue names (`@celery_app.task(queue='deepfake_queue')`).
- **B-009 (No Global Mutable State):** Microservice workers must never maintain in-memory global state between requests.
- **B-010 (Type Annotations):** Enforce 100% Python type hints across function arguments and return signatures (`def process_scan(scan_id: UUID) -> ScanResult:`).

---

# 5. AI Development & Model Lifecycle Rules

- **AI-001 (Model Registry & Versioning):** Every deployed AI model must be registered in the Model Registry with explicit versioning (e.g., `deepfake-video-v1.2.0.onnx`).
- **AI-002 (Standardized Model Output):** Every AI model prediction must output a normalized score dictionary:

```python
# AI Model Standard Output Contract
{
    "model_name": "deepfake-vision-v1.2.0",
    "raw_score": 0.94,          # 0.0 (Safe) to 1.0 (Manipulated)
    "confidence": 0.96,         # 0.0 to 1.0
    "evidence_features": [      # Key visual/audio features extracted
        {"feature": "lip_sync_mismatch", "value": 0.88},
        {"feature": "gan_frequency_noise", "value": 0.92}
    ]
}
```

- **AI-003 (Mandatory Model Testing):** No model may be deployed to production without passing benchmark evaluation tests on held-out test datasets (Precision $\ge 95\%$, Recall $\ge 93\%$).
- **AI-004 (ONNX Runtime Preferred):** Export trained PyTorch/TensorFlow models to ONNX format for deployment to maximize CPU/GPU execution efficiency.
- **AI-005 (Graceful Model Fallback):** If GPU VRAM exceeds 95% threshold or GPU worker is offline, the AI Gateway must automatically failover to CPU ONNX instances.
- **AI-006 (Inference Latency Tracking):** Log model inference execution time in milliseconds for every prediction (`ai_inference_latency_ms`).
- **AI-007 (Model Drift Monitoring):** Continuously log prediction confidence distributions to detect model drift and trigger automated retraining alerts.
- **AI-008 (Zero Overwriting of Weights):** Never overwrite production model weight files directly. Deploy new versions alongside existing ones to allow instant rollback.
- **AI-009 (Demographic & Visual Bias Audit):** Evaluate models across diverse demographic datasets to guarantee bias-free detection performance.
- **AI-010 (Reproducible Pipelines):** Model training pipelines must be fully reproducible using DVC (Data Version Control) and fixed seed configurations.

---

# 6. Database & Migration Rules

- **DB-001 (Automated Migrations Only):** Never modify production database schemas manually. All schema changes must occur via Alembic migrations.
- **DB-002 (UUID Primary Keys):** Use UUIDs (`UUIDv4`) for all primary key columns to prevent enumeration attacks and simplify distributed merging.
- **DB-003 (Indexing Strategy):** Create explicit database indexes on foreign keys, lookups, and frequently filtered query columns (`user_id`, `created_at`, `status`).
- **DB-004 (Migration Reversibility):** Every Alembic migration file must include a fully tested `downgrade()` function alongside `upgrade()`.
- **DB-005 (Zero Plaintext Passwords):** Never store raw passwords or plain text authentication secrets. Passwords must be hashed using Argon2id with unique salts.
- **DB-006 (Data Encryption at Rest):** Sensitive database fields (tokens, identity document numbers) must be encrypted using AES-256-GCM.
- **DB-007 (Connection Pooling):** Enforce SQLAlchemy connection pooling (`pool_size=20`, `max_overflow=10`, `pool_recycle=3600`).
- **DB-008 (Timezones):** All timestamp columns must store UTC time using `TIMESTAMP WITH TIME ZONE`.

---

# 7. API Design & Versioning Rules

- **API-001 (URI Versioning):** Every public API endpoint must include explicit versioning in the URL path (`/api/v1/scan`, `/api/v1/auth/login`).
- **API-002 (RESTful Naming Conventions):** Use plural nouns for resources (`/scans`, `/users`, `/reports`) and proper HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`).
- **API-003 (Mandatory Rate Limiting):** Enforce rate limiting at the API Gateway:
  - Free Citizens: 100 requests / minute.
  - Business APIs: 500 requests / minute.
- **API-004 (Explicit HTTP Status Codes):**
  - `200 OK`: Successful GET/PUT.
  - `201 Created`: Successful POST creation.
  - `202 Accepted`: Asynchronous task queued.
  - `400 Bad Request`: Input schema validation failure.
  - `401 Unauthorized`: Missing or invalid JWT.
  - `403 Forbidden`: Insufficient role permission.
  - `404 Not Found`: Resource does not exist.
  - `429 Too Many Requests`: Rate limit exceeded.
  - `500 Internal Error`: Standardized system error.
- **API-005 (OpenAPI Documentation):** Every endpoint must include clear docstrings, Pydantic schemas, and example response payloads auto-generated in Swagger/OpenAPI.
- **API-006 (Pagination Requirement):** Every list endpoint must support pagination via `page` and `limit` query parameters with defaults (`page=1`, `limit=20`).

---

# 8. Zero-Trust Security & Privacy Rules

- **SEC-001 (HTTPS Everywhere):** All transport communications must enforce TLS 1.3 encryption. HTTP traffic must redirect to HTTPS automatically.
- **SEC-002 (JWT Authentication & Short Lifespan):** Issue short-lived JWT access tokens (15-min expiration) paired with HttpOnly, Secure, SameSite refresh cookies (7-day expiration).
- **SEC-003 (Role-Based Access Control):** Validate user roles (`CITIZEN`, `BUSINESS`, `ANALYST`, `ADMIN`) on every protected route via API Gateway middleware.
- **SEC-004 (Malware Sandbox Inspection):** Every uploaded file (PNG, PDF, APK) must pass through anti-malware inspection (ClamAV) prior to storage or AI inference processing.
- **SEC-005 (Automatic Artifact Deletion):** In compliance with DPDP 2023, user uploaded files and temporary processing frames must be permanently purged after 30 days.
- **SEC-006 (Secure HTTP Headers):** Enforce strict security headers across API Gateway responses:
  - `Strict-Transport-Security: max-age=31536000; includeSubDomains`
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Content-Security-Policy: default-src 'self'`
- **SEC-007 (Audit Logging):** Audit log every authentication attempt, permission escalation, document check, and admin action with immutable timestamps and client IP hashes.
- **SEC-008 (Zero Stack Traces in Production):** Never expose internal Python/JS stack traces, SQL queries, or internal container IP addresses in API error responses.

---

# 9. Structured Logging & Telemetry Rules

- **LOG-001 (JSON Structured Logs):** Log entries must be output as single-line structured JSON objects to `stdout` for collection via ELK / Grafana Loki.
- **LOG-002 (No Raw `print()` Statements):** Standard Python `print()` or `console.log()` statements are strictly forbidden in production code. Use the standard logger.
- **LOG-003 (Contextual Correlation IDs):** Every log entry must include:
  - `traceId`: Unique request correlation ID.
  - `timestamp`: ISO 8601 UTC timestamp.
  - `service`: Microservice name.
  - `userId`: Hashed user ID (when authenticated).
- **LOG-004 (Log Severity Levels):** Use proper severity levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
- **LOG-005 (Zero PII in Application Logs):** Never log raw passwords, credit card numbers, unhashed Aadhaar numbers, or user JWT tokens.

```python
# Exemplary Python Structured Logging Pattern (LOG-001, LOG-003)
import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "service": "scan-router-service",
            "traceId": getattr(record, "traceId", "N/A"),
            "message": record.getMessage(),
            "module": record.module,
        }
        return json.dumps(log_obj)
```

---

# 10. Standardized Error Handling Rules

- **ERR-001 (Uniform Error Envelope):** All microservice errors must adhere to the standardized JSON error structure:

```json
{
  "success": false,
  "error": {
    "code": "TSX-4001",
    "message": "Resource validation failed.",
    "details": "The submitted URL contains an invalid domain structure.",
    "traceId": "req_8c91d2f34e5a"
  }
}
```

- **ERR-002 (Standard Error Code Prefix):** System error codes must follow domain prefixes:
  - `TSX-1xxx`: Authentication & Auth Errors.
  - `TSX-2xxx`: Validation & Input Errors.
  - `TSX-3xxx`: Scan Engine & File Router Errors.
  - `TSX-4xxx`: AI Gateway & Model Inference Errors.
  - `TSX-5xxx`: Database & Storage Errors.
  - `TSX-9xxx`: System Critical & Internal Failures.
- **ERR-003 (Sanitized Error Messages):** Error messages returned to client applications must be user-friendly and actionable, free from internal technical jargon.

---

# 11. Git Workflow & Conventional Commits

- **GIT-001 (Branching Model):** Main development branches: `main` (Production), `develop` (Integration). Feature branches follow naming standards:
  - `feature/<short-description>`
  - `bugfix/<short-description>`
  - `hotfix/<short-description>`
  - `release/<version>`
- **GIT-002 (Conventional Commits):** Commit messages must follow Conventional Commit specification:
  - `feat: add visual brand impersonation check`
  - `fix: resolve JWT token expiration refresh loop`
  - `docs: update system architecture microservice diagram`
  - `test: add unit tests for Aadhaar Verhoeff checksum`
  - `refactor: optimize website headless screenshot rendering`
- **GIT-003 (Atomic Commits):** Keep commits atomic and focused on a single logical change. Large multi-feature commits are prohibited.
- **GIT-004 (Pull Request Reviews):** Every PR requires at least one approving review from a core maintainer and passing CI/CD checks before merging.
- **GIT-005 (No Direct Push to Main):** Direct pushes to `main` or `develop` branches are strictly blocked via repository branch protection rules.

---

# 12. Testing & AI Benchmark Rules

- **TEST-001 (Minimum Code Coverage):** Maintain at least 80% line coverage for backend microservice business logic.
- **TEST-002 (Testing Layers):**
  - **Unit Tests:** Test isolated service functions and utility methods (`pytest`, `vitest`).
  - **Integration Tests:** Test database queries and internal API interactions (`pytest-asyncio`).
  - **E2E API Tests:** Validate complete request/response flows against running microservices (`httpx`).
- **TEST-003 (AI Model Benchmark Suite):** AI models must undergo automated benchmark evaluation prior to deployment:
  - Synthetic Deepfake Benchmark Dataset ($>1,000$ clips).
  - Phishing Website Visual Dataset ($>500$ captures).
  - Fraud Document Test Suite ($>200$ samples).
- **TEST-004 (Automated CI/CD Test Runner):** CI/CD pipelines must automatically run linting, static analysis, unit tests, and security scans on every pull request.

---

# 13. Documentation & Memory Maintenance

- **DOC-001 (Documentation as Source of Truth):** When code implementation and documentation disagree, **Documentation is the Source of Truth**. Update documentation before changing code.
- **DOC-002 (Module READMEs):** Every microservice directory in `/backend`, `/ai-services`, and `/apps` must contain a clear `README.md` detailing setup, environment variables, and usage.
- **DOC-003 (Memory.md Maintenance):** Maintain `docs/Memory.md` as an active log recording key architectural decisions, resolved issues, and context state across development sessions.
- **DOC-004 (Inline Code Comments):** Add docstrings to every public function and class explaining parameters, return values, and potential exceptions.

---

# 14. DevOps, Container & Infrastructure Rules

- **OPS-001 (Docker Containerization):** Every microservice must include a multi-stage `Dockerfile` producing minimal production container images (Alpine / Slim bases).
- **OPS-002 (Non-Root Container User):** Containerized applications must execute under a non-root system user (`USER appuser`) for security hardening.
- **OPS-003 (Environment Configuration):** Microservice configuration must be read strictly from environment variables (12-Factor App principles).
- **OPS-004 (Kubernetes Readiness Probes):** Define explicit `livenessProbe` and `readinessProbe` configs in Kubernetes deployment manifests targeting `/healthz` and `/readyz`.
- **OPS-005 (Resource Limits):** Define explicit CPU and Memory resource `requests` and `limits` for every Kubernetes container manifest.

---

# 15. UI/UX Design System Rules

- **UI-001 (Dark Theme Dominance):** Maintain a sleek, modern dark mode aesthetic (Deep Slate / Cyber Charcoal base `#0F172A`, Electric Cyan `#06B6D4` accents, Emerald Emerald `#10B981` safety badges).
- **UI-002 (Glassmorphism Accents):** Apply subtle backdrop blurring and border highlights (`backdrop-blur-md bg-slate-900/80 border border-slate-800`).
- **UI-003 (Micro-Animations):** Enhance user feedback with smooth micro-animations using Framer Motion (button hover states, scan loading indicators, score transitions).
- **UI-004 (Responsive Mobile Layouts):** All web screens must adapt seamlessly to mobile viewports ($320\text{px}$ to $1920\text{px}$).

---

# 16. AI Coding Assistant Directives (Antigravity / Cursor / Copilot)

AI assistants generating code for TruthShield X must strictly obey the following operational instructions:

- **AGENT-001 (Context Mandatory):** Before proposing code edits, always read `PRD.md`, `02-Architecture.md`, `03-Rules.md`, and `Memory.md`.
- **AGENT-002 (No Speculative Fields):** Never invent arbitrary database columns, API parameters, or external dependencies not specified in documentation.
- **AGENT-003 (Preserve Existing Functionality):** Never delete, refactor, or overwrite existing working code without explicit instruction or clear justification.
- **AGENT-004 (Always Include Tests):** When generating new service methods or backend endpoints, always generate corresponding unit/integration tests.
- **AGENT-005 (Enforce Standard Response Envelopes):** Ensure all generated FastAPI endpoints wrap output in the standard success/error JSON response envelopes.
- **AGENT-006 (Strict Type Annotations):** Always provide explicit Python type hints and TypeScript interface definitions.
- **AGENT-007 (No Plaintext Secrets):** Never hardcode dummy passwords or mock secrets directly into code snippets.
- **AGENT-008 (Update Documentation):** When implementing new features or modifying behavior, update the relevant documentation markdown files.
- **AGENT-009 (Follow Monorepo Path Structure):** Place generated code in its correct directory as defined in the Monorepo Structure specification.
- **AGENT-010 (Verify Lint & Syntax):** Ensure generated code passes linting and syntax checks before finalizing response.

---

# 17. Definition of Done (DoD) & Single Source of Truth

A feature or user story is considered **100% DONE** and ready for production merging only when:

1. **Functional Completeness:** All acceptance criteria specified in `PRD.md` are implemented and verified.
2. **Code Quality & Linting:** Code adheres to all `03-Rules.md` guidelines and passes automated linter checks (`ruff`, `eslint`).
3. **Automated Test Coverage:** Unit and integration tests pass with $\ge 80\%$ code coverage.
4. **Security Review:** Input validation, authentication, authorization, and sanitization checks are verified.
5. **API & Open API Docs:** API endpoints are documented with OpenAPI schemas and standard JSON response envelopes.
6. **Structured Logging:** Standardized JSON logging with `traceId` correlation is embedded.
7. **Error Handling:** Standardized error codes and user-friendly error messages are implemented.
8. **Documentation Update:** `PRD.md`, `02-Architecture.md`, and `Memory.md` are updated to reflect any technical changes.

---

# Single Source of Truth Directive

> **When code implementation and documentation disagree:**  
> **Documentation is the Single Source of Truth.**  
> *If documentation is missing, ambiguous, or incorrect, update the documentation and receive architectural sign-off before modifying production code.*

---
**[ END OF RULES SPECIFICATION v1.0 ]**
