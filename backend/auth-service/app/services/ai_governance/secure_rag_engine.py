"""
TruthShield X — Secure RAG Engine (Phase 31).

Enforces strict tenant isolation, document trust evaluation, and indirect prompt injection filtering in RAG pipelines.
"""

from typing import Dict, List, Any
from app.schemas.ai_security_governance_models import SecureRAGContextDTO, RAGDocumentTrustLiteral


class SecureRAGEngine:
    """Secures Retrieval-Augmented Generation by treating all retrieved content strictly as inert DATA."""

    def evaluate_retrieval_security(
        self,
        query: str,
        retrieved_documents: List[Dict[str, Any]],
        request_tenant_id: str,
    ) -> Dict[str, Any]:
        sanitized_docs = []
        injection_detected = False

        for doc in retrieved_documents:
            # 1. Tenant boundary enforcement
            if doc.get("tenant_id") != request_tenant_id:
                continue  # Drop cross-tenant data

            content = doc.get("content", "")

            # 2. Indirect Prompt Injection Defense
            lower_content = content.lower()
            if "ignore all previous instructions" in lower_content or "system prompt" in lower_content or "reveal credentials" in lower_content:
                injection_detected = True
                doc_trust: RAGDocumentTrustLiteral = "BLOCKED"
            elif doc.get("is_verified"):
                doc_trust = "VERIFIED"
            else:
                doc_trust = "TRUSTED"

            if doc_trust != "BLOCKED":
                sanitized_docs.append({
                    "doc_id": doc.get("doc_id"),
                    "trust_verdict": doc_trust,
                    "content": content,
                })

        return {
            "query": query,
            "tenant_id": request_tenant_id,
            "retrieved_count": len(sanitized_docs),
            "sanitized_documents": sanitized_docs,
            "prompt_injection_detected": injection_detected,
            "status": "PROMPT_INJECTION_DETECTED" if injection_detected else "RAG_RETRIEVAL_SECURED",
        }
