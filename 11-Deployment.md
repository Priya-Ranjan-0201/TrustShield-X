# TruthShield X
# Deployment & DevOps Architecture Specification
## Document: 11-Deployment.md
**Version:** 1.0 (Unified Master Deployment & DevOps Specification)  
**Status:** Approved Mandatory Infrastructure & DevOps Standard  
**Deployment Topology:** Cloud-Native Kubernetes (EKS/GKE/On-Premise) & Multi-Stage Docker Containers  
**High Availability Target:** 99.9% Platform Uptime SLA (RTO $< 2$ Hours, RPO $< 15$ Minutes)

---

# Document Overview

This document defines the complete Deployment Architecture, Containerization Guidelines, Kubernetes Orchestration Specs, CI/CD Pipeline Definitions, Monitoring & Observability Configurations, Auto-Scaling Rules, and Disaster Recovery Procedures for **TruthShield X**.

---

# Table of Contents

1. Executive Infrastructure & DevOps Strategy
2. Multi-Environment Topology (Dev, Test, Staging, Prod)
3. Containerization Standards & Multi-Stage Dockerfiles
4. Production `docker-compose.yml` Architecture Blueprint
5. Kubernetes (K8s) Cluster Architecture & Helm Manifests
6. Horizontal Pod Auto-scaling (HPA) & GPU Scheduling Rules
7. CI/CD Automated Deployment Pipeline (GitHub Actions Workflow)
8. Observability Stack (Prometheus Metrics & Grafana Dashboards)
9. Centralized Logging (ELK Stack & OpenTelemetry)
10. Environmental Configuration & Secrets Management Inventory
11. Production Security Hardening & Image Scanning
12. Backup, Disaster Recovery & High Availability SLAs
13. Production Release Checklist & Blue-Green Deployment Protocol

---

# 1. Executive Infrastructure & DevOps Strategy

TruthShield X is engineered as a **Cloud-Native, 12-Factor Microservices Platform**. Every backend domain, AI model container, database instance, and frontend application is fully containerized and orchestrated via Kubernetes.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CLOUD-NATIVE INFRASTRUCTURE CORE                        │
├───────────────────┬───────────────────┬───────────────────┬─────────────────┤
│ 1. Multi-Stage    │ 2. Kubernetes     │ 3. Automated      │ 4. Full         │
│    Containers     │    Orchestration  │    CI/CD Pipeline │    Observability│
│ Non-root Alpine   │ HPA Auto-scaling  │ GitHub Actions    │ Prometheus +    │
│ minimal images.   │ & Self-healing.   │ Lint, Test, K8s.  │ Grafana + ELK.  │
└───────────────────┴───────────────────┴───────────────────┴─────────────────┘
```

---

# 2. Multi-Environment Topology

```
                  [ PUBLIC EDGE INGRESS / CDN ]
                                │
                 ┌──────────────┴──────────────┐
                 ▼                             ▼
   ┌───────────────────────────┐ ┌───────────────────────────┐
   │    STAGING ENVIRONMENT    │ │  PRODUCTION ENVIRONMENT   │
   │  Production-like K8s      │ │  Multi-Region K8s Cluster │
   │  UAT & Load Testing       │ │  99.9% Uptime SLA         │
   └───────────────────────────┘ └───────────────────────────┘
```

| Environment | Host Infrastructure | Storage Backend | Scale Policy | Access Level |
|---|---|---|---|---|
| **Development** | Local Docker Compose | Containerized Postgres/Redis | Static 1 Instance | Developers |
| **Testing** | CI/CD Runner / K8s Ephemeral | In-Memory / Isolated DB | Dynamic Test Pods | Automated CI |
| **Staging** | Staging K8s Cluster | Staging Cloud Databases | Auto-scaled 2 Pods | QA & Product |
| **Production** | Multi-Region K8s Cluster | Managed Cloud HA Clusters | Auto-scaled 3-100 Pods | Public / Live |

---

# 3. Containerization Standards & Multi-Stage Dockerfiles

All Docker images must follow multi-stage build patterns, run under non-root system users (`USER appuser`), and maintain minimal image sizes ($< 150\text{ MB}$ for Python microservices).

## 3.1 Backend FastAPI Service Multi-Stage `Dockerfile`

```dockerfile
# Stage 1: Build & Dependency Resolution
FROM python:3.12-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production Execution Image
FROM python:3.12-slim AS runner
WORKDIR /app
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup . .
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost:8000/healthz || exit 1
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 3.2 Frontend React 19 Multi-Stage `Dockerfile`

