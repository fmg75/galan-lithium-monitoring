# Supuestos Técnicos y Limitaciones del Proyecto

## Propósito del Documento

Este documento detalla los supuestos, simplificaciones y limitaciones del sistema predictivo desarrollado, con el objetivo de establecer expectativas realistas y transparencia técnica sobre lo que el MVP actual puede y no puede hacer.

---

## 1. SUPUESTOS SOBRE DATOS

### 1.1 Datos Sintéticos vs Datos Reales

**Situación Actual:**
- Los datos utilizados son **100% sintéticos**, generados mediante modelo basado en literatura técnica de salmueras de litio
- N = 1,000 muestras simuladas
- Rango temporal: simulación de ~250 días de operación

**Supuestos del generador sintético:**

```python
# Modelo simplificado usado:
Li_concentration = (
    2000 + (days_evaporation - 30) * 25 +  # Base lineal
    (temperature - 25) * 15 +               # Factor temperatura
    -(humidity - 25) * 8 +                  # Factor humedad
    (conductivity - 80) * 3 +               # Correlación conductividad
    -max(0, (mg_li_ratio - 6) * 50) +      # Penalización Mg
    -max(0, (ca_li_ratio - 1.5) * 30) +    # Penalización Ca
    random_noise(0, 150)                    # Ruido gaussiano
)
```

**Lo que NO captura:**
- ❌ Eventos extremos: tormentas, contaminación accidental, fallas de equipo
- ❌ Variabilidad espacial dentro de una poza (asume homogeneidad)
- ❌ Interacciones químicas complejas (precipitación de sales, etc.)
- ❌ Efectos estacionales reales de clima catamarqueño
- ❌ Degradación de sensores (drift, descalibración)

**Impacto en producción:**
- El modelo deberá ser **reentrenado completamente** con datos reales
- Primeros 3-6 meses: validación en paralelo con laboratorio
- R² actual (0.89) puede bajar a 0.75-0.80 con datos reales inicialmente
- Mejorará a 0.85-0.92 tras reentrenamiento con datos históricos

---

### 1.2 Sensores: Inline vs Laboratorio

#### Variables Realmente Medibles Inline (Tiempo Real)

| Variable | Tecnología | Costo Sensor | Frecuencia | Realismo |
|----------|-----------|--------------|------------|----------|
| **Conductividad** | Sensor toroidal | $5,000 | Continua | ✅ 10/10 |
| **Densidad** | Resonador (Rheonics) | $12,000 | Continua | ✅ 10/10 |
| **Temperatura** | Termopar/RTD | $500 | Continua | ✅ 10/10 |
| **pH** | Electrodo de vidrio | $2,000 | Continua* | ⚠️ 7/10 |
| **Días evaporación** | Timestamp lógico | $0 | Automático | ✅ 10/10 |

*pH inline requiere mantenimiento frecuente y calibración

#### Variables que Requieren Laboratorio o Sensores Avanzados

| Variable | Tecnología Real | Costo | Frecuencia | En MVP |
|----------|----------------|-------|------------|--------|
| **Li+ concentración** | ICP-MS (lab) | $80k | 1-2/día | ❌ Es el OUTPUT del modelo |
| | Ion Chromatography inline | $150k | Cada 30min | 💰 Futuro |
| | NMR Analyzer | $120k | Tiempo real | 💰 Futuro |
| **Mg/Li ratio** | ICP-MS (lab) | - | 1-2/día | ⚠️ Asumido disponible |
| | Ion Selective Electrode | $30k | Continua | 💰 Emergente |
| **Ca/Li ratio** | ICP-MS (lab) | - | 1-2/día | ⚠️ Asumido disponible |

**Decisión de diseño en MVP:**
- El modelo **asume** que ratios Mg/Li y Ca/Li están disponibles (sintéticamente)
- En producción real, **dos opciones:**

**Opción A - Conservadora (Recomendada Fase 1):**
```python
# Modelo solo con sensores inline baratos
inputs_core = [
    'days_evaporation',
    'temperature_c',
    'humidity_percent',  # De estación meteorológica
    'conductivity_ms_cm',
    'density_g_cm3'
]
# Precisión esperada: R² ~ 0.82-0.85
```

**Opción B - Avanzada (Fase 2+):**
```python
# Modelo con todos los inputs (requiere inversión)
inputs_full = inputs_core + [
    'mg_li_ratio',  # Análisis lab 2x/día + interpolación
    'ca_li_ratio'   # o Ion Chromatography inline ($150k)
]
# Precisión esperada: R² ~ 0.88-0.91
```

---

## 2. SUPUESTOS SOBRE EL MODELO ML

### 2.1 Random Forest: Elección y Limitaciones

