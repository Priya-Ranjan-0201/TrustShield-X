# TruthShield X
# Security Architecture & Cybersecurity Standards Specification
## Document: 10-Security.md
**Version:** 1.0 (Unified Master Security Specification)  
**Status:** Approved Mandatory Technical Security Standard  
**Security Architecture Model:** Zero-Trust Architecture (ZTA) & Defense in Depth  
**Regulatory Compliance:** India DPDP Act 2023, CERT-In Cyber Security Directives, OWASP Top 10 (2021), ISO/IEC 27001 Alignment

---

# Document Overview

This document defines the complete Security Architecture, Cryptographic Standards, Zero-Trust Boundaries, Authentication Policies, Data Protection Controls, Threat Mitigation Strategies, and Incident Response Workflows for **TruthShield X**.

As India's National Digital Trust Platform, security is embedded into every layer of TruthShield X via **Security by Design** and **Privacy by Design** principles.

---

# Table of Contents

1. Executive Security Architecture & Zero-Trust Principles
2. Zero-Trust Boundary Topology & mTLS Inter-Service Security
3. Authentication & Credential Hardening Standards
   - 3.1 Argon2id Password Hashing Specification
   - 3.2 JWT Access Token & HttpOnly Refresh Cookie Lifecycle
   - 3.3 Multi-Factor Authentication (MFA) Strategy
4. Authorization & Role-Based Access Control (RBAC) Matrix
5. Cryptography & Encryption Standards (Transit, Rest, Secrets)
6. File Ingestion & Anti-Malware Sandbox Pipeline
7. Network, Web Application Firewall (WAF) & Header Hardening
8. OWASP Top 10 (2021) Vulnerability Mitigation Matrix
9. Privacy by Design & DPDP Act 2023 Compliance
10. AI Model Integrity & Adversarial Defense Security
11. Audit Logging, SIEM Integration & Observability
12. Security Incident Response Workflow (SIRT Protocol)
13. Backup, Disaster Recovery & High Availability SLAs
14. Secure Software Development Lifecycle (SSDL) & Gateways

---

# 1. Executive Security Architecture & Zero-Trust Principles

TruthShield X enforces a strict **Zero-Trust Architecture (ZTA)**. The system never assumes trust for any user, device, network location, or internal microservice call. Every transaction is authenticated, authorized, encrypted, and logged.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ZERO-TRUST SECURITY CORE                              │
├───────────────────┬───────────────────┬───────────────────┬─────────────────┤
│ 1. Explicit      │ 2. Least          │ 3. Assume         │ 4. Privacy      │
│    Verification   │    Privilege      │    Breach         │    by Design    │
│  Authenticate &   │ Enforce strict    │ Encrypt data in   │ 30-day artifact │
│  authorize every  │ RBAC roles on all │ transit & rest;   │ auto-purging    │
│  request always.  │ API endpoints.    │ isolate services. │ (DPDP 2023).    │
└───────────────────┴───────────────────┴───────────────────┴─────────────────┘
```

---

# 2. Zero-Trust Boundary Topology & mTLS Inter-Service Security

```
      [ UNTRUSTED PUBLIC CLIENTS (Web / Android / Extension) ]
                                 │
                        HTTPS / TLS 1.3 (WAF)
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │  API GATEWAY / INGRESS│
                     └───────────┬───────────┘
                                 │
            mTLS (Mutual TLS 1.3) + Signed Internal JWTs
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Auth Service    │     │ Scan Service    │     │ AI Gateway      │
│ (PostgreSQL DB) │     │ (MinIO Storage) │     │ (PyTorch/ONNX)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

- **Perimeter Edge:** All external traffic terminates at the API Gateway over TLS 1.3 guarded by Web Application Firewall (WAF) rules.
- **Inter-Service Mesh:** Internal microservices communicate over mutual TLS 1.3 (mTLS) with signed internal service JWT headers, preventing unauthorized east-west lateral movement.

---

# 3. Authentication & Credential Hardening Standards

## 3.1 Argon2id Password Hashing Specification
Plaintext passwords are strictly forbidden. All user passwords are saved using **Argon2id** algorithm settings configured to resist GPU/ASIC brute-force attacks:
- **Memory Cost ($m$):** 64 MB ($65,536\text{ KiB}$)
- **Time Cost ($t$):** 3 Iterations
- **Parallelism ($p$):** 4 Threads
- **Salt Length:** 16 bytes minimum (cryptographically generated)
- **Hash Length:** 32 bytes

## 3.2 JWT Access Token & HttpOnly Refresh Cookie Lifecycle

