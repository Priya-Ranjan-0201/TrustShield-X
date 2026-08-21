"""FastAPI REST API Router for AI Android APK Security Engine (Phase 3.7 Part 1A Message 3C.1).

Endpoints:
- POST /api/v1/apk/scan: Upload & parse Android APK
- GET /api/v1/apk/{scan_id}: Retrieve complete APK component analysis
- GET /api/v1/apk/history: Paginated, filtered user APK scan history
- DELETE /api/v1/apk/{scan_id}: Delete scan records and physical storage artifact
"""

import os
import uuid
import tempfile
import shutil
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.error_codes import ApkErrorCode, ERROR_DESCRIPTIONS
from app.api.deps import get_current_user, get_trace_id
from app.models.user import User
from app.schemas.envelope import ResponseEnvelope
from app.schemas.apk import (
    APKResponse,
    APKManifestDTO,
    APKPermissionDTO,
    APKDEXDTO,
    APKLibraryDTO,
    APKCertificateDTO,
    APKResourceDTO,
    APKHistoryItem,
    APKHistoryResponse,
    APKDeleteResponse,
)
from app.services.apk_processing_service import APKProcessingService
from app.repositories.apk_repository import APKRepository
from app.repositories.scan_repository import ScanRepository

router = APIRouter()


@router.post(
    "/scan",
    response_model=ResponseEnvelope[APKResponse],
    status_code=status.HTTP_200_OK,
    summary="Upload & Parse Android APK File",
    description="Uploads an Android APK archive file (up to 100MB), executes passive security validation, extracts AndroidManifest components, DEX inventory, native libraries, resources, and X.509 certificates, and persists records.",
)
async def upload_and_scan_apk(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
):
    filename = file.filename or "app.apk"
    if not filename.lower().endswith(".apk"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{ApkErrorCode.INVALID_APK}: Only .apk files are supported.",
        )

    scan_repo = ScanRepository(db)
    scan_record = await scan_repo.create_scan(
        user_id=current_user.id,
        target=filename,
        scan_type="APK",
        mime_type=file.content_type or "application/vnd.android.package-archive",
        module_used="apk-malware-ai",
    )

    # Save to temporary buffer for streaming validation
    temp_dir = tempfile.mkdtemp(prefix="tsx_apk_api_")
    temp_file_path = os.path.join(temp_dir, filename)

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        service = APKProcessingService(db)
        proc_result = await service.process_apk_file(
            scan_id=scan_record.id,
            file_path=temp_file_path,
            filename=filename,
            user_id=current_user.id,
            trace_id=trace_id,
        )

        if not proc_result.parsed_successfully:
            err_msg = proc_result.errors[0] if proc_result.errors else "APK validation or processing failed."
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{ApkErrorCode.VALIDATION_FAILED}: {err_msg}",
            )

        # Build Response DTO
        manifest_dto = None
        if proc_result.manifest:
            manifest_dto = APKManifestDTO(
                package_name=proc_result.package_name,
                version_name=proc_result.version_name,
                version_code=proc_result.version_code,
                min_sdk=proc_result.manifest.application_flags.get("min_sdk"),
                target_sdk=proc_result.manifest.application_flags.get("target_sdk"),
                permissions_count=len(proc_result.manifest.permissions),
                activities_count=len(proc_result.manifest.activities),
                services_count=len(proc_result.manifest.services),
                receivers_count=len(proc_result.manifest.receivers),
                providers_count=len(proc_result.manifest.providers),
                deep_links=proc_result.manifest.deep_links,
            )

        perm_dtos = [APKPermissionDTO(permission_name=p.name, protection_level=p.protection_level, declared_by_app=p.declared_by_app) for p in proc_result.permissions]
        dex_dtos = [APKDEXDTO(filename=d.filename, sha256=d.sha256, size=d.size, method_count=d.method_count, class_count=d.class_count) for d in (proc_result.dex_inventory.dex_files if proc_result.dex_inventory else [])]
        lib_dtos = [APKLibraryDTO(library_name=l.library_name, architecture=l.architecture, sha256=l.sha256, size=l.size) for l in (proc_result.native_libraries.libraries if proc_result.native_libraries else [])]
        cert_dtos = []
        if proc_result.certificates and not proc_result.certificates.certificate_unavailable and proc_result.certificates.sha256:
            cert_dtos.append(
                APKCertificateDTO(
                    subject=proc_result.certificates.subject,
                    issuer=proc_result.certificates.issuer,
                    serial_number=proc_result.certificates.serial_number,
                    signature_algorithm=proc_result.certificates.signature_algorithm,
                    public_key_algorithm=proc_result.certificates.public_key_algorithm,
                    public_key_size=proc_result.certificates.public_key_size,
                    sha256=proc_result.certificates.sha256,
                    sha1=proc_result.certificates.sha1,
                    valid_from=proc_result.certificates.valid_from,
                    valid_until=proc_result.certificates.valid_until,
                    expired=proc_result.certificates.expired,
                    self_signed=proc_result.certificates.self_signed,
                )
            )

        res_dto = None
        if proc_result.resource_inventory:
            res_dto = APKResourceDTO(
                resource_count=proc_result.resource_inventory.resource_count,
                asset_count=proc_result.resource_inventory.asset_count,
                xml_count=proc_result.resource_inventory.xml_count,
                image_count=proc_result.resource_inventory.image_count,
                font_count=proc_result.resource_inventory.font_count,
                audio_count=proc_result.resource_inventory.audio_count,
                video_count=proc_result.resource_inventory.video_count,
                binary_count=proc_result.resource_inventory.binary_count,
                largest_resource_name=proc_result.resource_inventory.largest_resource_name,
                largest_resource_bytes=proc_result.resource_inventory.largest_resource_bytes,
                average_resource_size_bytes=proc_result.resource_inventory.average_resource_size_bytes,
            )

        response_data = APKResponse(
            scan_id=str(scan_record.id),
            package_name=proc_result.package_name,
            version_name=proc_result.version_name,
            version_code=proc_result.version_code,
            apk_size=os.path.getsize(temp_file_path),
            apk_sha256="",
            parsed_successfully=True,
            manifest=manifest_dto,
            permissions=perm_dtos,
            dex_files=dex_dtos,
            native_libraries=lib_dtos,
            certificates=cert_dtos,
            resources=res_dto,
            processing_time_ms=proc_result.processing_time_ms,
        )

        return ResponseEnvelope.success_response(
            data=response_data,
            message="APK scanned and parsed successfully.",
            trace_id=trace_id,
        )

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@router.get(
    "/{scan_id}",
    response_model=ResponseEnvelope[APKResponse],
    summary="Retrieve Stored APK Component Analysis",
    description="Retrieves complete stored metadata, Manifest components, DEX inventory, native libraries, certificates, and resources for target scan ID.",
)
async def get_apk_analysis(
    scan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
):
    scan_repo = ScanRepository(db)
    scan_record = await scan_repo.get_user_scans(user_id=current_user.id, limit=1)
    
    apk_repo = APKRepository(db)
    apk_model = await apk_repo.get_apk_by_scan(scan_id)

    if not apk_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{ApkErrorCode.SCAN_NOT_FOUND}: APK scan ID '{scan_id}' not found.",
        )

    # Build Response DTO
    perm_dtos = [APKPermissionDTO(permission_name=p.permission_name, protection_level=p.protection_level, declared_by_app=p.declared_by_app) for p in apk_model.permissions]
    dex_dtos = [APKDEXDTO(filename=d.filename, sha256=d.sha256, size=d.size, method_count=d.method_count, class_count=d.class_count) for d in apk_model.dex_files]
    lib_dtos = [APKLibraryDTO(library_name=l.library_name, architecture=l.architecture, sha256=l.sha256, size=l.size) for l in apk_model.native_libraries]
    cert_dtos = [
        APKCertificateDTO(
            subject=c.subject,
            issuer=c.issuer,
            sha256=c.sha256,
            sha1=c.sha1,
            signature_algorithm=c.signature_algorithm,
            public_key_algorithm=c.public_key_algorithm,
            key_size=c.key_size,
            valid_from=c.valid_from,
            valid_until=c.valid_until,
            expired=c.expired,
            self_signed=c.self_signed,
        )
        for c in apk_model.certificates
    ]

    response_data = APKResponse(
        scan_id=str(apk_model.scan_id),
        package_name=apk_model.package_name,
        version_name=apk_model.version_name,
        version_code=apk_model.version_code,
        application_label=apk_model.application_label,
        min_sdk=apk_model.min_sdk,
        target_sdk=apk_model.target_sdk,
        compile_sdk=apk_model.compile_sdk,
        apk_size=apk_model.apk_size,
        apk_sha256=apk_model.apk_sha256,
        parsed_successfully=apk_model.parsed_successfully,
        permissions=perm_dtos,
        dex_files=dex_dtos,
        native_libraries=lib_dtos,
        certificates=cert_dtos,
        processing_time_ms=0,
    )

    return ResponseEnvelope.success_response(
        data=response_data,
        message="APK analysis retrieved successfully.",
        trace_id=trace_id,
    )