**Por qué Random Forest:**
1. Robusto con datos ruidosos (esperado en sensores de campo)
2. Maneja relaciones no-lineales sin feature engineering complejo
3. Interpretable (feature importance clara)
4. No requiere normalización estricta
5. Menor riesgo de overfitting que redes neuronales con pocos datos

**Limitaciones conocidas:**

**L1: No soporta fine-tuning incremental**
- Cada actualización requiere reentrenamiento completo
- Estrategia: Reentrenamiento trimestral con ventana deslizante de 12 meses

**L2: Alto consumo de memoria**
- 100 árboles × 15 profundidad = ~50MB en RAM
- No es problema para servidor, pero complicado para edge devices
- Solución: Inferencia en servidor central, no en edge gateway

**L3: Extrapolación limitada**
- Si datos nuevos están fuera del rango de entrenamiento, predicción puede degradarse
- Ejemplo: Si temperatura sube a 40°C (nunca visto en entrenamiento), el modelo predecirá mal
- Mitigación: Alertas cuando inputs están fuera de rango conocido

**L4: No captura tendencias temporales**
- Random Forest no tiene "memoria" de mediciones anteriores
- Cada predicción es independiente
- Alternativa futura: LSTM o XGBoost con lag features

### 2.2 Arquitectura del Modelo

```python
RandomForestRegressor(
    n_estimators=100,      # 100 árboles
    max_depth=15,          # Profundidad máxima
    min_samples_split=5,   # Mínimo para split
    min_samples_leaf=2,    # Mínimo en hojas
    max_features='sqrt',   # √12 ≈ 3-4 features por árbol
    random_state=42,
    n_jobs=-1              # Paralelización
)
```

**Decisiones de hiperparámetros:**

- **n_estimators=100**: Balance entre precisión y velocidad
  - Más árboles = más estable pero más lento
  - 100 es estándar industrial para este tamaño de dataset

- **max_depth=15**: Previene overfitting
  - Dataset con 1,000 muestras no justifica árboles más profundos
  - Validación: R² train (0.91) vs test (0.89) → diferencia aceptable

- **max_features='sqrt'**: Introduce diversidad entre árboles
  - Cada árbol ve solo ~30% de features → menos correlación entre árboles

**NO se usó grid search exhaustivo:**
- Estos hiperparámetros son "buenos defaults" de la literatura
- En producción con datos reales: GridSearchCV o RandomizedSearchCV para optimizar

---

### 2.3 Feature Engineering Aplicado

**Features originales:** 9 variables medidas

**Features derivadas creadas:**
```python
# Interacciones
'temp_x_days' = temperature * days_evaporation
'conductivity_density_ratio' = conductivity / density
'evaporation_rate' = days_evaporation / (humidity + 1)

# Polinomial
'days_evaporation_sq' = days_evaporation²
```

**Total inputs al modelo:** 13 features

**Feature importance (top 5):**
1. days_evaporation: ~35%
2. conductivity_ms_cm: ~22%
3. density_g_cm3: ~16%
4. temp_x_days (derivada): ~10%
5. temperature_c: ~8%

**Por qué estas interacciones:**
- `temp × days`: Captura que evaporación acelerada por calor sostenido
- `conductivity/density`: Proxy de concentración iónica específica
- `days²`: Evaporación no es lineal, se desacelera con el tiempo

---

## 3. SUPUESTOS OPERATIVOS

### 3.1 Condiciones de Operación

**Contexto asumido:**
- Operación en Salar del Hombre Muerto (4,000 msnm, Catamarca)
- Proceso por evaporación solar (no térmico artificial)
- 5 pozas en Fase 1, expansión a 15-20 en Fase 2
- Análisis de laboratorio 1-2 veces/día disponible para validación

**Rangos operativos válidos (entrenamiento):**
```
Variable                  Mín      Máx      Unidad
─────────────────────────────────────────────────
days_evaporation          30       180      días
temperature_c             15       35       °C
humidity_percent          10       40       %
ph                        7.0      8.5      -
conductivity_ms_cm        50       150      mS/cm
density_g_cm3             1.10     1.25     g/cm³
mg_li_ratio               3        15       -
ca_li_ratio               0.5      3        -
```

**⚠️ Alerta crítica:**
Si alguna medición cae fuera de estos rangos, el modelo puede no ser confiable.

**Sistema debe implementar:**
```python
def validate_input(sensor_data):
    if sensor_data['temperature_c'] > 35:
        return {"status": "warning", 
                "message": "Temperatura fuera de rango de entrenamiento"}
    # ... más validaciones
```

### 3.2 Frecuencia de Medición Asumida

**En el MVP:**
- Datos sintéticos simulan medición cada 6 horas

