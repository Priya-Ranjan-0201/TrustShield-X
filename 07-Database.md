# TruthShield X
# Database Design & Data Architecture
## Document: 07-Database.md
**Version:** 1.0 (Unified Master Database Architecture)  
**Status:** Approved Technical Specification  
**Architecture Style:** Polyglot Persistence (PostgreSQL, Redis, Neo4j, Qdrant, MinIO)  
**Target Environment:** Cloud-Native Kubernetes / Docker Microservices

---

# Document Overview

This document defines the comprehensive Database Design, Schema Blueprints, Data Models, Indexing Strategies, Encryption Rules, and Storage Policies for **TruthShield X**.

TruthShield X uses a **Polyglot Persistence Strategy**, selecting specialized storage engines optimized for relational transactions, in-memory caching, graph relationship queries, high-dimensional vector search, and encrypted object storage.

---

# Table of Contents

1. Executive Data Architecture & Polyglot Strategy
2. Data Flow Pipeline Architecture
3. PostgreSQL 16 — Relational Schema Blueprint
   - 3.1 `users` & `roles` Tables
   - 3.2 `scans` & `scan_evidence` Tables
   - 3.3 `reports` & `notifications` Tables
   - 3.4 `audit_logs` & `organizations` Tables
   - 3.5 `threat_feeds` & `scam_campaigns` Tables
4. Redis Cluster — Cache & Session Data Schemas
5. Neo4j 5.x — Graph Database Cypher Schemas
6. Qdrant — Vector Search Collection Specifications
7. MinIO — Object Storage Bucket & Lifecycle Policies
8. Database Migration Protocol (Alembic)
9. Encryption, Privacy & DPDP Compliance Standards
10. Backup, Disaster Recovery & High Availability (RTO/RPO)
11. Naming Conventions & Indexing Rules

---

# 1. Executive Data Architecture & Polyglot Strategy

No single database management system efficiently supports user authentication, real-time rate limiting, complex graph threat queries, deep learning visual embeddings, and high-volume media storage.

TruthShield X pairs workload characteristics directly to specialized storage technologies:

```
                                  POLYGLOT PERSISTENCE ARCHITECTURE
                                                  │
      ┌──────────────────┬────────────────────────┼────────────────────────┬──────────────────┐
      ▼                  ▼                        ▼                        ▼                  ▼
┌───────────────┐ ┌───────────────┐      ┌───────────────┐        ┌───────────────┐  ┌───────────────┐
│ PostgreSQL 16 │ │ Redis Cluster │      │   Neo4j 5.x   │        │ Qdrant Vector │  │ MinIO Storage │
│ (Relational)  │ │ (Cache/Queues)│      │  (Scam Graph) │        │ (Embeddings)  │  │(Object Files) │
└───────┬───────┘ └───────┬───────┘      └───────┬───────┘        └───────┬───────┘  └───────┬───────┘
        │                 │                      │                        │                  │
        ▼                 ▼                      ▼                        ▼                  ▼
  User Accounts,   JWT Tokens,            Scam Networks,           Visual Page       Images, Video,
  Scan History,    Rate Limits,           VPA-Domain-Phone         Embeddings,       Audio Clips,
  Reports & Audit  Task Queues            Entity Links             News Vectors      PDF & APK Files
```

## Polyglot Database Allocation Matrix

| Database Engine | Purpose / Workload | Storage Characteristics | Performance Target |
|---|---|---|---|
| **PostgreSQL 16** | Relational Transactional | Users, Roles, Scan Registry, Reports, Audit Logs | Sub-10ms transactional queries |
| **Redis 7.x Cluster** | In-Memory Cache & State | JWT Blacklist, Rate Limits, Session State, OTPs | Sub-2ms key-value lookups |
| **Neo4j 5.x** | Graph Threat Network | Scam Campaigns, Domain-VPA-Phone Entity Links | Sub-50ms multi-hop traversals |
| **Qdrant Vector DB** | Similarity Search | Visual Screenshot & Audio Feature Embeddings | Sub-30ms HNSW vector search |
| **MinIO Storage** | S3-Compatible Object Store | Scanned Images, Videos, PDFs, APKs, Generated PDFs | Encrypted streaming uploads |

