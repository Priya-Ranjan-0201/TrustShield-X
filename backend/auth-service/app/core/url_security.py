import ipaddress
import urllib.parse
from fastapi import HTTPException, status

PRIVATE_IP_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]

BLOCKED_HOSTNAMES = {
    "localhost",
    "localhost.localdomain",
    "metadata.google.internal",
    "169.254.169.254",
}


def validate_url_security(url: str) -> urllib.parse.ParseResult:
    """Validates URL security against SSRF, internal IP ranges, and malformed schemes."""
    if not url or not url.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL target cannot be empty.",
        )

    url_str = url.strip()

    # Prepend scheme if omitted
    if not url_str.startswith(("http://", "https://")):
        url_str = "https://" + url_str

    try:
        parsed = urllib.parse.urlparse(url_str)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Malformed URL string: {str(e)}",
        )

    if parsed.scheme not in ("http", "https"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported scheme '{parsed.scheme}'. Only http and https URLs are supported.",
        )

    hostname = parsed.hostname
    if not hostname:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL: Hostname missing.",
        )

    hostname_lower = hostname.lower()

    if hostname_lower in BLOCKED_HOSTNAMES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SSRF Blocked: Attempt to access internal/reserved hostname.",
        )

    # Check IP addresses
    try:
        ip = ipaddress.ip_address(hostname_lower)
        for net in PRIVATE_IP_NETWORKS:
            if ip in net:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"SSRF Blocked: Access to private/reserved IP address '{ip}' is prohibited.",
                )
    except ValueError:
        # Not an IP address string, which is fine for domain names
        pass

    return parsed
