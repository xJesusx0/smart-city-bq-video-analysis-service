from typing import Optional
from abc import ABC, abstractmethod
from app.core.models.location import DbLocation


class LocationRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[DbLocation]:
        pass