---

# 2. Data Flow Pipeline Architecture

```
User Intake (URL / File / QR / Text)
                │
                ▼
      [ API Gateway Validation ]
                │
                ▼
   [ MinIO Encrypted Upload ] ─── (Generates Storage Object URI)
                │
                ▼
     [ AI Gateway Inference ] ─── (Generates Feature Embeddings & Visual Vectors)
                │                         │
                ├─────────────────────────┼─────────────────────────┐
                ▼                         ▼                         ▼
     [ PostgreSQL Database ]       [ Qdrant Vector DB ]       [ Neo4j Graph DB ]
   (Stores Scan Metadata, Trust    (Stores Visual Feature    (Links Scam Entity
     Score & XAI Evidence)          Embedding Vectors)       Relationships & VPAs)
                │
                ▼
    [ Redis In-Memory Cache ] ─── (Caches Result for Subsequent Instant Lookups)
```

---

# 3. PostgreSQL 16 — Relational Schema Blueprint

All PostgreSQL tables use UUID primary keys (`UUIDv4`), strict foreign key constraints, UTC timestamps (`TIMESTAMP WITH TIME ZONE`), and modern index structures.

## 3.1 `users`, `roles` & `permissions` DDL

```sql
-- Enforce UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Roles Table
CREATE TABLE roles (
    role_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Users Table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id UUID NOT NULL REFERENCES roles(role_id) ON DELETE RESTRICT,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role_id);
```

## 3.2 `scans` & `scan_evidence` DDL

```sql
-- Scans Registry Table
CREATE TABLE scans (
    scan_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    artifact_type VARCHAR(50) NOT NULL, -- URL, IMAGE, VIDEO, AUDIO, PDF, APK, QR, TEXT
    artifact_hash VARCHAR(64) NOT NULL, -- SHA-256 Hash
    storage_path VARCHAR(512),         -- MinIO Object Reference
    trust_score INT CHECK (trust_score BETWEEN 0 AND 100),
    risk_level VARCHAR(20) NOT NULL,   -- TRUSTED, LOW_RISK, MEDIUM_RISK, HIGH_RISK, DANGEROUS
    status VARCHAR(20) NOT NULL DEFAULT 'PROCESSING', -- PROCESSING, COMPLETED, FAILED
    execution_time_ms INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Explainable AI (XAI) Evidence Table
CREATE TABLE scan_evidence (
    evidence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID NOT NULL REFERENCES scans(scan_id) ON DELETE CASCADE,
    detector_name VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,       -- CRITICAL, HIGH, MEDIUM, LOW
    factor_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    raw_score FLOAT NOT NULL,            -- 0.0 to 1.0
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scans_user ON scans(user_id);
CREATE INDEX idx_scans_hash ON scans(artifact_hash);
CREATE INDEX idx_scans_created ON scans(created_at DESC);
CREATE INDEX idx_evidence_scan ON scan_evidence(scan_id);
```

## 3.3 `reports` & `notifications` DDL

```sql
-- Generated Reports Table
CREATE TABLE reports (
    report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID UNIQUE NOT NULL REFERENCES scans(scan_id) ON DELETE CASCADE,
    report_pdf_path VARCHAR(512),
    summary_headline VARCHAR(255) NOT NULL,
    confidence_score FLOAT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Notifications Table
CREATE TABLE notifications (
    notification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) NOT NULL, -- SCAN_ALERT, THREAT_WARNING, SYSTEM
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_user_read ON notifications(user_id, is_read);
```

## 3.4 `audit_logs` & `organizations` DDL

