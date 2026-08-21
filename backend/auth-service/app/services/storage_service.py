import os
import uuid
import hashlib
from abc import ABC, abstractmethod
from fastapi import UploadFile, HTTPException, status

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/webp",
    "video/mp4",
    "video/webm",
    "audio/mpeg",
    "audio/wav",
    "audio/ogg",
    "application/vnd.android.package-archive",
    "text/plain",
}

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB


class BaseStorageProvider(ABC):
    @abstractmethod
    async def save_file(
        self, user_id: uuid.UUID, file: UploadFile
    ) -> tuple[str, str, str, str, int]:
        """Returns: (stored_filename, full_file_path, sha256_checksum, content_type, file_size_bytes)"""
        pass

    @abstractmethod
    async def get_file(self, file_path: str) -> bytes:
        pass


class LocalStorageProvider(BaseStorageProvider):
    def __init__(self, base_dir: str | None = None):
        self.base_dir = base_dir or os.path.join(os.getcwd(), "storage", "uploads")

    async def save_file(
        self, user_id: uuid.UUID, file: UploadFile
    ) -> tuple[str, str, str, str, int]:
        filename = file.filename or "uploaded_file"

        # 1. Path traversal & double extension security checks
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filename containing malicious path characters.",
            )

        ext_parts = filename.split(".")
        if len(ext_parts) > 2:
            # Check for executable double extension attack e.g. script.php.png
            dangerous_exts = {"php", "exe", "bat", "sh", "js", "py", "pl", "cgi"}
            if any(ext.lower() in dangerous_exts for ext in ext_parts[:-1]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Double extension executable attempt blocked.",
                )

        # 2. Content Type / MIME Whitelist validation
        content_type = file.content_type or "application/octet-stream"
        if content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file MIME type: {content_type}.",
            )

        # 3. Read file contents and compute SHA-256 checksum & size
        contents = await file.read()
        file_size = len(contents)

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size {file_size / (1024*1024):.2f}MB exceeds 25MB maximum limit.",
            )

        sha256_checksum = hashlib.sha256(contents).hexdigest()

        # 4. Storage directory structure: storage/uploads/{user_id}/
        user_dir = os.path.join(self.base_dir, str(user_id))
        os.makedirs(user_dir, exist_ok=True)

        stored_filename = f"{uuid.uuid4()}_{filename}"
        full_path = os.path.join(user_dir, stored_filename)

        with open(full_path, "wb") as f:
            f.write(contents)

        return stored_filename, full_path, sha256_checksum, content_type, file_size

    async def get_file(self, file_path: str) -> bytes:
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requested file artifact not found.",
            )
        with open(file_path, "rb") as f:
            return f.read()
