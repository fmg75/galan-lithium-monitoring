# 💼 Caso de Negocio: Sistema Predictivo de Calidad de Salmuera

## Resumen Ejecutivo

**Problema:** El proceso tradicional de análisis de calidad de salmuera en pozas de evaporación demora 24-48 horas, generando decisiones reactivas que impactan en eficiencia operativa y calidad del producto final.

**Solución:** Sistema inteligente que combina sensores IoT + Machine Learning + Automatización (n8n) para predicción en tiempo real de concentración de litio, reduciendo el tiempo de decisión a menos de 5 minutos.

**Impacto esperado:** Mejora del 15-20% en eficiencia operativa, reducción del 30-40% en costos de análisis, y mejora en calidad de producto premium (cloruro de litio alta pureza).

---

## 1. Contexto de Galan Lithium

### Operación Actual
- **Proyecto:** Hombre Muerto West, Salar del Hombre Muerto, Catamarca
- **Fase 1:** 5,400 tpa (toneladas por año) de LCE (Litio Carbonato Equivalente)
- **Fase 2:** Escalamiento a 21,000 tpa
- **Primera producción:** Programada para primer semestre 2026
- **Estrategia:** Producción de cloruro de litio de alta pureza (producto premium)

### Producto Estratégico
El **cloruro de litio** es un concentrado demandado por convertidores que producen:
- Fosfato de hierro y litio (LFP) para baterías
- Óxido de litio-níquel-manganeso-cobalto (NMC)
- Otros productos químicos de litio de alto valor

**Requerimiento crítico:** Control de calidad excepcional, especialmente en contenido de litio y bajo nivel de contaminantes (Mg, Ca).

---

## 2. El Problema Actual

### 2.1 Proceso Tradicional de Análisis

```
Toma de muestra → Transporte a laboratorio → Análisis químico → Resultado → Decisión
     (30 min)            (2-4 horas)            (8-12 horas)      (24-48h total)
```

### 2.2 Limitaciones Operativas

| Aspecto | Situación Actual | Impacto |
|---------|-----------------|---------|
| **Frecuencia** | 1-2 análisis por día | Información desactualizada |
| **Cobertura** | Muestreo puntual | No representa toda la poza |
| **Tiempo** | 24-48 horas | Decisiones tardías |
| **Costo** | $50-150 USD/análisis | Alto OPEX |
| **Trazabilidad** | Manual | Errores, falta de auditoría |

### 2.3 Consecuencias Empresariales

**Costos directos:**
- Análisis de laboratorio: ~$80,000 USD/año (Fase 1)
- Pérdidas por decisiones tardías: ~$120,000 USD/año estimado
- Reprocesamiento de salmuera fuera de especificación

**Costos indirectos:**
- Tiempo de operadores en gestión manual
- Riesgo de calidad en producto final (impacta precio de venta)
- Falta de datos para optimización continua

**Riesgo regulatorio:**
- RIGI requiere trazabilidad robusta
- Auditorías ambientales necesitan registros completos

---

## 3. La Solución Propuesta

### 3.1 Arquitectura del Sistema

```
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

### 3.2 Funcionalidades Clave

**Predicción en Tiempo Real:**
- Concentración de litio con 95%+ de precisión
- Actualización cada 15-30 minutos
- Confianza estadística en cada predicción

**Alertas Inteligentes:**
- Li > 4500 mg/L → "Listo para bombear a siguiente poza"
- Mg/Li > 10 → "Riesgo de contaminación - revisar"
- Tendencias anómalas → "Atención requerida"

**Trazabilidad Total:**
- Registro de todas las mediciones
- Historial de decisiones automatizadas
- Auditoría para cumplimiento RIGI

---

## 4. Retorno de Inversión (ROI)

### 4.1 Inversión Estimada

| Concepto | Costo (USD) | Notas |
|----------|-------------|-------|
| Sensores IoT (5 pozas) | $25,000 | pH, conductividad, temp, densidad |
| Gateway + conectividad | $8,000 | 4G/Satelital para zona remota |
| Servidor edge computing | $5,000 | Procesamiento local |
| Desarrollo e integración | $40,000 | 3 meses, equipo interno + consultoría |
| Licencias software | $6,000/año | n8n Cloud, hosting |
| **TOTAL CAPEX** | **$78,000** | |
| **OPEX anual** | **$12,000** | Conectividad, mantenimiento, software |

### 4.2 Ahorros y Beneficios

**Ahorros directos (año 1):**
- Reducción análisis de laboratorio: $60,000 (75% menos análisis)
- Mejora en eficiencia de bombeo: $80,000 (15% mejora operativa)
- Reducción de reprocesamiento: $40,000 (menos salmuera fuera de spec)
- **Total ahorros:** $180,000/año

**Beneficios indirectos:**
- Mejora en calidad de cloruro de litio → potencial premium de 2-5% en precio
- Datos para optimización continua → mejora acumulativa año tras año
- Cumplimiento RIGI más robusto → menos riesgo de perder beneficios fiscales

### 4.3 Cálculo de ROI

```
ROI = (Beneficios - Inversión) / Inversión × 100

