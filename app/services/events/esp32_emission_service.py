from app.models import AnalysisResponse
from app.services.events.event_emission_service import (
    EventEmissionBody,
    EventEmissionService,
)
import httpx
from app.core.config import settings


class ESP32EmissionService(EventEmissionService):
    def __init__(self, esp32_url: str):
        self.client = httpx.AsyncClient()
        self.esp32_url = esp32_url

    async def emit_event(self, event: EventEmissionBody):
        response = await self.client.get(
            f"{self.esp32_url}/events?v={event.vehicle_count}&p={event.pedestrian_count}",
        )
        return response.json()

    @classmethod
    def process_analysis_response(cls, response: AnalysisResponse):
        detections = response.detections
        pedestrian_count = 0
        vehicle_count = 0
        for detection in detections:
            if detection.class_name == "person":
                pedestrian_count += 1
            elif detection.class_name in ["car", "bus", "truck", "motorcycle"]:
                vehicle_count += 1
        return EventEmissionBody(
            vehicle_count=vehicle_count, pedestrian_count=pedestrian_count
        )


esp32_emission_service = ESP32EmissionService(settings.esp32_server_url)
