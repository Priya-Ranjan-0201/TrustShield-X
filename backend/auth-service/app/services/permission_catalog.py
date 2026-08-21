"""Android Permission Knowledge Base Catalog (Phase 3.7 Part 1A.8).

Provides metadata for official Android system permissions, categories, protection levels,
API support ranges, and documentation links.
"""

from typing import Dict, Any, Optional

ANDROID_PERMISSION_CATALOG: Dict[str, Dict[str, Any]] = {
    # Camera
    "android.permission.CAMERA": {
        "category": "Camera",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.CAMERA",
        "api_introduced": 1,
        "is_runtime": True,
        "description": "Required to access camera device.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#CAMERA",
    },
    # Location
    "android.permission.ACCESS_FINE_LOCATION": {
        "category": "Location",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.LOCATION",
        "api_introduced": 1,
        "is_runtime": True,
        "description": "Allows app to access precise location.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#ACCESS_FINE_LOCATION",
    },
    "android.permission.ACCESS_COARSE_LOCATION": {
        "category": "Location",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.LOCATION",
        "api_introduced": 1,
        "is_runtime": True,
        "description": "Allows app to access approximate location.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#ACCESS_COARSE_LOCATION",
    },
    "android.permission.ACCESS_BACKGROUND_LOCATION": {
        "category": "Location",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.LOCATION",
        "api_introduced": 29,
        "is_runtime": True,
        "description": "Allows app to access location in background.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#ACCESS_BACKGROUND_LOCATION",
    },
    # Microphone
    "android.permission.RECORD_AUDIO": {
        "category": "Microphone",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.MICROPHONE",
        "api_introduced": 1,
        "is_runtime": True,
        "description": "Allows app to record audio.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#RECORD_AUDIO",
    },
    # Storage
    "android.permission.READ_EXTERNAL_STORAGE": {
        "category": "Storage",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.STORAGE",
        "api_introduced": 16,
        "is_runtime": True,
        "description": "Allows app to read external storage.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#READ_EXTERNAL_STORAGE",
    },
    "android.permission.WRITE_EXTERNAL_STORAGE": {
        "category": "Storage",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.STORAGE",
        "api_introduced": 4,
        "is_runtime": True,
        "description": "Allows app to write to external storage.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#WRITE_EXTERNAL_STORAGE",
    },
    "android.permission.MANAGE_EXTERNAL_STORAGE": {
        "category": "Storage",
        "protection_level": "SPECIAL",
        "group": "android.permission-group.STORAGE",
        "api_introduced": 30,
        "is_runtime": False,
        "description": "Allows broad access to external storage.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#MANAGE_EXTERNAL_STORAGE",
    },
    # Contacts
    "android.permission.READ_CONTACTS": {
        "category": "Contacts",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.CONTACTS",
        "api_introduced": 1,
        "is_runtime": True,
        "description": "Allows app to read user contacts data.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#READ_CONTACTS",
    },
    "android.permission.WRITE_CONTACTS": {
        "category": "Contacts",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.CONTACTS",
        "api_introduced": 1,
        "is_runtime": True,
        "description": "Allows app to write user contacts data.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#WRITE_CONTACTS",
    },
    # SMS
    "android.permission.SEND_SMS": {
        "category": "SMS",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.SMS",
        "api_introduced": 1,
        "is_runtime": True,
        "description": "Allows app to send SMS messages.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#SEND_SMS",
    },
    "android.permission.RECEIVE_SMS": {
        "category": "SMS",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.SMS",
        "api_introduced": 1,
        "is_runtime": True,
        "description": "Allows app to receive SMS messages.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#RECEIVE_SMS",
    },
    "android.permission.READ_SMS": {
        "category": "SMS",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.SMS",
        "api_introduced": 1,
        "is_runtime": True,
        "description": "Allows app to read SMS messages.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#READ_SMS",
    },
    # Phone
    "android.permission.READ_PHONE_STATE": {
        "category": "Phone",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.PHONE",
        "api_introduced": 1,
        "is_runtime": True,
        "description": "Allows read-only access to phone state.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#READ_PHONE_STATE",
    },
    "android.permission.CALL_PHONE": {
        "category": "Phone",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.PHONE",
        "api_introduced": 1,
        "is_runtime": True,
        "description": "Allows app to initiate a phone call.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#CALL_PHONE",
    },
    # Network
    "android.permission.INTERNET": {
        "category": "Network",
        "protection_level": "NORMAL",
        "group": "android.permission-group.NETWORK",
        "api_introduced": 1,
        "is_runtime": False,
        "description": "Allows applications to open network sockets.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#INTERNET",
    },
    "android.permission.ACCESS_NETWORK_STATE": {
        "category": "Network",
        "protection_level": "NORMAL",
        "group": "android.permission-group.NETWORK",
        "api_introduced": 1,
        "is_runtime": False,
        "description": "Allows access to information about networks.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#ACCESS_NETWORK_STATE",
    },
    # Bluetooth
    "android.permission.BLUETOOTH": {
        "category": "Bluetooth",
        "protection_level": "NORMAL",
        "group": "android.permission-group.BLUETOOTH",
        "api_introduced": 1,
        "is_runtime": False,
        "description": "Allows applications to connect to paired bluetooth devices.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#BLUETOOTH",
    },
    "android.permission.BLUETOOTH_CONNECT": {
        "category": "Bluetooth",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.BLUETOOTH",
        "api_introduced": 31,
        "is_runtime": True,
        "description": "Required to connect to paired Bluetooth devices.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#BLUETOOTH_CONNECT",
    },
    # Notifications
    "android.permission.POST_NOTIFICATIONS": {
        "category": "Notifications",
        "protection_level": "DANGEROUS",
        "group": "android.permission-group.NOTIFICATIONS",
        "api_introduced": 33,
        "is_runtime": True,
        "description": "Allows app to post notifications.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#POST_NOTIFICATIONS",
    },
    # System Settings
    "android.permission.WRITE_SETTINGS": {
        "category": "System Settings",
        "protection_level": "SPECIAL",
        "group": "android.permission-group.SYSTEM",
        "api_introduced": 1,
        "is_runtime": False,
        "description": "Allows app to read or write system settings.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#WRITE_SETTINGS",
    },
    # Package Management
    "android.permission.REQUEST_INSTALL_PACKAGES": {
        "category": "Package Management",
        "protection_level": "SPECIAL",
        "group": "android.permission-group.SYSTEM",
        "api_introduced": 26,
        "is_runtime": False,
        "description": "Allows app to request installing packages.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#REQUEST_INSTALL_PACKAGES",
    },
    # Foreground Services
    "android.permission.FOREGROUND_SERVICE": {
        "category": "Foreground Services",
        "protection_level": "NORMAL",
        "group": "android.permission-group.SYSTEM",
        "api_introduced": 28,
        "is_runtime": False,
        "description": "Allows app to use foreground services.",
        "doc_url": "https://developer.android.com/reference/android/Manifest.permission#FOREGROUND_SERVICE",
    },
}