Año 1: ($180,000 - $78,000 - $12,000) / $78,000 = 115% ROI
Año 2: $180,000 / $12,000 = 1,400% ROI (solo OPEX)

Payback period: 5.2 meses
```

---

## 5. Escalabilidad

### 5.1 Fase 1 → Fase 2

El sistema está diseñado para escalar de 5,400 tpa a 21,000 tpa:

- **Arquitectura modular:** Agregar pozas no requiere rediseño
- **Costo marginal bajo:** Cada poza adicional = $5,000 (solo sensores)
- **Datos acumulados:** El modelo mejora con más datos

### 5.2 Expansión Funcional

Capacidades futuras sin cambio de arquitectura:

1. **Mantenimiento predictivo** de bombas y equipos
2. **Optimización de rutas de bombeo** entre pozas
3. **Forecasting de producción** semanal/mensual
4. **Integración con ERP** para planificación
5. **Dashboard ejecutivo** con KPIs en tiempo real

---

## 6. Riesgos y Mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Falla de sensores | Media | Medio | Redundancia, alertas de falla |
| Conectividad remota | Alta | Bajo | Cache local, sync posterior |
| Deriva del modelo | Media | Medio | Reentrenamiento trimestral |
| Rechazo de usuarios | Baja | Alto | Capacitación, UI intuitiva |

---

## 7. Comparación con Alternativas

### Opción A: Status Quo (Análisis Manual)
- ❌ Costos altos recurrentes ($80k/año)
- ❌ Tiempo de decisión lento (24-48h)
- ❌ Sin escalabilidad
- ❌ Trazabilidad limitada

### Opción B: Outsourcing de Monitoreo
- ⚠️ Costos medios-altos ($60k/año)
- ⚠️ Dependencia de terceros
- ❌ Datos fuera de control de Galan
- ⚠️ Latencia en decisiones

### Opción C: Sistema Propuesto (ML + Automatización)
- ✅ Inversión controlada ($78k CAPEX)
- ✅ OPEX bajo ($12k/año)
- ✅ Tiempo real (< 5 min)
- ✅ Datos y conocimiento in-house
- ✅ Escalable a Fase 2 sin grandes inversiones
- ✅ Trazabilidad total

---

## 8. Alineación Estratégica

### 8.1 Con Objetivos de Galan

- ✅ **Producto Premium:** Control de calidad para cloruro de litio alta pureza
- ✅ **Timeline 2026:** Sistema operativo antes de primera producción
- ✅ **RIGI Compliance:** Trazabilidad robusta para auditorías
- ✅ **Competitividad:** Eficiencia operativa en mercado global

### 8.2 Con Tendencias de la Industria

- ✅ **Minería 4.0:** Adopción de IoT + IA es tendencia global
- ✅ **ESG:** Optimización reduce consumo de recursos
- ✅ **Digitalización:** Cumple con expectativas de inversionistas

---

## 9. Plan de Implementación

### Fase 1: Piloto (Mes 1-2)
- Instrumentar 1 poza
- Entrenar modelo con datos históricos + sintéticos
- Validar predicciones vs. laboratorio

### Fase 2: Rollout (Mes 3-4)
- Instrumentar 5 pozas de Fase 1
- Automatización completa con n8n
- Capacitación de operadores

### Fase 3: Optimización (Mes 5-6)
- Ajuste fino del modelo con datos reales
- Expansión de funcionalidades
- Preparación para Fase 2

---

## 10. Conclusión

El **Sistema Predictivo de Calidad de Salmuera** es una inversión estratégica que:

1. **Genera valor inmediato:** ROI de 115% en año 1
2. **Reduce riesgos:** Mejora calidad y cumplimiento regulatorio
3. **Es escalable:** Crece con la operación (Fase 1 → Fase 2)
4. **Construye capacidad:** Conocimiento y datos in-house

**Recomendación:** Implementar antes de primera producción (2026) para maximizar beneficios desde el inicio de operaciones.

---

## Contacto

**Autor del Proyecto:**  
[Tu Nombre]  
Candidato - Analista Sr. de Inteligencia Artificial  
Email: tu.email@ejemplo.com  
LinkedIn: [tu-perfil]

**Propósito de este documento:**  
Demostración de capacidad de análisis de negocio y diseño de soluciones end-to-end para Galan Lithium.
