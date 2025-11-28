# 📊 Documentación de Datos - Salmuera de Litio

## Descripción General

Este dataset contiene mediciones sintéticas de parámetros físico-químicos de salmuera durante el proceso de extracción de litio por evaporación en pozas, simulando condiciones del **Salar del Hombre Muerto, Catamarca, Argentina**.

Los datos están basados en literatura técnica y científica sobre:
- Procesos de extracción de litio de salmueras
- Condiciones climáticas del altiplano catamarqueño
- Rangos operativos típicos de la industria

---

## Variables del Dataset

### Variables Temporales y de Identificación

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `timestamp` | DateTime | Fecha y hora de la medición |
| `poza_id` | String | Identificador de la poza de evaporación (POZA_1 a POZA_5) |

### Variables Independientes (Features)

#### 1. `days_evaporation`
- **Tipo:** Float
- **Rango:** 30 - 180 días
- **Descripción:** Tiempo transcurrido desde inicio del proceso de evaporación
- **Importancia:** Variable crítica - a mayor tiempo, mayor concentración
- **Unidad:** días

#### 2. `temperature_c`
- **Tipo:** Float
- **Rango:** 15 - 35 °C
- **Descripción:** Temperatura ambiente en la ubicación de la poza
- **Contexto:** Catamarca altiplano tiene alta amplitud térmica
- **Impacto:** Mayor temperatura → mayor tasa de evaporación → mayor concentración
- **Unidad:** Grados Celsius (°C)

#### 3. `humidity_percent`
- **Tipo:** Float
- **Rango:** 10 - 40%
- **Descripción:** Humedad relativa del ambiente
- **Contexto:** Clima árido típico del salar
- **Impacto:** Mayor humedad → menor evaporación → menor concentración
- **Unidad:** Porcentaje (%)

#### 4. `ph`
- **Tipo:** Float
- **Rango:** 7.0 - 8.5
- **Descripción:** Nivel de pH de la salmuera
- **Contexto:** Salmueras naturales tienden a ser ligeramente alcalinas
- **Importancia:** Afecta solubilidad de minerales y eficiencia de procesamiento
- **Unidad:** Escala de pH (adimensional)

#### 5. `conductivity_ms_cm`
- **Tipo:** Float
- **Rango:** 50 - 150 mS/cm
- **Descripción:** Conductividad eléctrica de la salmuera
- **Importancia:** Indicador directo de concentración total de sales disueltas
- **Relación:** Mayor conductividad → mayor concentración de iones → mayor Li
- **Unidad:** miliSiemens por centímetro (mS/cm)

#### 6. `density_g_cm3`
- **Tipo:** Float
- **Rango:** 1.10 - 1.25 g/cm³
- **Descripción:** Densidad de la salmuera
- **Contexto:** Agua pura = 1.0 g/cm³; salmuera concentrada > 1.2 g/cm³
- **Importancia:** Medición sencilla en campo que correlaciona con concentración
- **Unidad:** gramos por centímetro cúbico (g/cm³)

#### 7. `mg_li_ratio`
- **Tipo:** Float
- **Rango:** 3 - 15
- **Descripción:** Ratio molar de Magnesio respecto a Litio
- **Importancia:** **CRÍTICA** - El contaminante principal en salmueras
- **Criterio de calidad:**
  - Ratio < 6: **Excelente** (salmuera premium)
  - Ratio 6-10: **Aceptable** (requiere tratamiento)
  - Ratio > 10: **Problemático** (alto costo de purificación)
- **Unidad:** Adimensional (ratio molar)

#### 8. `ca_li_ratio`
- **Tipo:** Float
- **Rango:** 0.5 - 3
- **Descripción:** Ratio molar de Calcio respecto a Litio
- **Importancia:** Afecta pureza del producto final
- **Impacto:** Valores altos requieren pasos adicionales de purificación
- **Unidad:** Adimensional (ratio molar)

---

### Variable Objetivo (Target)

#### `li_concentration_mg_l`
- **Tipo:** Float
- **Rango:** 200 - 6000 mg/L
- **Descripción:** Concentración de litio en la salmuera
- **Importancia:** Variable a predecir - determina momento óptimo de bombeo
- **Criterios operativos:**
  - < 2000 mg/L: Concentración baja - continuar evaporación
  - 2000-3000 mg/L: Aceptable para procesamiento
  - 3000-4500 mg/L: Buena concentración
  - \> 4500 mg/L: Óptima - listo para bombear a siguiente etapa
- **Unidad:** miligramos por litro (mg/L)

---

### Variable Categórica Derivada

