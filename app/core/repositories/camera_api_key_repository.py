from typing import Optional
from abc import ABC, abstractmethod
from app.core.models.camera_api_key import DbCameraApiKey


class CameraApiKeyRepository(ABC):
    @abstractmethod
    def get_api_key_by_key(self, api_key: str) -> Optional[DbCameraApiKey]:
        pass
