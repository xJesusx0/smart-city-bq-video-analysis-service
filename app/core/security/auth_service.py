from app.core.repositories.camera_api_key_repository import CameraApiKeyRepository
from app.core.exceptions import get_entity_not_found_exception
from app.models import CameraAndLocation
from app.core.dependencies import LocationRepository
from datetime import datetime
from app.core.exceptions import get_credentials_exception


class AuthService:
    def __init__(
        self,
        camera_api_key_repository: CameraApiKeyRepository,
        location_repository: LocationRepository,
    ):
        self.camera_api_key_repository = camera_api_key_repository
        self.location_repository = location_repository

    def validate_key(self, api_key: str) -> CameraAndLocation:
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

        # Obtener la ubicación asociada
        location = self.location_repository.get_by_id(camera_api_key.location_id)
        if not location:
            raise get_entity_not_found_exception("Ubicación asociada no encontrada")

        camera_and_location = CameraAndLocation(
            camera=camera_api_key, location=location
        )
        return camera_and_location
