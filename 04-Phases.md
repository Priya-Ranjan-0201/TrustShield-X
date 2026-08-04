# TruthShield X
# Development Roadmap & Execution Plan
## Document: 04-Phases.md
**Version:** 1.0 (Unified Master Execution Plan)  
**Status:** Approved Technical Execution Roadmap  
**Target Milestone:** Smart India Hackathon (SIH) 2026 & Production Release v1.0  
**Execution Strategy:** AI-First, Microservice-Driven, Incremental Phase-by-Phase Delivery

---

# Document Overview

This document defines the authoritative 25-phase execution plan and sprint roadmap for **TruthShield X**. The development workflow follows a strict incremental strategy: every phase requires a complete, testable, and documented deliverable before advancing to subsequent phases.

All execution tasks must comply strictly with the functional specifications in [PRD.md](file:///c:/Users/PRIYE%20RANJAN/OneDrive/Desktop/PROJECTS/TrustShield%20X/PRD.md), the microservice specifications in [02-Architecture.md](file:///c:/Users/PRIYE%20RANJAN/OneDrive/Desktop/PROJECTS/TrustShield%20X/02-Architecture.md), and the quality standards in [03-Rules.md](file:///c:/Users/PRIYE%20RANJAN/OneDrive/Desktop/PROJECTS/TrustShield%20X/03-Rules.md).

---

# Table of Contents

1. Core Execution Principles & Delivery Standards
2. Master Dependency Graph & Phase Sequencing
3. Phase 0 — Project Infrastructure & Initialization
4. Phase 1 — Authentication & User Management Service
5. Phase 2 — Frontend Component Library & Dashboard Shell
6. Phase 3 — Backend API Gateway & Core Middleware
7. Phase 4 — Unified Scan Engine & Auto-Classifier Router
8. Phase 5 — Centralized AI Gateway Service
9. Phase 6 — Website Phishing & Brand Impersonation AI Module
10. Phase 7 — QR Code & Financial UPI Verification AI Module
11. Phase 8 — Email & SMS Phishing NLP AI Module
12. Phase 9 — Deepfake Vision AI Module (Image & Video)
13. Phase 10 — Audio & Voice Cloning AI Module
14. Phase 11 — Document Forgery & Identity Inspection AI Module
15. Phase 12 — Fake APK & Mobile Malware Inspection Module
16. Phase 13 — Fake News & Misinformation Verification Module
17. Phase 14 — Fake Recruiter & Job Offer Fraud Module
18. Phase 15 — Risk Aggregation & Trust Score Engine
19. Phase 16 — Explainable AI (XAI) Rationale Engine
20. Phase 17 — Threat Intelligence & Knowledge Graph Service
21. Phase 18 — Interactive Threat Analytics Dashboard
22. Phase 19 — Real-Time Browser Extension (Manifest V3)
23. Phase 20 — Native Android Mobile Security Suite
24. Phase 21 — Real-Time Notification Service
25. Phase 22 — Security Hardening & DPDP Privacy Audit
26. Phase 23 — End-to-End Quality Assurance & AI Benchmarking
27. Phase 24 — Cloud Infrastructure Deployment (K8s / Docker)
28. Phase 25 — Production Release v1.0 & Public Launch
29. Master Timeline, Sprint Schedule & SIH Hackathon Fast-Track
30. Definition of Done (DoD) & Phase Sign-Off Protocol

---

# 1. Core Execution Principles & Delivery Standards

1. **Single-Feature Completeness:** Build, integrate, and test one microservice feature completely before commencing subsequent features.
2. **Mandatory Automated Verification:** Every phase must achieve $\ge 80\%$ test coverage and pass automated unit/integration test suites before phase sign-off.
3. **Continuous Documentation & Memory Updates:** Every phase completion requires updating `docs/Memory.md` and OpenAPI documentation.
4. **Strict Rules Adherence:** Implementation must strictly obey the coding standards, security constraints, and response envelope rules in `03-Rules.md`.
5. **No Speculative Schema Drift:** Database tables, Pydantic DTOs, and TypeScript interfaces must match `02-Architecture.md` schemas.

---

# 2. Master Dependency Graph & Phase Sequencing

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PHASE 0: INITIALIZATION                         │
│       Monorepo, Docker, Postgres, Redis, Neo4j, Qdrant, MinIO          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      PHASE 1: AUTHENTICATION SERVICE                   │
│                JWT, Refresh Cookies, Argon2id, RBAC Roles              │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
                    ▼                                ▼
┌───────────────────────────────┐ ┌──────────────────────────────────────┐
│  PHASE 2: FRONTEND FOUNDATION │ │ PHASE 3: BACKEND GATEWAY & MIDDLEWARE│
│ React 19, Tailwind, ShadCN UI │ │  NGINX / FastAPI, Rate Limit, WAF    │
└───────────────┬───────────────┘ └──────────────────┬───────────────────┘
                │                                    │
                └───────────────────┬────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 PHASE 4: UNIFIED SCAN ENGINE ROUTER                    │
│             MIME Inspection, Storage Purging, Async Queues             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   PHASE 5: CENTRALIZED AI GATEWAY                      │
│             Model Registry, GPU Scheduler, ONNX Fallback               │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
┌──────────────┐             ┌──────────────┐             ┌──────────────┐
│ PHASES 6 - 8 │             │PHASES 9 - 11 │             │PHASES 12 - 14│
│ Web, QR, NLP │             │ Vision, Audio│             │ APK, News, HR│
└──────┬───────┘             └──────┬───────┘             └──────┬───────┘
       │                            │                            │
       └────────────────────────────┼────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│              PHASE 15 & 16: RISK ENGINE & EXPLAINABLE AI               │
│          Digital Trust Score (0-100) & Evidence Summary Rationale       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│          PHASE 17 & 18: THREAT INTELLIGENCE & ANALYTICS MAP            │
│                 Neo4j Scam Graph & Interactive Heatmap                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
       ┌────────────────────────────┴────────────────────────────┐
       ▼                                                         ▼
┌───────────────────────────────┐             ┌──────────────────────────┐
│  PHASE 19: BROWSER EXTENSION  │             │ PHASE 20: ANDROID SUITE  │
│ Manifest V3 Real-Time Guard   │             │ Camera QR, SMS Watcher   │
└───────────────┬───────────────┘             └──────────┬───────────────┘
                │                                        │
                └───────────────────┬────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             PHASES 21 - 25: SECURITY, QA, DEPLOYMENT & RELEASE         │
│     Security Hardening, K8s Deployment, SIH 2026 Production Launch   │
└────────────────────────────────────────────────────────────────────────┘
```

---

# 3. Phase-by-Phase Technical Specifications

## Phase 0 — Project Infrastructure & Initialization
- **Objective:** Establish the complete monorepo, containerized development environment, databases, and CI/CD pipelines.
- **Tasks:**
  - Initialize Git monorepo structure (`/apps`, `/backend`, `/ai-services`, `/infrastructure`, `/packages`).
  - Configure `docker-compose.yml` orchestrating PostgreSQL 16, Redis, Neo4j, Qdrant, MinIO, and RabbitMQ.
  - Setup core environment configs (`.env.example`) and HashiCorp Vault secrets interface.
  - Setup GitHub Actions CI workflow for automated linting (`ruff`, `eslint`) and type-checking.
- **Exit Criteria:** All database containers start cleanly; `docker-compose up` passes health checks; CI pipeline executes successfully.

---

## Phase 1 — Authentication & User Management Service
- **Objective:** Deliver enterprise authentication, user management, and Role-Based Access Control (RBAC).
- **Tasks:**
  - Build `auth-service` using FastAPI, SQLAlchemy 2.0 async, and Alembic migrations.
  - Implement Argon2id password hashing, email/phone verification, and Google OAuth2 integration.
  - Implement JWT access token issuing (15-min) and HttpOnly refresh token rotation (7-day).
  - Enforce RBAC middleware for `CITIZEN`, `BUSINESS`, `ANALYST`, and `ADMIN` roles.
- **Exit Criteria:** Unit tests pass ($\ge 85\%$ coverage); protected endpoints reject unauthorized requests with HTTP 401/403.

---

## Phase 2 — Frontend Component Library & Dashboard Shell
- **Objective:** Construct the modern React 19 web application architecture and reusable design system.
- **Tasks:**
  - Scaffold `apps/web` using React 19, TypeScript, Vite, Tailwind CSS, and ShadCN UI.
  - Configure Zustand global client store and TanStack Query server data provider.
  - Build core navigation shell (Header, Sidebar, User Profile Menu, Theme Manager).
  - Implement Dark Mode aesthetic (Cyber Charcoal `#0F172A`, Cyan `#06B6D4` accents).
- **Exit Criteria:** Responsive UI layout renders under 1.5 seconds across mobile and desktop viewports.

---

## Phase 3 — Backend API Gateway & Core Middleware
- **Objective:** Deploy the single public API Gateway managing request routing, authentication, and security policies.
- **Tasks:**
  - Implement API Gateway using NGINX / FastAPI Gateway wrapper.
  - Configure rate-limiting middleware (100 req/min free, 500 req/min business).
  - Enforce global CORS, TLS 1.3 termination, and secure HTTP response headers.
  - Setup correlation `traceId` propagation across all downstream requests.
- **Exit Criteria:** Gateway routes requests to downstream microservices with sub-150ms latency overhead.

---

## Phase 4 — Unified Scan Engine & Auto-Classifier Router
- **Objective:** Build the automated artifact intake, classification, and routing microservice.
- **Tasks:**
  - Build `scan-service` supporting file, URL, text, and QR byte ingestion up to 500 MB.
  - Implement deterministic MIME/magic-number auto-classifier routing inputs to target AI microservices.
  - Integrate ClamAV anti-malware inspection and MinIO encrypted object storage.
  - Enforce DPDP compliance automated 30-day file purging worker.
- **Exit Criteria:** Auto-classifier routes URLs, PDFs, PNGs, and audio clips to correct service queues with >99.9% accuracy.

---

## Phase 5 — Centralized AI Gateway Service
- **Objective:** Build the AI model orchestration control plane.
- **Tasks:**
  - Implement `ai-gateway` service managing ONNX Runtime and PyTorch inference sessions.
  - Build GPU VRAM scheduler and dynamic request batching queue.
  - Enforce automated CPU ONNX Runtime fallback if GPU VRAM exceeds 95%.
  - Log model inference latency (`ai_inference_latency_ms`) for telemetry.
- **Exit Criteria:** AI Gateway successfully loads model weights and handles CPU failover cleanly during simulated GPU overload.

---

## Phase 6 — Website Phishing & Brand Impersonation AI Module
- **Objective:** Implement domain inspection and visual brand cloning detection.
- **Tasks:**
  - Build `website-ai` service using Playwright for headless 1080p webpage screenshot capture.
  - Implement WHOIS domain age inspection (<30 days flag), SSL certificate checks, and DNS reputation checks.
  - Deploy Vision Transformer (ViT) comparing webpage screenshot layout against authentic bank/portal reference assets.
- **Exit Criteria:** Accurately flags spoofed domains (e.g., `sbi-netbanking-update.xyz`) with >95% confidence under 5 seconds.

---

## Phase 7 — QR Code & Financial UPI Verification AI Module
- **Objective:** Detect payment scam QR codes and deceptive UPI Virtual Payment Addresses (VPAs).
- **Tasks:**
  - Build `qr-ai` service utilizing OpenCV and ZXing for QR matrix extraction.
  - Implement `upi://pay` URI parser extracting Merchant VPA and payee name.
  - Cross-reference VPAs against Redis blacklists and active user scam reports.
- **Exit Criteria:** Decodes damaged/distorted QR codes and flags fraudulent VPAs in <2.5 seconds.

---

## Phase 8 — Email & SMS Phishing NLP AI Module
- **Objective:** Detect text-based phishing, SMS fraud, and urgent scam offers.
- **Tasks:**
  - Build `nlp-ai` service deploying DeBERTa / RoBERTa Transformer models.
  - Implement email header parser checking SPF, DKIM, DMARC records.
  - Extract coercive urgency language, credential harvesting prompts, and financial extortion attempts.
- **Exit Criteria:** Categorizes text intent (Phishing, Extortion, Safe) with >94% precision.

---

## Phase 9 — Deepfake Vision AI Module (Image & Video)
- **Objective:** Detect synthetic image manipulations and video face-swaps.
- **Tasks:**
  - Build `deepfake-ai` vision service employing Spatial-Temporal 3D-CNNs and MesoNet models.
  - Implement Image GAN/Diffusion frequency noise anomaly detector.
  - Implement Video frame lip-sync correlation, eye blink frequency, and face seam line inspector.
- **Exit Criteria:** Detects video face-swaps on 1080p 30-second clips in <30 seconds.

---

## Phase 10 — Audio & Voice Cloning AI Module
- **Objective:** Detect synthetic neural voice cloning and transcribe call fraud.
- **Tasks:**
  - Build `audio-ai` service integrating Whisper ASR for multi-lingual speech-to-text transcription.
  - Deploy Wav2Vec / ResMFCC model analyzing voice spectral anomalies and ElevenLabs voice signatures.
  - Implement conversational scam intent extraction on call transcripts.
- **Exit Criteria:** Detects synthetic cloned voice audio clips with >92% accuracy.

---

## Phase 11 — Document Forgery & Identity Inspection AI Module
- **Objective:** Validate identity documents (Aadhaar, PAN, DL) and inspect PDF scripts.
- **Tasks:**
  - Build `document-ai` service using PaddleOCR for alphanumeric field extraction.
  - Implement structural template checks, micro-print alignment, and Aadhaar 12-digit Verhoeff checksum validation.
  - Inspect PDF structures for digital signature tampering and hidden JavaScript payloads.
- **Exit Criteria:** Flags photo overlays, altered text fields, and invalid Aadhaar checksums in <6 seconds.

---

## Phase 12 — Fake APK & Mobile Malware Inspection Module
- **Objective:** Perform static and dynamic inspection of Android binaries (.apk).
- **Tasks:**
  - Implement APK static analyzer extracting `AndroidManifest.xml` permissions, API keys, and certificate signatures.
  - Flag over-privileged permissions (SMS reading + Accessibility + Background Recording).
  - Execute dynamic sandbox behavioral analysis inside Android emulator container.
- **Exit Criteria:** Generates threat alerts for trojanned APKs attempting background data exfiltration.

---

## Phase 13 — Fake News & Misinformation Verification Module
- **Objective:** Fact-check news claims against knowledge bases and trusted sources.
- **Tasks:**
  - Build claim extraction pipeline parsing input news text and social media screenshots.
  - Query trusted fact-checking knowledge bases and news API feeds.
  - Assign truth rating (Verified, Misleading, Unverified, False) with citation sources.
- **Exit Criteria:** Outputs claim rating with supporting reference links.

---

## Phase 14 — Fake Recruiter & Job Offer Fraud Module
- **Objective:** Protect job seekers from recruitment extortion scams.
- **Tasks:**
  - Build recruiter credibility profiler cross-referencing sender email domains and LinkedIn profile handles.
  - Parse offer letter PDFs for advance fee clauses, registration demands, and invalid corporate IDs.
- **Exit Criteria:** Identifies fake recruiters using free email handles (`company-hr@gmail.com`) claiming MNC affiliation.

---

## Phase 15 — Risk Aggregation & Trust Score Engine
- **Objective:** Synthesize multi-detector outputs into a single **Digital Trust Score (0–100)**.
- **Tasks:**
  - Implement `risk-engine` applying weighted risk fusion matrix ($\text{Risk Score} = \sum W_i S_i$).
  - Normalize scores and compute Digital Trust Score ($100 \times (1 - \text{Risk Score})$).
  - Categorize risk levels: Trusted (90-100), Low Risk (70-89), Medium Risk (50-69), High Risk (30-49), Dangerous (0-29).
- **Exit Criteria:** Consolidated Trust Score calculation completes in <200ms following detector outputs.

---

## Phase 16 — Explainable AI (XAI) Rationale Engine
- **Objective:** Generate human-readable evidence explanations for every score.
- **Tasks:**
  - Build `explainability` service formatting detector evidence into structured JSON XAI cards.
  - Generate headline, severity-rated key evidence factors, and actionable remediation steps.
- **Exit Criteria:** Every scan result displays clear evidence points without technical jargon.

---

## Phase 17 — Threat Intelligence & Knowledge Graph Service
- **Objective:** Build national scam knowledge graph and anonymized threat network.
- **Tasks:**
  - Implement `threat-service` managing Neo4j graph nodes (`Domain`, `IP`, `VPA`, `Phone`, `APKHash`).
  - Store visual screenshot embeddings in Qdrant Vector DB for similarity matching.
  - Aggregate anonymized citizen threat reports into regional scam trend statistics.
- **Exit Criteria:** Real-time graph queries return entity relationship links in <100ms.

---

## Phase 18 — Interactive Threat Analytics Dashboard
- **Objective:** Deliver institutional threat visualization portal for security analysts and government agencies.
- **Tasks:**
  - Build interactive Threat Analytics Dashboard in React 19.
  - Implement regional scam heatmaps of India filterable by state, threat category, and time range.
  - Export executive threat summary reports in PDF and CSV formats.
- **Exit Criteria:** Heatmap visualizer updates dynamically with sub-2s initial load time.

---

## Phase 19 — Real-Time Browser Extension (Manifest V3)
- **Objective:** Provide real-time web navigation security for Chrome/Edge/Firefox.
- **Tasks:**
  - Develop browser extension using Manifest V3 (Background Service Worker + Content Script).
  - Implement local Bloom filter and API Gateway URL reputation lookup (<300ms).
  - Display floating Trust Score badge and full-page blocking overlay for dangerous phishing sites.
- **Exit Criteria:** Extension blocks confirmed phishing domains seamlessly without slowing browser performance.

---

## Phase 20 — Native Android Mobile Security Suite
- **Objective:** Deploy native mobile application for on-device citizen defense.
- **Tasks:**
  - Develop native Android app following MVVM clean architecture.
  - Implement camera QR scanner, background SMS link watcher, call recorder assistant, and AI Chat UI.
- **Exit Criteria:** Mobile app operates cleanly with <2% background battery consumption per day.

---

## Phase 21 — Real-Time Notification Service
- **Objective:** Dispatch instant alerts for high-risk threats and system updates.
- **Tasks:**
  - Build `notification-service` consuming RabbitMQ event bus messages (`scan.completed`, `threat.alert`).
  - Integrate Firebase Cloud Messaging (Push), Twilio (SMS), and SendGrid (Email).
- **Exit Criteria:** Sends push notifications to mobile clients within 3 seconds of high-risk scan completion.

---

## Phase 22 — Security Hardening & DPDP Privacy Audit
- **Objective:** Conduct security penetration testing and data protection audit.
- **Tasks:**
  - Conduct static security analysis (SAST) and dependency vulnerability scans (Snyk/Trivy).
  - Validate Zero-Trust mTLS configuration, JWT token security, and OWASP Top 10 mitigations.
  - Verify automated 30-day file purging lifecycle in MinIO storage.
- **Exit Criteria:** Zero critical/high vulnerabilities; full DPDP 2023 compliance audit verification.

---

## Phase 23 — End-to-End Quality Assurance & AI Benchmarking
- **Objective:** Execute full system regression tests and AI model performance benchmarks.
- **Tasks:**
  - Execute end-to-end API test suites achieving $\ge 80\%$ backend code coverage.
  - Benchmark AI detection performance on held-out test datasets (Target: Precision $\ge 95\%$, Recall $\ge 93\%$).
  - Perform load testing with Locust simulating 10,000+ concurrent requests.
- **Exit Criteria:** All automated test suites pass cleanly under simulated peak load.

---

## Phase 24 — Cloud Infrastructure Deployment (K8s / Docker)
- **Objective:** Deploy platform to cloud Kubernetes cluster (EKS/GKE/On-Premise).
- **Tasks:**
  - Deploy Kubernetes manifests (Helm Charts, Ingress Controllers, HPA Horizontal Pod Autoscalers).
  - Provision Prometheus & Grafana monitoring dashboards and ELK logging stack.
  - Configure multi-region database failover and automated backup tasks.
- **Exit Criteria:** Kubernetes cluster auto-scales pods based on load spikes; health probes confirm 100% readiness.

---

## Phase 25 — Production Release v1.0 & Public Launch
- **Objective:** Launch TruthShield X v1.0 for Smart India Hackathon 2026 and public deployment.
- **Tasks:**
  - Finalize production DNS records, SSL certificates, and public developer API documentation.
  - Execute final deployment verification tests and operational sign-off.
  - Publish Android App APK to Google Play Store and Extension to Web Store.
- **Exit Criteria:** Platform is fully operational live at 99.9% uptime availability.

---

# 4. Master Timeline, Sprint Schedule & SIH Hackathon Fast-Track

```
Sprint 1 (W1-W2)   : Phase 0 (Setup), Phase 1 (Auth), Phase 2 (Frontend Shell), Phase 3 (Gateway)
Sprint 2 (W3-W4)   : Phase 4 (Scan Engine), Phase 5 (AI Gateway), Phase 6 (Website AI), Phase 7 (QR AI)
Sprint 3 (W5-W6)   : Phase 8 (NLP Email/SMS), Phase 9 (Deepfake Vision AI), Phase 11 (Document OCR)
Sprint 4 (W7-W8)   : Phase 15 (Risk Engine), Phase 16 (XAI Engine), Phase 18 (Analytics Dashboard)
                     ========================================================================
                     🏆 SIH 2026 HACKATHON MVP DELIVERABLE COMPLETED & DEMO-READY (END OF WEEK 8)
                     ========================================================================
Sprint 5 (W9-W10)  : Phase 10 (Audio AI), Phase 12 (APK Sandbox), Phase 17 (Threat Graph DB)
Sprint 6 (W11-W12) : Phase 19 (Extension), Phase 20 (Android App), Phase 21 (Notifications)
Sprint 7 (W13-W14) : Phase 22 (Security), Phase 23 (QA & Benchmarks), Phase 24 (K8s), Phase 25 (Release v1.0)
```

---

# 5. Definition of Done (DoD) & Phase Sign-Off Protocol

A Phase is officially marked **CLOSED & SIGNED OFF** only when:

- ✅ All phase-specific technical tasks and features are 100% implemented.
- ✅ Unit & Integration tests achieve $\ge 80\%$ line coverage and pass CI/CD checks.
- ✅ Security review confirms zero unhandled vulnerabilities or plain-text secrets.
- ✅ OpenAPI endpoints are documented with Pydantic schemas and standard JSON envelopes.
- ✅ Structured JSON logging with `traceId` correlation is verified.
- ✅ `docs/Memory.md` is updated with phase architectural decisions and state.
- ✅ Technical Sign-off is approved by Product Owner and Lead Architect.

---
**[ END OF MASTER EXECUTION ROADMAP v1.0 ]**
