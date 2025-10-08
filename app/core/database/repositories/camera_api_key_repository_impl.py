from app.core.models.camera_api_key import DbCameraApiKey
from typing import Optional
from sqlmodel.orm.session import Session
from app.core.repositories.camera_api_key_repository import CameraApiKeyRepository
from sqlmodel import select


class CameraApiKeyRepositoryImpl(CameraApiKeyRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_api_key_by_key(self, api_key: str) -> Optional[DbCameraApiKey]:
        if api_key is None or api_key.strip() == "":
            return None

        statement = select(DbCameraApiKey).where(DbCameraApiKey.api_key == api_key)
        result = self.session.exec(statement).first()
        return result