**En producción:**
- Sensores inline: **Continua** (1-60 segundos) → Agregación cada 5-15 min para ML
- Análisis laboratorio: **1-2 veces/día**

**Decisión de diseño:**
- El modelo NO necesita datos cada segundo
- Predicción cada 15-30 minutos es suficiente (concentración cambia lentamente)
- Reducir frecuencia ahorra:
  - Ancho de banda (importante en 4G/satelital)
  - Costo computacional
  - Almacenamiento

---

## 4. SUPUESTOS DE INFRAESTRUCTURA

### 4.1 Conectividad

**Asumido en el diseño:**
- Conectividad 4G o satelital disponible (aunque intermitente está ok)
- Latencia 50-500ms aceptable
- Ancho de banda mínimo: 1-5 Mbps

**Si conectividad falla:**
- Edge Gateway tiene buffer SQLite local (48h de datos)
- Modelo ML puede correr en edge si es crítico (requiere Raspberry Pi 4+ o similar)
- Sincronización diferida cuando conectividad vuelve

### 4.2 Integración con SCADA

**Supuesto:** Galan tiene sistema SCADA/PLC existente

**Dos escenarios:**

**Escenario A - Hay SCADA/Historian:**
- Lectura de datos vía API REST o OPC-UA
- Escritura de predicciones de vuelta al Historian
- Integración no-invasiva (ver `integration_architecture.md`)

**Escenario B - No hay SCADA aún (poco probable):**
- Sistema ML actúa como único sistema de monitoreo
- Necesita dashboard más robusto
- Mayor responsabilidad en confiabilidad

**Pregunta clave para la entrevista:**
"¿Tienen sistema SCADA desplegado actualmente? ¿Qué marca/modelo?"

---

## 5. LIMITACIONES CONOCIDAS

### 5.1 Limitaciones del Modelo

| Limitación | Descripción | Impacto | Mitigación |
|-----------|-------------|---------|------------|
| **Datos sintéticos** | Modelo no validado con datos reales | Alto | Validación paralela 3-6 meses |
| **No temporal** | No usa series de tiempo | Medio | Futuro: LSTM o XGBoost con lags |
| **Extrapolación** | Mal rendimiento fuera de rangos | Medio | Alertas de out-of-range |
| **No ensemble** | Solo Random Forest | Bajo | Futuro: Stacking con XGBoost |
| **Sin drift detection** | No detecta degradación del modelo | Medio | Monitoreo de MAE/R² en producción |

### 5.2 Limitaciones de Sensores

**pH inline:**
- Requiere calibración semanal
- Electrodos se degradan en salmueras concentradas
- Vida útil: 6-12 meses en estas condiciones
- Costo de reemplazo: $500-1000/año por poza

**Densidad inline:**
- Sensores premium (Rheonics) son costosos: $12k
- Alternativa: Medición manual con densímetro portátil ($500) + ingreso manual
- Trade-off: Costo vs automatización

**Mg/Li, Ca/Li inline:**
- Ion Chromatography ($150k) o laboratorio únicamente
- MVP asume datos de laboratorio 1-2/día
- Modelo interpola entre mediciones

### 5.3 Limitaciones Operativas

**Mantenimiento de sensores:**
- Cleaning mecánico trimestral
- Calibración semestral
- Reemplazo de electrodos anual

**Condiciones extremas:**
- Tormentas pueden diluir salmuera abruptamente → Modelo predecirá mal
- Solución: Detectar cambios bruscos de densidad y marcar como "evento anómalo"

**Escalabilidad a Fase 2:**
- Modelo actual es para 5 pozas
- 15-20 pozas requerirán servidor más potente (no cambio de arquitectura)
- Costo incremental: ~30% en hardware

---

## 6. ROADMAP DE VALIDACIÓN

### Fase 1: Piloto (Mes 1-3)

**Objetivo:** Probar en 1 poza real

```
Actividades:
1. Instalar sensores inline (conductividad + densidad)
2. Configurar edge gateway + conectividad
3. Desplegar modelo en servidor
4. Validación paralela:
   - Modelo predice cada 30 min
   - Laboratorio analiza 2x/día
   - Comparar resultados

Métricas de éxito:
- Disponibilidad sistema > 95%
- MAE < 300 mg/L (10% de concentración media)
- R² > 0.75 en datos reales
```

### Fase 2: Expansión (Mes 4-6)

**Objetivo:** Rollout a las 5 pozas de Fase 1

```
Actividades:
1. Reentrenamiento con datos reales de piloto
2. Instalación en 4 pozas restantes
3. Integración con SCADA/Historian
4. Capacitación de operadores

Métricas de éxito:
- R² > 0.82 promedio en las 5 pozas
- Reducción de 40% en análisis de laboratorio
- 0 incidentes de decisiones erróneas críticas
```

