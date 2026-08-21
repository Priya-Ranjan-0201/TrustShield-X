"""Speaker Embedding Abstraction Interface for AI Voice Clone Infrastructure.

Abstract base provider class with pluggable embedding extractors:
- ECAPATDNNEmbeddingExtractor (192-dim speaker embeddings via SpeechBrain)
- ResemblyzerEmbeddingExtractor (256-dim d-vector speaker embeddings)
- SpeechBrainEmbeddingExtractor (512-dim speaker embeddings)
- WavLMEmbeddingExtractor (1024-dim self-supervised WavLM embeddings)

Interface methods:
- initialize()
- preprocess()
- extract_embedding()
- unload()
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional


@dataclass
class SpeakerEmbeddingOutput:
    speaker_id: str
    embedding_dim: int
    embedding_vector: List[float] = field(default_factory=list)
    extractor_name: str = "ECAPA-TDNN"
    extractor_version: str = "1.0"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "speaker_id": self.speaker_id,
            "embedding_dim": self.embedding_dim,
            "extractor_name": self.extractor_name,
            "extractor_version": self.extractor_version,
            "vector_len": len(self.embedding_vector),
        }


class BaseSpeakerEmbeddingExtractor(ABC):
    """Abstract speaker embedding extractor interface."""

    @property
    @abstractmethod
    def extractor_name(self) -> str:
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        pass

    @property
    @abstractmethod
    def framework(self) -> str:
        pass

    @property
    @abstractmethod
    def embedding_dim(self) -> int:  # 192, 256, 512, 1024
        pass

    @abstractmethod
    def initialize(self) -> bool:
        pass

    @abstractmethod
    def preprocess(self, audio_bytes: bytes) -> Dict[str, Any]:
        pass

    @abstractmethod
    def extract_embedding(self, preprocessed_data: Dict[str, Any], speaker_id: str = "speaker_1") -> SpeakerEmbeddingOutput:
        pass

    @abstractmethod
    def unload(self) -> bool:
        pass


class ECAPATDNNEmbeddingExtractor(BaseSpeakerEmbeddingExtractor):
    """ECAPA-TDNN 192-dimensional speaker embedding extractor."""

    @property
    def extractor_name(self) -> str:
        return "ECAPA-TDNN"

    @property
    def version(self) -> str:
        return "1.0-SpeechBrain"

    @property
    def framework(self) -> str:
        return "PyTorch/SpeechBrain"

    @property
    def embedding_dim(self) -> int:
        return 192

    def initialize(self) -> bool:
        return True

    def preprocess(self, audio_bytes: bytes) -> Dict[str, Any]:
        return {"bytes_len": len(audio_bytes), "sample_rate": 16000}

    def extract_embedding(self, preprocessed_data: Dict[str, Any], speaker_id: str = "speaker_1") -> SpeakerEmbeddingOutput:
        # Generate normalized synthetic 192-dim vector for testing infrastructure
        vec = [round((i % 10) / 10.0 - 0.5, 4) for i in range(192)]
        return SpeakerEmbeddingOutput(
            speaker_id=speaker_id,
            embedding_dim=192,
            embedding_vector=vec,
            extractor_name=self.extractor_name,
            extractor_version=self.version,
        )

    def unload(self) -> bool:
        return True


class ResemblyzerEmbeddingExtractor(BaseSpeakerEmbeddingExtractor):
    """Resemblyzer 256-dimensional d-vector speaker embedding extractor."""

    @property
    def extractor_name(self) -> str:
        return "Resemblyzer-d-vector"

    @property
    def version(self) -> str:
        return "0.1.2"

    @property
    def framework(self) -> str:
        return "PyTorch"

    @property
    def embedding_dim(self) -> int:
        return 256

    def initialize(self) -> bool:
        return True

    def preprocess(self, audio_bytes: bytes) -> Dict[str, Any]:
        return {"bytes_len": len(audio_bytes)}

    def extract_embedding(self, preprocessed_data: Dict[str, Any], speaker_id: str = "speaker_1") -> SpeakerEmbeddingOutput:
        vec = [round((i % 10) / 10.0 - 0.5, 4) for i in range(256)]
        return SpeakerEmbeddingOutput(
            speaker_id=speaker_id,
            embedding_dim=256,
            embedding_vector=vec,
            extractor_name=self.extractor_name,
            extractor_version=self.version,
        )

    def unload(self) -> bool:
        return True


class SpeechBrainEmbeddingExtractor(BaseSpeakerEmbeddingExtractor):
    """SpeechBrain 512-dimensional x-vector speaker embedding extractor."""

    @property
    def extractor_name(self) -> str:
        return "SpeechBrain-x-vector"

    @property
    def version(self) -> str:
        return "0.5.14"

    @property
    def framework(self) -> str:
        return "PyTorch"

    @property
    def embedding_dim(self) -> int:
        return 512

    def initialize(self) -> bool:
        return True

    def preprocess(self, audio_bytes: bytes) -> Dict[str, Any]:
        return {"bytes_len": len(audio_bytes)}

    def extract_embedding(self, preprocessed_data: Dict[str, Any], speaker_id: str = "speaker_1") -> SpeakerEmbeddingOutput:
        vec = [0.1] * 512
        return SpeakerEmbeddingOutput(
            speaker_id=speaker_id,
            embedding_dim=512,
            embedding_vector=vec,
            extractor_name=self.extractor_name,
            extractor_version=self.version,
        )

    def unload(self) -> bool:
        return True


class WavLMEmbeddingExtractor(BaseSpeakerEmbeddingExtractor):
    """WavLM-Large 1024-dimensional self-supervised speaker embedding extractor."""

    @property
    def extractor_name(self) -> str:
        return "WavLM-Large-SV"

    @property
    def version(self) -> str:
        return "1.0-HuggingFace"

    @property
    def framework(self) -> str:
        return "PyTorch/Transformers"

    @property
    def embedding_dim(self) -> int:
        return 1024

    def initialize(self) -> bool:
        return True

    def preprocess(self, audio_bytes: bytes) -> Dict[str, Any]:
        return {"bytes_len": len(audio_bytes)}

    def extract_embedding(self, preprocessed_data: Dict[str, Any], speaker_id: str = "speaker_1") -> SpeakerEmbeddingOutput:
        vec = [0.05] * 1024
        return SpeakerEmbeddingOutput(
            speaker_id=speaker_id,
            embedding_dim=1024,
            embedding_vector=vec,
            extractor_name=self.extractor_name,
            extractor_version=self.version,
        )

    def unload(self) -> bool:
        return True
