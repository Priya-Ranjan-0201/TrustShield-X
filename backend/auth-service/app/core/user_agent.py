import re

def parse_user_agent(user_agent: str | None) -> dict[str, str]:
    if not user_agent:
        return {
            "device_name": "Unknown Device",
            "browser": "Unknown Browser",
            "operating_system": "Unknown OS",
        }

    ua = user_agent.lower()

    # Determine Operating System
    if "windows nt 10.0" in ua:
        os = "Windows 10/11"
    elif "windows" in ua:
        os = "Windows"
    elif "mac os x" in ua:
        os = "macOS"
    elif "android" in ua:
        os = "Android"
    elif "iphone" in ua or "ipad" in ua:
        os = "iOS"
    elif "linux" in ua:
        os = "Linux"
    else:
        os = "Unknown OS"

    # Determine Browser
    if "edg/" in ua or "edge" in ua:
        browser = "Microsoft Edge"
    elif "chrome" in ua and "chromium" not in ua:
        browser = "Google Chrome"
    elif "safari" in ua and "chrome" not in ua:
        browser = "Apple Safari"
    elif "firefox" in ua:
        browser = "Mozilla Firefox"
    elif "opera" in ua or "opr/" in ua:
        browser = "Opera"
    else:
        browser = "Browser Client"

    # Determine Device Type
    if "mobile" in ua or "android" in ua or "iphone" in ua:
        device = "Mobile Phone"
    elif "ipad" in ua or "tablet" in ua:
        device = "Tablet"
    else:
        device = "Desktop Workstation"

    return {
        "device_name": device,
        "browser": browser,
        "operating_system": os,
    }