```sql
-- Audit Logs Table
CREATE TABLE audit_logs (
    audit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource VARCHAR(255) NOT NULL,
    client_ip VARCHAR(45) NOT NULL,
    user_agent TEXT,
    trace_id VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Organizations / Institutional Accounts
CREATE TABLE organizations (
    org_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    org_type VARCHAR(50) NOT NULL, -- GOVERNMENT, ENTERPRISE, BANK, TELECOM
    api_key_hash VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_trace ON audit_logs(trace_id);
```

---

# 4. Redis Cluster — Cache & Session Data Schemas

Redis operates as an in-memory cache, JWT token blacklist, rate-limiting counter, and task queue state tracker.

## Key-Value Schema Registry

| Redis Key Pattern | Data Structure | TTL | Purpose |
|---|---|---|---|
| `jwt:blacklist:<jti>` | String (`"1"`) | Token Expiry (15m) | Revoked JWT Access Tokens |
| `rate:<ip>:<endpoint>` | Integer Counter | 60 seconds | API Gateway Rate Limiting |
| `cache:url:<url_hash>` | JSON String | 24 Hours | Scanned URL Trust Result Cache |
| `cache:upi:<vpa_hash>` | JSON String | 12 Hours | UPI VPA Threat Reputation Cache |
| `otp:<phone_number>` | String (Encrypted OTP) | 5 minutes | Phone/SMS Verification OTP |
| `job:progress:<scan_id>`| Hash (`status`, `pct`) | 1 Hour | Active Async Scan Progress Tracker |

---

# 5. Neo4j 5.x — Graph Database Cypher Schemas

Neo4j models threat campaigns and entity relationships across malicious artifacts.

```
       (Domain:PhishingSite) ──► HOSTS ──► (IPAddress:MaliciousIP)
                 │                                    │
             IMPERSONATES                         ASSOCIATED_WITH
                 ▼                                    ▼
       (Organization:SBI)                 (UPI_VPA:ScamVPA)
```

## Node Labels & Property Specifications
- **`:Domain`** → `{name: "sbi-update-netbanking.top", age_days: 2, created_at: datetime()}`
- **`:IPAddress`** → `{ip: "185.220.101.5", country: "RU", blacklisted: true}`
- **`:UPI_VPA`** → `{vpa: "paytm-kyc-verify@ybl", report_count: 42}`
- **`:PhoneNumber`** → `{phone: "+919876543210", scam_type: "DIGITAL_ARREST"}`
- **`:APKHash`** → `{hash: "a8f9c2...", package_name: "com.fake.sbi"}`
- **`:ScamCampaign`** → `{name: "Operation Fake KYC", risk_score: 95}`

## Standard Cypher Queries

```cypher
// Link a fraudulent Domain to an Impersonated Organization and IP Address
MATCH (o:Organization {name: "State Bank of India"})
MERGE (d:Domain {name: "sbi-update-netbanking.top"})
MERGE (ip:IPAddress {ip: "185.220.101.5"})
MERGE (d)-[:IMPERSONATES]->(o)
MERGE (d)-[:HOSTS]->(ip);

// Find all scam VPAs associated with a malicious domain cluster
MATCH (d:Domain)-[:ASSOCIATED_WITH]->(v:UPI_VPA)
WHERE d.name CONTAINS "sbi-update"
RETURN d.name, v.vpa, v.report_count;
```

---

# 6. Qdrant — Vector Search Collection Specifications

Qdrant stores 512-dimensional visual embeddings extracted from web page screenshots and deepfake face crops for instantaneous similarity matching.

## Collection Configurations

```json
{
  "collection_name": "phishing_screenshots",
  "vectors": {
    "size": 512,
    "distance": "Cosine"
  },
  "hnsw_config": {
    "m": 16,
    "ef_construct": 100
  },
  "optimizers_config": {
    "default_segment_number": 2
  }
}
```

