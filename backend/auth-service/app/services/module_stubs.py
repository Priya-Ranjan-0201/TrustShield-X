import time
from typing import Dict, Any


class DetectionModuleResult:
    def __init__(
        self,
        module_code: str,
        trust_score: int,
        risk_score: int,
        confidence_score: float,
        findings_json: Dict[str, Any],
        execution_time_ms: int,
    ):
        self.module_code = module_code
        self.trust_score = trust_score
        self.risk_score = risk_score
        self.confidence_score = confidence_score
        self.findings_json = findings_json
        self.execution_time_ms = execution_time_ms


class ModuleStubRegistry:
    @staticmethod
    def execute_stub(module_code: str, target: str) -> DetectionModuleResult:
        start_time = time.time()

        is_suspicious = (
            "phish" in target.lower()
            or "fake" in target.lower()
            or "scam" in target.lower()
            or "trojan" in target.lower()
        )
        trust_score = 14 if is_suspicious else 94
        risk_score = 100 - trust_score
        confidence_score = 0.98 if is_suspicious else 0.96

        findings = {
            "module_code": module_code,
            "inspected_target": target,
            "threat_detected": is_suspicious,
            "rationale": (
                "Deep learning model & signature inspection flagged malicious indicators."
                if is_suspicious
                else "Zero threat signals detected. Authentic digital artifact."
            ),
            "indicators": (
                ["brand_impersonation", "suspicious_domain_age", "credential_harvester"]
                if is_suspicious
                else ["valid_digital_signature", "clean_file_header"]
            ),
        }

        execution_time_ms = int((time.time() - start_time) * 1000)

        return DetectionModuleResult(
            module_code=module_code,
            trust_score=trust_score,
            risk_score=risk_score,
            confidence_score=confidence_score,
            findings_json=findings,
            execution_time_ms=execution_time_ms,
        )

    @staticmethod
    def get_registered_modules() -> Dict[str, Dict[str, Any]]:
        return {
            "WEBSITE_ENGINE": {"version": "1.0", "status": "ACTIVE"},
            "QR_ENGINE": {"version": "1.0", "status": "ACTIVE"},
            "DOCUMENT_ENGINE": {"version": "1.0", "status": "ACTIVE"},
            "DEEPFAKE_ENGINE": {"version": "1.0", "status": "ACTIVE"},
            "VOICE_CLONE_ENGINE": {"version": "1.0", "status": "ACTIVE"},
            "APK_ENGINE": {"version": "1.0", "status": "ACTIVE"},
        }
