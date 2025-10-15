from app.models import AnalysisResponse
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from datetime import datetime

from app.core.config import settings


class MongoDB:
    """Cliente de MongoDB para almacenar métricas de tráfico"""

    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    async def connect(self):
        """Conectar a MongoDB"""
        try:
            print(f"🔌 Conectando a MongoDB: {settings.mongodb_url}")
            self.client = AsyncIOMotorClient(settings.mongodb_url)
            self.db = self.client[settings.mongodb_database]

            # Verificar conexión
            await self.client.admin.command("ping")
            print(
                f"✅ Conectado a MongoDB - Base de datos: {settings.mongodb_database}"
            )

            # Crear índices
            await self._create_indexes()

        except Exception as e:
            print(f"❌ Error al conectar a MongoDB: {e}")
            raise

    async def _create_indexes(self):
        """Crear índices para optimizar consultas"""
        collection = self.db[settings.mongodb_collection]

        # Índice compuesto por location_id y timestamp (consultas frecuentes)
        await collection.create_index(
            [("location_id", 1), ("timestamp", -1)], name="idx_location_timestamp"
        )

        # Índice por timestamp solo (consultas de rango de fechas)
        await collection.create_index([("timestamp", -1)], name="idx_timestamp")

        # Índice por location_id solo (filtros por ubicación)
        await collection.create_index([("location_id", 1)], name="idx_location_id")

        # Índice por vehicle_count (para queries de tráfico alto/bajo)
        await collection.create_index([("vehicle_count", -1)], name="idx_vehicle_count")

        # Índice geoespacial (para coordenadas latitude/longitude)
        # Ahora con formato GeoJSON correcto
        await collection.create_index(
            [("location", "2dsphere")], name="idx_location_geo"
        )

        print("📊 Índices de MongoDB creados")
        print("   - idx_location_timestamp (location_id + timestamp)")
        print("   - idx_timestamp (timestamp)")
        print("   - idx_location_id (location_id)")
        print("   - idx_vehicle_count (vehicle_count)")
        print("   - idx_coordinates (latitude + longitude)")
        print("   - idx_location_geo (GeoJSON para queries geoespaciales)")

    async def close(self):
        """Cerrar conexión"""
        if self.client:
            self.client.close()
            print("🔌 Conexión a MongoDB cerrada")

    async def save_metric(self, metric_data: AnalysisResponse) -> str:
        """
        Guardar métrica de tráfico en MongoDB

        Args:
            metric_data: Diccionario con los datos de la métrica

        Returns:
            ID del documento insertado
        """
        collection = self.db[settings.mongodb_collection]
        # Asegurar que tiene timestamp
        metric_data.timestamp = datetime.now()

        metric_data_json = metric_data.model_dump()

        # Agregar metadata de inserción
        metric_data_json["created_at"] = datetime.now()

        # Transformar coordenadas a formato GeoJSON (si existen)
        if "latitude" in metric_data_json and "longitude" in metric_data_json:
            metric_data_json["location"] = {
                "type": "Point",
                "coordinates": [
                    metric_data_json["longitude"],  # Primero longitud
                    metric_data_json["latitude"],  # Después latitud
                ],
            }
            # Mantener también los campos individuales por compatibilidad

        # Insertar documento
        result = await collection.insert_one(metric_data_json)

        print(f"💾 Métrica guardada con ID: {result.inserted_id}")

        return str(result.inserted_id)


# Instancia global
mongodb = MongoDB()
