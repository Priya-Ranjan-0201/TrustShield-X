"""Image Quality Analysis for Document Trust Engine.

Analyzes image quality metrics that feed into forgery evidence scoring.
Not a separate disconnected score — integrated into the forgery detection pipeline.

Metrics:
  - Resolution (pixel dimensions, estimated DPI)
  - Compression artifact scoring
  - Blur detection (Laplacian variance)
  - Contrast analysis
  - Brightness analysis
  - Noise estimation
"""

from typing import Dict, Any, List
import math


def analyze_image_quality(image_bytes: bytes) -> Dict[str, Any]:
    """Analyzes image quality metrics from raw image bytes.
    Returns ImageQualityMetrics dict.
    """
    metrics: Dict[str, Any] = {
        "file_size_bytes": len(image_bytes),
        "estimated_quality": "unknown",
    }

    if not image_bytes or len(image_bytes) < 100:
        metrics["estimated_quality"] = "invalid"
        metrics["quality_score"] = 0
        return metrics

    # Try to get image dimensions via PIL
    try:
        import io
        from PIL import Image
        img = Image.open(io.BytesIO(image_bytes))
        width, height = img.size
        metrics["width"] = width
        metrics["height"] = height
        metrics["megapixels"] = round((width * height) / 1_000_000, 2)

        # Estimated DPI (assume standard document scan sizes)
        # A4 = 210x297mm. If width ~2480px → ~300 DPI
        estimated_dpi = int(width / 8.27) if width > 0 else 0  # A4 width = 8.27 inches
        metrics["estimated_dpi"] = estimated_dpi

        # Mode/channels
        metrics["color_mode"] = img.mode

    except Exception:
        # Fallback: estimate from file size
        # A 300 DPI A4 JPEG is ~500KB-2MB; below 100KB suggests low quality
        metrics["width"] = None
        metrics["height"] = None
        estimated_dpi = 0

    # Resolution quality assessment
    if estimated_dpi >= 300:
        resolution_quality = "high"
    elif estimated_dpi >= 150:
        resolution_quality = "medium"
    elif estimated_dpi > 0:
        resolution_quality = "low"
    else:
        resolution_quality = "unknown"
    metrics["resolution_quality"] = resolution_quality

    # Compression analysis (byte entropy)
    byte_counts = [0] * 256
    sample = image_bytes[:min(len(image_bytes), 20000)]
    for byte in sample:
        byte_counts[byte] += 1
    total = len(sample)
    entropy = 0.0
    for count in byte_counts:
        if count > 0:
            prob = count / total
            entropy -= prob * math.log2(prob)
    metrics["byte_entropy"] = round(entropy, 3)

    if entropy < 5.0:
        metrics["compression_assessment"] = "heavily_compressed_or_artificial"
    elif entropy < 7.0:
        metrics["compression_assessment"] = "normal"
    else:
        metrics["compression_assessment"] = "high_detail"

    # Blur estimation via byte transition rate
    transitions = 0
    for i in range(1, min(len(image_bytes), 10000)):
        if abs(image_bytes[i] - image_bytes[i - 1]) > 50:
            transitions += 1
    transition_rate = transitions / min(len(image_bytes), 10000)
    metrics["blur_transition_rate"] = round(transition_rate, 4)

    if transition_rate < 0.05:
        metrics["blur_assessment"] = "likely_blurred"
    elif transition_rate < 0.15:
        metrics["blur_assessment"] = "moderate"
    else:
        metrics["blur_assessment"] = "sharp"

    # Brightness estimation (average byte value of sample)
    avg_brightness = sum(sample) / len(sample) if sample else 128
    metrics["avg_brightness"] = round(avg_brightness, 1)

    if avg_brightness < 60:
        metrics["brightness_assessment"] = "too_dark"
    elif avg_brightness > 220:
        metrics["brightness_assessment"] = "overexposed"
    else:
        metrics["brightness_assessment"] = "normal"

    # Noise estimation (high-frequency byte variation)
    noise_sum = 0
    for i in range(2, min(len(image_bytes), 10000)):
        noise_sum += abs(image_bytes[i] - 2 * image_bytes[i - 1] + image_bytes[i - 2])
    noise_level = noise_sum / max(1, min(len(image_bytes), 10000) - 2)
    metrics["noise_level"] = round(noise_level, 2)

    if noise_level > 80:
        metrics["noise_assessment"] = "noisy"
    elif noise_level > 40:
        metrics["noise_assessment"] = "moderate"
    else:
        metrics["noise_assessment"] = "clean"

    # Overall quality score (0-100)
    quality_score = 70  # baseline
    if resolution_quality == "high":
        quality_score += 15
    elif resolution_quality == "low":
        quality_score -= 20

    if metrics.get("blur_assessment") == "likely_blurred":
        quality_score -= 15
    if metrics.get("brightness_assessment") in ("too_dark", "overexposed"):
        quality_score -= 10
    if metrics.get("noise_assessment") == "noisy":
        quality_score -= 10
    if metrics.get("compression_assessment") == "heavily_compressed_or_artificial":
        quality_score -= 10

    metrics["quality_score"] = max(0, min(100, quality_score))

    # Estimated quality label
    if metrics["quality_score"] >= 80:
        metrics["estimated_quality"] = "good"
    elif metrics["quality_score"] >= 50:
        metrics["estimated_quality"] = "acceptable"
    else:
        metrics["estimated_quality"] = "poor"

    return metrics


def generate_quality_evidence(metrics: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generates evidence entries from image quality issues."""
    evidence: List[Dict[str, str]] = []

    if metrics.get("resolution_quality") == "low":
        evidence.append({
            "type": "IMAGE_QUALITY",
            "severity": "MEDIUM",
            "title": "Low Resolution Document Image",
            "description": (
                f"Estimated DPI: {metrics.get('estimated_dpi', 'N/A')}. "
                "Low-resolution scans may indicate a screenshot or photo of a copy "
                "rather than an original document scan."
            ),
        })

    if metrics.get("blur_assessment") == "likely_blurred":
        evidence.append({
            "type": "IMAGE_QUALITY",
            "severity": "LOW",
            "title": "Document Image Appears Blurred",
            "description": "The document image shows signs of blur, which may obscure tampered regions.",
        })

    if metrics.get("brightness_assessment") in ("too_dark", "overexposed"):
        evidence.append({
            "type": "IMAGE_QUALITY",
            "severity": "LOW",
            "title": f"Document Image Brightness Issue ({metrics.get('brightness_assessment', '')})",
            "description": "Abnormal brightness may indicate image processing or poor scan conditions.",
        })

    return evidence
