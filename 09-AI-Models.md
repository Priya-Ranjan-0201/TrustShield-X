# TruthShield X
# AI Models & Intelligence Architecture Specification
## Document: 09-AI-Models.md
**Version:** 1.0 (Unified Master AI Specification)  
**Status:** Approved Technical Architecture & Model Governance Standard  
**Target Environment:** AI Gateway, PyTorch, ONNX Runtime, CUDA Acceleration  
**Evaluation Thresholds:** Precision $\ge 95.0\%$, Recall $\ge 93.0\%$, F1 Score $\ge 94.0\%$

---

# Document Overview

This document defines the complete AI Model Architecture, Deep Learning Pipelines, Feature Extraction Protocols, Model Registry Governance, ONNX Optimization Steps, and Benchmark Benchmarks for **TruthShield X**.

TruthShield X is a **Multi-Modal AI Defense Platform** unifying Computer Vision, Natural Language Processing (NLP), Speech & Audio Intelligence, Optical Character Recognition (OCR), Graph Intelligence, and Explainable AI (XAI) under a centralized **AI Gateway control plane**.

---

# Table of Contents

1. Executive AI Architecture & Multi-Modal Pipeline
2. AI Gateway & Hardware Resource Scheduling
3. Computer Vision AI Subsystem (Deepfake Image & Video)
4. Natural Language Processing (NLP) Subsystem
5. Speech & Audio Intelligence Subsystem (Voice Cloning & ASR)
6. Optical Character Recognition (OCR) & Document Forgery Subsystem
7. Website Vision & Technical Inspection Subsystem
8. Android APK Binary Inspection Subsystem
9. Risk Fusion & Digital Trust Score Algorithm
10. Explainable AI (XAI) Rationale Generation Architecture
11. AI Model Registry Schema & Versioning Lifecycle
12. Training, DVC Data Pipelines & Automated Retraining
13. Model Benchmarking, Drift Monitoring & Hardware Specs

---

# 1. Executive AI Architecture & Multi-Modal Pipeline

TruthShield X rejects isolated, black-box AI tools. All incoming digital artifacts are auto-classified by the Unified Scan Engine, dispatched to specialized AI microservices via the AI Gateway, aggregated into a unified **Digital Trust Score (0–100)**, and explained via an XAI rationale engine.

```
                     ┌─────────────────────────────────────────┐
                     │     UNIFIED SCAN INTAKE AUTO-ROUTER     │
                     └────────────────────┬────────────────────┘
                                          │
                                          ▼
                     ┌─────────────────────────────────────────┐
                     │            AI GATEWAY ROUTER            │
                     │ (Model Registry, ONNX & GPU Scheduler)  │
                     └────────────────────┬────────────────────┘
                                          │
    ┌────────────────────┬────────────────┼────────────────────┬────────────────────┐
    ▼                    ▼                ▼                    ▼                    ▼
┌──────────────┐  ┌──────────────┐ ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Vision AI   │  │   NLP AI     │ │   Audio AI   │     │ Document OCR │     │ Graph AI     │
│ (ViT/3D-CNN) │  │  (DeBERTa)   │ │(Whisper/W2V) │     │ (PaddleOCR)  │     │   (Neo4j)    │
└──────┬───────┘  └──────┬───────┘ └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                 │                │                    │                    │
       └─────────────────┴────────────────┼────────────────────┴────────────────────┘
                                          │
                                          ▼
                     ┌─────────────────────────────────────────┐
                     │      RISK AGGREGATION & FUSION ENGINE   │
                     │       (Weighted Matrix Score 0-100)     │
                     └────────────────────┬────────────────────┘
                                          │
                                          ▼
                     ┌─────────────────────────────────────────┐
                     │      EXPLAINABLE AI (XAI) ENGINE        │
                     │    (SHAP Rationale & Evidence Cards)    │
                     └─────────────────────────────────────────┘
```

---

# 2. AI Gateway & Hardware Resource Scheduling

The **AI Gateway** manages model serving, GPU VRAM allocation, dynamic request batching, and ONNX Runtime execution.

