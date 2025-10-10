from app.models import CameraAndLocation
from app.core.models.camera_api_key import CameraApiKeyBase
from app.core.exceptions import get_credentials_exception
from app.core.exceptions import get_forbidden_exception
from typing import Optional
from app.core.database.repositories.camera_api_key_repository_impl import (
    CameraApiKeyRepositoryImpl,
)
from app.core.database.repositories.location_repository_impl import (
    LocationRepositoryImpl,
)
from app.core.repositories.camera_api_key_repository import CameraApiKeyRepository
from app.core.repositories.location_repository import LocationRepository
from app.core.database.connection import SessionDep
from app.core.security.auth_service import AuthService
from typing import Annotated

from fastapi import Depends, Header

# --- Repositories


def get_camera_api_key_repository(session: SessionDep) -> CameraApiKeyRepository:
    return CameraApiKeyRepositoryImpl(session)


def get_location_repository(session: SessionDep) -> LocationRepository:
    return LocationRepositoryImpl(session)


CameraApiKeyRepoDep = Annotated[
    CameraApiKeyRepository, Depends(get_camera_api_key_repository)
]

LocationRepoDep = Annotated[LocationRepository, Depends(get_location_repository)]

# --- Services


def get_auth_service(
    camera_api_key_repository: CameraApiKeyRepoDep, location_repository: LocationRepoDep
) -> AuthService:
    return AuthService(camera_api_key_repository, location_repository)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

# --- Security


def valid_key(
    x_api_key: Annotated[Optional[str], Header(alias="X-API-Key")],
    auth_service: AuthServiceDep,
) -> CameraAndLocation:
    if not x_api_key:
        raise get_forbidden_exception("Api key no proporcionada")

    camera_and_location = auth_service.validate_key(x_api_key)
    if not camera_and_location:
        raise get_credentials_exception("Api key invalida")

    if not camera_and_location.camera.active:
        raise get_forbidden_exception("API key expirada")
    return camera_and_location


ValidKeyDep = Annotated[CameraAndLocation, Depends(valid_key)]
