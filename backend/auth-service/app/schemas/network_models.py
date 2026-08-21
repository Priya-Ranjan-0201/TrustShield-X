"""Pydantic v2 DTO Schemas for Enterprise Network Communication Intelligence Engine (Phase 3.8 Part 1A.19).

Strictly typed DTOs for endpoints, domains, IPs, network operations, libraries,
sockets, DNS, WebSockets, gRPC, MQTT, FTP, Bluetooth, NFC, Wi-Fi, VPN, Proxies,
authentication mechanisms, network graph, evidence, metrics, and result DTO.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class NetworkEndpointDTO(BaseModel):
    url: str
    scheme: str = "https"
    host: str
    port: int = 443
    path: Optional[str] = "/"
    query: Optional[str] = None
    source_class: str
    source_method: str
    is_cleartext: bool = False
    library: str = "Unknown"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkDomainDTO(BaseModel):
    domain: str
    domain_type: str = "FQDN"  # FQDN, SUBDOMAIN, ROOT, LOCALHOST, INTERNAL
    root_domain: Optional[str] = None
    source_method: str
    protocol: str = "HTTPS"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkIPDTO(BaseModel):
    ip_address: str
    ip_version: str = "IPv4"  # IPv4, IPv6
    is_private: bool = False
    is_loopback: bool = False
    source_method: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkOperationDTO(BaseModel):
    caller_method: str
    operation_type: str  # HTTP_REQUEST, SOCKET_CONNECT, DNS_LOOKUP
    http_method: Optional[str] = "GET"
    target_url: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkLibraryDTO(BaseModel):
    library_name: str  # OkHttp, Retrofit, Volley, Cronet, Netty, gRPC, Paho
    version: Optional[str] = "Unknown"
    detection_evidence: str
    dex_location: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkSocketDTO(BaseModel):
    caller_method: str
    socket_type: str = "TCP"  # TCP, UDP, SSL_SOCKET, NIO
    host: str
    port: int
    is_server: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkDNSDTO(BaseModel):
    caller_method: str
    domain: str
    resolution_method: str = "InetAddress.getByName"
    is_doh: bool = False
    is_dot: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkWebSocketDTO(BaseModel):
    caller_method: str
    endpoint: str
    subprotocol: Optional[str] = None
    library: str = "OkHttp WebSocket"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkGrpcDTO(BaseModel):
    caller_method: str
    service_name: str
    method_name: str
    host: str
    port: int = 443

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkMqttDTO(BaseModel):
    caller_method: str
    broker_url: str
    port: int = 1883
    topic: Optional[str] = None
    qos: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkFileTransferDTO(BaseModel):
    caller_method: str
    protocol: str = "SFTP"  # FTP, FTPS, SFTP
    host: str
    port: int = 22

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkBluetoothDTO(BaseModel):
    caller_method: str
    bluetooth_type: str = "BLE"  # CLASSIC, BLE
    uuid: Optional[str] = None
    operation: str = "DISCOVERY"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkNfcDTO(BaseModel):
    caller_method: str
    technology: str = "NDEF"  # NDEF, ISO_DEP, MIFARE
    action: str = "READ"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkWifiDTO(BaseModel):
    caller_method: str
    wifi_feature: str = "WIFI_DIRECT"  # WIFI_MANAGER, WIFI_DIRECT, P2P
    ssid: Optional[str] = "[REDACTED_SSID]"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkVpnDTO(BaseModel):
    caller_method: str
    vpn_service: str = "android.net.VpnService"
    tunnel_config: Optional[str] = "TUN_INTERFACE"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkProxyDTO(BaseModel):
    caller_method: str
    proxy_type: str = "HTTP"  # HTTP, HTTPS, SOCKS, PAC
    host: str
    port: int

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkAuthenticationDTO(BaseModel):
    caller_method: str
    auth_type: str = "BEARER"  # BASIC, BEARER, OAUTH2, API_KEY, MTLS
    header_name: str = "Authorization"
    redacted_token: str = "[REDACTED_BEARER_TOKEN]"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkGraphEdgeDTO(BaseModel):
    source_node: str
    target_node: str
    relationship: str = "CONNECTS_TO"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkEvidenceDTO(BaseModel):
    dex_id: str
    class_name: str
    method_name: str
    instruction_offset: int = 0
    evidence_type: str = "URL_STRING"
    raw_evidence: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkMetricsDTO(BaseModel):
    endpoints_count: int = 0
    domains_count: int = 0
    ips_count: int = 0
    libraries_count: int = 0
    cleartext_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NetworkIntelligenceResultDTO(BaseModel):
    endpoints: List[NetworkEndpointDTO] = Field(default_factory=list)
    domains: List[NetworkDomainDTO] = Field(default_factory=list)
    ips: List[NetworkIPDTO] = Field(default_factory=list)
    operations: List[NetworkOperationDTO] = Field(default_factory=list)
    libraries: List[NetworkLibraryDTO] = Field(default_factory=list)
    sockets: List[NetworkSocketDTO] = Field(default_factory=list)
    dns_records: List[NetworkDNSDTO] = Field(default_factory=list)
    websockets: List[NetworkWebSocketDTO] = Field(default_factory=list)
    grpc_services: List[NetworkGrpcDTO] = Field(default_factory=list)
    mqtt_brokers: List[NetworkMqttDTO] = Field(default_factory=list)
    file_transfers: List[NetworkFileTransferDTO] = Field(default_factory=list)
    bluetooth_usages: List[NetworkBluetoothDTO] = Field(default_factory=list)
    nfc_usages: List[NetworkNfcDTO] = Field(default_factory=list)
    wifi_usages: List[NetworkWifiDTO] = Field(default_factory=list)
    vpn_usages: List[NetworkVpnDTO] = Field(default_factory=list)
    proxies: List[NetworkProxyDTO] = Field(default_factory=list)
    authentications: List[NetworkAuthenticationDTO] = Field(default_factory=list)
    network_graph: List[NetworkGraphEdgeDTO] = Field(default_factory=list)
    evidence: List[NetworkEvidenceDTO] = Field(default_factory=list)
    metrics: NetworkMetricsDTO = Field(default_factory=NetworkMetricsDTO)
    json_export: Optional[str] = None
    csv_export: Optional[str] = None
    graphml_export: Optional[str] = None
    dot_export: Optional[str] = None
    mermaid_export: Optional[str] = None
    analysis_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
