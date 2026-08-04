# TruthShield X
# Testing & Quality Assurance Strategy Specification
## Document: 12-Testing.md
**Version:** 1.0 (Unified Master QA & Testing Specification)  
**Status:** Approved Mandatory Quality Assurance Standard  
**Testing Pyramid Target:** 70% Unit Tests, 20% Integration Tests, 10% End-to-End Tests  
**Code Coverage Target:** $\ge 80\%$ Minimum Line Coverage for Backend & Frontend Codebases  
**AI Model Evaluation Targets:** Accuracy $\ge 95.0\%$, Precision $\ge 95.0\%$, Recall $\ge 93.0\%$, F1 $\ge 94.0\%$

---

# Document Overview

This document defines the complete Quality Assurance Strategy, Test Framework Configurations, Automated Unit/Integration Test Patterns, AI Model Benchmark Pipelines, Load & Performance Specs (Locust), Security Vulnerability Test Workflows, and Quality Release Gate Protocols for **TruthShield X**.

---

# Table of Contents

1. Executive Testing Philosophy & Quality Strategy
2. Testing Pyramid & Target Distribution
3. Backend Unit & Integration Testing (Pytest + FastAPI TestClient)
4. Frontend UI & Component Testing (Vitest + React Testing Library)
5. AI Model Validation & Benchmark Pipeline
6. Performance, Load & Scalability Testing (Locust & k6)
7. Security Vulnerability & Dynamic Scanning (OWASP ZAP & Trivy)
8. End-to-End (E2E) Test Automation (Playwright)
9. Automated CI/CD Quality Gate Integration
10. Test Data Curation & Privacy Controls
11. Bug Severity Matrix & Triage Protocols
12. Quality Release Gate & Definition of Done (DoD) Sign-Off

---

# 1. Executive Testing Philosophy & Quality Strategy

TruthShield X enforces a **Quality-First Engineering Culture**. No feature, API endpoint, or AI model weights file reaches production without satisfying strict automated quality gates.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        QUALITY ASSURANCE CORE                               │
├───────────────────┬───────────────────┬───────────────────┬─────────────────┤
│ 1. 80% Minimum    │ 2. Automated AI   │ 3. Load & Scale   │ 4. Security     │
│    Line Coverage   │    Benchmarks     │    Verification   │    Scanning     │
│ Enforced via      │ Precision >= 95%  │ 10,000+ Users     │ OWASP Top 10 +  │
│ Pytest & Vitest.  │ Recall >= 93%.    │ Locust Load test. │ Trivy SAST.     │
└───────────────────┴───────────────────┴───────────────────┴─────────────────┘
```

---

# 2. Testing Pyramid & Target Distribution

```
                              TESTING PYRAMID
                                    ▲
                                   / \
                                  / E2E\            (10% - Playwright)
                                 /------\
                                /  INTEG \          (20% - Pytest Integration)
                               /----------\
                              /    UNIT    \        (70% - Pytest & Vitest)
                             /--------------\
```

- **Unit Tests (70%):** Validate isolated functions, algorithms, Pydantic schemas, and React components.
- **Integration Tests (20%):** Validate database operations, API gateway routing, and AI gateway model calls.
- **End-to-End Tests (10%):** Validate complete user flows (Intake $\rightarrow$ AI Inference $\rightarrow$ Score $\rightarrow$ XAI Report).

---

# 3. Backend Unit & Integration Testing (Pytest + FastAPI TestClient)

All backend Python services use **Pytest** with `pytest-asyncio` for asynchronous endpoint testing.

## Exemplary Pytest Code Pattern (`tests/test_scan_router.py`)

```python
import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_url_scan_auto_classification():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        payload = {"url": "https://sbi-update-netbanking.top"}
        response = await client.post("/api/v1/scan", json=payload)
        
        assert response.status_code == 202
        data = response.json()
        assert data["success"] is True
        assert data["data"]["detectedType"] == "URL"
        assert "scanId" in data["data"]

@pytest.mark.asyncio
async def test_invalid_file_upload_rejection():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        files = {"file": ("test.exe", b"MZ...", "application/x-msdownload")}
        response = await client.post("/api/v1/scan", files=files)
        
        assert response.status_code == 422
        data = response.json()
        assert data["success"] is False
        assert data["error"]["code"] == "TSX-2002"
```

---

# 4. Frontend UI & Component Testing (Vitest + React Testing Library)

All web components in `apps/web` use **Vitest** and **React Testing Library** for component render and accessibility testing.

## Exemplary Vitest Code Pattern (`src/components/TrustScoreGauge.test.tsx`)

```typescript
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { TrustScoreGauge } from './TrustScoreGauge';

describe('TrustScoreGauge Component', () => {
  it('renders score correctly with DANGEROUS status badge', () => {
    render(<TrustScoreGauge score={14} status="DANGEROUS" />);
    
    expect(screen.getByText('14')).toBeInTheDocument();
    expect(screen.getByText('DANGEROUS')).toBeInTheDocument();
  });

  it('applies emerald color for TRUSTED score (>=90)', () => {
    render(<TrustScoreGauge score={95} status="TRUSTED" />);
    
    const badge = screen.getByText('TRUSTED');
    expect(badge).toHaveStyle({ backgroundColor: '#10B981' });
  });
});
```

---

# 5. AI Model Validation & Benchmark Pipeline

No AI model weights file is released to production without undergoing benchmark evaluation on held-out test datasets.

```
Model Weights (.onnx) ──► Dataset Evaluation ──► Confusion Matrix ──► Metric Check
                                                                           │
     ┌─────────────────────────────────────────────────────────────────────┘
     ▼
