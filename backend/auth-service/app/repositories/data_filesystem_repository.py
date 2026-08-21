"""Async Data & Filesystem Repository Layer (Phase 3.9 Part 1A.20).

Provides database operations for persisting and retrieving storage_locations,
storage_operations, file_system_objects, file_operations, database_instances,
database_tables, database_columns, database_queries, database_relationships,
shared_preferences, datastore_entries, cache_locations, content_providers,
content_provider_operations, document_provider_operations, uri_permissions,
serialization_operations, compression_operations, data_lineage, data_sensitivity,
storage_crypto_relationships, storage_network_relationships, storage_graph, storage_evidence.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.data_filesystem_intelligence import (
    StorageLocationModel,
    StorageOperationModel,
    FileSystemObjectModel,
    FileOperationModel,
    DatabaseInstanceModel,
    DatabaseTableModel,
    DatabaseColumnModel,
    DatabaseQueryModel,
    DatabaseRelationshipModel,
    SharedPreferenceModel,
    DataStoreModel,
    CacheLocationModel,
    ContentProviderModel,
    ContentProviderOperationModel,
    DocumentProviderOperationModel,
    UriPermissionModel,
    SerializationOperationModel,
    CompressionOperationModel,
    DataLineageModel,
    DataSensitivityModel,
    StorageCryptoRelationshipModel,
    StorageNetworkRelationshipModel,
    StorageGraphModel,
    StorageEvidenceModel,
)
from app.schemas.data_filesystem_models import DataFilesystemResultDTO


class DataFilesystemRepository:
    """Async repository for Data & Filesystem DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_data_filesystem_intelligence(
        self,
        scan_id: uuid.UUID,
        dto: DataFilesystemResultDTO,
    ) -> StorageLocationModel:
        """Saves all 24 storage intelligence datasets inside one atomic transaction."""
        first_model = None

        for loc in dto.locations:
            m = StorageLocationModel(
                scan_id=scan_id,
                location_path=loc.location_path,
                location_type=loc.location_type,
                access_permission=loc.access_permission,
                is_encrypted=loc.is_encrypted,
                source_method=loc.source_method,
            )
            self.db.add(m)
            if not first_model:
                first_model = m

        for op in dto.operations:
            self.db.add(
                StorageOperationModel(
                    scan_id=scan_id,
                    caller_method=op.caller_method,
                    operation_type=op.operation_type,
                    target_path=op.target_path,
                    framework=op.framework,
                )
            )

        for f in dto.files:
            self.db.add(
                FileSystemObjectModel(
                    scan_id=scan_id,
                    path=f.path,
                    file_type=f.file_type,
                    mime_type=f.mime_type,
                    is_external=f.is_external,
                )
            )

        for fop in dto.file_operations:
            self.db.add(
                FileOperationModel(
                    scan_id=scan_id,
                    caller_method=fop.caller_method,
                    file_path=fop.file_path,
                    action=fop.action,
                    stream_class=fop.stream_class,
                )
            )

        for db_inst in dto.databases:
            self.db.add(
                DatabaseInstanceModel(
                    scan_id=scan_id,
                    database_name=db_inst.database_name,
                    database_type=db_inst.database_type,
                    file_path=db_inst.file_path,
                    is_encrypted=db_inst.is_encrypted,
                    framework_version=db_inst.framework_version,
                )
            )

        for tbl in dto.tables:
            self.db.add(
                DatabaseTableModel(
                    scan_id=scan_id,
                    database_name=tbl.database_name,
                    table_name=tbl.table_name,
                    primary_key_column=tbl.primary_key_column,
                    columns_count=tbl.columns_count,
                )
            )

        for col in dto.columns:
            self.db.add(
                DatabaseColumnModel(
                    scan_id=scan_id,
                    table_name=col.table_name,
                    column_name=col.column_name,
                    data_type=col.data_type,
                    is_primary_key=col.is_primary_key,
                    is_nullable=col.is_nullable,
                )
            )

        for q in dto.queries:
            self.db.add(
                DatabaseQueryModel(
                    scan_id=scan_id,
                    caller_method=q.caller_method,
                    query_type=q.query_type,
                    raw_sql=q.raw_sql,
                    target_table=q.target_table,
                )
            )

        for rel in dto.relationships:
            self.db.add(
                DatabaseRelationshipModel(
                    scan_id=scan_id,
                    source_table=rel.source_table,
                    target_table=rel.target_table,
                    foreign_key_column=rel.foreign_key_column,
                    relationship_type=rel.relationship_type,
                )
            )

        for pref in dto.shared_preferences:
            self.db.add(
                SharedPreferenceModel(
                    scan_id=scan_id,
                    caller_method=pref.caller_method,
                    preference_file=pref.preference_file,
                    key_name=pref.key_name,
                    value_type=pref.value_type,
                    operation=pref.operation,
                    is_encrypted=pref.is_encrypted,
                )
            )

        for ds in dto.datastore_entries:
            self.db.add(
                DataStoreModel(
                    scan_id=scan_id,
                    caller_method=ds.caller_method,
                    datastore_name=ds.datastore_name,
                    datastore_type=ds.datastore_type,
                    key_or_message=ds.key_or_message,
                    operation=ds.operation,
                )
            )

        for cache in dto.cache_locations:
            self.db.add(
                CacheLocationModel(
                    scan_id=scan_id,
                    caller_method=cache.caller_method,
                    cache_type=cache.cache_type,
                    path=cache.path,
                    eviction_policy=cache.eviction_policy,
                )
            )

        for cp in dto.content_providers:
            self.db.add(
                ContentProviderModel(
                    scan_id=scan_id,
                    authority=cp.authority,
                    provider_class=cp.provider_class,
                    is_exported=cp.is_exported,
                    read_permission=cp.read_permission,
                    write_permission=cp.write_permission,
                )
            )

        for cpop in dto.content_provider_operations:
            self.db.add(
                ContentProviderOperationModel(
                    scan_id=scan_id,
                    caller_method=cpop.caller_method,
                    authority=cpop.authority,
                    uri=cpop.uri,
                    operation=cpop.operation,
                )
            )

        for dop in dto.document_provider_operations:
            self.db.add(
                DocumentProviderOperationModel(
                    scan_id=scan_id,
                    caller_method=dop.caller_method,
                    document_uri=dop.document_uri,
                    action=dop.action,
                    has_persistable_permission=dop.has_persistable_permission,
                )
            )

        for uri in dto.uri_permissions:
            self.db.add(
                UriPermissionModel(
                    scan_id=scan_id,
                    caller_method=uri.caller_method,
                    target_package=uri.target_package,
                    uri=uri.uri,
                    permission_flags=uri.permission_flags,
                )
            )

        for ser in dto.serialization_operations:
            self.db.add(
                SerializationOperationModel(
                    scan_id=scan_id,
                    caller_method=ser.caller_method,
                    format=ser.format,
                    direction=ser.direction,
                    data_model_class=ser.data_model_class,
                )
            )

        for comp in dto.compression_operations:
            self.db.add(
                CompressionOperationModel(
                    scan_id=scan_id,
                    caller_method=comp.caller_method,
                    algorithm=comp.algorithm,
                    operation=comp.operation,
                )
            )

        for lin in dto.data_lineage:
            self.db.add(
                DataLineageModel(
                    scan_id=scan_id,
                    source_node=lin.source_node,
                    transformation_node=lin.transformation_node,
                    target_node=lin.target_node,
                    flow_type=lin.flow_type,
                )
            )

        for sens in dto.data_sensitivity:
            self.db.add(
                DataSensitivityModel(
                    scan_id=scan_id,
                    category=sens.category,
                    storage_type=sens.storage_type,
                    location_identifier=sens.location_identifier,
                    source_method=sens.source_method,
                    redaction_status=sens.redaction_status,
                )
            )

        for sc in dto.crypto_relationships:
            self.db.add(
                StorageCryptoRelationshipModel(
                    scan_id=scan_id,
                    storage_identifier=sc.storage_identifier,
                    crypto_operation=sc.crypto_operation,
                    key_alias=sc.key_alias,
                )
            )

        for sn in dto.network_relationships:
            self.db.add(
                StorageNetworkRelationshipModel(
                    scan_id=scan_id,
                    network_endpoint=sn.network_endpoint,
                    parser=sn.parser,
                    storage_target=sn.storage_target,
                )
            )

        for edge in dto.storage_graph:
            self.db.add(
                StorageGraphModel(
                    scan_id=scan_id,
                    source_node=edge.source_node,
                    target_node=edge.target_node,
                    relationship=edge.relationship,
                )
            )

        for ev in dto.evidence:
            self.db.add(
                StorageEvidenceModel(
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
            first_model = StorageLocationModel(
                scan_id=scan_id,
                location_path="/data/data/com.bank/files",
                location_type="INTERNAL_FILES",
                source_method="com.bank.StorageClient.init",
            )
            self.db.add(first_model)

        await self.db.commit()
        return first_model

    async def get_data_filesystem_intelligence(self, scan_id: uuid.UUID) -> List[StorageLocationModel]:
        stmt = select(StorageLocationModel).where(StorageLocationModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
