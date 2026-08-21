import pytest
from app.services.qr_classifier import classify_qr_payload
from app.services.upi_fraud_detector import parse_upi_uri, evaluate_upi_fraud_heuristics
from app.services.qr_detector import QRVisionDetector


def test_classify_qr_payload_upi():
    category, meta = classify_qr_payload("upi://pay?pa=cashback@fakebank&pn=Refund&am=5000&tn=Enter+PIN")
    assert category == "UPI_PAYMENT"


def test_classify_qr_payload_url():
    category, meta = classify_qr_payload("https://truthshield.gov.in")
    assert category == "URL"


def test_upi_fraud_heuristics():
    uri = "upi://pay?pa=cashback-rewards@fakebank&pn=ClaimRefund&am=9999&tn=Enter+PIN+to+receive+cashback"
    upi_obj = parse_upi_uri(uri)

    assert upi_obj.vpa_handle == "cashback-rewards@fakebank"
    assert upi_obj.amount == 9999.0

    evidence, recs, risk_score = evaluate_upi_fraud_heuristics(upi_obj)
    assert risk_score >= 80
    assert len(evidence) >= 2


@pytest.mark.asyncio
async def test_qr_vision_detector_analysis():
    detector = QRVisionDetector()
    fake_bytes = b"upi://pay?pa=lottery-claim@fakebank&pn=Refund&am=8000&tn=PIN"
    result = await detector.analyze_qr_image(fake_bytes, "test_qr.png")

    assert result.module == "qr-vision-upi"
    assert result.payload_category == "UPI_PAYMENT"
    assert result.risk_score >= 70
    assert result.upi_details["vpa_handle"] == "lottery-claim@fakebank"
