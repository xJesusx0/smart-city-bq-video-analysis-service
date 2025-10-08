from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración del servicio de análisis"""

    # Configuración del servidor
    app_name: str = "Video Analysis Service"
    host: str = "0.0.0.0"
    port: int = 8001
    debug: bool = True

    # Directorios
    upload_dir: Path = Path("uploads")
    models_dir: Path = Path("models")

    # Configuración de YOLO
    yolo_model: str = "yolov8n.pt"  # nano (más rápido, menos preciso)
    # Otras opciones: yolov8s.pt (small), yolov8m.pt (medium)
    confidence_threshold: float = 0.5  # Confianza mínima para detección

    # Clases de vehículos del dataset COCO
    # 2: car, 3: motorcycle, 5: bus, 7: truck
    vehicle_classes: list[int] = [2, 3, 5, 7]

    # Configuración de procesamiento
    max_image_size: int = 1280  # Redimensionar imágenes grandes

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instancia global de configuración
settings = Settings()

# Crear directorios si no existen
settings.upload_dir.mkdir(exist_ok=True)
settings.models_dir.mkdir(exist_ok=True)
