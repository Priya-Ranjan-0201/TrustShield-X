"""DEX Discovery Engine for AI Android APK Security Engine (Phase 3.7 Part 1A Message 2 & Part 1A.6).

Wraps DEXIntelligenceParser to provide backward compatible DEXSummary responses.
"""

from typing import List, Tuple
from app.schemas.apk_models import DEXSummary
from app.services.dex_parser import DEXIntelligenceParser, DEXScanner as LegacyDEXScanner

__all__ = ["DEXScanner", "DEX_HEADER_MAGIC"]

DEX_HEADER_MAGIC = (b"dex\n035\x00", b"dex\n037\x00", b"dex\n038\x00", b"dex\n039\x00")


class DEXScanner(LegacyDEXScanner):
    """Production DEX Bytecode File Discovery & Header Scanner Wrapper."""
    pass
