"""
TruthShield X — RPO & RTO Measurement Engine (Phase 23).

Measures empirical Recovery Point Objective (RPO) and Recovery Time Objective (RTO) with strict NOT_VERIFIED guards.
"""

from typing import Dict, Optional
from app.schemas.cyber_resilience_models import RTOEngineDTO, RPOEngineDTO


class RPORTOEngine:
    """Computes empirical RTO and RPO metrics grounded in measured recovery drills."""

    def evaluate_rto(
        self,
        service_id: str,
        target_rto_minutes: int = 30,
        measured_time_minutes: Optional[float] = None,
        is_empirically_tested: bool = False,
    ) -> RTOEngineDTO:
        if not is_empirically_tested or measured_time_minutes is None:
            return RTOEngineDTO(
                service_id=service_id,
                target_rto_minutes=target_rto_minutes,
                actual_rto_minutes=None,
                validation_status="NOT_VERIFIED",
            )

        status = "VERIFIED" if measured_time_minutes <= target_rto_minutes else "EXCEEDED_TARGET"
        return RTOEngineDTO(
            service_id=service_id,
            target_rto_minutes=target_rto_minutes,
            actual_rto_minutes=measured_time_minutes,
            validation_status=status,
            evidence_reference=f"ev_drill_rto_{service_id}",
        )

    def evaluate_rpo(
        self,
        service_id: str,
        target_rpo_minutes: int = 15,
        measured_loss_minutes: Optional[float] = None,
        is_empirically_tested: bool = False,
    ) -> RPOEngineDTO:
        if not is_empirically_tested or measured_loss_minutes is None:
            return RPOEngineDTO(
                service_id=service_id,
                target_rpo_minutes=target_rpo_minutes,
                actual_data_loss_minutes=None,
                validation_status="NOT_VERIFIED",
            )

        status = "VERIFIED" if measured_loss_minutes <= target_rpo_minutes else "EXCEEDED_TARGET"
        return RPOEngineDTO(
            service_id=service_id,
            target_rpo_minutes=target_rpo_minutes,
            actual_data_loss_minutes=measured_loss_minutes,
            validation_status=status,
            evidence_reference=f"ev_drill_rpo_{service_id}",
        )
