from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import uvicorn

from app.core.config import settings
from app.models import AnalysisResponse, HealthResponse, ErrorResponse
from app.detector import VehicleDetector
from app.core.dependencies import ValidKeyDep

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    description="Servicio de análisis de imágenes para detección de vehículos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variable global para el detector (se inicializa después)
detector = None


@app.on_event("startup")
async def startup_event():
    """Se ejecuta al iniciar el servidor"""
    global detector
    print("🚀 Iniciando Video Analysis Service...")
    print(f"📁 Directorio de uploads: {settings.upload_dir}")
    print(f"🤖 Modelo YOLO: {settings.yolo_model}")

    try:
        detector = VehicleDetector()
        print("✅ Detector YOLO inicializado correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar detector: {e}")
        print("⚠️  El servicio funcionará pero no podrá procesar imágenes")


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "service": settings.app_name,
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Verificar estado del servicio"""
    return HealthResponse(
        status="healthy", service=settings.app_name, model_loaded=detector is not None
    )


@app.get("/model-info", tags=["Info"])
async def get_model_info():
    """Obtener información del modelo YOLO"""
    if detector is None:
        raise HTTPException(status_code=503, detail="Detector no disponible")
    return detector.get_model_info()


@app.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_image(
    camera_and_location: ValidKeyDep,
    file: UploadFile = File(..., description="Imagen a analizar"),
):
    """
    Analiza una imagen y detecta vehículos

    - **file**: Archivo de imagen (JPG, PNG)
    """

    if detector is None:
        raise HTTPException(status_code=503, detail="Detector YOLO no está disponible")

    # Validar tipo de archivo
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    try:
        start_time = datetime.now()

        # Guardar imagen
        file_path = settings.upload_dir / file.filename
        with file_path.open("wb") as buffer:
            content = await file.read()
            buffer.write(content)

        print(f"📥 Imagen recibida: {file.filename} ({len(content)} bytes)")

        # Detectar vehículos
        result = detector.detect_vehicles(file_path)

        # Generar imagen anotada
        annotated_path = settings.upload_dir / f"annotated_{file.filename}"
        detector.detect_and_annotate(file_path, annotated_path)

        processing_time = (datetime.now() - start_time).total_seconds()

        return AnalysisResponse(
            success=True,
            location_id=camera_and_location.camera.location_id,
            image_path=str(file_path),
            vehicle_count=result["vehicle_count"],
            detections=result["detections"],
            processing_time=processing_time,
            longitude=camera_and_location.location.longitude or 0.0,
            latitude=camera_and_location.location.latitude or 0.0,
            location_name=camera_and_location.location.name,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al procesar la imagen: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Manejador global de excepciones"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error", detail=str(exc)
        ).model_dump(),
    )


def start():
    """Función para iniciar el servidor"""
    uvicorn.run(
        "app.main:app", host=settings.host, port=settings.port, reload=settings.debug
    )


if __name__ == "__main__":
    start()