(Precision >= 95% & Recall >= 93%?) ── YES ──► Approve Model for Production
     │ NO
     └──► Reject Model Build & Trigger Alert
```

## AI Evaluation Metrics Thresholds

| Metric | Minimum Required Threshold | Calculation Formula |
|---|---|---|
| **Accuracy** | $\ge 95.0\%$ | $\frac{TP + TN}{TP + TN + FP + FN}$ |
| **Precision** | $\ge 95.0\%$ | $\frac{TP}{TP + FP}$ |
| **Recall** | $\ge 93.0\%$ | $\frac{TP}{TP + FN}$ |
| **F1 Score** | $\ge 94.0\%$ | $2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$ |
| **Inference Latency** | $< 300\text{ms}$ (Text/URL), $< 30\text{s}$ (Video) | Measured execution time on ONNX runtime |

---

# 6. Performance, Load & Scalability Testing (Locust & k6)

Load testing validates that TruthShield X supports **10,000+ active concurrent users** without degradation.

## Exemplary Locust Load Test Script (`tests/locustfile.py`)

```python
from locust import HttpUser, task, between

class TruthShieldUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def test_url_scan(self):
        self.client.post("/api/v1/scan", json={"url": "https://sbi-update.xyz"})

    @task(1)
    def test_threat_map(self):
        self.client.get("/api/v1/threats/map?state=MAHARASHTRA")
```

---

# 7. Security Vulnerability & Dynamic Scanning (OWASP ZAP & Trivy)

- **SAST & Dependency Scan:** Snyk and Trivy scan Python packages, Node modules, and Docker containers for CVEs. Builds with `CRITICAL` or `HIGH` vulnerabilities are automatically blocked.
- **DAST Dynamic Scan:** OWASP ZAP runs against Staging API endpoints testing for SQL injection, XSS, broken access control, and header misconfigurations.

---

# 8. End-to-End (E2E) Test Automation (Playwright)

**Playwright** executes multi-step browser user flows testing complete platform integration.

## Exemplary Playwright E2E Script (`tests/e2e/scan_flow.spec.ts`)

```typescript
import { test, expect } from '@playwright/test';

test('User can submit URL scan and view XAI evidence card', async ({ page }) => {
  await page.goto('http://localhost:3000');
  
  // Fill scan form input
  await page.fill('input[aria-label="URL Input"]', 'https://sbi-update-netbanking.top');
  await page.click('button:has-text("Inspect Website")');

  // Verify processing state
  await expect(page.locator('text=Analyzing Website')).toBeVisible();

  // Verify results render
  await expect(page.locator('text=DANGEROUS')).toBeVisible({ timeout: 10000 });
  await expect(page.locator('text=Domain Age')).toBeVisible();
});
```

---

# 9. Automated CI/CD Quality Gate Integration

Every GitHub pull request automatically triggers the quality verification pipeline:

```
PR Opened ──► Lint Check (Ruff/ESLint) ──► Pytest & Vitest (80% Coverage) ──► Trivy SAST
                                                                                     │
     ┌───────────────────────────────────────────────────────────────────────────────┘
     ▼
(All Gate Checks Pass?) ── YES ──► Allow PR Merge
     │ NO
     └──► Block Merge
```

---

# 10. Test Data Curation & Privacy Controls

- **Zero Production Data in Test:** Production user data, submitted identity documents, and personal details are strictly forbidden in test environments.
- **Synthetic Test Datasets:** Tests utilize anonymized, synthetic datasets curated in `datasets/`:
  - `datasets/urls/`: Phishing vs Legitimate URL samples.
  - `datasets/deepfakes/`: Synthetic GAN image & face-swap video clips.
  - `datasets/documents/`: Synthetic Aadhaar & PAN sample templates.

---

# 11. Bug Severity Matrix & Triage Protocols

| Severity Level | Definition | SLA for Resolution | Action Protocol |
|---|---|---|---|
| **CRITICAL** | System unavailable, security breach, or data corruption | $< 2$ Hours | Emergency hotfix trigger; stop all feature work. |
| **HIGH** | Core detector broken or API gateway failing | $< 24$ Hours | High-priority sprint bugfix. |
| **MEDIUM** | Feature partially degraded; workaround available | $< 3$ Days | Scheduled in current sprint. |
| **LOW** | Minor visual defect or cosmetic typo | $< 1$ Week | Scheduled in backlog refinement. |

---

# 12. Quality Release Gate & Definition of Done (DoD) Sign-Off

Before approving any release tag or deployment build:

- [x] Code coverage exceeds $\ge 80\%$ for backend and frontend codebases.
- [x] All Pytest, Vitest, and Playwright E2E test suites pass with 100% success rate.
- [x] AI models meet accuracy thresholds (Precision $\ge 95\%$, Recall $\ge 93\%$).
- [x] Locust load testing verifies sub-300ms gateway latency under load.
- [x] Trivy and OWASP ZAP security scans report zero `CRITICAL` or `HIGH` vulnerabilities.
- [x] Technical QA sign-off approved.

---
**[ END OF MASTER TESTING SPECIFICATION v1.0 ]**
