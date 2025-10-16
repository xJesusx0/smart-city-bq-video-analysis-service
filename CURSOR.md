# Video Analysis Service - Contexto del Proyecto

## 📋 Resumen del Proyecto

El **Video Analysis Service** es un microservicio de inteligencia artificial que forma parte del sistema inteligente de gestión de semáforos para ciudades inteligentes (Smart Cities). Su función principal es procesar imágenes de cámaras de tráfico en tiempo real para detectar y contar vehículos, proporcionando datos críticos para la optimización dinámica de semáforos.

### 🎯 Propósito Principal

- **Análisis de imágenes**: Procesa imágenes de cámaras de tráfico usando modelos YOLO
- **Detección de vehículos**: Identifica automóviles, autobuses, camiones, motocicletas, bicicletas y peatones
- **Conteo inteligente**: Proporciona métricas de densidad vehicular por ubicación
- **Integración de datos**: Almacena métricas en MongoDB para análisis posterior

## 🏗️ Arquitectura del Sistema

### Rol en el Ecosistema Smart City

```
Cámaras → Video Analysis Service → Traffic Decision Service → Traffic Lights Service
                ↓
            Traffic API (MongoDB) → Web Client
```

Este servicio actúa como el **cerebro analítico** del sistema, transformando datos visuales en información procesable para la toma de decisiones de tráfico.

### Componentes Principales

- **FastAPI**: Framework web para la API REST
- **YOLOv8**: Modelo de detección de objetos en tiempo real
- **MongoDB**: Base de datos NoSQL para métricas de tráfico
- **MySQL**: Base de datos relacional para autenticación y configuración
- **OpenCV**: Procesamiento de imágenes y anotaciones

## 🛠️ Stack Tecnológico

### Lenguaje y Framework

- **Python 3.13+**: Lenguaje principal
- **FastAPI**: Framework web moderno y rápido
- **Pydantic**: Validación de datos y modelos
- **Uvicorn**: Servidor ASGI para producción

### Inteligencia Artificial

- **Ultralytics YOLOv8**: Modelo de detección de objetos
- **OpenCV**: Procesamiento de imágenes
- **PIL (Pillow)**: Manipulación de imágenes
- **Modelos disponibles**: YOLOv8n, YOLOv8s, YOLOv8m, YOLOv8l

### Bases de Datos

- **MongoDB**: Métricas de tráfico y análisis temporal
- **MySQL**: Gestión de usuarios, API keys y ubicaciones
- **Motor**: Driver asíncrono para MongoDB
- **PyMySQL**: Driver para MySQL

### Herramientas de Desarrollo

- **UV**: Gestor de paquetes y dependencias
- **Pydantic Settings**: Configuración basada en variables de entorno
- **Python Multipart**: Manejo de archivos subidos

## 📁 Estructura del Proyecto

```
video-analysis-service/
├── app/
│   ├── core/                    # Configuración y utilidades centrales
│   │   ├── config.py           # Configuración del servicio
│   │   ├── dependencies.py     # Inyección de dependencias
│   │   ├── exceptions.py       # Manejo de excepciones
│   │   ├── database/           # Conexiones a bases de datos
│   │   │   ├── mongo/          # Cliente MongoDB
│   │   │   └── mysql/          # Conexión MySQL y repositorios
│   │   ├── models/             # Modelos de dominio
│   │   ├── repositories/       # Interfaces de repositorios
│   │   └── security/          # Servicios de autenticación
│   ├── detector.py             # Lógica de detección YOLO
│   ├── main.py                 # Aplicación FastAPI principal
│   └── models.py               # Modelos Pydantic para API
├── models/                     # Modelos YOLO preentrenados
├── uploads/                    # Directorio de imágenes procesadas
└── pyproject.toml             # Configuración del proyecto
```

## 🔧 Funcionalidades Implementadas

### Endpoints de la API

- `GET /` - Información del servicio
- `GET /health` - Health check del servicio
- `GET /model-info` - Información del modelo YOLO
- `POST /analyze` - Análisis de imagen con detección de vehículos

### Características de Detección

- **Clases detectadas**: Personas, bicicletas, automóviles, motocicletas, autobuses, camiones
- **Umbral de confianza**: Configurable (por defecto 0.5)
- **Preprocesamiento**: Redimensionado automático de imágenes grandes
- **Anotación**: Generación de imágenes con detecciones marcadas

