"""
TruthShield X — Defense Network Manager (Phase 28).

Manages authorized defense networks, participant memberships, trust levels, and expirations.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone, timedelta
from app.schemas.global_defense_models import DefenseNetworkDTO, TrustLevelLiteral


class DefenseNetworkManager:
    """Maintains authorized sharing networks and tracks relationship expiration."""

    def __init__(self):
        self._networks: Dict[str, DefenseNetworkDTO] = {}
        self._seed_default_network()

    def _seed_default_network(self):
        n1 = DefenseNetworkDTO(
            network_id="net_financial_isac",
            name="Global Financial ISAC Cyber Defense Network",
            participants=["tenant_finance_alpha", "tenant_cloud_beta", "cert_eu_exchange"],
            scope="CROSS_ORGANIZATION_THREAT_SHARING",
            trust_level="VERIFIED",
            expiration=(datetime.now(timezone.utc) + timedelta(days=90)).isoformat(),
            status="ACTIVE",
        )
        self._networks[n1.network_id] = n1

    def create_network(
        self,
        name: str,
        participants: List[str],
        trust_level: TrustLevelLiteral = "VERIFIED",
        duration_days: int = 90,
    ) -> DefenseNetworkDTO:
        dto = DefenseNetworkDTO(
            name=name,
            participants=participants,
            scope="CROSS_ORGANIZATION_THREAT_SHARING",
            trust_level=trust_level,
            expiration=(datetime.now(timezone.utc) + timedelta(days=duration_days)).isoformat(),
            status="ACTIVE",
        )
        self._networks[dto.network_id] = dto
        return dto

    def get_network(self, network_id: str) -> Optional[DefenseNetworkDTO]:
        net = self._networks.get(network_id)
        if not net:
            return None
        # Check expiration
        if datetime.fromisoformat(net.expiration) < datetime.now(timezone.utc):
            expired_dto = DefenseNetworkDTO(
                network_id=net.network_id,
                name=net.name,
                participants=net.participants,
                scope=net.scope,
                trust_level=net.trust_level,
                expiration=net.expiration,
                status="EXPIRED",
            )
            self._networks[network_id] = expired_dto
            return expired_dto
        return net

    def list_networks(self) -> List[DefenseNetworkDTO]:
        return list(self._networks.values())
