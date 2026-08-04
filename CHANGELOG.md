# TruthShield X — Changelog

All notable changes to the TruthShield X project will be documented in this file.

## [1.1.0] - 2026-08-04

### Added — Phase 1 Production Hardening
- **Email Verification Workflow**: Added `email_verifications` table, verification token generation, `/api/v1/auth/verify-email`, `/api/v1/auth/resend-verification` endpoints, and configurable login enforcement (`REQUIRE_EMAIL_VERIFICATION`).
- **User Session Tracking**: Added `user_sessions` table storing device name, browser, operating system, IP address, country, refresh token JTI, and session management APIs (`GET /users/sessions`, `DELETE /users/sessions/{id}`, `DELETE /users/sessions`).
- **Standardized Error Codes**: Introduced `TSX-AUTH-XXX` standardized error codes across all authentication and user management exception handlers.
- **API Response Envelope Metadata**: Added `meta` envelope block containing `traceId`, `timestamp`, and `version` (`v1`).
- **Startup Validation**: Implemented lifespan startup checks enforcing JWT secret key length and verifying PostgreSQL and Redis connection health.
- **Security Headers**: Added middleware setting `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, `Content-Security-Policy`, and `HSTS`.
- **Structured Logging**: Implemented JSON logging separating Application, Security, and Audit logs.
- **Active Sessions UI**: Added device sessions management section to React Profile Page.

## [1.0.0] - 2026-08-04

### Added — Phase 1 Initial Release
- Baseline PostgreSQL 16 schema with SQLAlchemy 2.0 async models (`User`, `Role`, `RefreshToken`, `AuditLog`, `PasswordResetToken`).
- Argon2id password hashing and top-10k password policy check.
- Redis-backed rate limiting and JWT JTI blacklisting.
- React 19 web application with Zustand in-memory store and Axios silent token refresh interceptor.
- Multistage Dockerfiles and docker-compose.yml orchestration.
