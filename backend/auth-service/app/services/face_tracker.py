"""Face Tracking Engine across Video Frames for Deepfake Detection Engine.

Tracks face identities across extracted frames using IoU (Intersection over Union)
and centroid distance matching.

Assigns persistent track_ids (e.g. face_track_1, face_track_2) and records:
- track_id
- total_frames_tracked
- avg_confidence
- bounding_boxes_json (list of per-frame bbox, timestamp, landmarks)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple
from app.services.face_detector import FaceBBox
from app.services.frame_extractor import ExtractedFrame


def compute_iou(boxA: Tuple[int, int, int, int], boxB: Tuple[int, int, int, int]) -> float:
    """Computes Intersection over Union (IoU) between two bounding boxes (x, y, w, h)."""
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    if interArea == 0:
        return 0.0

    boxAArea = boxA[2] * boxA[3]
    boxBArea = boxB[2] * boxB[3]

    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou


@dataclass
class FaceTrackRecord:
    track_id: str
    total_frames_tracked: int
    avg_confidence: float
    frame_entries: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "track_id": self.track_id,
            "total_frames_tracked": self.total_frames_tracked,
            "avg_confidence": round(self.avg_confidence, 3),
            "frame_entries": self.frame_entries,
        }


class FaceTrackerEngine:
    """Tracks face identities across video frames using IoU matching."""

    def __init__(self, iou_threshold: float = 0.3):
        self.iou_threshold = iou_threshold
        self.active_tracks: Dict[str, Dict[str, Any]] = {}
        self.next_track_num = 1

    def process_frame(
        self, frame_index: int, timestamp_sec: float, detected_faces: List[FaceBBox]
    ) -> List[Tuple[str, FaceBBox]]:
        """Matches detected faces in current frame to active tracks or spawns new tracks."""
        assignments: List[Tuple[str, FaceBBox]] = []

        if not detected_faces:
            return assignments

        unmatched_faces = list(detected_faces)
        matched_track_ids = set()

        # Match against existing tracks
        for track_id, track_data in self.active_tracks.items():
            last_bbox = track_data["last_bbox"]
            best_iou = 0.0
            best_face = None

            for face in unmatched_faces:
                iou = compute_iou(last_bbox, (face.x, face.y, face.w, face.h))
                if iou > best_iou:
                    best_iou = iou
                    best_face = face

            if best_iou >= self.iou_threshold and best_face is not None:
                # Assign to existing track
                assignments.append((track_id, best_face))
                matched_track_ids.add(track_id)
                unmatched_faces.remove(best_face)

                # Update track history
                track_data["last_bbox"] = (best_face.x, best_face.y, best_face.w, best_face.h)
                track_data["confidences"].append(best_face.confidence)
                track_data["history"].append({
                    "frame_index": frame_index,
                    "timestamp_sec": round(timestamp_sec, 3),
                    "bbox": [best_face.x, best_face.y, best_face.w, best_face.h],
                    "confidence": round(best_face.confidence, 3),
                })

        # Spawn new tracks for unmatched faces
        for face in unmatched_faces:
            new_track_id = f"face_track_{self.next_track_num}"
            self.next_track_num += 1

            self.active_tracks[new_track_id] = {
                "last_bbox": (face.x, face.y, face.w, face.h),
                "confidences": [face.confidence],
                "history": [{
                    "frame_index": frame_index,
                    "timestamp_sec": round(timestamp_sec, 3),
                    "bbox": [face.x, face.y, face.w, face.h],
                    "confidence": round(face.confidence, 3),
                }],
            }
            assignments.append((new_track_id, face))

        return assignments

    def get_track_records(self) -> List[FaceTrackRecord]:
        """Finalizes and returns list of FaceTrackRecord summaries."""
        records: List[FaceTrackRecord] = []

        for track_id, track_data in self.active_tracks.items():
            confs = track_data["confidences"]
            avg_conf = sum(confs) / len(confs) if confs else 0.0

            records.append(
                FaceTrackRecord(
                    track_id=track_id,
                    total_frames_tracked=len(track_data["history"]),
                    avg_confidence=avg_conf,
                    frame_entries=track_data["history"],
                )
            )

        return records
