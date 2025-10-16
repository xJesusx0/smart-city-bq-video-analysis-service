from abc import ABC, abstractmethod
from pydantic import BaseModel


class EventEmissionBody(BaseModel):
    vehicle_count: int
    pedestrian_count: int


class EventEmissionService(ABC):
    @abstractmethod
    async def emit_event(self, event: EventEmissionBody):
        pass
