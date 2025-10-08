from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class CameraApiKeyBase(SQLModel):
    location_id: int = Field(foreign_key="locations.id", nullable=False)
    api_key: str = Field(max_length=64, unique=True, nullable=False)
    key_name: Optional[str] = Field(default=None, max_length=255)
    active: bool = Field(default=True, nullable=False)
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class DbCameraApiKey(CameraApiKeyBase, table=True):
    __tablename__ = "camera_api_keys"

    id: Optional[int] = Field(default=None, primary_key=True)
    creation_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    update_date: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False,
    )
