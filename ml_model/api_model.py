"""
API FastAPI para servir modelo predictivo de concentración de litio
Galan Lithium - Hombre Muerto West
"""

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
from typing import Optional
import joblib
import pandas as pd
from datetime import datetime
import logging
import os

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Variables globales para modelo
MODEL = None
MODEL_METADATA = None
FEATURE_NAMES = None

# Rangos válidos de features (del entrenamiento)
# Actualizados con datos climáticos reales de Salar del Hombre Muerto
VALID_RANGES = {
    'days_evaporation': (30, 180),
    'temperature_c': (5, 30),      # Ajustado: heladas (-10°C) a verano (30°C)
    'humidity_percent': (5, 40),   # Clima muy árido
    'ph': (7.0, 8.5),
    'conductivity_ms_cm': (50, 150),
    'density_g_cm3': (1.10, 1.25),
    'mg_li_ratio': (3, 15),
    'ca_li_ratio': (0.5, 3)
}


def load_model():
    """Cargar modelo y metadata al inicio"""
    global MODEL, MODEL_METADATA, FEATURE_NAMES
    
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
        metadata_path = os.path.join(os.path.dirname(__file__), 'model_metadata.pkl')
        
        if not os.path.exists(model_path):
            logger.error(f"Modelo no encontrado en: {model_path}")
            raise FileNotFoundError("Modelo no encontrado")
        
        MODEL = joblib.load(model_path)
        logger.info("Modelo cargado exitosamente")
        
        if os.path.exists(metadata_path):
            MODEL_METADATA = joblib.load(metadata_path)
            FEATURE_NAMES = MODEL_METADATA.get('feature_cols', [])
            logger.info(f"Metadata cargada. Features: {len(FEATURE_NAMES)}")
        else:
            logger.warning("Metadata no encontrada, usando features por defecto")
            FEATURE_NAMES = list(VALID_RANGES.keys())
        
        return True
        
    except Exception as e:
        logger.error(f"Error cargando modelo: {str(e)}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    logger.info("Iniciando API...")
    load_model()
    logger.info("API lista para recibir requests")
    yield
    # Shutdown
    logger.info("Cerrando API...")


# Inicializar FastAPI con lifespan
app = FastAPI(
    title="Galan Lithium - Brine Concentration Predictor API",
    description="API REST para predicción de concentración de litio en salmuera",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


class SensorData(BaseModel):
    """Modelo de datos de entrada desde sensores"""
    
    poza_id: str = Field(..., description="Identificador de la poza", examples=["POZA_1"])
    timestamp: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="Timestamp de la medición"
    )
    days_evaporation: float = Field(
        ..., 
        ge=0, 
        le=365,
        description="Días desde inicio de evaporación",
        examples=[87.5]
    )
    temperature_c: float = Field(
        ...,
        description="Temperatura ambiente (°C) - Rango: -10 a 30°C",
        examples=[24.5]
    )
    humidity_percent: float = Field(
        ...,
        ge=0,
        le=100,
        description="Humedad relativa (%) - Clima árido: 5-40%",
        examples=[18.2]
    )
    ph: float = Field(
        ...,
        ge=0,
        le=14,
        description="pH de la salmuera",
        examples=[7.8]
    )
    conductivity_ms_cm: float = Field(
        ...,
        description="Conductividad eléctrica (mS/cm)",
        examples=[98.3]
    )
    density_g_cm3: float = Field(
        ...,
        description="Densidad de la salmuera (g/cm³)",
        examples=[1.182]
    )
    mg_li_ratio: Optional[float] = Field(
        None,
        description="Ratio Mg/Li (opcional, de laboratorio)",
        examples=[5.2]
    )
    ca_li_ratio: Optional[float] = Field(
        None,
        description="Ratio Ca/Li (opcional, de laboratorio)",
        examples=[1.3]
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "poza_id": "POZA_1",
                    "days_evaporation": 87.5,
                    "temperature_c": 24.5,
                    "humidity_percent": 18.2,
                    "ph": 7.8,
                    "conductivity_ms_cm": 98.3,
                    "density_g_cm3": 1.182,
                    "mg_li_ratio": 5.2,
                    "ca_li_ratio": 1.3
                }
            ]
        }
    }


class PredictionResponse(BaseModel):
    """Modelo de respuesta de predicción"""
    
    poza_id: str
    timestamp: datetime
    predicted_concentration_mg_l: float
    confidence: str
    quality_status: str
    recommendation: str
    warnings: list[str]
    model_version: str


def validate_input_ranges(data: SensorData) -> list[str]:
    """Validar que los inputs están en rangos conocidos"""
    warnings = []
    
    for feature, (min_val, max_val) in VALID_RANGES.items():
        value = getattr(data, feature, None)
        
        if value is None:
            continue
            
        if value < min_val or value > max_val:
            warnings.append(
                f"{feature}={value:.2f} está fuera del rango de entrenamiento "
                f"({min_val}-{max_val}). Predicción puede ser menos confiable."
            )
    
    return warnings


def calculate_derived_features(data: dict) -> dict:
    """Calcular features derivadas (feature engineering)"""
    
    # Interacciones
    data['temp_x_days'] = data['temperature_c'] * data['days_evaporation']
    data['conductivity_density_ratio'] = data['conductivity_ms_cm'] / data['density_g_cm3']
    data['evaporation_rate'] = data['days_evaporation'] / (data['humidity_percent'] + 1)
    
    # Polinomial
    data['days_evaporation_sq'] = data['days_evaporation'] ** 2
    
    return data


