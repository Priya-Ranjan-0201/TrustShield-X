import time
from typing import Dict, Any, List
from app.services.qr_decoder import decode_qr_image
from app.services.qr_classifier import classify_qr_payload
from app.services.upi_fraud_detector import parse_upi_uri, evaluate_upi_fraud_heuristics
from app.services.website_detector import WebsitePhishingDetector


class QRVisionDetectorResult:
    def __init__(
        self,
        module: str,
        status: str,
        payload_category: str,
        decoded_payload: str,
        risk_score: int,
        confidence_score: float,
        severity: str,
        upi_details: Dict[str, Any] | None,
        evidence: List[Dict[str, str]],
        recommendations: List[str],
        execution_time_ms: int,
    ):
        self.module = module
        self.status = status
        self.payload_category = payload_category
        self.decoded_payload = decoded_payload
        self.risk_score = risk_score
        self.confidence_score = confidence_score
        self.severity = severity
        self.upi_details = upi_details
        self.evidence = evidence
        self.recommendations = recommendations
        self.execution_time_ms = execution_time_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module": self.module,
            "status": self.status,
            "payload_category": self.payload_category,
            "decoded_payload": self.decoded_payload,
            "risk_score": self.risk_score,
            "confidence_score": self.confidence_score,
            "severity": self.severity,
            "upi_details": self.upi_details,
            "evidence": self.evidence,
            "recommendations": self.recommendations,
            "execution_time_ms": self.execution_time_ms,
        }


class QRVisionDetector:
    def __init__(self):
        self.website_detector = WebsitePhishingDetector()

    async def analyze_qr_image(self, file_bytes: bytes, filename: str | None = None) -> QRVisionDetectorResult:
        start_time = time.time()

        # 1. Decode QR Image
        qr_decode = decode_qr_image(file_bytes, filename)
        raw_payload = qr_decode.raw_payload

        # 2. Classify Payload
        category, metadata = classify_qr_payload(raw_payload)

        evidence_list: List[Dict[str, str]] = []
        recommendations: List[str] = []
        risk_score = 0
        upi_details = None

        # 3. Branch Processing by Payload Category
        if category == "UPI_PAYMENT":
            upi_obj = parse_upi_uri(raw_payload)
            evidence_list, recommendations, risk_score = evaluate_upi_fraud_heuristics(upi_obj)
            upi_details = {
                "vpa_handle": upi_obj.vpa_handle,
                "payee_name": upi_obj.payee_name,
                "amount": upi_obj.amount,
                "currency": upi_obj.currency,
                "note": upi_obj.note,
                "merchant_code": upi_obj.merchant_code,
            }

        elif category == "URL":
            # Delegate URL to Phase 3.2 Website Phishing Detection Engine without duplicate code
            web_res = await self.website_detector.analyze_url(raw_payload)
            risk_score = web_res.risk_score
            evidence_list = web_res.evidence
            recommendations = web_res.recommendations

        else:
            # Plain Text / Contact / WiFi / Other
            evidence_list.append(
                {
                    "type": "QR_PAYLOAD",
                    "severity": "INFO",
                    "title": f"Decoded {category} Payload",
                    "description": f"Extracted payload content: '{raw_payload[:100]}'.",
                }
            )
            recommendations.append("Inspect non-URL and non-payment QR codes before authorizing system configuration changes.")

        # Compute Severity & Confidence
        if risk_score >= 80:
            severity = "CRITICAL"
        elif risk_score >= 50:
            severity = "HIGH"
        elif risk_score >= 25:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        confidence_score = 0.96 if qr_decode.is_decoded else 0.80
        execution_time_ms = int((time.time() - start_time) * 1000)

        return QRVisionDetectorResult(
            module="qr-vision-upi",
            status="completed",
            payload_category=category,
            decoded_payload=raw_payload,
            risk_score=risk_score,
            confidence_score=confidence_score,
            severity=severity,
            upi_details=upi_details,
            evidence=evidence_list,
            recommendations=recommendations,
            execution_time_ms=execution_time_ms,
        )