- **Vector Distance metric:** Cosine Similarity.
- **Indexing Algorithm:** HNSW (Hierarchical Navigable Small World) graph index for sub-30ms vector retrieval.
- **Payload Schema:** `{ "domain": "sbi-update.top", "brand": "SBI", "first_seen": "2026-08-04" }`.

---

# 7. MinIO — Object Storage Bucket & Lifecycle Policies

MinIO provides S3-compatible encrypted storage for raw files and generated PDFs.

## Bucket Structure

```
minio-storage/
├── uploads-temp/               # Temporary incoming scan files (Images, Videos, PDFs, APKs)
├── reports-pdf/                # Generated PDF Verification Certificates
├── website-screenshots/        # Captured 1080p Headless Web Screenshots
└── model-weights/              # Versioned AI Model ONNX Weights Checkpoints
```

## DPDP 2023 Compliance Auto-Purge Policy
In compliance with Section 6 of India's DPDP Act 2023, all objects inside `uploads-temp` and `website-screenshots` automatically expire and are permanently purged after **30 days**:

```xml
<LifecycleConfiguration>
    <Rule>
        <ID>DPDP-30-Day-Auto-Purge</ID>
        <Status>Enabled</Status>
        <Prefix>uploads-temp/</Prefix>
        <Expiration>
            <Days>30</Days>
        </Expiration>
    </Rule>
</LifecycleConfiguration>
```

---

# 8. Database Migration Protocol (Alembic)

All PostgreSQL schema changes must execute via Alembic migrations.

## Migration Command Workflow
1. Generate migration script:  
   `alembic revision --autogenerate -m "add_threat_feeds_table"`
2. Verify generated script in `backend/auth-service/alembic/versions/`.
3. Apply migration:  
   `alembic upgrade head`
4. Test rollback function:  
   `alembic downgrade -1`

---

# 9. Encryption, Privacy & DPDP Compliance Standards

- **Passwords:** Argon2id with unique 16-byte random salts.
- **Data in Transit:** TLS 1.3 for all database connection strings (`sslmode=require`).
- **Data at Rest:** AES-256-GCM transparent data encryption for sensitive columns (`api_key_hash`, `phone_number`).
- **Data Anonymization:** Threat telemetry stored in Neo4j and Qdrant uses cryptographic SHA-256 hashes of identifiers, preserving full user anonymity.

---

# 10. Backup, Disaster Recovery & High Availability (RTO/RPO)

| Database System | High Availability Setup | Backup Frequency | Target RTO | Target RPO |
|---|---|---|---|---|
| **PostgreSQL 16** | Primary-Secondary Read Replicas | WAL Continuous Archiving + 6h Snapshot | $< 2$ Hours | $< 15$ Mins |
| **Redis 7.x** | Sentinel / Cluster 3-Node Topology | Daily RDB Snapshot | $< 15$ Mins | $< 1$ Min |
| **Neo4j 5.x** | Causal Cluster Topology | Daily Backup | $< 1$ Hour | $< 1$ Hour |
| **Qdrant** | Distributed Multi-Node Cluster | Daily Snapshot | $< 1$ Hour | $< 1$ Hour |
| **MinIO** | Distributed 4-Drive Erasure Coding | Daily Geo-Replication | $< 2$ Hours | $< 15$ Mins |

---

# 11. Naming Conventions & Indexing Rules

- **Database Tables:** Plural, `snake_case` (`users`, `scans`, `scan_evidence`).
- **Columns:** Singular, `snake_case` (`user_id`, `created_at`, `trust_score`).
- **Primary Keys:** UUID named `<table>_id` or `id` (e.g., `user_id`, `scan_id`).
- **Foreign Keys:** References primary key as `<singular_table>_id` (e.g., `user_id REFERENCES users(user_id)`).
- **Index Names:** Explicitly prefixed as `idx_<table_name>_<column_name>`.

---
**[ END OF DATABASE ARCHITECTURE SPECIFICATION v1.0 ]**
