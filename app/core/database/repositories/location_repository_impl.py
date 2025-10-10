from app.core.models.location import DbLocation
from typing import Optional
from sqlmodel.orm.session import Session
from app.core.repositories.location_repository import LocationRepository
from sqlmodel import select


class LocationRepositoryImpl(LocationRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Optional[DbLocation]:
        if id is None:
            return None

        statement = select(DbLocation).where(DbLocation.id == id)
        result = self.session.exec(statement).first()
        return result
