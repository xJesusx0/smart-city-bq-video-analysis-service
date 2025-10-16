from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración del servicio de análisis"""

    # Configuración del servidor
    app_name: str = "Video Analysis Service"
    host: str = "0.0.0.0"
    port: int = 8001
    debug: bool = True
    db_url: str = ""

    # Directorios
    upload_dir: Path = Path("uploads")
    models_dir: Path = Path("models")

    # Configuración de YOLO
    yolo_model: str = "yolov8n.pt"  # nano (más rápido, menos preciso)
    # Otras opciones: yolov8s.pt (small), yolov8m.pt (medium)
    confidence_threshold: float = 0.5  # Confianza mínima para detección

    # Clases de vehículos del dataset COCO
    # 0: person, 1: bicycle, 2: car, 3: motorcycle, 5: bus, 7: truck
    vehicle_classes: list[int] = [0, 1, 2, 3, 5, 7]

    # Configuración de procesamiento
    max_image_size: int = 1280  # Redimensionar imágenes grandes

    mongodb_url: str = "mongodb://admin:admin123@localhost:27017"
    mongodb_database: str = "smart_traffic"
    mongodb_collection: str = "traffic_metrics"

    esp32_server_url: str = "http://localhost:9090"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instancia global de configuración
settings = Settings()

# Crear directorios si no existen
settings.upload_dir.mkdir(exist_ok=True)
settings.models_dir.mkdir(exist_ok=True)
