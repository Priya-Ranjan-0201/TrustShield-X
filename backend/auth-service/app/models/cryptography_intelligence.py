"""SQLAlchemy 2.0 ORM Models for Enterprise Cryptography & Secure Communication Intelligence Engine (Phase 3.7 Part 1A.18).

Defines database models for crypto_algorithms, crypto_operations,
crypto_keys, crypto_certificates, keystore_usage, tls_sessions,
secure_random_usage, digital_signatures, and crypto_graph.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class CryptoAlgorithmModel(Base):
    __tablename__ = "crypto_algorithms"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    algorithm_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    family: Mapped[str] = mapped_column(String(64), nullable=False, default="SYMMETRIC")
    key_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mode: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    padding: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CryptoOperationModel(Base):
    __tablename__ = "crypto_operations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    operation_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    api_used: Mapped[str] = mapped_column(String(256), nullable=False)
    algorithm: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CryptoKeyModel(Base):
    __tablename__ = "crypto_keys"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    key_alias: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    key_type: Mapped[str] = mapped_column(String(64), nullable=False, default="SECRET_KEY")
    provider: Mapped[str] = mapped_column(String(128), nullable=False, default="AndroidKeyStore")
    is_hardware_backed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CryptoCertificateModel(Base):
    __tablename__ = "crypto_certificates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    issuer_dn: Mapped[str] = mapped_column(String(512), nullable=False)
    subject_dn: Mapped[str] = mapped_column(String(512), nullable=False)
    serial_number: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    is_pinned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class KeyStoreModel(Base):
    __tablename__ = "keystore_usage"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    keystore_type: Mapped[str] = mapped_column(String(128), nullable=False, default="AndroidKeyStore")
    operation: Mapped[str] = mapped_column(String(64), nullable=False, default="GET_KEY")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class TLSSessionModel(Base):
    __tablename__ = "tls_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    tls_version: Mapped[str] = mapped_column(String(64), nullable=False, default="TLSv1.3")
    hostname_verifier: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    pinning_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SecureRandomModel(Base):
    __tablename__ = "secure_random_usage"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    rng_class: Mapped[str] = mapped_column(String(256), nullable=False, default="java.security.SecureRandom")
    has_seed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DigitalSignatureModel(Base):
    __tablename__ = "digital_signatures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    caller_method: Mapped[str] = mapped_column(String(512), nullable=False)
    signature_algorithm: Mapped[str] = mapped_column(String(128), nullable=False, default="SHA256withRSA")
    operation: Mapped[str] = mapped_column(String(64), nullable=False, default="SIGN")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CryptoGraphModel(Base):
    __tablename__ = "crypto_graph"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    source_node: Mapped[str] = mapped_column(String(512), nullable=False)
    target_node: Mapped[str] = mapped_column(String(512), nullable=False)
    relationship: Mapped[str] = mapped_column(String(64), nullable=False, default="USES_ALGORITHM")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