```
Client                        API Gateway                  Auth Service
  │                                │                            │
  │── POST /api/v1/auth/login ────►│───────────────────────────►│
  │                                │                            │── Verify Argon2id Hash
  │                                │                            │── Generate Tokens
  │◄── HTTP 200 OK ────────────────│◄── Return JWT & Cookie ────│
  │   - JSON Payload: accessToken (15-min TTL)
  │   - Header: Set-Cookie: tsx_refresh (7-day TTL, HttpOnly, Secure, SameSite=Strict)
```

- **JWT Access Token:** Short-lived (15-minute expiration) signed with RSA-256 / Ed25519. Transmitted via `Authorization: Bearer <token>` header.
- **Refresh Token Cookie:** Long-lived (7-day expiration) stored exclusively in an `HttpOnly`, `Secure`, `SameSite=Strict` cookie, preventing JavaScript XSS theft.
- **Token Invalidation:** Revoked tokens are immediately stored in Redis blacklist (`jwt:blacklist:<jti>`).

---

# 4. Authorization & Role-Based Access Control (RBAC) Matrix

TruthShield X enforces granular RBAC across 5 primary roles:

| Role Name | Access Level | Target Capabilities |
|---|---|---|
| **`CITIZEN`** | Standard User | Submit scans, view personal scan history, generate PDF report summaries. |
| **`BUSINESS`** | Enterprise API | Execute batch scan APIs, integrate webhook threat feeds, access team history. |
| **`ANALYST`** | Cyber Officer | View regional threat map, inspect raw threat telemetry, query Neo4j graph. |
| **`GOVERNMENT`** | Institutional | Access national scam analytics, issue public cyber advisories, request CERT-In data. |
| **`ADMIN`** | System Admin | Manage user accounts, retrain/deploy AI models, inspect system security audit logs. |

---

# 5. Cryptography & Encryption Standards (Transit, Rest, Secrets)

- **Data in Transit:** Enforce TLS 1.3 exclusively across all endpoints. Disable legacy TLS 1.0, 1.1, and SSLv3. Require cipher suites with Forward Secrecy (ECDHE-ECDSA-AES256-GCM-SHA384).
- **Data at Rest:** All sensitive PostgreSQL columns (phone numbers, user document metadata) and MinIO object storage files are encrypted using **AES-256-GCM** with unique per-field Initialization Vectors (IVs).
- **Secrets Management:** Microservice passwords, DB connection strings, and private key signatures are injected at runtime via **HashiCorp Vault**. Hardcoding secrets in source code or `.env` files committed to Git is prohibited.

---

# 6. File Ingestion & Anti-Malware Sandbox Pipeline

Every uploaded file (Image, PDF, APK, Audio) must pass through a strict sanitization pipeline prior to storage or AI inference:

```
Upload Stream ──► MIME & Magic Byte Check ──► ClamAV Anti-Malware ──► Sandbox Storage (MinIO)
                          │                         │
                 (Mismatch? Block)          (Infected? Block)
```

1. **Magic Byte Signature Inspection:** Validates actual binary file headers against declared extension (`.pdf` = `%PDF-`, `.png` = `\x89PNG`).
2. **ClamAV Anti-Malware Engine:** Scans incoming files for known virus/trojan signatures before saving to storage.
3. **APK Sandbox Execution:** Android `.apk` binaries run inside isolated micro-VM containers to monitor malicious C2 runtime behavior.

---

# 7. Network, Web Application Firewall (WAF) & Header Hardening

All HTTP responses from the API Gateway must include mandatory security headers:

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

---

# 8. OWASP Top 10 (2021) Vulnerability Mitigation Matrix

| OWASP Risk Category | Primary Vulnerability | TruthShield X Engineering Mitigation |
|---|---|---|
| **A01: Broken Access Control** | Unauthorized API Data Exposure | Enforce JWT RBAC middleware check on every protected FastAPI endpoint. |
| **A02: Cryptographic Failures** | Plaintext Secrets / Weak Hashes | Mandatory TLS 1.3, AES-256-GCM at-rest encryption, Argon2id password hashing. |
| **A03: Injection** | SQL, Command & XSS Injection | SQLAlchemy 2.0 parameterized queries, Pydantic input schemas, React XSS auto-escaping. |
| **A04: Insecure Design** | Unrestricted File Ingest | Anti-malware scanning (ClamAV), magic byte validation, isolated execution sandboxes. |
| **A05: Security Misconfiguration** | Verbose Stack Traces in Production | Global exception middleware returning standardized JSON error envelopes (`TSX-xxxx`). |
| **A06: Vulnerable Components** | Known Dependency CVEs | Automated CI/CD dependency vulnerability scanning via Snyk and Trivy. |
| **A07: Identification & Auth** | Brute-force & Credential Stuffing | API Gateway rate limiting (100 req/min), HttpOnly refresh cookies, account lockouts. |
| **A08: Software & Data Integrity** | Tampered Code / AI Model Poisoning | Signed Docker container images, signed AI model ONNX weight checkpoints. |
| **A09: Logging & Monitoring** | Unnoticed Attack Attempts | Structured JSON logging (`traceId`), ELK central collection, Prometheus security alerts. |
| **A10: Server-Side Request Forgery** | SSRF via Headless Web Scraper | Restrict Playwright website scraper to public IP ranges; block private/internal Subnet IPs. |

