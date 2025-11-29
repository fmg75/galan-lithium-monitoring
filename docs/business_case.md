# Caso de Negocio: Sistema Predictivo de Calidad de Salmuera

## Resumen Ejecutivo

**Problema:** El proceso tradicional de análisis de calidad de salmuera en pozas de evaporación demora 24-48 horas, generando decisiones reactivas que impactan en eficiencia operativa y calidad del producto final.

**Solución:** Sistema inteligente que combina sensores IoT + Machine Learning + Automatización (n8n) para predicción en tiempo real de concentración de litio, reduciendo el tiempo de decisión a menos de 5 minutos.

**Impacto esperado:** Mejora del 15-20 % en eficiencia operativa, reducción del 30-40 % en costos de análisis y mejora en la calidad de producto premium (cloruro de litio de alta pureza).

---

## 1. Contexto de Galan Lithium

### Operación actual

- **Proyecto:** Hombre Muerto West, Salar del Hombre Muerto, Catamarca  
- **Fase 1:** 5.400 tpa (toneladas por año) de LCE (Litio Carbonato Equivalente)  
- **Fase 2:** Escalamiento a 21.000 tpa  
- **Primera producción:** Programada para primer semestre de 2026  
- **Estrategia:** Producción de cloruro de litio de alta pureza (producto premium)

### Producto estratégico

El **cloruro de litio** es un concentrado demandado por convertidores que producen:

- Fosfato de hierro y litio (LFP) para baterías  
- Óxido de litio-níquel-manganeso-cobalto (NMC)  
- Otros productos químicos de litio de alto valor  

**Requerimiento crítico:** Control de calidad excepcional, especialmente en contenido de litio y niveles muy bajos de contaminantes (Mg, Ca).

---

## 2. El problema actual

### 2.1 Proceso tradicional de análisis

```text
Toma de muestra → Transporte a laboratorio → Análisis químico → Resultado → Decisión
     (30 min)            (2-4 horas)              (8-12 horas)         (24-48 h total)
```

### 2.2 Limitaciones operativas

| Aspecto        | Situación actual       | Impacto                      |
|----------------|------------------------|------------------------------|
| Frecuencia     | 1-2 análisis por día   | Información desactualizada   |
| Cobertura      | Muestreo puntual       | No representa toda la poza   |
| Tiempo         | 24-48 horas            | Decisiones tardías           |
| Costo          | 50-150 USD/análisis    | Alto OPEX                    |
| Trazabilidad   | Manual                 | Errores, falta de auditoría  |

### 2.3 Consecuencias empresariales

**Costos directos:**

- Análisis de laboratorio: ~80.000 USD/año (Fase 1)  
- Pérdidas por decisiones tardías: ~120.000 USD/año (estimado)  
- Reprocesamiento de salmuera fuera de especificación  

**Costos indirectos:**

- Tiempo de operadores en gestión manual  
- Riesgo de calidad en producto final (impacta precio de venta)  
- Falta de datos para optimización continua  

**Riesgo regulatorio:**

- El régimen RIGI requiere trazabilidad robusta  
- Auditorías ambientales necesitan registros completos  

---

## 3. La solución propuesta

### 3.1 Arquitectura del sistema

```text
CAPA 1: SENSORES IoT
├── pH
├── Conductividad eléctrica
├── Temperatura
├── Densidad
└── Estación meteorológica

CAPA 2: AUTOMATIZACIÓN (n8n)
├── Ingesta de datos
├── Preprocesamiento
└── Orquestación de flujos

CAPA 3: INTELIGENCIA ARTIFICIAL
├── Modelo ML predictivo
├── API FastAPI
└── Validación continua

CAPA 4: ACCIONES AUTOMATIZADAS
├── Alertas en tiempo real
├── Dashboard operativo
├── Reportes automáticos
└── Base de datos auditada
```

### 3.2 Funcionalidades clave

**Predicción en tiempo real:**

- Concentración de litio con más del 95 % de precisión  
- Actualización cada 15-30 minutos  
- Confianza estadística en cada predicción  

**Alertas inteligentes:**

- Li > 4.500 mg/L → “Listo para bombear a siguiente poza”  
- Mg/Li > 10 → “Riesgo de contaminación: revisar”  
- Tendencias anómalas → “Atención requerida”  

**Trazabilidad total:**

- Registro de todas las mediciones  
- Historial de decisiones automatizadas  
- Auditoría para cumplimiento del régimen RIGI  

---

## 4. Retorno de inversión (ROI)

### 4.1 Inversión estimada

| Concepto                 | Costo (USD) | Notas                                             |
|--------------------------|-------------|---------------------------------------------------|
| Sensores IoT (5 pozas)   | 25.000      | pH, conductividad, temperatura, densidad         |
| Gateway + conectividad   | 8.000       | 4G/satelital para zona remota                    |
| Servidor edge computing  | 5.000       | Procesamiento local                              |
| Desarrollo e integración | 40.000      | 3 meses, equipo interno + consultoría           |
| Licencias software       | 6.000/año   | n8n Cloud, hosting                               |
| **TOTAL CAPEX**          | **78.000**  |                                                   |
| **OPEX anual**           | **12.000**  | Conectividad, mantenimiento, software            |

### 4.2 Ahorros y beneficios

**Ahorros directos (año 1):**

- Reducción de análisis de laboratorio: 60.000 USD (alrededor de 75 % menos análisis)  
- Mejora en eficiencia de bombeo: 80.000 USD (15 % de mejora operativa)  
- Reducción de reprocesamiento: 40.000 USD (menos salmuera fuera de especificación)  

