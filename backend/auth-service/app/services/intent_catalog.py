"""Android Intent Action Knowledge Base Catalog (Phase 3.7 Part 1A.10).

Provides metadata describing official Android intent actions, system-only flags,
API introduction levels, and documentation references.
"""

from typing import Dict, Any, Optional

ANDROID_INTENT_CATALOG: Dict[str, Dict[str, Any]] = {
    "android.intent.action.MAIN": {
        "action_name": "android.intent.action.MAIN",
        "category": "LAUNCHER",
        "purpose": "Start as a main entry point, does not expect to receive data.",
        "is_system_only": False,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/content/Intent#ACTION_MAIN",
    },
    "android.intent.action.VIEW": {
        "action_name": "android.intent.action.VIEW",
        "category": "NAVIGATION",
        "purpose": "Display data to the user (Deep links, web URLs, media content).",
        "is_system_only": False,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/content/Intent#ACTION_VIEW",
    },
    "android.intent.action.SEND": {
        "action_name": "android.intent.action.SEND",
        "category": "SHARING",
        "purpose": "Deliver data to another application.",
        "is_system_only": False,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/content/Intent#ACTION_SEND",
    },
    "android.intent.action.SENDTO": {
        "action_name": "android.intent.action.SENDTO",
        "category": "MESSAGING",
        "purpose": "Send a message to someone specified by the data URI.",
        "is_system_only": False,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/content/Intent#ACTION_SENDTO",
    },
    "android.intent.action.BOOT_COMPLETED": {
        "action_name": "android.intent.action.BOOT_COMPLETED",
        "category": "SYSTEM_BROADCAST",
        "purpose": "Broadcast after system has finished booting.",
        "is_system_only": True,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/content/Intent#ACTION_BOOT_COMPLETED",
    },
    "android.intent.action.LOCKED_BOOT_COMPLETED": {
        "action_name": "android.intent.action.LOCKED_BOOT_COMPLETED",
        "category": "SYSTEM_BROADCAST",
        "purpose": "Broadcast after device has booted but while user is locked (Direct Boot).",
        "is_system_only": True,
        "api_introduced": 24,
        "doc_url": "https://developer.android.com/reference/android/content/Intent#ACTION_LOCKED_BOOT_COMPLETED",
    },
    "android.intent.action.PACKAGE_ADDED": {
        "action_name": "android.intent.action.PACKAGE_ADDED",
        "category": "SYSTEM_BROADCAST",
        "purpose": "Broadcast when a new application package has been installed.",
        "is_system_only": True,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/content/Intent#ACTION_PACKAGE_ADDED",
    },
    "android.intent.action.PACKAGE_REMOVED": {
        "action_name": "android.intent.action.PACKAGE_REMOVED",
        "category": "SYSTEM_BROADCAST",
        "purpose": "Broadcast when an existing application package has been removed.",
        "is_system_only": True,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/content/Intent#ACTION_PACKAGE_REMOVED",
    },
    "android.intent.action.MY_PACKAGE_REPLACED": {
        "action_name": "android.intent.action.MY_PACKAGE_REPLACED",
        "category": "SYSTEM_BROADCAST",
        "purpose": "Broadcast sent to the application package that was updated.",
        "is_system_only": True,
        "api_introduced": 12,
        "doc_url": "https://developer.android.com/reference/android/content/Intent#ACTION_MY_PACKAGE_REPLACED",
    },
    "android.intent.action.USER_PRESENT": {
        "action_name": "android.intent.action.USER_PRESENT",
        "category": "SYSTEM_BROADCAST",
        "purpose": "Broadcast when user unlocks device screen.",
        "is_system_only": True,
        "api_introduced": 3,
        "doc_url": "https://developer.android.com/reference/android/content/Intent#ACTION_USER_PRESENT",
    },
    "android.intent.action.BATTERY_CHANGED": {
        "action_name": "android.intent.action.BATTERY_CHANGED",
        "category": "SYSTEM_BROADCAST",
        "purpose": "Sticky broadcast containing battery status and charge level.",
        "is_system_only": True,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/content/Intent#ACTION_BATTERY_CHANGED",
    },
    "android.intent.action.CONNECTIVITY_CHANGE": {
        "action_name": "android.intent.action.CONNECTIVITY_CHANGE",
        "category": "SYSTEM_BROADCAST",
        "purpose": "Broadcast when network connectivity state changes.",
        "is_system_only": True,
        "api_introduced": 1,
        "doc_url": "https://developer.android.com/reference/android/net/ConnectivityManager#CONNECTIVITY_ACTION",
    },
}


def lookup_intent_action(action_name: str) -> Dict[str, Any]:
    """Looks up intent action metadata from the Android intent knowledge base catalog."""
    normalized = action_name.strip()
    if normalized in ANDROID_INTENT_CATALOG:
        entry = ANDROID_INTENT_CATALOG[normalized].copy()
        entry["is_known"] = True
        return entry

    if normalized.startswith("android.intent.action."):
        return {
            "action_name": normalized,
            "category": "SYSTEM_BROADCAST",
            "purpose": "Official Android system intent action.",
            "is_system_only": True,
            "api_introduced": 1,
            "doc_url": "",
            "is_known": False,
        }

    return {
        "action_name": normalized,
        "category": "CUSTOM",
        "purpose": "Custom application or vendor intent action.",
        "is_system_only": False,
        "api_introduced": 1,
        "doc_url": "",
        "is_known": False,
    }
