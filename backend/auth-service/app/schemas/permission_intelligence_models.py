"""Pydantic v2 DTO Schemas for Permission Intelligence Engine (Phase 3.7 Part 1A.8).

Strictly typed DTOs for permission categories, protection levels, enriched permissions,
and permission statistics.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class PermissionCategory(str, Enum):
    ACCOUNTS = "Accounts"
    CALENDAR = "Calendar"
    CAMERA = "Camera"
    CONTACTS = "Contacts"
    LOCATION = "Location"
    MICROPHONE = "Microphone"
    NETWORK = "Network"
    PHONE = "Phone"
    SMS = "SMS"
    STORAGE = "Storage"
    SENSORS = "Sensors"
    BLUETOOTH = "Bluetooth"
    WIFI = "WiFi"
    NFC = "NFC"
    MEDIA = "Media"
    NOTIFICATIONS = "Notifications"
    HEALTH = "Health"
    BIOMETRICS = "Biometrics"
    ACCESSIBILITY = "Accessibility"
    SYSTEM_SETTINGS = "System Settings"
    PACKAGE_MANAGEMENT = "Package Management"
    FOREGROUND_SERVICES = "Foreground Services"
    BACKGROUND_SERVICES = "Background Services"
    ALARMS = "Alarms"
    DEVICE_ADMINISTRATION = "Device Administration"
    VPN = "VPN"
    COMPANION_DEVICE = "Companion Device"
    EXACT_ALARM = "Exact Alarm"
    ADVERTISING = "Advertising"
    PRIVACY = "Privacy"
    SECURITY = "Security"
    CUSTOM = "Custom"
    UNKNOWN = "Unknown"


class ProtectionLevel(str, Enum):
    NORMAL = "NORMAL"
    DANGEROUS = "DANGEROUS"
    SIGNATURE = "SIGNATURE"
    SIGNATURE_OR_SYSTEM = "SIGNATURE_OR_SYSTEM"
    INTERNAL = "INTERNAL"
    DEVELOPMENT = "DEVELOPMENT"
    SPECIAL = "SPECIAL"
    APPOPS = "APPOPS"
    VENDOR = "VENDOR"
    CUSTOM = "CUSTOM"
    UNKNOWN = "UNKNOWN"


class EnrichedPermissionDTO(BaseModel):
    permission_name: str
    category: str
    protection_level: str
    permission_group: Optional[str] = None
    is_runtime: bool = False
    is_dangerous: bool = False
    is_custom: bool = False
    is_vendor: bool = False
    is_unknown: bool = False
    target_sdk_supported: bool = True
    description: Optional[str] = None
    doc_url: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class PermissionStatisticsDTO(BaseModel):
    total_permissions: int = 0
    normal_count: int = 0
    dangerous_count: int = 0
    signature_count: int = 0
    special_count: int = 0
    custom_count: int = 0
    vendor_count: int = 0
    unknown_count: int = 0
    runtime_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class PermissionIntelligenceResultDTO(BaseModel):
    permissions: List[EnrichedPermissionDTO] = Field(default_factory=list)
    statistics: PermissionStatisticsDTO = Field(default_factory=PermissionStatisticsDTO)
    knowledge_base_hits: int = 0
    normalization_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