### Fase 3: Optimización (Mes 7-12)

**Objetivo:** Ajuste fino y automatización

```
Actividades:
1. Incorporar feedback de operadores
2. Reentrenamiento trimestral automático
3. Dashboard unificado con SCADA
4. Piloto de decisiones semi-automáticas en 1 poza

Métricas de éxito:
- R² > 0.87 sostenido
- ROI positivo (ahorros > inversión)
- Adopción del 80%+ por operadores
```

---

## 7. RIESGOS TÉCNICOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Modelo no alcanza precisión en datos reales | Media | Alto | Validación extensa, reentrenamiento iterativo |
| Sensores inline no soportan ambiente extremo | Baja | Medio | Selección de equipos industriales certificados |
| Conectividad 4G inestable | Alta | Bajo | Buffer local + sync diferida |
| Operadores no adoptan sistema | Media | Alto | Capacitación, UI intuitiva, validación paralela larga |
| Costo de sensores Ion Chromatography no justificable | Media | Bajo | Modelo funciona sin ellos (R² 0.82 vs 0.89) |

---

## 8. ALTERNATIVAS CONSIDERADAS

### 8.1 Modelos Alternativos

**XGBoost:**
- **Pros:** +2-3% de precisión típicamente
- **Contras:** Más difícil de interpretar, más hiperparámetros
- **Decisión:** Usar Random Forest para MVP, evaluar XGBoost en Fase 3

**Redes Neuronales (MLP):**
- **Pros:** Muy flexible
- **Contras:** Requiere más datos (10k+ muestras), caja negra, overfitting fácil
- **Decisión:** No apropiado para este dataset/problema

**Regresión Lineal:**
- **Pros:** Muy simple, rápido
- **Contras:** Asume linealidad (relación NO es lineal)
- **Decisión:** Solo para baseline de comparación

### 8.2 Arquitecturas de Despliegue

**Cloud-only:**
- Todos los datos y modelo en AWS/GCP
- **Rechazo:** Latencia, costo de datos celular, dependencia de conectividad

**Edge-only:**
- Todo corre en gateway local
- **Rechazo:** Limitación computacional para modelos grandes, dificulta actualización

**Híbrido (Elegido):**
- Inferencia en servidor central
- Buffer y preprocesamiento en edge
- **Ventaja:** Balance de costo, latencia, y mantenibilidad

---

## 9. TRANSPARENCIA Y HONESTIDAD

### Lo que este proyecto ES:

✅ Demostración técnica de concepto end-to-end  
✅ Arquitectura productizable con ajustes  
✅ Modelo ML funcional con datos sintéticos realistas  
✅ Análisis de negocio y ROI fundamentado  
✅ Integración pensada con sistemas industriales reales  

### Lo que este proyecto NO ES:

❌ Sistema listo para producción inmediata  
❌ Modelo validado con datos reales  
❌ Certificado para ambiente industrial  
❌ Reemplazo de análisis de laboratorio sin validación  
❌ Solución a todos los problemas de calidad de salmuera  

### Expectativa realista de timeline:

```
MVP (este proyecto):           [====] 1 semana
+ Instalación sensores:        [====] 2-3 semanas
+ Validación piloto:           [============] 3 meses
+ Reentrenamiento datos reales:[====] 1 mes
+ Rollout completo Fase 1:     [========] 2 meses
──────────────────────────────────────────────────
TOTAL a producción:            7-9 meses desde inicio
```

---

## 10. CONCLUSIÓN

Este proyecto representa un **punto de partida sólido** para implementar predicción ML de concentración de litio en Galan Lithium, con conciencia clara de:

1. **Dónde estamos:** MVP con datos sintéticos, arquitectura diseñada
2. **Qué falta:** Validación con datos reales, ajuste de sensores, integración con SCADA
3. **Cómo llegar:** Roadmap de 7-9 meses con validación exhaustiva

**La propuesta de valor no es un sistema terminado, sino:**
- Demostración de capacidad técnica y pensamiento sistemático
- Reducción significativa de riesgo de implementación
- Aceleración del timeline (de 12-18 meses a 7-9 meses)

---

## Referencias

- Flexer, V. et al. (2018). "Lithium recovery from brines: A vital raw material for green energies with a potential environmental impact" *Science of the Total Environment*
- Jaskula, B. (2024). "Mineral Commodity Summaries - Lithium" *USGS*
- Rheonics. (2024). "Process Monitoring in Lithium Extraction"
- Metrohm. (2024). "Ion Chromatography in Brine Analysis"

---

**Autor:** Fernando Molas García  
**Versión:** 1.0  
**Fecha:** Diciembre 2025  
**Propósito:** Establecer transparencia técnica sobre supuestos y limitaciones del proyecto