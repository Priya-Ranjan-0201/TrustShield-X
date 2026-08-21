"""
External Attack Surface Management (EASM) Engine (Phase 34)
===========================================================
Discovers public assets, open ports, exposed APIs, certificate expirations,
domain/DNS records, web frameworks, technology fingerprints, and shadow IT.
Invariant: Only scan assets within explicitly authorized scope; never perform unauthorized exploitation.
"""

from typing import Dict, Any, List, Optional
import datetime


class ExternalAttackSurfaceEngine:
    def __init__(self):
        self._discovered_assets: Dict[str, Dict[str, Any]] = {}
        self._domain_intel: Dict[str, Dict[str, Any]] = {}
        self._certificate_intel: Dict[str, Dict[str, Any]] = {}
        self._service_fingerprints: Dict[str, Dict[str, Any]] = {}
        self._scan_history: List[Dict[str, Any]] = []

    def register_public_asset(
        self,
        asset_id: str,
        tenant_id: str,
        domain_or_ip: str,
        asset_type: str = "DOMAIN",
        open_ports: Optional[List[int]] = None,
        ssl_valid_until: Optional[str] = None,
        is_managed: bool = True,
        discovery_method: str = "PASSIVE_DISCOVERY",
        confidence: float = 1.0,
        owner: str = "SecOps",
        criticality: str = "HIGH",
        technologies: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        ports = open_ports or [80, 443]
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        asset = {
            "asset_id": asset_id,
            "tenant_id": tenant_id,
            "identifier": domain_or_ip,
            "domain_or_ip": domain_or_ip,
            "asset_type": asset_type,
            "open_ports": ports,
            "ssl_valid_until": ssl_valid_until or (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=90)).isoformat(),
            "is_managed": is_managed,
            "discovery_method": discovery_method,
            "confidence": min(1.0, max(0.0, confidence)),
            "owner": owner,
            "criticality": criticality,
            "technologies": technologies or [],
            "risk_score": 0.0,
            "vulnerabilities": [],
            "first_seen": now,
            "last_seen": now,
            "last_scanned_at": now
        }

        # Calculate initial risk based on risky ports
        risky_ports = [21, 22, 23, 3389, 5432, 27017, 9200]
        exposed_risky = [p for p in ports if p in risky_ports]
        if exposed_risky:
            asset["risk_score"] = min(10.0, 5.0 + len(exposed_risky) * 1.5)
            asset["vulnerabilities"].append(f"CRITICAL_INTERNAL_PORT_EXPOSED_{exposed_risky}")

        self._discovered_assets[asset_id] = asset
        return asset

    def discover_asset(
        self,
        asset_id: str,
        tenant_id: str,
        identifier: str,
        asset_type: str = "DOMAIN",
        discovery_method: str = "PASSIVE_DISCOVERY",
        confidence: float = 1.0,
        owner: str = "SecOps",
        criticality: str = "HIGH",
        open_ports: Optional[List[int]] = None,
        technologies: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        return self.register_public_asset(
            asset_id=asset_id,
            tenant_id=tenant_id,
            domain_or_ip=identifier,
            asset_type=asset_type,
            discovery_method=discovery_method,
            confidence=confidence,
            owner=owner,
            criticality=criticality,
            open_ports=open_ports,
            technologies=technologies
        )

    # Domain Intelligence (Section 28)
    def record_domain_intelligence(
        self,
        domain: str,
        tenant_id: str,
        dns_records: Dict[str, Any],
        registrar: Optional[str] = None,
        hosting_provider: Optional[str] = None,
        subdomains: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        intel = {
            "domain": domain,
            "tenant_id": tenant_id,
            "dns_records": dns_records,
            "registrar": registrar,
            "hosting_provider": hosting_provider,
            "subdomains": subdomains or [],
            "first_seen": now,
            "last_seen": now
        }
        self._domain_intel[domain] = intel
        return intel

    # Certificate Intelligence (Section 29)
    def record_certificate_intelligence(
        self,
        fingerprint: str,
        tenant_id: str,
        subject: str,
        issuer: str,
        san_list: List[str],
        valid_until: str,
        is_expired: bool = False,
        mismatch_detected: bool = False
    ) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc)
        record = {
            "fingerprint": fingerprint,
            "tenant_id": tenant_id,
            "subject": subject,
            "issuer": issuer,
            "san_list": san_list,
            "valid_until": valid_until,
            "is_expired": is_expired,
            "mismatch_detected": mismatch_detected,
            "last_verified_at": now.isoformat()
        }
        self._certificate_intel[fingerprint] = record
        return record

    # Technology Fingerprinting (Section 31)
    def fingerprint_technology(
        self,
        asset_id: str,
        tenant_id: str,
        framework: str,
        server: str,
        version: Optional[str] = None,
        confidence: float = 0.95
    ) -> Dict[str, Any]:
        fingerprint = {
            "asset_id": asset_id,
            "tenant_id": tenant_id,
            "web_framework": framework,
            "web_server": server,
            "detected_version": version,
            "confidence": confidence,
            "fingerprinted_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._service_fingerprints[asset_id] = fingerprint
        return fingerprint

    # Shadow IT Detection (Section 27)
    def detect_shadow_it(self, tenant_id: str) -> List[Dict[str, Any]]:
        tenant_assets = [a for a in self._discovered_assets.values() if a["tenant_id"] == tenant_id]
        return [a for a in tenant_assets if not a.get("is_managed", True)]

    def scan_attack_surface(self, tenant_id: str) -> Dict[str, Any]:
        tenant_assets = [a for a in self._discovered_assets.values() if a["tenant_id"] == tenant_id]
        total_assets = len(tenant_assets)
        risky_assets = [a for a in tenant_assets if a["risk_score"] >= 5.0]
        unmanaged_assets = [a for a in tenant_assets if not a.get("is_managed", True)]

        result = {
            "tenant_id": tenant_id,
            "total_assets_scanned": total_assets,
            "high_risk_assets_count": len(risky_assets),
            "shadow_it_count": len(unmanaged_assets),
            "assets": tenant_assets,
            "scan_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._scan_history.append(result)
        return result

    def get_discovered_assets(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [a for a in self._discovered_assets.values() if a["tenant_id"] == tenant_id]

    def discover_asset(
        self,
        asset_id: str,
        tenant_id: str,
        asset_type: str,
        identifier: str,
        discovery_method: str = "PASSIVE_DISCOVERY",
        confidence: float = 1.0,
        owner: str = "SecOps",
        **kwargs
    ) -> Dict[str, Any]:
        is_shadow = (owner == "UNKNOWN")
        is_managed = not is_shadow
        res = self.register_public_asset(
            asset_id=asset_id,
            tenant_id=tenant_id,
            domain_or_ip=identifier,
            asset_type=asset_type,
            discovery_method=discovery_method,
            confidence=confidence,
            owner=owner,
            is_managed=is_managed,
            **kwargs
        )
        res["is_shadow_it"] = is_shadow
        return res

    def get_external_assets(self, tenant_id: str) -> List[Dict[str, Any]]:
        return self.get_discovered_assets(tenant_id)


external_attack_surface_engine = ExternalAttackSurfaceEngine()