def lookup_permission(permission_name: str) -> Dict[str, Any]:
    """Looks up permission metadata from the Android permission knowledge base catalog."""
    normalized = permission_name.strip()
    if normalized in ANDROID_PERMISSION_CATALOG:
        entry = ANDROID_PERMISSION_CATALOG[normalized].copy()
        entry["is_known"] = True
        return entry

    # Classification for Vendor / Custom / Unknown
    if normalized.startswith("com.google.") or normalized.startswith("com.android."):
        return {
            "category": "System Settings",
            "protection_level": "SIGNATURE",
            "group": "android.permission-group.SYSTEM",
            "api_introduced": 1,
            "is_runtime": False,
            "is_known": False,
            "description": "Android internal/system permission.",
            "doc_url": "",
        }
    if "." in normalized and not normalized.startswith("android.permission."):
        return {
            "category": "Custom",
            "protection_level": "CUSTOM",
            "group": "CUSTOM",
            "api_introduced": 1,
            "is_runtime": False,
            "is_known": False,
            "description": "Custom or vendor application permission.",
            "doc_url": "",
        }

    return {
        "category": "Unknown",
        "protection_level": "UNKNOWN",
        "group": "UNKNOWN",
        "api_introduced": 1,
        "is_runtime": False,
        "is_known": False,
        "description": "Unrecognized Android permission.",
        "doc_url": "",
    }