**Total ahorros estimados:** 180.000 USD/año.

**Beneficios indirectos:**

- Mejora en calidad de cloruro de litio → potencial incremento de 2-5 % en precio de venta  
- Datos para optimización continua → mejora acumulativa año tras año  
- Cumplimiento RIGI más robusto → menor riesgo de perder beneficios fiscales  

### 4.3 Cálculo de ROI

```text
ROI = (Beneficios - Inversión) / Inversión × 100

Año 1:
(180.000 - 78.000 - 12.000) / 78.000 ≈ 115 % de ROI

Año 2:
180.000 / 12.000 ≈ 1.400 % de ROI (solo OPEX)

Período de repago (payback): aproximadamente 5,2 meses.
```

---

## 5. Escalabilidad

### 5.1 De Fase 1 a Fase 2

El sistema está diseñado para escalar de 5.400 tpa a 21.000 tpa:

- Arquitectura modular: agregar pozas no requiere rediseño  
- Costo marginal bajo: cada poza adicional ~5.000 USD (sensores)  
- Datos acumulados: el modelo mejora con más información histórica  

### 5.2 Expansión funcional

Capacidades futuras sin cambio de arquitectura:

1. Mantenimiento predictivo de bombas y equipos  
2. Optimización de rutas de bombeo entre pozas  
3. Proyección de producción (forecasting) semanal/mensual  
4. Integración con ERP para planificación  
5. Dashboard ejecutivo con indicadores clave (KPIs) en tiempo real  

---

## 6. Riesgos y mitigación

| Riesgo                | Probabilidad | Impacto | Mitigación                                       |
|-----------------------|--------------|---------|--------------------------------------------------|
| Falla de sensores     | Media        | Medio   | Redundancia, alertas específicas de falla       |
| Conectividad remota   | Alta         | Bajo    | Cache local, sincronización diferida             |
| Deriva del modelo     | Media        | Medio   | Reentrenamiento trimestral con datos recientes  |
| Resistencia de usuarios | Baja       | Alto    | Capacitación, interfaces simples e intuitivas   |

---

## 7. Comparación con alternativas

### Opción A: Continuar con el esquema actual (análisis manual)

- Costos altos recurrentes (~80.000 USD/año).  
- Tiempo de decisión lento (24-48 horas).  
- Escalabilidad limitada.  
- Trazabilidad parcial y con riesgo de errores.

### Opción B: Tercerizar el monitoreo

- Costos medios–altos (~60.000 USD/año).  
- Dependencia de proveedores externos.  
- Datos fuera del control directo de Galan.  
- Latencia adicional en la toma de decisiones.

### Opción C: Sistema propuesto (ML + automatización)

- Inversión controlada (78.000 USD de CAPEX).  
- OPEX bajo (12.000 USD/año).  
- Información en tiempo cercano al real (< 5 minutos).  
- Datos y conocimiento quedan dentro de la organización.  
- Escalable a Fase 2 sin grandes incrementos de inversión.  
- Trazabilidad completa para auditorías internas y externas.

---

## 8. Alineación estratégica

### 8.1 Con los objetivos de Galan

- Producto premium: control de calidad consistente para cloruro de litio de alta pureza.  
- Cumplimiento del cronograma: sistema operativo antes de la primera producción prevista para 2026.  
- RIGI y marco regulatorio: soporte a trazabilidad robusta y auditoría permanente.  
- Competitividad: mejora en eficiencia y calidad en un mercado global exigente.

### 8.2 Con tendencias de la industria

- Minería 4.0: adopción de IoT y modelos de IA en operación.  
- ESG: uso más eficiente de recursos y reducción de reprocesos.  
- Digitalización: alineación con expectativas de inversores y socios tecnológicos.

---

## 9. Plan de implementación

### Fase 1: Piloto (Meses 1-2)

- Instrumentar una poza piloto.  
- Entrenar el modelo con datos históricos combinados con datos sintéticos.  
- Validar predicciones frente a resultados de laboratorio.

### Fase 2: Despliegue (Meses 3-4)

- Instrumentar 5 pozas en Fase 1.  
- Automatización completa con n8n.  
- Capacitación de operadores y supervisores.

### Fase 3: Optimización (Meses 5-6)

- Ajuste fino del modelo con datos reales.  
- Incorporación progresiva de nuevas funcionalidades.  
- Preparación para la transición a Fase 2 (21.000 tpa).

---

## 10. Conclusión

El **Sistema Predictivo de Calidad de Salmuera** constituye una inversión estratégica que:

1. Genera valor económico tangible desde el primer año (ROI estimado de 115 %).  
2. Reduce riesgos operativos y de calidad, y refuerza el cumplimiento regulatorio.  
3. Acompaña el crecimiento del proyecto, desde Fase 1 hasta Fase 2.  
4. Construye capacidades internas basadas en datos y conocimiento propio.

**Recomendación:** avanzar con la implementación antes del inicio de la primera producción (2026) para capturar beneficios desde el arranque de operaciones.

---

## Contacto

**Autor del proyecto**  
Fernando Molas García  
Candidato – Analista Sr. de Inteligencia Artificial  

- Email: f.mg@outlook.com  
- LinkedIn: [fernando-molas-garcia](https://www.linkedin.com/in/fernando-molas-garcia/)  
- GitHub: [fmg75](https://github.com/fmg75)

**Propósito de este documento:**  
Demostración de capacidad de análisis de negocio y diseño de soluciones de punta a punta para Galan Lithium.
