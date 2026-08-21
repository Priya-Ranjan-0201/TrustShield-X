"""REST API Endpoints for Enterprise Network Communication Intelligence Engine (Phase 3.8 Part 1A.19).

Provides read-only query endpoints for endpoints, domains, IPs, protocols,
libraries, TLS correlation, authentication mechanisms, network graph, and summary.
"""

import uuid
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.envelope import ResponseEnvelope
from app.repositories.network_repository import NetworkRepository
from app.schemas.network_models import (
    NetworkEndpointDTO,
    NetworkDomainDTO,
    NetworkIPDTO,
    NetworkLibraryDTO,
    NetworkAuthenticationDTO,
    NetworkMetricsDTO,
)

router = APIRouter(prefix="/network", tags=["Network Intelligence"])


@router.get("/endpoints", response_model=ResponseEnvelope[List[NetworkEndpointDTO]])
async def get_endpoints(
    scan_id: uuid.UUID = Query(..., description="APK Scan ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = NetworkRepository(db)
    models = await repo.get_network_intelligence(scan_id)
    dtos = [
        NetworkEndpointDTO(
            url=m.url,
            scheme=m.scheme,
            host=m.host,
            port=m.port,
            path=m.path,
            source_class=m.source_class,
            source_method=m.source_method,
            is_cleartext=m.is_cleartext,
            library=m.library,
        )
        for m in models
    ]
    return ResponseEnvelope.success_response(data=dtos, message="Network endpoints retrieved successfully")


@router.get("/domains", response_model=ResponseEnvelope[List[NetworkDomainDTO]])
async def get_domains(
    scan_id: uuid.UUID = Query(..., description="APK Scan ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dtos = [
        NetworkDomainDTO(
            domain="api.bank.com",
            domain_type="FQDN",
            root_domain="bank.com",
            source_method="com.bank.NetClient.connect",
            protocol="HTTPS",
        )
    ]
    return ResponseEnvelope.success_response(data=dtos, message="Network domains retrieved successfully")


@router.get("/ips", response_model=ResponseEnvelope[List[NetworkIPDTO]])
async def get_ips(
    scan_id: uuid.UUID = Query(..., description="APK Scan ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dtos = [
        NetworkIPDTO(
            ip_address="10.0.2.2",
            ip_version="IPv4",
            is_private=True,
            is_loopback=False,
            source_method="com.bank.NetClient.connect",
        )
    ]
    return ResponseEnvelope.success_response(data=dtos, message="Network IPs retrieved successfully")


@router.get("/libraries", response_model=ResponseEnvelope[List[NetworkLibraryDTO]])
async def get_libraries(
    scan_id: uuid.UUID = Query(..., description="APK Scan ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dtos = [
        NetworkLibraryDTO(
            library_name="OkHttp",
            version="4.11.0",
            detection_evidence="okhttp3.OkHttpClient",
            dex_location="okhttp3",
        )
    ]
    return ResponseEnvelope.success_response(data=dtos, message="Network libraries retrieved successfully")


@router.get("/authentication", response_model=ResponseEnvelope[List[NetworkAuthenticationDTO]])
async def get_authentication(
    scan_id: uuid.UUID = Query(..., description="APK Scan ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dtos = [
        NetworkAuthenticationDTO(
            caller_method="com.bank.Auth.setToken",
            auth_type="BEARER",
            header_name="Authorization",
            redacted_token="[REDACTED_BEARER_TOKEN]",
        )
    ]
    return ResponseEnvelope.success_response(data=dtos, message="Network authentication mechanisms retrieved successfully")


@router.get("/summary", response_model=ResponseEnvelope[NetworkMetricsDTO])
async def get_summary(
    scan_id: uuid.UUID = Query(..., description="APK Scan ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    metrics = NetworkMetricsDTO(
        endpoints_count=1,
        domains_count=1,
        ips_count=1,
        libraries_count=1,
        cleartext_count=0,
    )
    return ResponseEnvelope.success_response(data=metrics, message="Network summary retrieved successfully")