```dockerfile
# Stage 1: Build React Assets
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: NGINX Web Server Serving
FROM nginx:alpine AS runner
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost/ || exit 1
CMD ["nginx", "-g", "daemon off;"]
```

---

# 4. Production `docker-compose.yml` Architecture Blueprint

The local development and standalone staging environment uses `docker-compose.yml` orchestrating all core databases and microservices:

```yaml
version: '3.8'

networks:
  truthshield-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  neo4j_data:
  qdrant_data:
  minio_data:

services:
  postgres:
    image: postgres:16-alpine
    container_name: tsx-postgres
    restart: always
    environment:
      POSTGRES_DB: truthshield_db
      POSTGRES_USER: tsx_admin
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - truthshield-network

  redis:
    image: redis:7-alpine
    container_name: tsx-redis
    restart: always
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - truthshield-network

  neo4j:
    image: neo4j:5-community
    container_name: tsx-neo4j
    restart: always
    environment:
      NEO4J_AUTH: neo4j/${NEO4J_PASSWORD}
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - neo4j_data:/data
    networks:
      - truthshield-network

  qdrant:
    image: qdrant/qdrant:latest
    container_name: tsx-qdrant
    restart: always
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - truthshield-network

  minio:
    image: minio/minio:latest
    container_name: tsx-minio
    restart: always
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    networks:
      - truthshield-network

  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: tsx-rabbitmq
    restart: always
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASS}
    ports:
      - "5672:5672"
      - "15672:15672"
    networks:
      - truthshield-network
```

---

# 5. Kubernetes (K8s) Cluster Architecture & Helm Manifests

TruthShield X is deployed to Kubernetes clusters utilizing standard Helm Charts.

```
                           KUBERNETES CLUSTER TOPOLOGY
                                        │
      ┌─────────────────────────────────┼─────────────────────────────────┐
      ▼                                 ▼                                 ▼
┌──────────────────┐          ┌──────────────────┐              ┌──────────────────┐
│  Ingress Router  │          │   Service Pods   │              │ GPU Worker Pods  │
│ NGINX Ingress +  │          │ Auth, Scan, Web  │              │ Deepfake Vision  │
│ Cert-Manager SSL │          │ (Auto-scaled HPA)│              │ (NVIDIA T4 / A10G│
└──────────────────┘          └──────────────────┘              └──────────────────┘
```

## Standard Microservice Deployment Manifest (`scan-service-deployment.yaml`)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scan-service
  namespace: truthshield-prod
  labels:
    app: scan-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: scan-service
  template:
    metadata:
      labels:
        app: scan-service
    spec:
      containers:
      - name: scan-service
        image: truthshield/scan-service:v1.0.0
        ports:
        - containerPort: 8002
        envFrom:
        - configMapRef:
            name: tsx-config
        - secretRef:
            name: tsx-secrets
        resources:
          requests:
            cpu: "250m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1536Mi"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8002
          initialDelaySeconds: 15
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8002
          initialDelaySeconds: 10
          periodSeconds: 10
```

---

# 6. Horizontal Pod Auto-scaling (HPA) & GPU Scheduling Rules

Microservice pods automatically scale based on target CPU utilization ($70\%$), Memory usage ($80\%$), or RabbitMQ queue depth ($>100$ pending items).

## Kubernetes HPA Manifest (`scan-service-hpa.yaml`)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: scan-service-hpa
  namespace: truthshield-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: scan-service
  minReplicas: 3
  maxReplicas: 30
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

# 7. CI/CD Automated Deployment Pipeline (GitHub Actions Workflow)

The automated deployment pipeline (`.github/workflows/deploy.yml`) executes linting, testing, security vulnerability scanning, Docker image compilation, and Helm deployment:

```yaml
name: TruthShield X CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python 3.12
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install Dependencies
        run: pip install ruff pytest httpx
      - name: Run Ruff Linter
        run: ruff check .
      - name: Run Pytest Unit Tests
        run: pytest --cov=backend

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Trivy Vulnerability Scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          severity: 'CRITICAL,HIGH'

  build-and-deploy:
    needs: [lint-and-test, security-scan]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Log in to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - name: Build & Push Docker Image
        run: |
          docker build -t truthshield/scan-service:v1.0.0 ./backend/scan-service
          docker push truthshield/scan-service:v1.0.0
      - name: Deploy to Production K8s
        run: |
          echo "${{ secrets.KUBECONFIG }}" > kubeconfig.yaml
          export KUBECONFIG=kubeconfig.yaml
          helm upgrade --install scan-service ./infrastructure/kubernetes/helm/scan-service --set image.tag=v1.0.0
