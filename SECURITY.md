# TruthShield X Security Policy & Specifications

## 1. Authentication Security Standards

### Password Security & Policy
- **Hashing Algorithm**: Argon2id (`time_cost=3`, `memory_cost=65536`, `parallelism=4`).
- **Password Strength Rules**:
  - Minimum length: 10 characters.
  - Required characters: At least 1 uppercase letter (`A-Z`), 1 lowercase letter (`a-z`), 1 numeric digit (`0-9`), and 1 special character.
  - Blacklist: Checked against a top-10k static common password blacklist.

### Token Security & Session Storage
- **Access Tokens**: Short-lived (15 minutes), returned strictly in the JSON response payload, and stored exclusively in application memory (Zustand store). Access tokens are never written to `localStorage`, `sessionStorage`, or non-HttpOnly cookies.
- **Refresh Tokens**: Long-lived (7-day sliding window), stored in `HttpOnly`, `Secure`, `SameSite=Strict` cookies (`tsx_refresh_token`).
- **Token Rotation & Theft Detection**: Every refresh request revokes the presented refresh token JTI and issues a new pair. Re-presenting an already-revoked refresh token triggers automated token theft detection: all active refresh tokens and device sessions for that user ID are revoked in PostgreSQL and Redis, and a `TOKEN_THEFT_DETECTED` security alert is generated.

### Rate Limiting
- **Redis-Backed Sliding Window**:
  - `/api/v1/auth/login`: 5 attempts per 15 minutes per `IP + Email`.
  - `/api/v1/auth/register`: 3 attempts per hour per `IP`.
  - Exceeded limits return HTTP 429 `Too Many Requests` with a `Retry-After` header.

---

## 2. Standardized Error Codes (`TSX-AUTH-XXX`)

| Error Code | HTTP Status | Description |
| :--- | :--- | :--- |
| `TSX-AUTH-001` | 401 Unauthorized | Invalid email or password credentials. |
| `TSX-AUTH-002` | 403 Forbidden | Email address not verified. |
| `TSX-AUTH-003` | 401 Unauthorized | Access or refresh token expired. |
| `TSX-AUTH-004` | 401 Unauthorized | Token revoked or reused (token theft). |
| `TSX-AUTH-005` | 403 Forbidden | Account suspended, inactive, or disabled. |
| `TSX-AUTH-006` | 429 Too Many Requests | Rate limit exceeded. |
| `TSX-AUTH-007` | 404 Not Found | Requested user or resource not found. |
| `TSX-AUTH-008` | 400 Bad Request | Password policy complexity check failed. |
| `TSX-AUTH-009` | 400 Bad Request | Request payload or query validation error. |
| `TSX-AUTH-010` | 401 Unauthorized | Authentication token missing or invalid. |
| `TSX-AUTH-011` | 403 Forbidden | Role-based access control (RBAC) forbidden. |
| `TSX-AUTH-999` | 500 Internal Error | Unhandled server error. |

---

## 3. Security Headers Middleware
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- `Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none';`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains` (Enforced in Production)

---

## 4. Reporting Vulnerabilities
If you discover a security vulnerability in TruthShield X, please report it via encrypted security email to `security@truthshield.gov.in`.
