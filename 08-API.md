# TruthShield X
# API Specification Document
## Document: 08-API.md
**Version:** 1.0 (Unified Master API Specification)  
**Status:** Approved Mandatory REST & WebSocket API Standard  
**Base URL (Dev):** `http://localhost:8000/api/v1`  
**Base URL (Prod):** `https://api.truthshieldx.gov.in/api/v1`  
**Protocol:** HTTPS / TLS 1.3 / WSS (WebSockets)

---

# Document Overview

This document defines the complete RESTful and WebSocket API Specification for **TruthShield X**.

All client platforms (Web App, Android Mobile Suite, Browser Extension, Institutional Dashboards) and external enterprise integrations interact with TruthShield X microservices strictly through the endpoints specified in this document.

---

# Table of Contents

1. API Architecture Principles & Security Standard
2. Standard Request & Response Envelopes
3. Error Code Catalog (`TSX-xxxx`)
4. Module 1 — Authentication & Session APIs
5. Module 2 — User Profile & Settings APIs
6. Module 3 — Unified Scan Engine APIs (Core Intake)
7. Module 4 — Specialized AI Detection Endpoint Modules
   - 7.1 Website Phishing & Brand Impersonation API
   - 7.2 QR Code & UPI Risk Verification API
   - 7.3 Email Phishing NLP API
   - 7.4 SMS Scam Detection API
   - 7.5 Deepfake Vision API (Image & Video)
   - 7.6 Audio & Voice Clone API
   - 7.7 Document OCR & Forgery API (Aadhaar/PAN/DL)
   - 7.8 Fake APK Inspection API
   - 7.9 Fake News & Misinformation API
   - 7.10 Fake Recruiter & Job Fraud API
8. Module 5 — Risk Aggregation & XAI Rationale APIs
9. Module 6 — Threat Intelligence & Heatmap APIs
10. Module 7 — Verification Report Generation APIs
11. Module 8 — Real-Time WebSocket Event Protocol
12. Module 9 — Microservice Health & Readiness APIs
13. Module 10 — Administrative & AI Governance APIs
14. Pagination, Filtering, Sorting & Rate Limits

---

# 1. API Architecture Principles & Security Standard

- **RESTful First:** Standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`) with plural resource URIs (`/scans`, `/users`, `/reports`).
- **Strict Versioning:** URI path versioning mandatory (`/api/v1/...`).
- **JWT Authentication:** All protected endpoints require a valid Bearer token header: `Authorization: Bearer <JWT_ACCESS_TOKEN>`.
- **JSON Payload Format:** Request and response bodies use UTF-8 JSON payloads.
- **Pydantic Validation:** Every backend endpoint validates incoming JSON against explicit Pydantic schemas.
- **Rate Limiting:** Enforced at the Gateway per user/IP (100 req/min free citizens, 500 req/min business API keys).

---

# 2. Standard Request & Response Envelopes

Every API endpoint returns a standardized JSON response structure.

## Success Response Envelope (HTTP 200 / 201 / 202)

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": {},
  "meta": {
    "traceId": "req_8f92c1d34e5a",
    "timestamp": "2026-08-04T14:52:00Z"
  }
}
```

## Error Response Envelope (HTTP 4xx / 5xx)

```json
{
  "success": false,
  "error": {
    "code": "TSX-2001",
    "message": "Resource validation failed.",
    "details": "The submitted URL contains an invalid domain structure.",
    "traceId": "req_8f92c1d34e5a"
  }
}
```

---

# 3. Error Code Catalog (`TSX-xxxx`)

| Error Code | Category | HTTP Status | Description |
|---|---|---|---|
| **TSX-1001** | Auth | `401 Unauthorized` | Invalid email or password credentials. |
| **TSX-1002** | Auth | `401 Unauthorized` | Expired or malformed JWT access token. |
| **TSX-1003** | Auth | `403 Forbidden` | Insufficient role permissions for target resource. |
| **TSX-2001** | Validation | `400 Bad Request` | Request payload schema validation failure. |
| **TSX-2002** | Validation | `422 Unprocessable` | Unsupported file format or file size > 500 MB. |
| **TSX-3001** | Scan Router | `404 Not Found` | Target `scanId` does not exist in registry. |
| **TSX-3002** | Scan Router | `409 Conflict` | Scan task has already finished or failed. |
| **TSX-4001** | AI Gateway | `503 Unavailable` | Target AI microservice or GPU worker is offline. |
| **TSX-4002** | AI Gateway | `504 Gateway Timeout` | AI model inference exceeded SLA timeout. |
| **TSX-5001** | Database | `500 Internal Error` | Database transaction error or connection pool failure. |
| **TSX-8001** | Rate Limit | `429 Too Many Requests` | Request rate limit threshold exceeded. |

---

# 4. Module 1 — Authentication & Session APIs

## 4.1 Register User
- **HTTP Method:** `POST`
- **Path:** `/api/v1/auth/register`
- **Auth:** Public
- **Request Body:**

```json
{
  "fullName": "Priya Ranjan",
  "email": "user@example.com",
  "password": "Password@1234",
  "phoneNumber": "+919876543210"
}
```

