"""Alembic Migration 026: Cryptography & Secure Communication Schema (Phase 3.7 Part 1A.18).

Creates tables:
- crypto_algorithms
- crypto_operations
- crypto_keys
- crypto_certificates
- keystore_usage
- tls_sessions
- secure_random_usage
- digital_signatures
- crypto_graph
with ON DELETE CASCADE foreign key constraints and performance indexes.

Revision ID: 026_cryptography_intelligence
Revises: 025_reflection_intelligence
Create Date: 2026-08-10
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "026_cryptography_intelligence"
down_revision: Union[str, None] = "025_reflection_intelligence"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create crypto_algorithms table
    op.create_table(
        "crypto_algorithms",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("algorithm_name", sa.String(length=128), nullable=False),
        sa.Column("family", sa.String(length=64), nullable=False, server_default="'SYMMETRIC'"),
        sa.Column("key_size", sa.Integer(), nullable=True),
        sa.Column("mode", sa.String(length=64), nullable=True),
        sa.Column("padding", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_crypto_algorithms_scan_id", "crypto_algorithms", ["scan_id"])
    op.create_index("ix_crypto_algorithms_algorithm_name", "crypto_algorithms", ["algorithm_name"])

    # 2. Create crypto_operations table
    op.create_table(
        "crypto_operations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("operation_type", sa.String(length=64), nullable=False),
        sa.Column("api_used", sa.String(length=256), nullable=False),
        sa.Column("algorithm", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_crypto_operations_scan_id", "crypto_operations", ["scan_id"])
    op.create_index("ix_crypto_operations_caller_method", "crypto_operations", ["caller_method"])
    op.create_index("ix_crypto_operations_operation_type", "crypto_operations", ["operation_type"])

    # 3. Create crypto_keys table
    op.create_table(
        "crypto_keys",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("key_alias", sa.String(length=256), nullable=True),
        sa.Column("key_type", sa.String(length=64), nullable=False, server_default="'SECRET_KEY'"),
        sa.Column("provider", sa.String(length=128), nullable=False, server_default="'AndroidKeyStore'"),
        sa.Column("is_hardware_backed", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_crypto_keys_scan_id", "crypto_keys", ["scan_id"])

    # 4. Create crypto_certificates table
    op.create_table(
        "crypto_certificates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("issuer_dn", sa.String(length=512), nullable=False),
        sa.Column("subject_dn", sa.String(length=512), nullable=False),
        sa.Column("serial_number", sa.String(length=128), nullable=True),
        sa.Column("is_pinned", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_crypto_certificates_scan_id", "crypto_certificates", ["scan_id"])

    # 5. Create keystore_usage table
    op.create_table(
        "keystore_usage",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("keystore_type", sa.String(length=128), nullable=False, server_default="'AndroidKeyStore'"),
        sa.Column("operation", sa.String(length=64), nullable=False, server_default="'GET_KEY'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_keystore_usage_scan_id", "keystore_usage", ["scan_id"])

    # 6. Create tls_sessions table
    op.create_table(
        "tls_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("tls_version", sa.String(length=64), nullable=False, server_default="'TLSv1.3'"),
        sa.Column("hostname_verifier", sa.String(length=128), nullable=True),
        sa.Column("pinning_enabled", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_tls_sessions_scan_id", "tls_sessions", ["scan_id"])

    # 7. Create secure_random_usage table
    op.create_table(
        "secure_random_usage",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("rng_class", sa.String(length=256), nullable=False, server_default="'java.security.SecureRandom'"),
        sa.Column("has_seed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_secure_random_usage_scan_id", "secure_random_usage", ["scan_id"])

    # 8. Create digital_signatures table
    op.create_table(
        "digital_signatures",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("caller_method", sa.String(length=512), nullable=False),
        sa.Column("signature_algorithm", sa.String(length=128), nullable=False, server_default="'SHA256withRSA'"),
        sa.Column("operation", sa.String(length=64), nullable=False, server_default="'SIGN'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_digital_signatures_scan_id", "digital_signatures", ["scan_id"])

    # 9. Create crypto_graph table
    op.create_table(
        "crypto_graph",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_node", sa.String(length=512), nullable=False),
        sa.Column("target_node", sa.String(length=512), nullable=False),
        sa.Column("relationship", sa.String(length=64), nullable=False, server_default="'USES_ALGORITHM'"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_crypto_graph_scan_id", "crypto_graph", ["scan_id"])


def downgrade() -> None:
    op.drop_index("ix_crypto_graph_scan_id", table_name="crypto_graph")
    op.drop_table("crypto_graph")

    op.drop_index("ix_digital_signatures_scan_id", table_name="digital_signatures")
    op.drop_table("digital_signatures")

    op.drop_index("ix_secure_random_usage_scan_id", table_name="secure_random_usage")
    op.drop_table("secure_random_usage")

    op.drop_index("ix_tls_sessions_scan_id", table_name="tls_sessions")
    op.drop_table("tls_sessions")

    op.drop_index("ix_keystore_usage_scan_id", table_name="keystore_usage")
    op.drop_table("keystore_usage")

    op.drop_index("ix_crypto_certificates_scan_id", table_name="crypto_certificates")
    op.drop_table("crypto_certificates")

    op.drop_index("ix_crypto_keys_scan_id", table_name="crypto_keys")
    op.drop_table("crypto_keys")

    op.drop_index("ix_crypto_operations_operation_type", table_name="crypto_operations")
    op.drop_index("ix_crypto_operations_caller_method", table_name="crypto_operations")
    op.drop_index("ix_crypto_operations_scan_id", table_name="crypto_operations")
    op.drop_table("crypto_operations")

    op.drop_index("ix_crypto_algorithms_algorithm_name", table_name="crypto_algorithms")
    op.drop_index("ix_crypto_algorithms_scan_id", table_name="crypto_algorithms")
    op.drop_table("crypto_algorithms")
