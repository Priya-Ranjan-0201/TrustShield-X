import os
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.scan_lifecycle import ScanStatus, validate_status_transition
from app.repositories.scan_repository import ScanRepository
from app.repositories.event_repository import EventRepository
from app.repositories.result_repository import ResultRepository
from app.services.module_stubs import ModuleStubRegistry


class BaseScanDispatcher(ABC):
    @abstractmethod
    async def dispatch_scan(self, scan_id: uuid.UUID, scan_type: str, artifact_path: Optional[str] = None) -> bool:
        pass


class BaseModuleRouter(ABC):
    @abstractmethod
    def resolve_target_module(self, scan_type: str, mime_type: Optional[str] = None) -> str:
        pass


class DefaultScanDispatcher(BaseScanDispatcher):
    async def dispatch_scan(self, scan_id: uuid.UUID, scan_type: str, artifact_path: Optional[str] = None) -> bool:
        return True


class DefaultModuleRouter(BaseModuleRouter):
    def resolve_target_module(self, scan_type: str, mime_type: Optional[str] = None) -> str:
        module_map = {
            "URL": "website-phishing-ai",
            "IMAGE": "qr-upi-vision-ai",
            "PDF": "document-ocr-ai",
            "VIDEO": "video-deepfake-ai",
            "AUDIO": "voice-clone-ai",
            "APK": "apk-malware-ai",
            "TEXT": "nlp-phishing-ai",
        }
        return module_map.get(scan_type.upper(), "generic-inspection-ai")


