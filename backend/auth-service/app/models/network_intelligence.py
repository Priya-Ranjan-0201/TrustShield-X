"""SQLAlchemy 2.0 ORM Models for Enterprise Network Communication Intelligence Engine (Phase 3.8 Part 1A.19).

Defines database models for 19 network intelligence tables:
network_endpoints, network_domains, network_ips, network_operations, network_libraries,
network_sockets, network_dns, network_websockets, network_grpc, network_mqtt,
network_file_transfers, network_bluetooth, network_nfc, network_wifi, network_vpn,
network_proxies, network_authentication, network_graph, network_evidence.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class NetworkEndpointModel(Base):
    __tablename__ = "network_endpoints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    url: Mapped[str] = mapped_column(String(1024), nullable=False, index=True)
    scheme: Mapped[str] = mapped_column(String(32), nullable=False, default="https")
    host: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    port: Mapped[int] = mapped_column(Integer, nullable=False, default=443)
    path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    query: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    source_class: Mapped[str] = mapped_column(String(256), nullable=False)
    source_method: Mapped[str] = mapped_column(String(512), nullable=False)
    is_cleartext: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    library: Mapped[str] = mapped_column(String(128), nullable=False, default="Unknown")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkDomainModel(Base):
    __tablename__ = "network_domains"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    domain: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    domain_type: Mapped[str] = mapped_column(String(64), nullable=False, default="FQDN")
    root_domain: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    source_method: Mapped[str] = mapped_column(String(512), nullable=False)
    protocol: Mapped[str] = mapped_column(String(32), nullable=False, default="HTTPS")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkIPModel(Base):
    __tablename__ = "network_ips"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    ip_address: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    ip_version: Mapped[str] = mapped_column(String(16), nullable=False, default="IPv4")
    is_private: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_loopback: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    source_method: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkOperationModel(Base):
    __tablename__ = "network_operations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    operation_type: Mapped[str] = mapped_column(String(64), nullable=False)
    http_method: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    target_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkLibraryModel(Base):
    __tablename__ = "network_libraries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    library_name: Mapped[str] = mapped_column(String(128), nullable=False)
    version: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    detection_evidence: Mapped[str] = mapped_column(String(256), nullable=False)
    dex_location: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkSocketModel(Base):
    __tablename__ = "network_sockets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    socket_type: Mapped[str] = mapped_column(String(32), nullable=False, default="TCP")
    host: Mapped[str] = mapped_column(String(256), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    is_server: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkDNSModel(Base):
    __tablename__ = "network_dns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    domain: Mapped[str] = mapped_column(String(256), nullable=False)
    resolution_method: Mapped[str] = mapped_column(String(128), nullable=False)
    is_doh: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_dot: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkWebSocketModel(Base):
    __tablename__ = "network_websockets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    endpoint: Mapped[str] = mapped_column(String(512), nullable=False)
    subprotocol: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    library: Mapped[str] = mapped_column(String(128), nullable=False, default="OkHttp WebSocket")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkGrpcModel(Base):
    __tablename__ = "network_grpc"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    service_name: Mapped[str] = mapped_column(String(256), nullable=False)
    method_name: Mapped[str] = mapped_column(String(256), nullable=False)
    host: Mapped[str] = mapped_column(String(256), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False, default=443)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkMqttModel(Base):
    __tablename__ = "network_mqtt"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    broker_url: Mapped[str] = mapped_column(String(512), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False, default=1883)
    topic: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    qos: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkFileTransferModel(Base):
    __tablename__ = "network_file_transfers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    protocol: Mapped[str] = mapped_column(String(32), nullable=False, default="SFTP")
    host: Mapped[str] = mapped_column(String(256), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False, default=22)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkBluetoothModel(Base):
    __tablename__ = "network_bluetooth"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    bluetooth_type: Mapped[str] = mapped_column(String(32), nullable=False, default="BLE")
    uuid: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    operation: Mapped[str] = mapped_column(String(64), nullable=False, default="DISCOVERY")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkNfcModel(Base):
    __tablename__ = "network_nfc"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    technology: Mapped[str] = mapped_column(String(64), nullable=False, default="NDEF")
    action: Mapped[str] = mapped_column(String(64), nullable=False, default="READ")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkWifiModel(Base):
    __tablename__ = "network_wifi"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    wifi_feature: Mapped[str] = mapped_column(String(64), nullable=False, default="WIFI_MANAGER")
    ssid: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, default="[REDACTED_SSID]")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkVpnModel(Base):
    __tablename__ = "network_vpn"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    vpn_service: Mapped[str] = mapped_column(String(256), nullable=False, default="android.net.VpnService")
    tunnel_config: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkProxyModel(Base):
    __tablename__ = "network_proxies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    proxy_type: Mapped[str] = mapped_column(String(32), nullable=False, default="HTTP")
    host: Mapped[str] = mapped_column(String(256), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False, default=8080)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkAuthenticationModel(Base):
    __tablename__ = "network_authentication"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    auth_type: Mapped[str] = mapped_column(String(64), nullable=False, default="BEARER")
    header_name: Mapped[str] = mapped_column(String(128), nullable=False, default="Authorization")
    redacted_token: Mapped[str] = mapped_column(String(256), nullable=False, default="[REDACTED_BEARER_TOKEN]")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkGraphModel(Base):
    __tablename__ = "network_graph"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_node: Mapped[str] = mapped_column(String(512), nullable=False)
    target_node: Mapped[str] = mapped_column(String(512), nullable=False)
    relationship: Mapped[str] = mapped_column(String(64), nullable=False, default="CONNECTS_TO")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NetworkEvidenceModel(Base):
    __tablename__ = "network_evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    dex_id: Mapped[str] = mapped_column(String(128), nullable=False)
    class_name: Mapped[str] = mapped_column(String(256), nullable=False)
    method_name: Mapped[str] = mapped_column(String(256), nullable=False)
    instruction_offset: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    evidence_type: Mapped[str] = mapped_column(String(64), nullable=False, default="URL_STRING")
    raw_evidence: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
