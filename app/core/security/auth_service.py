from datetime import datetime
from app.core.exceptions import get_credentials_exception
from app.core.models.camera_api_key import CameraApiKeyBase


class AuthService:
    def __init__(self, camera_api_key_repository):
        self.camera_api_key_repository = camera_api_key_repository

    def validate_key(self, api_key: str) -> CameraApiKeyBase:
        """
        Valida la existencia y vigencia de una API key de cámara.
        Retorna el registro de CameraApiKey si es válida.
        """
        camera_api_key = self.camera_api_key_repository.get_api_key_by_key(api_key)

        # Si no existe
        if not camera_api_key:
            raise get_credentials_exception("API key inválida o no encontrada")

        # Si está expirada
        if camera_api_key.expires_at and camera_api_key.expires_at < datetime.utcnow():
            raise get_credentials_exception("API key expirada")

        # (Opcional) actualizar fecha de último uso
        # camera_api_key.last_used_at = datetime.utcnow()
        # self.camera_api_key_repository.update(camera_api_key)

        return camera_api_key
