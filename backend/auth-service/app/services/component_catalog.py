"""Android Component Knowledge Base Catalog (Phase 3.7 Part 1A.9).

Provides metadata describing Android application component types, default export behaviors,
intent filter requirements, process isolation rules, and documentation references.
"""

from typing import Dict, Any, Optional

ANDROID_COMPONENT_CATALOG: Dict[str, Dict[str, Any]] = {
    "ACTIVITY": {
        "type_name": "Activity",
        "android_purpose": "Provides a user interface screen for user interaction.",
        "lifecycle_type": "UI_LIFECYCLE",
        "default_exported_behavior": "FALSE_UNLESS_INTENT_FILTER_PRESENT",
        "supports_intent_filters": True,
        "supports_permissions": True,
        "supports_process_isolation": False,
        "supports_multiprocess": True,
        "supports_direct_boot": True,
        "supports_foreground_mode": False,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/app/Activity",
    },
    "ACTIVITY_ALIAS": {
        "type_name": "Activity Alias",
        "android_purpose": "Target alias for launching an existing activity under a different name/theme.",
        "lifecycle_type": "UI_LIFECYCLE",
        "default_exported_behavior": "FALSE_UNLESS_INTENT_FILTER_PRESENT",
        "supports_intent_filters": True,
        "supports_permissions": True,
        "supports_process_isolation": False,
        "supports_multiprocess": False,
        "supports_direct_boot": True,
        "supports_foreground_mode": False,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/guide/topics/manifest/activity-alias-element",
    },
    "SERVICE": {
        "type_name": "Service",
        "android_purpose": "Executes long-running background processing without a UI.",
        "lifecycle_type": "BACKGROUND_LIFECYCLE",
        "default_exported_behavior": "FALSE_UNLESS_INTENT_FILTER_PRESENT",
        "supports_intent_filters": True,
        "supports_permissions": True,
        "supports_process_isolation": True,
        "supports_multiprocess": False,
        "supports_direct_boot": True,
        "supports_foreground_mode": True,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/app/Service",
    },
    "FOREGROUND_SERVICE": {
        "type_name": "Foreground Service",
        "android_purpose": "Executes user-noticeable background tasks with a persistent notification.",
        "lifecycle_type": "FOREGROUND_BACKGROUND_LIFECYCLE",
        "default_exported_behavior": "FALSE",
        "supports_intent_filters": True,
        "supports_permissions": True,
        "supports_process_isolation": False,
        "supports_multiprocess": False,
        "supports_direct_boot": True,
        "supports_foreground_mode": True,
        "api_introduced": 28,
        "doc_url": "https://developer.android.com/guide/components/foreground-services",
    },
    "BROADCAST_RECEIVER": {
        "type_name": "Broadcast Receiver",
        "android_purpose": "Receives system-wide or app-specific broadcast intent notifications.",
        "lifecycle_type": "EVENT_DRIVEN_LIFECYCLE",
        "default_exported_behavior": "FALSE_UNLESS_INTENT_FILTER_PRESENT",
        "supports_intent_filters": True,
        "supports_permissions": True,
        "supports_process_isolation": False,
        "supports_multiprocess": False,
        "supports_direct_boot": True,
        "supports_foreground_mode": False,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/content/BroadcastReceiver",
    },
    "CONTENT_PROVIDER": {
        "type_name": "Content Provider",
        "android_purpose": "Manages a structured data repository and exposes content URI access.",
        "lifecycle_type": "DATA_REPOSITORY_LIFECYCLE",
        "default_exported_behavior": "FALSE_SINCE_API17",
        "supports_intent_filters": False,
        "supports_permissions": True,
        "supports_process_isolation": True,
        "supports_multiprocess": True,
        "supports_direct_boot": True,
        "supports_foreground_mode": False,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/content/ContentProvider",
    },
    "INSTRUMENTATION": {
        "type_name": "Instrumentation",
        "android_purpose": "Monitors application interactions and system events for testing.",
        "lifecycle_type": "SYSTEM_TESTING_LIFECYCLE",
        "default_exported_behavior": "FALSE",
        "supports_intent_filters": False,
        "supports_permissions": False,
        "supports_process_isolation": False,
        "supports_multiprocess": False,
        "supports_direct_boot": False,
        "supports_foreground_mode": False,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/app/Instrumentation",
    },
}


def lookup_component_type(component_type: str) -> Dict[str, Any]:
    """Looks up component metadata from the Android component knowledge base catalog."""
    normalized = component_type.upper().strip()
    if normalized in ANDROID_COMPONENT_CATALOG:
        entry = ANDROID_COMPONENT_CATALOG[normalized].copy()
        entry["is_known"] = True
        return entry

    return {
        "type_name": normalized,
        "android_purpose": "Generic Android application component.",
        "lifecycle_type": "UNKNOWN_LIFECYCLE",
        "default_exported_behavior": "UNKNOWN",
        "supports_intent_filters": True,
        "supports_permissions": True,
        "supports_process_isolation": False,
        "supports_multiprocess": False,
        "supports_direct_boot": False,
        "supports_foreground_mode": False,
        "api_introduced": 1,
        "doc_url": "",
        "is_known": False,
    }