- **Success Response (HTTP 201 Created):**

```json
{
  "success": true,
  "message": "User account created successfully.",
  "data": {
    "userId": "9b1deb4d-3b7d-4149-9d28-79e43b339d57",
    "email": "user@example.com",
    "role": "CITIZEN"
  }
}
```

## 4.2 User Login
- **HTTP Method:** `POST`
- **Path:** `/api/v1/auth/login`
- **Auth:** Public
- **Request Body:**

```json
{
  "email": "user@example.com",
  "password": "Password@1234"
}
```

- **Success Response (HTTP 200 OK):** Sets HttpOnly Refresh Cookie (`tsx_refresh_token`).

```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
    "tokenType": "Bearer",
    "expiresInSeconds": 900,
    "user": {
      "userId": "9b1deb4d-3b7d-4149-9d28-79e43b339d57",
      "fullName": "Priya Ranjan",
      "email": "user@example.com",
      "role": "CITIZEN"
    }
  }
}
```

## 4.3 Refresh Access Token
- **HTTP Method:** `POST`
- **Path:** `/api/v1/auth/refresh`
- **Auth:** Refresh Token Cookie Required
- **Success Response (HTTP 200 OK):** Returns new signed JWT access token.

## 4.4 User Logout
- **HTTP Method:** `POST`
- **Path:** `/api/v1/auth/logout`
- **Auth:** Bearer Token Required
- **Success Response (HTTP 200 OK):** Blacklists active JWT JTI in Redis and clears HttpOnly refresh cookie.

---

# 5. Module 2 — User Profile & Settings APIs

## 5.1 Get Current User Profile
- **HTTP Method:** `GET`
- **Path:** `/api/v1/users/me`
- **Auth:** Bearer Token Required
- **Success Response (HTTP 200 OK):** Returns user details, role permissions, and scan statistics summary.

## 5.2 Update User Profile
- **HTTP Method:** `PUT`
- **Path:** `/api/v1/users/me`
- **Auth:** Bearer Token Required
- **Request Body:** `{ "fullName": "Priya Ranjan", "phoneNumber": "+919876543210" }`

## 5.3 Delete Account (DPDP Erasure)
- **HTTP Method:** `DELETE`
- **Path:** `/api/v1/users/me`
- **Auth:** Bearer Token Required
- **Success Response (HTTP 200 OK):** Immediately purges user data and revokes all active sessions.

---

# 6. Module 3 — Unified Scan Engine APIs (Core Intake)

## 6.1 Upload & Auto-Classify Artifact
- **HTTP Method:** `POST`
- **Path:** `/api/v1/scan`
- **Auth:** Bearer Token Optional (Supports Anonymous Free Scans)
- **Content-Type:** `multipart/form-data` or `application/json`
- **Request Payload:** Accepts file upload (`file`), URL string (`url`), or text payload (`text`).
- **Success Response (HTTP 202 Accepted):**

```json
{
  "success": true,
  "message": "Artifact accepted and auto-classified. Scan processing initiated.",
  "data": {
    "scanId": "c4259e7a-cf65-4ac7-a07d-39c06ede42a9",
    "detectedType": "URL",
    "status": "PROCESSING",
    "estimatedTimeSeconds": 4
  }
}
```

## 6.2 Get Scan Status & Digital Trust Score Result
- **HTTP Method:** `GET`
- **Path:** `/api/v1/scan/{scanId}`
- **Auth:** Optional
- **Success Response (HTTP 200 OK):**

```json
{
  "success": true,
  "message": "Scan execution complete.",
  "data": {
    "scanId": "c4259e7a-cf65-4ac7-a07d-39c06ede42a9",
    "status": "COMPLETED",
    "artifactType": "URL",
    "trustScore": 14,
    "riskLevel": "DANGEROUS",
    "executionTimeMs": 3420,
    "xaiSummary": {
      "headline": "High Risk Phishing Portal Impersonating State Bank of India",
      "confidence": 0.96,
      "keyEvidence": [
        {
          "factor": "Domain Age",
          "severity": "CRITICAL",
          "description": "Domain registered 2 days ago."
        },
        {
          "factor": "Brand Impersonation",
          "severity": "CRITICAL",
          "description": "Page visually clones official SBI logo on an unauthorized domain."
        }
      ],
      "recommendations": [
        "Do NOT enter passwords, OTPs, or financial info.",
        "Report link immediately via official bank portal."
      ]
    }
  }
}
```

## 6.3 List Scan History
- **HTTP Method:** `GET`
- **Path:** `/api/v1/scan/history?page=1&limit=20&type=URL`
- **Auth:** Bearer Token Required
- **Success Response (HTTP 200 OK):** Returns paginated scan history list.

---

# 7. Specialized AI Detection Endpoint Modules

## 7.1 Website Phishing Inspection
- **POST** `/api/v1/scan/website` → `{ "url": "https://sbi-update.xyz" }`