---

# 9. Privacy by Design & DPDP Act 2023 Compliance

TruthShield X is fully compliant with India's **Digital Personal Data Protection (DPDP) Act 2023**:

- **Section 6 (Consent & Purpose Limitation):** Users explicitly consent to temporary artifact scanning before upload. Content is processed exclusively for authenticity analysis.
- **Section 6(7) (Automated Data Erasure):** Inactive user upload files and temporary frame captures stored in MinIO automatically expire and are permanently purged after **30 days** via automated S3 lifecycle rules.
- **Right to Erasure (Data Wiping API):** Executing `DELETE /api/v1/users/me` immediately purges user profile data, session keys, and scan metadata from PostgreSQL and Redis.
- **Anonymized Telemetry:** Threat intelligence shared with Neo4j and Qdrant uses cryptographic SHA-256 hashes of domains, VPAs, and phone numbers, ensuring zero personal identity exposure.

---

# 10. AI Model Integrity & Adversarial Defense Security

- **Signed ONNX Checkpoints:** AI model weight files are cryptographically signed using SHA-256 hashes verified by the AI Gateway prior to memory loading.
- **Adversarial Noise Defense:** Deepfake vision models employ visual preprocessing normalization to neutralize adversarial noise perturbations intended to bypass detection.
- **Prompt Injection Hardening:** LLM claim extraction engines sanitize input text strings to prevent prompt injection or system instruction override attacks.

---

# 11. Audit Logging, SIEM Integration & Observability

Every sensitive system event is logged as a structured JSON object forwarded to central ELK Stack SIEM:

```json
{
  "timestamp": "2026-08-04T14:56:00Z",
  "level": "SECURITY",
  "service": "auth-service",
  "event": "FAILED_LOGIN_ATTEMPT",
  "clientIp": "203.0.113.195",
  "traceId": "req_9f82c1d34e5a",
  "details": {
    "email": "user@example.com",
    "attemptCount": 3
  }
}
```

---

# 12. Security Incident Response Workflow (SIRT Protocol)

```
[ Incident Trigger ] ──► [ Phase 1: Detect ] ──► [ Phase 2: Contain ]
                                                       │
     ┌─────────────────────────────────────────────────┘
     ▼
[ Phase 3: Eradicate ] ──► [ Phase 4: Recover ] ──► [ Phase 5: Post-Mortem Audit ]
```

- **Low / Medium Alert:** Automated API Gateway rate-limit escalation or IP block.
- **High / Critical Alert:** Emergency SIRT trigger, circuit-breaker isolation of target microservice, immediate notification to Security Lead and CERT-In reporting channel within mandatory timeline.

---

# 13. Backup, Disaster Recovery & High Availability SLAs

- **Recovery Time Objective (RTO):** $< 2$ Hours (Time to fully restore platform operations following datacenter failure).
- **Recovery Point Objective (RPO):** $< 15$ Minutes (Maximum allowable data loss window, enforced via PostgreSQL continuous WAL archiving).
- **Redundancy:** Multi-region PostgreSQL read replicas, Redis Sentinel 3-node cluster, and distributed MinIO storage with 4-drive erasure coding.

---

# 14. Secure Software Development Lifecycle (SSDL) & Gateways

```
Code Commit ──► Static SAST (Ruff/ESLint) ──► Dependency Scan (Snyk) ──► Image Scan (Trivy)
                                                                               │
     ┌─────────────────────────────────────────────────────────────────────────┘
     ▼
(Passed All Scans?) ── YES ──► Sign Docker Image ──► Deploy to Kubernetes Cluster
     │ NO
     └──► Block CI/CD Build
```

---
**[ END OF MASTER SECURITY SPECIFICATION v1.0 ]**