#### `quality_status`
- **Tipo:** String (Categórica)
- **Valores posibles:**
  - `"Óptimo"`: Li > 4500 mg/L y Mg/Li < 6
  - `"Bueno"`: Li > 3000 mg/L y Mg/Li < 10
  - `"Aceptable"`: Li > 2000 mg/L
  - `"Bajo"`: Li < 2000 mg/L
- **Descripción:** Clasificación del estado de la salmuera
- **Uso:** Alertas y decisiones automatizadas

---

## Modelo de Generación de Datos

Los datos sintéticos fueron generados usando el siguiente modelo:

```python
# Concentración base por días de evaporación
base_concentration = 2000 + (days_evaporation - 30) * 25

# Factores ambientales
temp_factor = (temperature - 25) * 15      # Más calor = más evaporación
humidity_factor = -(humidity - 25) * 8     # Más humedad = menos evaporación
conductivity_factor = (conductivity - 80) * 3

# Penalización por contaminantes
mg_penalty = -max(0, (mg_li_ratio - 6) * 50)
ca_penalty = -max(0, (ca_li_ratio - 1.5) * 30)

# Concentración final con ruido
li_concentration = base + factores + random_noise(0, 150)
```

---

## Correlaciones Esperadas

| Variable | Correlación con Li | Tipo |
|----------|-------------------|------|
| `days_evaporation` | **+0.85** | Fuerte positiva |
| `conductivity_ms_cm` | **+0.78** | Fuerte positiva |
| `density_g_cm3` | **+0.72** | Fuerte positiva |
| `temperature_c` | **+0.45** | Moderada positiva |
| `humidity_percent` | **-0.38** | Moderada negativa |
| `mg_li_ratio` | **-0.35** | Moderada negativa |
| `ph` | **+0.12** | Débil |

---

## Estadísticas Descriptivas

### Distribución de Concentración de Litio

```
Mínimo:     ~200 mg/L
Q1 (25%):   ~2100 mg/L
Mediana:    ~3200 mg/L
Q3 (75%):   ~4300 mg/L
Máximo:     ~6000 mg/L
Media:      ~3250 mg/L
Desv. Est.: ~1100 mg/L
```

### Distribución por Calidad

- **Óptimo:** ~18% de muestras
- **Bueno:** ~35% de muestras
- **Aceptable:** ~32% de muestras
- **Bajo:** ~15% de muestras

---

## Consideraciones para Modelado

### Variables más predictivas (Top 5)
1. `days_evaporation` - La más importante
2. `conductivity_ms_cm` - Proxy directo de sales
3. `density_g_cm3` - Medición física correlacionada
4. `temperature_c` - Factor ambiental clave
5. `mg_li_ratio` - Afecta concentración efectiva

### Preprocesamiento recomendado
- ✅ **Normalización:** StandardScaler para variables numéricas
- ✅ **Feature Engineering:**
  - Interacción: `days_evaporation × temperature`
  - Ratio: `conductivity / density`
- ⚠️ **Outliers:** Valores extremos son legítimos (no remover)
- ⚠️ **Missing values:** No hay en datos sintéticos, pero en producción requerir imputación

### Modelos recomendados
- **Random Forest:** Robusto, interpretable
- **XGBoost:** Mayor precisión, maneja no-linealidades
- **Ridge/Lasso:** Para baseline lineal rápido

---

## Limitaciones del Dataset Sintético

1. **No captura eventos extremos:**
   - Tormentas que diluyen salmuera
   - Fallas de bombeo
   - Contaminación accidental

2. **Simplificación de química:**
   - Otros iones (K, B, SO4) no modelados
   - Reacciones químicas complejas simplificadas

3. **Temporal:**
   - No hay estacionalidad real
   - Variación climática es simulada

4. **Espacial:**
   - No diferencias entre pozas
   - Asume homogeneidad dentro de cada poza

---

## Uso en Producción

Al migrar a datos reales de sensores IoT, considerar:

1. **Calibración de sensores:** Drift con el tiempo
2. **Frecuencia de medición:** 6 horas es realista, pero ajustable
3. **Validación cruzada:** Con análisis de laboratorio periódicos
4. **Reentrenamiento:** Modelo debe actualizarse con nuevos datos cada 1-3 meses

---

## Referencias Técnicas

Este dataset sintético está inspirado en:
- Literatura sobre salares del altiplano sudamericano
- Reportes técnicos de operaciones en Salar del Hombre Muerto
- Rangos operativos estándar de la industria del litio
- Correlaciones físico-químicas establecidas en investigación académica

---

## Contacto

Para preguntas sobre este dataset:
- Autor: Fernando Molas García
- Email: f.mg@outlook.com
- LinkedIn: [fernando-molas-garcia](https://www.linkedin.com/in/fernando-molas-garcia/)
- GitHub: [fmg75](https://github.com/fmg75)
- Proyecto: Galan Lithium Intelligent Monitoring System