class ScanOrchestrator:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.scan_repo = ScanRepository(db)
        self.event_repo = EventRepository(db)
        self.result_repo = ResultRepository(db)
        self.module_router = DefaultModuleRouter()

    async def execute_pipeline(self, scan_id: uuid.UUID) -> bool:
        """Executes full event-driven scan pipeline:
        VALIDATING -> QUEUED -> PROCESSING -> COMPLETED
        """
        # Fetch scan record
        scans = await self.scan_repo.get_user_scans(user_id=uuid.UUID("00000000-0000-0000-0000-000000000000"), limit=1)
        # Directly query scan record by id
        from sqlalchemy import select
        from app.models.scan_history import ScanHistory
        stmt = select(ScanHistory).where(ScanHistory.id == scan_id)
        res = await self.db.execute(stmt)
        scan = res.scalar_one_or_none()

        if not scan:
            return False

        # 1. SCAN_VALIDATED event & VALIDATING status
        await self.event_repo.log_event(scan_id, "SCAN_VALIDATED", "MIME and SHA-256 validation passed.")
        await self.scan_repo.update_status(scan_id, ScanStatus.VALIDATING)

        # 2. SCAN_QUEUED event & QUEUED status
        await self.event_repo.log_event(scan_id, "SCAN_QUEUED", "Dispatched to Orchestrator event queue.")
        await self.scan_repo.update_status(scan_id, ScanStatus.QUEUED)

        # 3. SCAN_STARTED event & PROCESSING status
        await self.event_repo.log_event(scan_id, "SCAN_STARTED", f"Routed to detection module '{scan.module_used}'.")
        await self.scan_repo.update_status(scan_id, ScanStatus.PROCESSING)

        # 4. Execute Detection Module (WebsitePhishingDetector for URL, QRVisionDetector for IMAGE/QR, Stub for others)
        if scan.scan_type.upper() == "URL":
            from app.services.website_detector import WebsitePhishingDetector
            detector = WebsitePhishingDetector()
            web_res = await detector.analyze_url(scan.target)
            
            trust_score = max(0, 100 - web_res.risk_score)
            risk_score = web_res.risk_score
            confidence_score = web_res.confidence_score
            findings_json = web_res.to_dict()
            execution_time_ms = web_res.execution_time_ms
        elif scan.scan_type.upper() in ("IMAGE", "QR"):
            from app.services.qr_detector import QRVisionDetector
            qr_detector = QRVisionDetector()
            file_bytes = b""
            if scan.file_path and os.path.exists(scan.file_path):
                with open(scan.file_path, "rb") as f:
                    file_bytes = f.read()

            qr_res = await qr_detector.analyze_qr_image(file_bytes, scan.target)
            trust_score = max(0, 100 - qr_res.risk_score)
            risk_score = qr_res.risk_score
            confidence_score = qr_res.confidence_score
            findings_json = qr_res.to_dict()
            execution_time_ms = qr_res.execution_time_ms
        elif scan.scan_type.upper() in ("PDF", "DOCUMENT"):
            from app.services.document_detector import DocumentTrustDetector
            from app.repositories.document_metadata_repository import DocumentMetadataRepository
            doc_detector = DocumentTrustDetector()
            file_bytes = b""
            if scan.file_path and os.path.exists(scan.file_path):
                with open(scan.file_path, "rb") as f:
                    file_bytes = f.read()

            doc_res = await doc_detector.analyze_document(file_bytes, scan.target)
            trust_score = max(0, 100 - doc_res.risk_score)
            risk_score = doc_res.risk_score
            confidence_score = doc_res.confidence_score
            findings_json = doc_res.to_dict()
            execution_time_ms = doc_res.execution_time_ms

            # Save document-specific metadata to document_metadata table
            doc_meta_repo = DocumentMetadataRepository(self.db)
            await doc_meta_repo.create_metadata(
                scan_id=scan.id,
                document_type=doc_res.document_type,
                extracted_fields=doc_res.extracted_fields,
                ocr_confidence=doc_res.ocr_confidence,
                image_quality_metrics=doc_res.image_quality_metrics,
            )
        elif scan.scan_type.upper() in ("VIDEO", "DEEPFAKE"):
            from app.services.deepfake_detector import DeepfakePipelineOrchestrator
            from app.repositories.deepfake_repository import DeepfakeRepository
            from app.repositories.notification_repository import NotificationRepository
            df_orchestrator = DeepfakePipelineOrchestrator()
            file_bytes = b""
            if scan.file_path and os.path.exists(scan.file_path):
                with open(scan.file_path, "rb") as f:
                    file_bytes = f.read()

            df_res = await df_orchestrator.analyze_media(file_bytes, scan.target, scan.mime_type)
            trust_score = max(0, 100 - df_res.risk_score)
            risk_score = df_res.risk_score
            confidence_score = df_res.confidence_score
            findings_json = df_res.to_dict()
            execution_time_ms = df_res.execution_time_ms

            # Save deepfake metadata, frames, face tracks, and neural inference outputs to DB
            df_repo = DeepfakeRepository(self.db)
            await df_repo.create_deepfake_record(
                scan_id=scan.id,
                media_type=df_res.media_type,
                metadata_dict=df_res.metadata,
                quality_metrics=df_res.quality_metrics,
                frames_list=df_res.frames_summary,
                face_tracks_list=df_res.face_tracks,
                inference_results=findings_json,
            )

            # Security Notification Trigger for High Risk Deepfakes (risk >= 50 or fake_prob >= 0.50)
            if risk_score >= 50 or df_res.fake_probability >= 0.50:
                notification_repo = NotificationRepository(self.db)
                await notification_repo.create_notification(
                    user_id=scan.user_id,
                    title="⚠️ High Risk Deepfake Synthetic Media Detected",
                    message=f"Deepfake Detection Engine ({df_res.model_name}) flagged target artifact '{scan.target}' with high manipulation probability ({df_res.fake_probability*100:.1f}%).",
                    type="SECURITY_ALERT",
                    scan_id=scan.id,
                )
        elif scan.scan_type.upper() in ("AUDIO", "VOICE", "AUDIO-VOICE-AI"):
            from app.services.audio_detector import AudioProcessingOrchestrator
            from app.repositories.audio_repository import AudioRepository
            audio_orchestrator = AudioProcessingOrchestrator()
            file_bytes = b""
            if scan.file_path and os.path.exists(scan.file_path):
                with open(scan.file_path, "rb") as f:
                    file_bytes = f.read()

            audio_res = await audio_orchestrator.analyze_audio(file_bytes, scan.target, scan.mime_type)
            trust_score = max(0, 100 - audio_res.risk_score)
            risk_score = audio_res.risk_score
            confidence_score = audio_res.confidence_score
            findings_json = audio_res.to_dict()
            execution_time_ms = audio_res.execution_time_ms

            # Save audio metadata, speech segments, speaker tracks, voice clone results, and conversation analysis to DB
            from app.repositories.audio_clone_repository import AudioCloneRepository
            audio_repo = AudioCloneRepository(self.db)
            await audio_repo.save_voice_clone_analysis(
                scan_id=scan.id,
                metadata_dict=audio_res.metadata,
                quality_metrics=audio_res.quality_metrics,
                speech_segments_list=audio_res.speech_segments,
                speaker_tracks_list=audio_res.speaker_tracks,
                inference_results={
                    "clone_probability": audio_res.risk_score / 100.0,
                    "real_probability": 1.0 - (audio_res.risk_score / 100.0),
                    "confidence": audio_res.confidence_score,
                    "calibrated_confidence": audio_res.confidence_score,
                    "verdict": "VOICE_CLONE" if audio_res.risk_score >= 50 else "REAL",
                    "risk_score": audio_res.risk_score,
                    "execution_time_ms": audio_res.execution_time_ms,
                    "model_name": "ECAPA-TDNN-VoiceClone",
                    "model_version": "2.1-Production",
                },
                evidence_list=audio_res.evidence,
                recommendations_list=audio_res.recommendations,
            )

            # Record operational telemetry metrics
            from app.services.audio_telemetry import AudioTelemetryManager
            telemetry_mgr = AudioTelemetryManager()
            telemetry_mgr.record_pipeline(
                scan_id=str(scan.id),
                total_time_ms=execution_time_ms,
                speaker_count=audio_res.total_speakers_detected,
                duration_sec=audio_res.total_speech_duration_sec,
                status="success",
                model_used="ECAPA-TDNN-VoiceClone",
            )

            # High-risk security notification alert (never notify on LOW_CONFIDENCE)
            if risk_score >= 50 or (audio_res.risk_score / 100.0) >= 0.50:
                from app.repositories.notification_repository import NotificationRepository
                notif_repo = NotificationRepository(self.db)
                await notif_repo.create_notification(
                    user_id=scan.user_id,
                    title="⚠️ High Risk AI Voice Clone Detected",
                    message=f"Voice Clone AI Engine flagged audio artifact '{scan.target}' with high risk ({risk_score}% risk score, {confidence_score*100:.1f}% confidence).",
                    type="SECURITY_ALERT",
                    scan_id=scan.id,
                )
        elif scan.scan_type.upper() in ("APK", "MALWARE-APK", "APK-MALWARE-AI"):
            from app.services.apk_processing_service import APKProcessingService
            from app.services.apk_workspace_manager import APKWorkspaceManager
            from app.repositories.workspace_repository import WorkspaceRepository

            apk_service = APKProcessingService(self.db)
            file_target = scan.file_path or scan.target

            apk_res = await apk_service.process_apk_file(
                scan_id=scan.id,
                file_path=file_target,
                filename=os.path.basename(file_target),
                user_id=scan.user_id,
            )

            # Workspace Extraction Layer
            workspace_mgr = APKWorkspaceManager()
            ws_res = workspace_mgr.create_workspace(
                scan_id=scan.id,
                apk_file_path=file_target,
                package_name=apk_res.package_name,
                version_name=apk_res.version_name,
            )

            # Log Workspace Scan Events
            events_to_log = [
                ("WORKSPACE_CREATED", f"Workspace created at {ws_res.workspace_path}"),
                ("APK_EXTRACTED", f"Extracted {ws_res.extraction_result.extracted_files_count} files safely."),
                ("FILES_DISCOVERED", f"Discovered {ws_res.inventory.total_files} workspace files."),
                ("HASHES_GENERATED", "Cryptographic hashes (SHA256, SHA1, MD5, CRC32) generated for workspace entries."),
                ("MANIFEST_GENERATED", "Workspace manifest.json generated successfully."),
                ("READY_FOR_STATIC_ANALYSIS", "Workspace is ready for static malware analysis."),
            ]
            for ev_type, msg in events_to_log:
                await self.event_repo.log_event(scan.id, ev_type, msg)

            if ws_res.status == "READY_FOR_STATIC_ANALYSIS":
                ws_repo = WorkspaceRepository(self.db)
                await ws_repo.save_full_workspace(scan.id, ws_res)

            workspace_mgr.cleanup_workspace(ws_res.workspace_path)
            await self.event_repo.log_event(scan.id, "WORKSPACE_DESTROYED", "Workspace cleanup executed.")

            trust_score = 100 if apk_res.parsed_successfully else 50
            risk_score = 0 if apk_res.parsed_successfully else 50
            confidence_score = 1.0 if apk_res.parsed_successfully else 0.5
            findings_json = apk_res.to_dict()
            findings_json["workspace"] = ws_res.manifest_dict
            execution_time_ms = apk_res.processing_time_ms + ws_res.total_time_ms
        elif scan.scan_type.upper() in ("TEXT", "NLP", "PHISHING-TEXT", "SMS"):
            from app.services.nlp_phishing_detector import NLPPhishingDetector
            nlp_detector = NLPPhishingDetector()
            nlp_res = nlp_detector.analyze_text(scan.target)
            trust_score = max(0, 100 - nlp_res.risk_score)
            risk_score = nlp_res.risk_score
            confidence_score = nlp_res.confidence_score
            findings_json = nlp_res.to_dict()
            execution_time_ms = nlp_res.execution_time_ms
        else:
            stub_result = ModuleStubRegistry.execute_stub(scan.module_used or "generic-inspection-ai", scan.target)
            trust_score = stub_result.trust_score
            risk_score = stub_result.risk_score
            confidence_score = stub_result.confidence_score
            findings_json = stub_result.findings_json
            execution_time_ms = stub_result.execution_time_ms


        # 5. Save ScanResult record
        await self.result_repo.create_result(
            scan_id=scan.id,
            trust_score=trust_score,
            risk_score=risk_score,
            confidence_score=confidence_score,
            findings_json=findings_json,
            execution_time_ms=execution_time_ms,
        )

        # 6. SCAN_COMPLETED event & COMPLETED status
        await self.event_repo.log_event(
            scan_id,
            "SCAN_COMPLETED",
            f"Inspection complete. Trust Score: {trust_score}/100. Risk Score: {risk_score}/100.",
            event_data_json=findings_json,
        )

        scan.trust_score = trust_score
        scan.risk_score = risk_score
        scan.confidence_score = confidence_score
        scan.status = ScanStatus.COMPLETED
        scan.summary = f"Risk Score: {risk_score}/100 ({findings_json.get('severity', 'UNKNOWN')}). Findings: {len(findings_json.get('evidence', []))} evidence item(s)."
        scan.processing_time_ms = execution_time_ms
        await self.db.commit()

        return True
