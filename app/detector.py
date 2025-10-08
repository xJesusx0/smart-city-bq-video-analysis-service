from ultralytics import YOLO
from pathlib import Path
from PIL import Image
import cv2
from typing import Dict
import time

from app.config import settings
from app.models import VehicleDetection, BoundingBox


class VehicleDetector:
    """Detector de vehículos usando YOLOv8"""

    def __init__(self):
        """Inicializa el modelo YOLO"""
        self.model = None
        self.model_path = settings.models_dir / settings.yolo_model

        # ✅ Definir PRIMERO class_names
        self.class_names = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}

        # ✅ DESPUÉS cargar el modelo
        self._load_model()

    def _load_model(self):
        """Carga el modelo YOLO"""
        try:
            print(f"🔄 Cargando modelo YOLO: {settings.yolo_model}")

            # YOLO descargará automáticamente el modelo si no existe
            self.model = YOLO(settings.yolo_model)

            print(f"✅ Modelo cargado exitosamente")
            print(f"📊 Clases de vehículos: {list(self.class_names.values())}")

        except Exception as e:
            print(f"❌ Error al cargar el modelo: {e}")
            raise

    def _preprocess_image(self, image_path: Path) -> Path:
        """
        Preprocesa la imagen antes del análisis
        - Redimensiona si es muy grande
        - Convierte formatos si es necesario
        """
        try:
            img = Image.open(image_path)

            # Redimensionar si excede el tamaño máximo
            max_size = settings.max_image_size
            if max(img.size) > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                print(f"🔧 Imagen redimensionada a: {img.size}")

            # Guardar imagen procesada
            processed_path = image_path.parent / f"processed_{image_path.name}"
            img.save(processed_path)

            return processed_path

        except Exception as e:
            print(f"⚠️  Error en preprocesamiento: {e}")
            return image_path  # Retornar original si falla

    def detect_vehicles(self, image_path: Path) -> Dict:
        """
        Detecta vehículos en una imagen

        Args:
            image_path: Ruta a la imagen

        Returns:
            Dict con información de detecciones
        """
        if self.model is None:
            raise RuntimeError("Modelo YOLO no está cargado")

        start_time = time.time()

        try:
            # Preprocesar imagen
            processed_path = self._preprocess_image(image_path)

            # Ejecutar detección
            results = self.model(
                str(processed_path),
                conf=settings.confidence_threshold,
                verbose=False,  # No mostrar logs de YOLO
            )

            # Procesar resultados
            detections = []
            for result in results:
                boxes = result.boxes

                for box in boxes:
                    class_id = int(box.cls[0])

                    # Filtrar solo vehículos
                    if class_id in settings.vehicle_classes:
                        # Obtener coordenadas
                        coords = box.xyxy[0].tolist()

                        detection = VehicleDetection(
                            class_name=self.class_names.get(class_id, "unknown"),
                            confidence=float(box.conf[0]),
                            bbox=BoundingBox(
                                x1=coords[0], y1=coords[1], x2=coords[2], y2=coords[3]
                            ),
                        )
                        detections.append(detection)

            processing_time = time.time() - start_time

            print(
                f"🚗 Detectados {len(detections)} vehículos en {processing_time:.2f}s"
            )

            return {
                "vehicle_count": len(detections),
                "detections": detections,
                "processing_time": processing_time,
            }

        except Exception as e:
            print(f"❌ Error en detección: {e}")
            raise

    def detect_and_annotate(self, image_path: Path, output_path: Path) -> Dict:
        """
        Detecta vehículos y genera imagen anotada con las detecciones

        Args:
            image_path: Ruta a la imagen original
            output_path: Ruta donde guardar la imagen anotada

        Returns:
            Dict con información de detecciones
        """
        # Obtener detecciones
        result = self.detect_vehicles(image_path)

        # Cargar imagen original
        img = cv2.imread(str(image_path))

        # Dibujar detecciones
        for detection in result["detections"]:
            bbox = detection.bbox

            # Coordenadas
            x1, y1 = int(bbox.x1), int(bbox.y1)
            x2, y2 = int(bbox.x2), int(bbox.y2)

            # Color según tipo de vehículo
            colors = {
                "car": (0, 255, 0),  # Verde
                "truck": (255, 0, 0),  # Azul
                "bus": (0, 0, 255),  # Rojo
                "motorcycle": (255, 255, 0),  # Cian
            }
            color = colors.get(detection.class_name, (255, 255, 255))

            # Dibujar rectángulo
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

            # Agregar etiqueta
            label = f"{detection.class_name} {detection.confidence:.2f}"
            cv2.putText(
                img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            )

        # Guardar imagen anotada
        cv2.imwrite(str(output_path), img)

        print(f"💾 Imagen anotada guardada en: {output_path}")

        return result

    def get_model_info(self) -> Dict:
        """Retorna información del modelo"""
        return {
            "model_name": settings.yolo_model,
            "model_loaded": self.model is not None,
            "confidence_threshold": settings.confidence_threshold,
            "vehicle_classes": list(self.class_names.values()),
        }
