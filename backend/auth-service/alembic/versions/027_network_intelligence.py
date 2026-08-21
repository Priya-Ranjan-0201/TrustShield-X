"""Alembic Migration 027: Network Communication Schema (Phase 3.8 Part 1A.19).

Creates 19 network tables:
network_endpoints, network_domains, network_ips, network_operations, network_libraries,
network_sockets, network_dns, network_websockets, network_grpc, network_mqtt,
network_file_transfers, network_bluetooth, network_nfc, network_wifi, network_vpn,
network_proxies, network_authentication, network_graph, network_evidence
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 027_network_intelligence
Revises: 026_cryptography_intelligence
Create Date: 2026-08-10
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "027_network_intelligence"
down_revision: Union[str, None] = "026_cryptography_intelligence"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. network_endpoints
    op.create_table(
        "network_endpoints",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("url", sa.String(length=1024), nullable=False),
        sa.Column("scheme", sa.String(length=32), nullable=False, server_default="'https'"),
        sa.Column("host", sa.String(length=256), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False, server_default="443"),
        sa.Column("path", sa.String(length=512), nullable=True),
        sa.Column("query", sa.String(length=512), nullable=True),
        sa.Column("source_class", sa.String(length=256), nullable=False),
        sa.Column("source_method", sa.String(length=512), nullable=False),
        sa.Column("is_cleartext", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("library", sa.String(length=128), nullable=False, server_default="'Unknown'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_endpoints_scan_id", "network_endpoints", ["scan_id"])
    op.create_index("ix_network_endpoints_host", "network_endpoints", ["host"])

    # 2. network_domains
    op.create_table(
        "network_domains",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("domain", sa.String(length=256), nullable=False),
        sa.Column("domain_type", sa.String(length=64), nullable=False, server_default="'FQDN'"),
        sa.Column("root_domain", sa.String(length=256), nullable=True),
        sa.Column("source_method", sa.String(length=512), nullable=False),
        sa.Column("protocol", sa.String(length=32), nullable=False, server_default="'HTTPS'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_domains_scan_id", "network_domains", ["scan_id"])
    op.create_index("ix_network_domains_domain", "network_domains", ["domain"])

    # 3. network_ips
    op.create_table(
        "network_ips",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("ip_address", sa.String(length=64), nullable=False),
        sa.Column("ip_version", sa.String(length=16), nullable=False, server_default="'IPv4'"),
        sa.Column("is_private", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_loopback", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("source_method", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_ips_scan_id", "network_ips", ["scan_id"])

    # 4. network_operations
    op.create_table(
        "network_operations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("operation_type", sa.String(length=64), nullable=False),
        sa.Column("http_method", sa.String(length=16), nullable=True),
        sa.Column("target_url", sa.String(length=1024), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_operations_scan_id", "network_operations", ["scan_id"])

    # 5. network_libraries
    op.create_table(
        "network_libraries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("library_name", sa.String(length=128), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=True),
        sa.Column("detection_evidence", sa.String(length=256), nullable=False),
        sa.Column("dex_location", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_libraries_scan_id", "network_libraries", ["scan_id"])

    # 6. network_sockets
    op.create_table(
        "network_sockets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("socket_type", sa.String(length=32), nullable=False, server_default="'TCP'"),
        sa.Column("host", sa.String(length=256), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False),
        sa.Column("is_server", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_sockets_scan_id", "network_sockets", ["scan_id"])

    # 7. network_dns
    op.create_table(
        "network_dns",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("domain", sa.String(length=256), nullable=False),
        sa.Column("resolution_method", sa.String(length=128), nullable=False),
        sa.Column("is_doh", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_dot", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_dns_scan_id", "network_dns", ["scan_id"])

    # 8. network_websockets
    op.create_table(
        "network_websockets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("endpoint", sa.String(length=512), nullable=False),
        sa.Column("subprotocol", sa.String(length=128), nullable=True),
        sa.Column("library", sa.String(length=128), nullable=False, server_default="'OkHttp WebSocket'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_websockets_scan_id", "network_websockets", ["scan_id"])

    # 9. network_grpc
    op.create_table(
        "network_grpc",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("service_name", sa.String(length=256), nullable=False),
        sa.Column("method_name", sa.String(length=256), nullable=False),
        sa.Column("host", sa.String(length=256), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False, server_default="443"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_grpc_scan_id", "network_grpc", ["scan_id"])

    # 10. network_mqtt
    op.create_table(
        "network_mqtt",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("broker_url", sa.String(length=512), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False, server_default="1883"),
        sa.Column("topic", sa.String(length=256), nullable=True),
        sa.Column("qos", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_mqtt_scan_id", "network_mqtt", ["scan_id"])

    # 11. network_file_transfers
    op.create_table(
        "network_file_transfers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("protocol", sa.String(length=32), nullable=False, server_default="'SFTP'"),
        sa.Column("host", sa.String(length=256), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False, server_default="22"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_file_transfers_scan_id", "network_file_transfers", ["scan_id"])

    # 12. network_bluetooth
    op.create_table(
        "network_bluetooth",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("bluetooth_type", sa.String(length=32), nullable=False, server_default="'BLE'"),
        sa.Column("uuid", sa.String(length=128), nullable=True),
        sa.Column("operation", sa.String(length=64), nullable=False, server_default="'DISCOVERY'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_bluetooth_scan_id", "network_bluetooth", ["scan_id"])

    # 13. network_nfc
    op.create_table(
        "network_nfc",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("technology", sa.String(length=64), nullable=False, server_default="'NDEF'"),
        sa.Column("action", sa.String(length=64), nullable=False, server_default="'READ'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_nfc_scan_id", "network_nfc", ["scan_id"])

    # 14. network_wifi
    op.create_table(
        "network_wifi",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("wifi_feature", sa.String(length=64), nullable=False, server_default="'WIFI_MANAGER'"),
        sa.Column("ssid", sa.String(length=128), nullable=True, server_default="'[REDACTED_SSID]'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_wifi_scan_id", "network_wifi", ["scan_id"])

    # 15. network_vpn
    op.create_table(
        "network_vpn",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("vpn_service", sa.String(length=256), nullable=False, server_default="'android.net.VpnService'"),
        sa.Column("tunnel_config", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_vpn_scan_id", "network_vpn", ["scan_id"])

    # 16. network_proxies
    op.create_table(
        "network_proxies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("proxy_type", sa.String(length=32), nullable=False, server_default="'HTTP'"),
        sa.Column("host", sa.String(length=256), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False, server_default="8080"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_proxies_scan_id", "network_proxies", ["scan_id"])

    # 17. network_authentication
    op.create_table(
        "network_authentication",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("auth_type", sa.String(length=64), nullable=False, server_default="'BEARER'"),
        sa.Column("header_name", sa.String(length=128), nullable=False, server_default="'Authorization'"),
        sa.Column("redacted_token", sa.String(length=256), nullable=False, server_default="'[REDACTED_BEARER_TOKEN]'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_authentication_scan_id", "network_authentication", ["scan_id"])

    # 18. network_graph
    op.create_table(
        "network_graph",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_node", sa.String(length=512), nullable=False),
        sa.Column("target_node", sa.String(length=512), nullable=False),
        sa.Column("relationship", sa.String(length=64), nullable=False, server_default="'CONNECTS_TO'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_graph_scan_id", "network_graph", ["scan_id"])

    # 19. network_evidence
    op.create_table(
        "network_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("dex_id", sa.String(length=128), nullable=False),
        sa.Column("class_name", sa.String(length=256), nullable=False),
        sa.Column("method_name", sa.String(length=256), nullable=False),
        sa.Column("instruction_offset", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("evidence_type", sa.String(length=64), nullable=False, server_default="'URL_STRING'"),
        sa.Column("raw_evidence", sa.String(length=1024), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_network_evidence_scan_id", "network_evidence", ["scan_id"])


def downgrade() -> None:
    for tbl in [
        "network_evidence", "network_graph", "network_authentication", "network_proxies",
        "network_vpn", "network_wifi", "network_nfc", "network_bluetooth",
        "network_file_transfers", "network_mqtt", "network_grpc", "network_websockets",
        "network_dns", "network_sockets", "network_libraries", "network_operations",
        "network_ips", "network_domains", "network_endpoints",
    ]:
        op.drop_index(f"ix_{tbl}_scan_id", table_name=tbl)
        op.drop_table(tbl)
