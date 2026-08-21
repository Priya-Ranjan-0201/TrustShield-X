import socket
import ssl
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List


class DNSAndSSLResult:
    def __init__(
        self,
        dns_records: Dict[str, List[str]],
        ssl_valid: bool,
        ssl_issuer: str | None,
        ssl_expires_at: str | None,
        ssl_is_self_signed: bool,
        ssl_error: str | None,
    ):
        self.dns_records = dns_records
        self.ssl_valid = ssl_valid
        self.ssl_issuer = ssl_issuer
        self.ssl_expires_at = ssl_expires_at
        self.ssl_is_self_signed = ssl_is_self_signed
        self.ssl_error = ssl_error


async def inspect_dns_and_ssl(hostname: str, scheme: str = "https", port: int = 443) -> DNSAndSSLResult:
    """Asynchronously inspects DNS records and SSL certificate status."""
    dns_records: Dict[str, List[str]] = {"A": [], "AAAA": [], "MX": [], "NS": []}

    # 1. Asynchronous DNS A Record Lookup
    loop = asyncio.get_running_loop()
    try:
        addresses = await loop.run_in_executor(
            None, lambda: socket.getaddrinfo(hostname, None, socket.AF_INET)
        )
        dns_records["A"] = list(set(addr[4][0] for addr in addresses))
    except Exception:
        dns_records["A"] = []

    # 2. SSL Inspection (for HTTPS URLs)
    ssl_valid = False
    ssl_issuer = None
    ssl_expires_at = None
    ssl_is_self_signed = False
    ssl_error = None

    if scheme.lower() == "https":
        try:
            context = ssl.create_default_context()
            context.timeout = 5.0

            def _get_cert():
                with socket.create_connection((hostname, port), timeout=5.0) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        return ssock.getpeercert()

            cert = await loop.run_in_executor(None, _get_cert)

            if cert:
                ssl_valid = True
                issuer_tuples = cert.get("issuer", ())
                issuer_parts = []
                for t in issuer_tuples:
                    for k, v in t:
                        if k == "organizationName" or k == "commonName":
                            issuer_parts.append(v)
                ssl_issuer = ", ".join(issuer_parts) or "Valid Certificate Authority"

                not_after = cert.get("notAfter")
                if not_after:
                    ssl_expires_at = not_after

        except ssl.SSLCertVerificationError as cert_err:
            ssl_valid = False
            ssl_error = f"SSL Certificate Verification Failed: {cert_err.verify_message}"
            if "self signed" in str(cert_err).lower():
                ssl_is_self_signed = True
        except Exception as e:
            ssl_valid = False
            ssl_error = f"SSL Connection Failed: {str(e)}"

    return DNSAndSSLResult(
        dns_records=dns_records,
        ssl_valid=ssl_valid,
        ssl_issuer=ssl_issuer,
        ssl_expires_at=ssl_expires_at,
        ssl_is_self_signed=ssl_is_self_signed,
        ssl_error=ssl_error,
    )
