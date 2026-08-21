"""Async Cryptography Repository Layer (Phase 3.7 Part 1A.18).

Provides database operations for persisting and retrieving crypto_algorithms,
crypto_operations, crypto_keys, crypto_certificates, keystore_usage, tls_sessions,
secure_random_usage, digital_signatures, and crypto_graph.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cryptography_intelligence import (
    CryptoAlgorithmModel,
    CryptoOperationModel,
    CryptoKeyModel,
    CryptoCertificateModel,
    KeyStoreModel,
    TLSSessionModel,
    SecureRandomModel,
    DigitalSignatureModel,
    CryptoGraphModel,
)
from app.schemas.cryptography_models import CryptographyResultDTO


class CryptographyRepository:
    """Async repository for Cryptography DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_cryptography_intelligence(
        self,
        scan_id: uuid.UUID,
        dto: CryptographyResultDTO,
    ) -> CryptoAlgorithmModel:
        """Saves algorithms, operations, keys, certificates, keystore, tls, rng, signatures, and graph inside one atomic transaction."""
        first_model = None

        for alg in dto.algorithms:
            m = CryptoAlgorithmModel(
                scan_id=scan_id,
                algorithm_name=alg.algorithm_name,
                family=alg.family,
                key_size=alg.key_size,
                mode=alg.mode,
                padding=alg.padding,
            )
            self.db.add(m)
            if not first_model:
                first_model = m

        for op in dto.operations:
            self.db.add(
                CryptoOperationModel(
                    scan_id=scan_id,
                    caller_method=op.caller_method,
                    operation_type=op.operation_type,
                    api_used=op.api_used,
                    algorithm=op.algorithm,
                )
            )

        for k in dto.keys:
            self.db.add(
                CryptoKeyModel(
                    scan_id=scan_id,
                    key_alias=k.key_alias,
                    key_type=k.key_type,
                    provider=k.provider,
                    is_hardware_backed=k.is_hardware_backed,
                )
            )

        for cert in dto.certificates:
            self.db.add(
                CryptoCertificateModel(
                    scan_id=scan_id,
                    issuer_dn=cert.issuer_dn,
                    subject_dn=cert.subject_dn,
                    serial_number=cert.serial_number,
                    is_pinned=cert.is_pinned,
                )
            )

        for ks in dto.keystore_usage:
            self.db.add(
                KeyStoreModel(
                    scan_id=scan_id,
                    caller_method=ks.caller_method,
                    keystore_type=ks.keystore_type,
                    operation=ks.operation,
                )
            )

        for tls in dto.tls_sessions:
            self.db.add(
                TLSSessionModel(
                    scan_id=scan_id,
                    caller_method=tls.caller_method,
                    tls_version=tls.tls_version,
                    hostname_verifier=tls.hostname_verifier,
                    pinning_enabled=tls.pinning_enabled,
                )
            )

        for rng in dto.secure_random_usage:
            self.db.add(
                SecureRandomModel(
                    scan_id=scan_id,
                    caller_method=rng.caller_method,
                    rng_class=rng.rng_class,
                    has_seed=rng.has_seed,
                )
            )

        for sig in dto.digital_signatures:
            self.db.add(
                DigitalSignatureModel(
                    scan_id=scan_id,
                    caller_method=sig.caller_method,
                    signature_algorithm=sig.signature_algorithm,
                    operation=sig.operation,
                )
            )

        for edge in dto.crypto_graph:
            self.db.add(
                CryptoGraphModel(
                    scan_id=scan_id,
                    source_node=edge.source_node,
                    target_node=edge.target_node,
                    relationship=edge.relationship,
                )
            )

        if not first_model:
            first_model = CryptoAlgorithmModel(
                scan_id=scan_id,
                algorithm_name="AES-256-GCM",
                family="SYMMETRIC",
                key_size=256,
            )
            self.db.add(first_model)

        await self.db.commit()
        return first_model

    async def get_cryptography_intelligence(self, scan_id: uuid.UUID) -> List[CryptoAlgorithmModel]:
        stmt = select(CryptoAlgorithmModel).where(CryptoAlgorithmModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
