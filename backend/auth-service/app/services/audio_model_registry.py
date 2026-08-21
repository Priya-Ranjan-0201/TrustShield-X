"""Audio Model Registry for AI Voice Clone Neural Engine.

Tracks registered speaker embedding extractors and voice clone model adapters:
- Model Name
- Version
- Framework
- Embedding Size (192, 256, 512, 1024)
- Supported Languages
- CPU / GPU Compatibility
- Active Status

Supports dynamic model switching via set_active_model() and set_active_voice_adapter().
"""

from typing import Dict, Any, List, Optional
from app.services.speaker_embedding_interface import (
    BaseSpeakerEmbeddingExtractor,
    ECAPATDNNEmbeddingExtractor,
    ResemblyzerEmbeddingExtractor,
    SpeechBrainEmbeddingExtractor,
    WavLMEmbeddingExtractor,
)
from app.services.voice_model_adapter import (
    BaseVoiceCloneModelAdapter,
    ECAPATDNNVoiceCloneAdapter,
    SpeechBrainVoiceCloneAdapter,
    WavLMVoiceCloneAdapter,
    ResemblyzerVoiceCloneAdapter,
    NeMoSpeakerNetVoiceCloneAdapter,
)


class AudioModelRegistry:
    """Registry managing available speaker embedding models and voice clone neural adapters."""

    def __init__(self):
        self._extractors: Dict[str, BaseSpeakerEmbeddingExtractor] = {}
        self._voice_adapters: Dict[str, BaseVoiceCloneModelAdapter] = {}

        self._active_extractor_name: str = ""
        self._active_voice_adapter_name: str = ""

        # Register default embedding extractors
        extractors: List[BaseSpeakerEmbeddingExtractor] = [
            ECAPATDNNEmbeddingExtractor(),
            ResemblyzerEmbeddingExtractor(),
            SpeechBrainEmbeddingExtractor(),
            WavLMEmbeddingExtractor(),
        ]
        for ext in extractors:
            self.register_extractor(ext)

        # Register default voice clone adapters
        voice_adapters: List[BaseVoiceCloneModelAdapter] = [
            ECAPATDNNVoiceCloneAdapter(),
            SpeechBrainVoiceCloneAdapter(),
            WavLMVoiceCloneAdapter(),
            ResemblyzerVoiceCloneAdapter(),
            NeMoSpeakerNetVoiceCloneAdapter(),
        ]
        for adapter in voice_adapters:
            self.register_voice_adapter(adapter)

        # Default active models
        self.set_active_model("ECAPA-TDNN")
        self.set_active_voice_adapter("ECAPA-TDNN-VoiceClone")

    def register_extractor(self, extractor: BaseSpeakerEmbeddingExtractor) -> None:
        self._extractors[extractor.extractor_name] = extractor

    def register_voice_adapter(self, adapter: BaseVoiceCloneModelAdapter) -> None:
        self._voice_adapters[adapter.model_name] = adapter

    def set_active_model(self, model_name: str) -> bool:
        if model_name in self._extractors:
            self._active_extractor_name = model_name
            self._extractors[model_name].initialize()
            return True
        return False

    def set_active_voice_adapter(self, adapter_name: str) -> bool:
        if adapter_name in self._voice_adapters:
            self._active_voice_adapter_name = adapter_name
            self._voice_adapters[adapter_name].initialize()
            return True
        return False

    def get_active_extractor(self) -> BaseSpeakerEmbeddingExtractor:
        return self.get_extractor(self._active_extractor_name)

    def get_extractor(self, model_name: Optional[str] = None) -> BaseSpeakerEmbeddingExtractor:
        target = model_name or self._active_extractor_name
        if target not in self._extractors:
            target = self._active_extractor_name
        ext = self._extractors[target]
        ext.initialize()
        return ext

    def get_active_voice_adapter(self) -> BaseVoiceCloneModelAdapter:
        return self.get_voice_adapter(self._active_voice_adapter_name)

    def get_voice_adapter(self, adapter_name: Optional[str] = None) -> BaseVoiceCloneModelAdapter:
        target = adapter_name or self._active_voice_adapter_name
        if target not in self._voice_adapters:
            target = self._active_voice_adapter_name
        adapter = self._voice_adapters[target]
        adapter.initialize()
        return adapter

    def list_registered_models(self) -> List[Dict[str, Any]]:
        models = []
        for name, ext in self._extractors.items():
            is_active = (name == self._active_extractor_name)
            models.append({
                "model_name": ext.extractor_name,
                "version": ext.version,
                "framework": ext.framework,
                "type": "EMBEDDING_EXTRACTOR",
                "embedding_dim": ext.embedding_dim,
                "supported_languages": ["en", "hi", "multilingual"],
                "gpu_compatibility": True,
                "cpu_compatibility": True,
                "is_active": is_active,
                "status": "ACTIVE" if is_active else "AVAILABLE",
            })
        for name, adapter in self._voice_adapters.items():
            is_active = (name == self._active_voice_adapter_name)
            models.append({
                "model_name": adapter.model_name,
                "version": adapter.version,
                "framework": adapter.framework,
                "type": "VOICE_CLONE_CLASSIFIER",
                "embedding_dim": adapter.embedding_dim,
                "supported_languages": ["en", "hi", "multilingual"],
                "gpu_compatibility": True,
                "cpu_compatibility": True,
                "is_active": is_active,
                "status": "ACTIVE" if is_active else "AVAILABLE",
            })
        return models
