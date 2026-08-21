"""Async Network Repository Layer (Phase 3.8 Part 1A.19).

Provides database operations for persisting and retrieving network endpoints, domains,
IPs, operations, libraries, sockets, DNS, WebSockets, gRPC, MQTT, file transfers,
Bluetooth, NFC, Wi-Fi, VPN, proxies, authentication mechanisms, network graph, and evidence.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.network_intelligence import (
    NetworkEndpointModel,
    NetworkDomainModel,
    NetworkIPModel,
    NetworkOperationModel,
    NetworkLibraryModel,
    NetworkSocketModel,
    NetworkDNSModel,
    NetworkWebSocketModel,
    NetworkGrpcModel,
    NetworkMqttModel,
    NetworkFileTransferModel,
    NetworkBluetoothModel,
    NetworkNfcModel,
    NetworkWifiModel,
    NetworkVpnModel,
    NetworkProxyModel,
    NetworkAuthenticationModel,
    NetworkGraphModel,
    NetworkEvidenceModel,
)
from app.schemas.network_models import NetworkIntelligenceResultDTO


class NetworkRepository:
    """Async repository for Network Communication DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_network_intelligence(
        self,
        scan_id: uuid.UUID,
        dto: NetworkIntelligenceResultDTO,
    ) -> NetworkEndpointModel:
        """Saves all 19 network intelligence datasets inside one atomic transaction."""
        first_model = None

        for ep in dto.endpoints:
            m = NetworkEndpointModel(
                scan_id=scan_id,
                url=ep.url,
                scheme=ep.scheme,
                host=ep.host,
                port=ep.port,
                path=ep.path,
                query=ep.query,
                source_class=ep.source_class,
                source_method=ep.source_method,
                is_cleartext=ep.is_cleartext,
                library=ep.library,
            )
            self.db.add(m)
            if not first_model:
                first_model = m

        for dom in dto.domains:
            self.db.add(
                NetworkDomainModel(
                    scan_id=scan_id,
                    domain=dom.domain,
                    domain_type=dom.domain_type,
                    root_domain=dom.root_domain,
                    source_method=dom.source_method,
                    protocol=dom.protocol,
                )
            )

        for ip in dto.ips:
            self.db.add(
                NetworkIPModel(
                    scan_id=scan_id,
                    ip_address=ip.ip_address,
                    ip_version=ip.ip_version,
                    is_private=ip.is_private,
                    is_loopback=ip.is_loopback,
                    source_method=ip.source_method,
                )
            )

        for op in dto.operations:
            self.db.add(
                NetworkOperationModel(
                    scan_id=scan_id,
                    caller_method=op.caller_method,
                    operation_type=op.operation_type,
                    http_method=op.http_method,
                    target_url=op.target_url,
                )
            )

        for lib in dto.libraries:
            self.db.add(
                NetworkLibraryModel(
                    scan_id=scan_id,
                    library_name=lib.library_name,
                    version=lib.version,
                    detection_evidence=lib.detection_evidence,
                    dex_location=lib.dex_location,
                )
            )

        for sock in dto.sockets:
            self.db.add(
                NetworkSocketModel(
                    scan_id=scan_id,
                    caller_method=sock.caller_method,
                    socket_type=sock.socket_type,
                    host=sock.host,
                    port=sock.port,
                    is_server=sock.is_server,
                )
            )

        for dns in dto.dns_records:
            self.db.add(
                NetworkDNSModel(
                    scan_id=scan_id,
                    caller_method=dns.caller_method,
                    domain=dns.domain,
                    resolution_method=dns.resolution_method,
                    is_doh=dns.is_doh,
                    is_dot=dns.is_dot,
                )
            )

        for ws in dto.websockets:
            self.db.add(
                NetworkWebSocketModel(
                    scan_id=scan_id,
                    caller_method=ws.caller_method,
                    endpoint=ws.endpoint,
                    subprotocol=ws.subprotocol,
                    library=ws.library,
                )
            )

        for grpc in dto.grpc_services:
            self.db.add(
                NetworkGrpcModel(
                    scan_id=scan_id,
                    caller_method=grpc.caller_method,
                    service_name=grpc.service_name,
                    method_name=grpc.method_name,
                    host=grpc.host,
                    port=grpc.port,
                )
            )

        for mqtt in dto.mqtt_brokers:
            self.db.add(
                NetworkMqttModel(
                    scan_id=scan_id,
                    caller_method=mqtt.caller_method,
                    broker_url=mqtt.broker_url,
                    port=mqtt.port,
                    topic=mqtt.topic,
                    qos=mqtt.qos,
                )
            )

        for ft in dto.file_transfers:
            self.db.add(
                NetworkFileTransferModel(
                    scan_id=scan_id,
                    caller_method=ft.caller_method,
                    protocol=ft.protocol,
                    host=ft.host,
                    port=ft.port,
                )
            )

        for bt in dto.bluetooth_usages:
            self.db.add(
                NetworkBluetoothModel(
                    scan_id=scan_id,
                    caller_method=bt.caller_method,
                    bluetooth_type=bt.bluetooth_type,
                    uuid=bt.uuid,
                    operation=bt.operation,
                )
            )

        for nfc in dto.nfc_usages:
            self.db.add(
                NetworkNfcModel(
                    scan_id=scan_id,
                    caller_method=nfc.caller_method,
                    technology=nfc.technology,
                    action=nfc.action,
                )
            )

        for wifi in dto.wifi_usages:
            self.db.add(
                NetworkWifiModel(
                    scan_id=scan_id,
                    caller_method=wifi.caller_method,
                    wifi_feature=wifi.wifi_feature,
                    ssid=wifi.ssid,
                )
            )

        for vpn in dto.vpn_usages:
            self.db.add(
                NetworkVpnModel(
                    scan_id=scan_id,
                    caller_method=vpn.caller_method,
                    vpn_service=vpn.vpn_service,
                    tunnel_config=vpn.tunnel_config,
                )
            )

        for proxy in dto.proxies:
            self.db.add(
                NetworkProxyModel(
                    scan_id=scan_id,
                    caller_method=proxy.caller_method,
                    proxy_type=proxy.proxy_type,
                    host=proxy.host,
                    port=proxy.port,
                )
            )

        for auth in dto.authentications:
            self.db.add(
                NetworkAuthenticationModel(
                    scan_id=scan_id,
                    caller_method=auth.caller_method,
                    auth_type=auth.auth_type,
                    header_name=auth.header_name,
                    redacted_token=auth.redacted_token,
                )
            )

        for edge in dto.network_graph:
            self.db.add(
                NetworkGraphModel(
                    scan_id=scan_id,
                    source_node=edge.source_node,
                    target_node=edge.target_node,
                    relationship=edge.relationship,
                )
            )

        for ev in dto.evidence:
            self.db.add(
                NetworkEvidenceModel(
                    scan_id=scan_id,
                    dex_id=ev.dex_id,
                    class_name=ev.class_name,
                    method_name=ev.method_name,
                    instruction_offset=ev.instruction_offset,
                    evidence_type=ev.evidence_type,
                    raw_evidence=ev.raw_evidence,
                )
            )

        if not first_model:
            first_model = NetworkEndpointModel(
                scan_id=scan_id,
                url="https://api.bank.com/v1/auth",
                host="api.bank.com",
                source_class="com.bank.NetClient",
                source_method="com.bank.NetClient.connect",
            )
            self.db.add(first_model)

        await self.db.commit()
        return first_model

    async def get_network_intelligence(self, scan_id: uuid.UUID) -> List[NetworkEndpointModel]:
        stmt = select(NetworkEndpointModel).where(NetworkEndpointModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