## Key Serving Specifications:
- **ONNX Runtime Acceleration:** Trained PyTorch models are converted to FP16 ONNX models for $3\times$ faster CPU/GPU inference speed.
- **Dynamic Batching:** Groups concurrent single-image inference requests into batch vectors of size 8/16.
- **VRAM Threshold Monitor & CPU Fallback:** If GPU VRAM utilization exceeds 95%, the gateway automatically routes incoming requests to CPU ONNX Runtime worker nodes.
- **Latency Tracking:** Logs exact inference latency (`ai_inference_latency_ms`) for telemetry.

---

# 3. Computer Vision AI Subsystem (Deepfake Image & Video)

## 3.1 Deepfake Image Inspection Pipeline
- **Model Architecture:** Vision Transformer (ViT-Base) + XceptionNet.
- **Feature Extraction:** Analyzes high-frequency GAN noise artifacts, eye reflection asymmetry, skin texture boundary blur, and EXIF metadata editing.
- **Output:** Synthetic Probability Score ($0.0 - 1.0$) + Spatial Attention Heatmap highlighting manipulated face regions.

## 3.2 Deepfake Video Temporal Inspection Pipeline
- **Model Architecture:** Spatial-Temporal 3D-CNN (ResNet3D) + LSTM temporal frame aggregator.
- **Feature Extraction:** Extracts 16-frame clip sequences, evaluating lip-sync visual correlation, blink rate frequency, temporal flickering, and face-swap seam boundaries.
- **SLA Target:** Processes 1080p 30-second video clips in $< 30$ seconds using Keyframe Adaptive Sampling (2 frames/sec).

---

# 4. Natural Language Processing (NLP) Subsystem

## 4.1 Phishing Email & SMS Fraud Inspection
- **Model Architecture:** Fine-tuned DeBERTa-v3-Large + RoBERTa.
- **Feature Extraction:** Classifies text intent across 4 primary risk categories: Credential Phishing, Financial Extortion, Urgency Scams, Safe.
- **NLP Tasks:** Named Entity Recognition (NER) extracting spoofed brand names, bank accounts, and malicious URLs.

## 4.2 Fake News & Claim Verification Engine
- **Model Architecture:** Llama-3 / Gemma reasoning model + Semantic Vector Search (Qdrant).
- **Feature Extraction:** Extracts atomic factual claims from input text and queries trusted knowledge graphs to assign a Truth Rating (Verified, Misleading, Unverified, False).

---

# 5. Speech & Audio Intelligence Subsystem (Voice Cloning & ASR)

```
Audio Input (.mp3/.wav) ──► Whisper ASR ──► Text Transcript ──► NLP Fraud Intent Check
                              │
                              ▼
                      Mel-Spectrogram ──► Wav2Vec2 / ResMFCC ──► Synthetic Voice Score
```

- **Speech-to-Text (ASR):** OpenAI Whisper (Medium) transcribes call recordings into structured text supporting English and Indian regional languages (Hindi, Tamil, Telugu, Bengali).
- **Voice Clone Detector:** Wav2Vec2 + ECAPA-TDNN extracts speaker embeddings and Mel-frequency cepstral coefficients (MFCC) to detect neural synthetic voice signatures (Tacotron, ElevenLabs).

---

# 6. Optical Character Recognition (OCR) & Document Forgery Subsystem

- **OCR Engine:** PaddleOCR + LayoutLM-v3.
- **Document Targets:** Aadhaar Card, PAN Card, Driving Licence, Passport, PDF contracts.
- **Inspection Verification Pipeline:**
  1. Extract text fields via bounding-box OCR.
  2. Verify field layout structure against standard state templates.
  3. Validate micro-print alignment and photo overlay boundaries.
  4. Recalculate 12-digit Aadhaar Verhoeff Checksum to flag forged identification numbers.

---

# 7. Website Vision & Technical Inspection Subsystem

- **Headless Scraper:** Playwright renders target webpage and captures 1080p screenshot.
- **Technical Engine:** Checks WHOIS domain age (<30 days flag), SSL validity, DNS records, and redirect chains.
- **Visual Brand Matching:** Vision Transformer (ViT) compares webpage screenshot layout against authentic bank/portal reference assets stored in Qdrant Vector DB.

---

# 8. Android APK Binary Inspection Subsystem

