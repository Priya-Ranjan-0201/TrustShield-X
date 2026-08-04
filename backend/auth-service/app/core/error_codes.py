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
}