def determine_quality_status(concentration: float, mg_li_ratio: Optional[float]) -> str:
    """Determinar estado de calidad de la salmuera"""
    
    if mg_li_ratio is None:
        # Sin ratio Mg/Li, solo basado en concentración
        if concentration > 4500:
            return "Bueno - Alto Li"
        elif concentration > 3000:
            return "Aceptable"
        elif concentration > 2000:
            return "Bajo"
        else:
            return "Muy Bajo"
    
    # Con ratio Mg/Li (completo)
    if concentration > 4500 and mg_li_ratio < 6:
        return "Óptimo"
    elif concentration > 3000 and mg_li_ratio < 10:
        return "Bueno"
    elif concentration > 2000:
        return "Aceptable"
    else:
        return "Bajo"


def generate_recommendation(concentration: float, quality_status: str) -> str:
    """Generar recomendación operativa"""
    
    if concentration > 4500:
        return "Concentración óptima alcanzada. Recomendar bombeo a siguiente etapa."
    elif concentration > 3500:
        return "Concentración buena. Continuar evaporación 1-2 semanas más."
    elif concentration > 2500:
        return "Concentración en desarrollo. Continuar evaporación."
    else:
        return "Concentración baja. Continuar evaporación, monitorear clima."


@app.get("/")
async def root():
    """Endpoint raíz con información básica"""
    return {
        "service": "Galan Lithium - Brine Concentration Predictor",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Verificar salud de la API"""
    
    model_loaded = MODEL is not None
    
    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "timestamp": datetime.now().isoformat(),
        "features_count": len(FEATURE_NAMES) if FEATURE_NAMES else 0
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_concentration(data: SensorData):
    """
    Predecir concentración de litio en salmuera
    
    Recibe datos de sensores y devuelve predicción con recomendaciones
    """
    
    if MODEL is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo no disponible. Contactar administrador."
        )
    
    try:
        # Validar rangos
        warnings = validate_input_ranges(data)
        
        # Preparar features
        features_dict = {
            'days_evaporation': data.days_evaporation,
            'temperature_c': data.temperature_c,
            'humidity_percent': data.humidity_percent,
            'ph': data.ph,
            'conductivity_ms_cm': data.conductivity_ms_cm,
            'density_g_cm3': data.density_g_cm3,
            'mg_li_ratio': data.mg_li_ratio or 7.0,
            'ca_li_ratio': data.ca_li_ratio or 1.5
        }
        
        # Calcular features derivadas
        features_dict = calculate_derived_features(features_dict)
        
        # Crear DataFrame en el orden correcto
        features_df = pd.DataFrame([features_dict])
        
        # Asegurar que tenemos todas las features en orden correcto
        if FEATURE_NAMES:
            missing_features = set(FEATURE_NAMES) - set(features_df.columns)
            if missing_features:
                raise ValueError(f"Features faltantes: {missing_features}")
            
            features_df = features_df[FEATURE_NAMES]
        
        # Predicción
        prediction = MODEL.predict(features_df)[0]
        
        # Determinar confianza
        if warnings:
            confidence = "BAJA - Inputs fuera de rango de entrenamiento"
        elif data.mg_li_ratio is None:
            confidence = "MEDIA - Sin ratios de impurezas (Mg/Li, Ca/Li)"
        else:
            confidence = "ALTA"
        
        # Determinar calidad
        quality_status = determine_quality_status(prediction, data.mg_li_ratio)
        
        # Generar recomendación
        recommendation = generate_recommendation(prediction, quality_status)
        
        # Logging
        logger.info(
            f"Predicción: {data.poza_id} | "
            f"Días: {data.days_evaporation:.1f} | "
            f"Predicción: {prediction:.1f} mg/L | "
            f"Confianza: {confidence}"
        )
        
        return PredictionResponse(
            poza_id=data.poza_id,
            timestamp=data.timestamp,
            predicted_concentration_mg_l=round(prediction, 2),
            confidence=confidence,
            quality_status=quality_status,
            recommendation=recommendation,
            warnings=warnings,
            model_version=MODEL_METADATA.get('model_type', 'RandomForest') if MODEL_METADATA else 'Unknown'
        )
        
    except ValueError as ve:
        logger.error(f"Error de validación: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en predicción: {str(e)}"
        )


@app.get("/model/info")
async def model_info():
    """Información sobre el modelo cargado"""
    
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        # Info básica siempre disponible
        info = {
            "model_type": "RandomForestRegressor",
            "status": "loaded"
        }
        
        # Agregar features si existen
        if FEATURE_NAMES:
            info['features_count'] = len(FEATURE_NAMES)
            info['features_sample'] = FEATURE_NAMES[:5]  # Primeras 5
        
        # Agregar n_estimators del modelo
        try:
            if hasattr(MODEL, 'n_estimators'):
                info['n_estimators'] = int(MODEL.n_estimators)
        except:
            pass
        
        # Agregar métricas si existen en metadata - CORREGIDO
        try:
            if MODEL_METADATA:
                if isinstance(MODEL_METADATA, dict) and 'metrics' in MODEL_METADATA:
                    metrics = MODEL_METADATA['metrics']
                    # Convertir explícitamente a tipos serializables
                    info['metrics'] = {}
                    for key, value in metrics.items():
                        # Convertir numpy/pandas types a Python natives
                        if hasattr(value, 'item'):  # numpy scalar
                            info['metrics'][key] = float(value.item())
                        elif isinstance(value, (int, float, str, bool, type(None))):
                            info['metrics'][key] = value
                        else:
                            # Para otros tipos, convertir a string
                            info['metrics'][key] = str(value)
        except Exception as e:
            logger.warning(f"No se pudieron agregar métricas: {str(e)}")
            # No fallar, simplemente no incluir las métricas
        
        return info
        
    except Exception as e:
        logger.error(f"Error en model_info: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    # Cargar modelo antes de iniciar
    load_model()
    
    # Iniciar servidor
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )