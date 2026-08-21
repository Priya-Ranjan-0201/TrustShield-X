"""Speaker Similarity Engine for AI Voice Clone Neural Inference.

Computes multi-dimensional speaker embedding metrics:
- Cosine Similarity ([-1.0, 1.0])
- Euclidean Distance (L2 norm)
- Angular Distance ([0, pi])
"""

import math
from typing import List, Dict, Any


def compute_cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Computes cosine similarity between two float vectors."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    sim = dot_product / (norm_a * norm_b)
    return max(-1.0, min(1.0, round(sim, 4)))


def compute_euclidean_distance(vec_a: List[float], vec_b: List[float]) -> float:
    """Computes L2 Euclidean distance between two float vectors."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0

    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(vec_a, vec_b)))
    return round(dist, 4)


def compute_angular_distance(vec_a: List[float], vec_b: List[float]) -> float:
    """Computes normalized angular distance between two float vectors."""
    cos_sim = compute_cosine_similarity(vec_a, vec_b)
    # Clamp cosine similarity to [-1.0, 1.0] for acos
    cos_clamped = max(-1.0, min(1.0, cos_sim))
    angle_rad = math.acos(cos_clamped)
    # Normalized angular distance in [0, 1]
    angular_dist = angle_rad / math.pi
    return round(angular_dist, 4)


def analyze_speaker_embedding_similarity(
    speaker_embeddings: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Computes pairwise speaker similarity metrics across extracted speaker embeddings."""
    if len(speaker_embeddings) < 2:
        return {
            "pairwise_metrics": [],
            "avg_cosine_similarity": 1.0,
            "avg_euclidean_distance": 0.0,
            "avg_angular_distance": 0.0,
            "similarity_anomaly_detected": False,
        }

    pairwise = []
    total_cos = 0.0
    total_euc = 0.0
    total_ang = 0.0
    count = 0

    for i in range(len(speaker_embeddings)):
        for j in range(i + 1, len(speaker_embeddings)):
            emb_i = speaker_embeddings[i].get("embedding_vector", [])
            emb_j = speaker_embeddings[j].get("embedding_vector", [])

            cos_sim = compute_cosine_similarity(emb_i, emb_j)
            euc_dist = compute_euclidean_distance(emb_i, emb_j)
            ang_dist = compute_angular_distance(emb_i, emb_j)

            pairwise.append({
                "speaker_a": speaker_embeddings[i].get("speaker_id"),
                "speaker_b": speaker_embeddings[j].get("speaker_id"),
                "cosine_similarity": cos_sim,
                "euclidean_distance": euc_dist,
                "angular_distance": ang_dist,
            })

            total_cos += cos_sim
            total_euc += euc_dist
            total_ang += ang_dist
            count += 1

    avg_cos = round(total_cos / count, 4) if count > 0 else 1.0
    avg_euc = round(total_euc / count, 4) if count > 0 else 0.0
    avg_ang = round(total_ang / count, 4) if count > 0 else 0.0

    return {
        "pairwise_metrics": pairwise,
        "avg_cosine_similarity": avg_cos,
        "avg_euclidean_distance": avg_euc,
        "avg_angular_distance": avg_ang,
        "similarity_anomaly_detected": avg_cos > 0.95,  # Unusually high inter-speaker similarity indicates voice morphing/clone
    }
