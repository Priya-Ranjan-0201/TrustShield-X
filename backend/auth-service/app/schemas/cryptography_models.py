"""Pydantic v2 DTO Schemas for Enterprise Cryptography & Secure Communication Intelligence Engine (Phase 3.7 Part 1A.18).

Strictly typed DTOs for algorithms, operations, keys, certificates, keystore usage,
TLS sessions, secure random usage, digital signatures, crypto graph, and metrics.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class CryptoAlgorithmDTO(BaseModel):
    algorithm_name: str  # AES, RSA, SHA-256, HMAC, etc.
    family: str = "SYMMETRIC"  # SYMMETRIC, ASYMMETRIC, HASH, MAC, KDF
    key_size: Optional[int] = None
    mode: Optional[str] = None  # GCM, CBC, CTR
    padding: Optional[str] = None  # PKCS5Padding, NoPadding

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CryptoOperationDTO(BaseModel):
    caller_method: str
    operation_type: str  # ENCRYPT, DECRYPT, HASH, SIGN, VERIFY, KEYGEN
    api_used: str  # javax.crypto.Cipher, java.security.MessageDigest
    algorithm: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CryptoKeyDTO(BaseModel):
    key_alias: Optional[str] = None
    key_type: str = "SECRET_KEY"  # SECRET_KEY, PRIVATE_KEY, PUBLIC_KEY
    provider: str = "AndroidKeyStore"
    is_hardware_backed: bool = True

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CryptoCertificateDTO(BaseModel):
    issuer_dn: str
    subject_dn: str
    serial_number: Optional[str] = None
    is_pinned: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class KeyStoreUsageDTO(BaseModel):
    caller_method: str
    keystore_type: str = "AndroidKeyStore"
    operation: str = "GET_KEY"  # GET_KEY, SET_KEY, DELETE_KEY

    model_config = ConfigDict(frozen=True, from_attributes=True)


class TLSSessionDTO(BaseModel):
    caller_method: str
    tls_version: str = "TLSv1.3"
    hostname_verifier: Optional[str] = "STRICT"
    pinning_enabled: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class SecureRandomUsageDTO(BaseModel):
    caller_method: str
    rng_class: str = "java.security.SecureRandom"
    has_seed: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DigitalSignatureDTO(BaseModel):
    caller_method: str
    signature_algorithm: str = "SHA256withRSA"
    operation: str = "SIGN"  # SIGN, VERIFY

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CryptoGraphEdgeDTO(BaseModel):
    source_node: str
    target_node: str
    relationship: str = "USES_ALGORITHM"  # USES_ALGORITHM, USES_KEY, PROTECTED_BY_TLS

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CryptoMetricsDTO(BaseModel):
    algorithms_count: int = 0
    operations_count: int = 0
    keys_count: int = 0
    tls_sessions_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CryptographyResultDTO(BaseModel):
    algorithms: List[CryptoAlgorithmDTO] = Field(default_factory=list)
    operations: List[CryptoOperationDTO] = Field(default_factory=list)
    keys: List[CryptoKeyDTO] = Field(default_factory=list)
    certificates: List[CryptoCertificateDTO] = Field(default_factory=list)
    keystore_usage: List[KeyStoreUsageDTO] = Field(default_factory=list)
    tls_sessions: List[TLSSessionDTO] = Field(default_factory=list)
    secure_random_usage: List[SecureRandomUsageDTO] = Field(default_factory=list)
    digital_signatures: List[DigitalSignatureDTO] = Field(default_factory=list)
    crypto_graph: List[CryptoGraphEdgeDTO] = Field(default_factory=list)
    metrics: CryptoMetricsDTO = Field(default_factory=CryptoMetricsDTO)
    json_export: Optional[str] = None
    csv_export: Optional[str] = None
    dot_export: Optional[str] = None
    mermaid_export: Optional[str] = None
    parsing_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