## 7.2 QR Code & UPI Risk Verification
- **POST** `/api/v1/scan/qr` → Accepts QR Image file upload or parsed UPI string (`upi://pay?...`).

## 7.3 Email Phishing NLP Inspection
- **POST** `/api/v1/scan/email` → Accepts `.eml` / `.msg` file upload or raw email header text.

## 7.4 SMS Scam Detection
- **POST** `/api/v1/scan/sms` → `{ "smsText": "Your bank account is blocked. Click http://bit.ly/123 to unblock" }`

## 7.5 Deepfake Media Inspection (Image & Video)
- **POST** `/api/v1/scan/deepfake/image` → Upload `.png` / `.jpg` image for GAN noise check.
- **POST** `/api/v1/scan/deepfake/video` → Upload `.mp4` video clip for 3D-CNN face-swap check.

## 7.6 Audio & Voice Clone Analysis
- **POST** `/api/v1/scan/audio` → Upload `.mp3` / `.wav` call clip for voice clone & ASR transcript fraud check.

## 7.7 Document Forgery & Identity Inspection
- **POST** `/api/v1/scan/document` → Upload Aadhaar / PAN / DL image or PDF for OCR structure inspection.

## 7.8 Fake APK Inspection
- **POST** `/api/v1/scan/apk` → Upload `.apk` binary file for permission manifest & malware sandbox check.

## 7.9 Fake News & Misinformation Fact-Check
- **POST** `/api/v1/scan/news` → `{ "claimText": "Government offering free 5G smartphones to all citizens." }`

## 7.10 Fake Recruiter & Job Offer Fraud
- **POST** `/api/v1/scan/recruiter` → Upload offer letter PDF or recruiter email handle for verification.

---

# 8. Module 5 — Risk Aggregation & XAI Rationale APIs

## 8.1 Re-evaluate Risk Aggregation
- **HTTP Method:** `POST`
- **Path:** `/api/v1/risk/evaluate`
- **Auth:** Internal / Admin
- **Request Body:** `{ "scanId": "c4259e7a...", "detectorOutputs": [...] }`
- **Success Response:** Computes score using weighted fusion formula $\sum W_i S_i$.

---

# 9. Module 6 — Threat Intelligence & Heatmap APIs

## 9.1 Query Threat Graph Entities
- **HTTP Method:** `GET`
- **Path:** `/api/v1/threats?query=sbi-update.xyz`
- **Auth:** Bearer Token Required
- **Success Response (HTTP 200 OK):** Returns graph entity nodes (Domain, IP, VPA, Phone, ScamCampaign).

## 9.2 Get Regional Scam Heatmap Data
- **HTTP Method:** `GET`
- **Path:** `/api/v1/threats/map?state=MAHARASHTRA&category=UPI`
- **Auth:** Optional
- **Success Response (HTTP 200 OK):** Returns geo-coordinate heat clusters of reported threat trends across India.

---

# 10. Module 7 — Verification Report Generation APIs

## 10.1 Export Verification Certificate PDF
- **HTTP Method:** `GET`
- **Path:** `/api/v1/reports/{scanId}/pdf`
- **Auth:** Optional
- **Success Response (HTTP 200 OK):** Downloads formatted executive PDF report (`TruthShieldX_ScanReport_<scanId>.pdf`).

---

# 11. Module 8 — Real-Time WebSocket Event Protocol

- **WebSocket Connection URI:** `wss://api.truthshieldx.gov.in/ws/v1/scans?token=<JWT>`

## Server-to-Client Event Payloads

```json
{
  "event": "scan.progress",
  "data": {
    "scanId": "c4259e7a-cf65-4ac7-a07d-39c06ede42a9",
    "percentage": 65,
    "currentStage": "Analyzing Video Lip Sync Alignment"
  }
}
```

```json
{
  "event": "scan.completed",
  "data": {
    "scanId": "c4259e7a-cf65-4ac7-a07d-39c06ede42a9",
    "trustScore": 14,
    "riskLevel": "DANGEROUS"
  }
}
```

---

# 12. Module 9 — Microservice Health & Readiness APIs

- **`GET /healthz`** → Liveness check (HTTP 200 OK if process is running).
- **`GET /readyz`** → Readiness check (HTTP 200 OK if PostgreSQL, Redis, and AI services are connected).

---

# 13. Module 10 — Administrative & AI Governance APIs

- **`GET /api/v1/admin/ai/models`** → Returns active deployed AI model registry versions.
- **`POST /api/v1/admin/alerts`** → Broadcasts national cyber threat alert to regional users.

---

# 14. Pagination, Filtering, Sorting & Rate Limits

- **Pagination Params:** `?page=1&limit=20` (Default `limit=20`, max `limit=100`).
- **Filtering Params:** `?riskLevel=DANGEROUS&artifactType=URL`.
- **Sorting Params:** `?sort=created_at&order=desc`.
- **Rate Limit Headers Included in Responses:**
  - `X-RateLimit-Limit: 100`
  - `X-RateLimit-Remaining: 98`
  - `X-RateLimit-Reset: 1722783000`

---
**[ END OF MASTER API SPECIFICATION v1.0 ]**
