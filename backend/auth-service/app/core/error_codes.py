from enum import Enum


class AuthErrorCode(str, Enum):
    INVALID_CREDENTIALS = "TSX-AUTH-001"
    EMAIL_NOT_VERIFIED = "TSX-AUTH-002"
    TOKEN_EXPIRED = "TSX-AUTH-003"
    TOKEN_REVOKED = "TSX-AUTH-004"
    ACCOUNT_DISABLED = "TSX-AUTH-005"
    RATE_LIMIT_EXCEEDED = "TSX-AUTH-006"
    NOT_FOUND = "TSX-AUTH-007"
    WEAK_PASSWORD = "TSX-AUTH-008"
    VALIDATION_ERROR = "TSX-AUTH-009"
    UNAUTHORIZED = "TSX-AUTH-010"
    FORBIDDEN = "TSX-AUTH-011"
    INTERNAL_ERROR = "TSX-AUTH-999"


class AudioErrorCode(str, Enum):
    VALIDATION_ERROR = "TSX-AUDIO-100"
    INFERENCE_ERROR = "TSX-AUDIO-200"
    REPOSITORY_ERROR = "TSX-AUDIO-300"
    API_ERROR = "TSX-AUDIO-400"
    UNEXPECTED_ERROR = "TSX-AUDIO-500"


class ApkErrorCode(str, Enum):
    INVALID_APK = "TSX-APK-001"
    CORRUPTED_ARCHIVE = "TSX-APK-002"
    APK_TOO_LARGE = "TSX-APK-003"
    ZIP_BOMB_DETECTED = "TSX-APK-004"
    INVALID_MIME = "TSX-APK-005"
    PATH_TRAVERSAL_DETECTED = "TSX-APK-006"
    CRC_FAILURE = "TSX-APK-007"
    MALFORMED_ZIP = "TSX-APK-008"
    UNSUPPORTED_APK_VARIANT = "TSX-APK-009"
    UNEXPECTED_FAILURE = "TSX-APK-010"
    UPLOAD_FAILED = "TSX-APK-100"
    VALIDATION_FAILED = "TSX-APK-101"
    PARSER_FAILED = "TSX-APK-102"
    DATABASE_FAILED = "TSX-APK-103"
    SCAN_NOT_FOUND = "TSX-APK-104"
    PERMISSION_DENIED = "TSX-APK-105"
    HISTORY_FETCH_FAILED = "TSX-APK-106"
    DELETE_FAILED = "TSX-APK-107"
    REPOSITORY_FAILURE = "TSX-APK-108"
    UNEXPECTED_ERROR = "TSX-APK-109"


ERROR_DESCRIPTIONS = {
    AuthErrorCode.INVALID_CREDENTIALS: "Invalid email or password.",
    AuthErrorCode.EMAIL_NOT_VERIFIED: "Email address is not verified. Please verify your email before logging in.",
    AuthErrorCode.TOKEN_EXPIRED: "Authentication token has expired.",
    AuthErrorCode.TOKEN_REVOKED: "Authentication token has been revoked or reused.",
    AuthErrorCode.ACCOUNT_DISABLED: "User account is suspended or inactive.",
    AuthErrorCode.RATE_LIMIT_EXCEEDED: "Too many authentication requests. Please try again later.",
    AuthErrorCode.NOT_FOUND: "Requested resource or user profile not found.",
    AuthErrorCode.WEAK_PASSWORD: "Password does not meet required complexity standards.",
    AuthErrorCode.VALIDATION_ERROR: "Invalid request payload or query parameters.",
    AuthErrorCode.UNAUTHORIZED: "Authentication credentials were not provided or are invalid.",
    AuthErrorCode.FORBIDDEN: "You do not have permission to access this resource.",
    AuthErrorCode.INTERNAL_ERROR: "An internal server error occurred. Please contact system administrator.",
    AudioErrorCode.VALIDATION_ERROR: "Audio file validation failed (corrupted file, unsupported format, or invalid sample rate).",
    AudioErrorCode.INFERENCE_ERROR: "Neural voice clone inference pipeline error.",
    AudioErrorCode.REPOSITORY_ERROR: "Database persistence error while saving voice clone analysis.",
    AudioErrorCode.API_ERROR: "Audio REST API endpoint request error or scan ID not found.",
    AudioErrorCode.UNEXPECTED_ERROR: "An unexpected error occurred during audio scan processing.",
    ApkErrorCode.INVALID_APK: "Invalid Android package archive.",
    ApkErrorCode.CORRUPTED_ARCHIVE: "APK ZIP archive structure is corrupted.",
    ApkErrorCode.APK_TOO_LARGE: "APK file size exceeds the 100 MB maximum threshold.",
    ApkErrorCode.ZIP_BOMB_DETECTED: "Potential ZIP bomb or excessive compression ratio detected.",
    ApkErrorCode.INVALID_MIME: "MIME type is not a valid Android package archive.",
    ApkErrorCode.PATH_TRAVERSAL_DETECTED: "Malicious path traversal sequence detected in archive entry.",
    ApkErrorCode.CRC_FAILURE: "CRC-32 checksum mismatch detected in ZIP archive entry.",
    ApkErrorCode.MALFORMED_ZIP: "Malformed Central Directory or Local Header structure in APK.",
    ApkErrorCode.UNSUPPORTED_APK_VARIANT: "APK variant is currently unsupported (XAPK, APKM, AAB formats).",
    ApkErrorCode.UNEXPECTED_FAILURE: "An unexpected error occurred during APK validation.",
    ApkErrorCode.UPLOAD_FAILED: "APK file upload processing failed.",
    ApkErrorCode.VALIDATION_FAILED: "APK upload security validation failed.",
    ApkErrorCode.PARSER_FAILED: "APK component parsing failed.",
    ApkErrorCode.DATABASE_FAILED: "Database error while persisting APK metadata.",
    ApkErrorCode.SCAN_NOT_FOUND: "Target APK scan ID was not found.",
    ApkErrorCode.PERMISSION_DENIED: "You do not have permission to access or modify this APK scan record.",
    ApkErrorCode.HISTORY_FETCH_FAILED: "Error fetching user APK scan history.",
    ApkErrorCode.DELETE_FAILED: "Error deleting APK scan records and physical storage artifact.",
    ApkErrorCode.REPOSITORY_FAILURE: "Database repository error during APK query execution.",
    ApkErrorCode.UNEXPECTED_ERROR: "An unexpected error occurred during APK REST API processing.",
}
