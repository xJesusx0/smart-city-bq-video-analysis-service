from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class LocationBase(SQLModel):
    name: str = Field(nullable=False)
    latitude: float = Field(nullable=False)
    longitude: float = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    active: bool = Field(default=True, nullable=False)


class DbLocation(LocationBase, table=True):
    __tablename__ = "locations"

    id: Optional[int] = Field(default=None, primary_key=True)
    creation_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    update_date: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False,
    )