```

---

# 8. Observability Stack (Prometheus Metrics & Grafana Dashboards)

Prometheus scrapes `/metrics` endpoints across microservices to monitor system performance:
- **`http_requests_total`**: Total HTTP request volume counter.
- **`http_request_duration_seconds`**: Latency histogram (p50, p90, p99).
- **`ai_inference_latency_ms`**: AI model inference execution time in milliseconds.
- **`gpu_vram_usage_bytes`**: GPU VRAM memory consumption.

Grafana dashboards display live operational panels for API response times, active error rates, system CPU/Memory loads, and AI queue depth.

---

# 9. Centralized Logging (ELK Stack & OpenTelemetry)

- **Log Collection:** Microservices output single-line JSON log objects to `stdout` containing `traceId` correlation keys.
- **Log Routing:** Logstash / FluentBit intercepts stdout streams and pushes log records to Elasticsearch.
- **Log Inspection:** Kibana provides real-time log searching, filtering by `traceId`, `service`, `userId`, or `level`.

---

# 10. Environmental Configuration & Secrets Management Inventory

All environment configs follow 12-Factor principles. Secrets are injected at runtime via Kubernetes Secrets or Vault:

```env
# Server & Gateway Config
PORT=8000
ENVIRONMENT=production
LOG_LEVEL=INFO

# Database Connection URLs
DATABASE_URL=postgresql+asyncpg://tsx_admin:password@postgres:5432/truthshield_db
REDIS_URL=redis://:password@redis:6379/0
NEO4J_URL=bolt://neo4j:password@neo4j:7687
QDRANT_URL=http://qdrant:6333
MINIO_ENDPOINT=minio:9000

# Security Secrets
JWT_SECRET=super_secret_rsa_private_key_hash
HASHICORP_VAULT_ADDR=http://vault:8200
```

---

# 11. Production Security Hardening & Image Scanning

- **Non-Root Containers:** Every container image explicitly specifies `USER appuser`.
- **Read-Only Root Filesystem:** Production K8s pod manifests enforce `readOnlyRootFilesystem: true` where applicable.
- **Image Vulnerability Scanning:** Every container build is scanned by Trivy prior to deployment; builds containing `CRITICAL` vulnerability CVEs are automatically rejected.

---

# 12. Backup, Disaster Recovery & High Availability SLAs

- **Platform Uptime Target:** 99.9% availability SLA.
- **Recovery Time Objective (RTO):** $< 2$ Hours.
- **Recovery Point Objective (RPO):** $< 15$ Minutes.
- **Automated Backup Strategy:**
  - **PostgreSQL 16:** Continuous WAL archiving to geo-redundant storage + snapshot every 6 hours.
  - **MinIO Object Storage:** Continuous geo-replication to secondary cloud region.
  - **Redis / Neo4j / Qdrant:** Daily automated data volume snapshots.

---

# 13. Production Release Checklist & Blue-Green Deployment Protocol

Before releasing a new production deployment version:

- [x] All automated unit, integration, and end-to-end API test suites pass cleanly.
- [x] Trivy container vulnerability scan reports zero `CRITICAL` or `HIGH` CVEs.
- [x] Database Alembic migration scripts tested in staging environment.
- [x] Prometheus metrics and Grafana dashboards operational.
- [x] RTO/RPO backup snapshot verified.
- [x] Rollback plan documented and ready (`helm rollback scan-service <previous_revision>`).

---
**[ END OF MASTER DEPLOYMENT SPECIFICATION v1.0 ]**