@router.get(
    "/history",
    response_model=ResponseEnvelope[APKHistoryResponse],
    summary="List User APK Scan History",
    description="Retrieves a paginated list of historical APK scans for the authenticated user.",
)
async def list_apk_history(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    package_name: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
):
    apk_repo = APKRepository(db)
    models = await apk_repo.list_user_apks(user_id=current_user.id, limit=limit, offset=offset)

    if package_name:
        models = [m for m in models if m.package_name and package_name.lower() in m.package_name.lower()]

    items = [
        APKHistoryItem(
            scan_id=str(m.scan_id),
            package_name=m.package_name,
            version_name=m.version_name,
            apk_size=m.apk_size,
            apk_sha256=m.apk_sha256,
            certificate_sha256=m.certificates[0].sha256 if m.certificates else None,
            parsed_successfully=m.parsed_successfully,
            created_at=m.created_at.isoformat(),
        )
        for m in models
    ]

    history_resp = APKHistoryResponse(
        total_count=len(items),
        limit=limit,
        offset=offset,
        items=items,
    )

    return ResponseEnvelope.success_response(
        data=history_resp,
        message="APK history retrieved successfully.",
        trace_id=trace_id,
    )


@router.delete(
    "/{scan_id}",
    response_model=ResponseEnvelope[APKDeleteResponse],
    summary="Delete APK Scan Records & File Artifact",
    description="Atomically deletes metadata, component inventories, scan history events, and physical storage file artifact.",
)
async def delete_apk_scan(
    scan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    trace_id: str = Depends(get_trace_id),
):
    scan_repo = ScanRepository(db)
    scan_record = await scan_repo.get_user_scans(user_id=current_user.id, limit=1)

    apk_repo = APKRepository(db)
    deleted = await apk_repo.delete_by_scan(scan_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{ApkErrorCode.SCAN_NOT_FOUND}: Scan ID '{scan_id}' not found or already deleted.",
        )

    del_resp = APKDeleteResponse(
        scan_id=str(scan_id),
        deleted=True,
        message="APK scan records and physical storage artifact deleted successfully.",
    )

    return ResponseEnvelope.success_response(
        data=del_resp,
        message="APK scan deleted successfully.",
        trace_id=trace_id,
    )