### Seguridad

- **Autenticación por API Key**: Validación mediante X-API-Key header
- **Autorización por ubicación**: Cada API key está asociada a una ubicación específica
- **Validación de archivos**: Verificación de tipos de archivo permitidos

## 📊 Almacenamiento de Datos

### MongoDB (Métricas de Tráfico)

- **Colección**: `traffic_metrics`
- **Índices optimizados**: Por ubicación, timestamp, conteo vehicular
- **Formato GeoJSON**: Para consultas geoespaciales
- **Datos almacenados**: Conteos, coordenadas, timestamps, detecciones

### MySQL (Configuración)

- **Tablas**: Cámaras, ubicaciones, API keys
- **Repositorios**: Patrón Repository para acceso a datos
- **Relaciones**: Cámaras vinculadas a ubicaciones geográficas

## 🚀 Puntos de Mejora Identificados

### 1. **Rendimiento y Escalabilidad**

- **Procesamiento asíncrono**: Implementar colas de procesamiento (Redis/RabbitMQ)
- **Cache de modelos**: Reutilizar instancias del modelo YOLO entre requests
- **Batch processing**: Procesar múltiples imágenes simultáneamente
- **Load balancing**: Distribuir carga entre múltiples instancias

### 2. **Monitoreo y Observabilidad**

- **Métricas de Prometheus**: Integrar métricas de rendimiento
- **Logging estructurado**: Implementar logging con niveles y contexto
- **Tracing distribuido**: Agregar OpenTelemetry para seguimiento de requests
- **Alertas**: Configurar alertas para fallos de modelo o alta latencia

### 3. **Calidad del Código**

- **Testing**: Implementar tests unitarios y de integración
- **Type hints**: Completar anotaciones de tipos en todo el código
- **Documentación**: Agregar docstrings detallados
- **Linting**: Configurar pre-commit hooks con black, flake8, mypy

### 4. **Seguridad**

- **Rate limiting**: Implementar límites de requests por API key
- **Validación de imágenes**: Verificar integridad y tamaño de archivos
- **HTTPS**: Configurar certificados SSL para producción
- **Secrets management**: Usar servicios como HashiCorp Vault

### 5. **Funcionalidades Avanzadas**

- **Streaming de video**: Soporte para procesamiento de video en tiempo real
- **Múltiples modelos**: Permitir selección dinámica de modelos YOLO
- **Análisis temporal**: Detectar patrones de tráfico a lo largo del tiempo
- **Machine Learning**: Implementar modelos personalizados para casos específicos

### 6. **DevOps y Despliegue**

- **Containerización**: Crear Dockerfile optimizado
- **Kubernetes**: Configurar manifiestos para orquestación
- **CI/CD**: Pipeline automatizado de testing y despliegue
- **Health checks**: Endpoints más robustos para monitoreo

## 🔄 Flujo de Datos

1. **Recepción**: Cámara envía imagen vía POST /analyze
2. **Autenticación**: Validación de API key y ubicación
3. **Preprocesamiento**: Redimensionado y optimización de imagen
4. **Detección**: YOLO procesa imagen y detecta vehículos
5. **Anotación**: Generación de imagen con detecciones marcadas
6. **Almacenamiento**: Métricas guardadas en MongoDB
7. **Respuesta**: Datos de análisis devueltos al cliente

## 📈 Métricas Clave

- **Tiempo de procesamiento**: Latencia del análisis de imágenes
- **Precisión de detección**: Accuracy del modelo YOLO
- **Throughput**: Imágenes procesadas por segundo
- **Disponibilidad**: Uptime del servicio
- **Conteo vehicular**: Densidad de tráfico por ubicación

## 🎯 Objetivos de Desarrollo

### Corto Plazo

- Implementar testing básico
- Mejorar logging y monitoreo
- Optimizar rendimiento del modelo

### Mediano Plazo

- Agregar soporte para video streaming
- Implementar cache de resultados
- Desarrollar dashboard de métricas

### Largo Plazo

- Integración con sistemas de IA más avanzados
- Análisis predictivo de tráfico
- Optimización automática de parámetros

---

_Este servicio es fundamental para el funcionamiento del ecosistema de Smart Cities, proporcionando la inteligencia necesaria para optimizar la movilidad urbana de manera automática y eficiente._