- **Static Analyzer:** Androguard parses `AndroidManifest.xml` permissions, API keys, and certificate signatures.
- **Permission Risk Engine:** Flags over-privileged combinations (e.g., SMS Reading + Accessibility Service + Background Audio Recording in a utility app).
- **Dynamic Sandbox:** Runs APK inside isolated Android emulator container to detect C2 network calls and overlay injection attempts.

---

# 9. Risk Fusion & Digital Trust Score Algorithm

The Risk Engine synthesizes detector outputs into a single score:

$$\text{Risk Score} = \sum_{i=1}^{n} (W_i \times S_i)$$

$$\text{Digital Trust Score} = \max\left(0, \min\left(100, 100 \times (1 - \text{Risk Score})\right)\right)$$

## Detector Weight Assignment Table

| Detector Microservice ($i$) | Assigned Weight ($W_i$) | Primary Evaluation Metric |
|---|---|---|
| Domain Technical & WHOIS | 0.25 | Domain Age < 7 days, SSL mismatch |
| Visual Brand Impersonation | 0.25 | ViT Screenshot similarity > 85% on fake domain |
| Deepfake Vision / Audio | 0.25 | GAN noise, lip-sync mismatch, synthetic voice score |
| Threat Graph & Blacklist | 0.15 | Historical fraud reports on VPA / Phone / IP |
| NLP & Text Urgency | 0.10 | Coercive financial language, phishing intent |

---

# 10. Explainable AI (XAI) Rationale Generation Architecture

Every prediction returns an explicit XAI evidence payload:

```json
{
  "modelName": "truthshield-fusion-v1.0",
  "trustScore": 14,
  "riskLevel": "DANGEROUS",
  "confidence": 0.96,
  "xaiSummary": {
    "headline": "High Risk Phishing Portal Impersonating State Bank of India",
    "evidence": [
      {
        "detector": "website-ai",
        "factor": "Domain Age",
        "severity": "CRITICAL",
        "description": "Domain 'sbi-update-netbanking.top' was registered 2 days ago."
      },
      {
        "detector": "website-ai",
        "factor": "Brand Impersonation",
        "severity": "CRITICAL",
        "description": "Page visually clones official SBI logo on an unauthorized domain."
      }
    ],
    "recommendations": [
      "Do NOT enter net banking credentials or OTPs.",
      "Report link immediately via official bank portal."
    ]
  }
}
```

---

# 11. AI Model Registry Schema & Versioning Lifecycle

Every model deployment is registered with explicit version metadata:

```json
{
  "modelId": "deepfake-vision-v1.2.0",
  "task": "DEEPFAKE_IMAGE_DETECTION",
  "framework": "PyTorch / ONNX",
  "weightsVersion": "v1.2.0-onnx-fp16",
  "metrics": {
    "precision": 0.962,
    "recall": 0.941,
    "f1Score": 0.951,
    "accuracy": 0.958
  },
  "trainingDatasetHash": "sha256:8f92c1...",
  "onnxPath": "s3://model-weights/deepfake-vision-v1.2.0.onnx",
  "deploymentDate": "2026-08-04T14:54:00Z"
}
```

---

# 12. Training, DVC Data Pipelines & Automated Retraining

```
[ Data Curation ] ──► [ DVC Versioning ] ──► [ PyTorch Training ] ──► [ Benchmark Eval ]
                                                                             │
     ┌───────────────────────────────────────────────────────────────────────┘
     ▼
(Passed Benchmarks?) ── YES ──► [ ONNX Conversion ] ──► [ Deploy to AI Gateway ]
     │ NO
     └──► Retrain Hyperparameters
```

---

# 13. Model Benchmarking, Drift Monitoring & Hardware Specs

## Evaluation Threshold Targets
- **Accuracy:** $\ge 95.0\%$
- **Precision:** $\ge 95.0\%$
- **Recall:** $\ge 93.0\%$
- **F1 Score:** $\ge 94.0\%$

## Hardware Requirements
- **Development Node:** CPU 8+ Cores, 32 GB RAM, NVIDIA RTX 4070 (12 GB VRAM).
- **Production Kubernetes Cluster:** Multi-GPU Nodes (NVIDIA T4 / A10G), CUDA 12.x, High-Speed SSD Storage.

---
**[ END OF MASTER AI SPECIFICATION v1.0 ]**
