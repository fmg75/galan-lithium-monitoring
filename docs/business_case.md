# Caso de Negocio: Sistema Predictivo de Calidad de Salmuera

## Resumen Ejecutivo

**Problema:** El proceso tradicional de análisis de calidad de salmuera en pozas de evaporación demora 24-48 horas, generando decisiones reactivas que impactan en eficiencia operativa y calidad del producto final.

**Solución:** Sistema inteligente que combina sensores IoT + Machine Learning + Automatización (n8n) para predicción en tiempo real de concentración de litio, reduciendo el tiempo de decisión a menos de 5 minutos.

**Impacto esperado:** Mejora del 15-20% en eficiencia operativa, reducción del 30-40% en costos de análisis, y mejora en calidad de producto premium (cloruro de litio alta pureza).

---

## 1. Contexto de Galan Lithium

### Operación Actual
- **Proyecto:** Hombre Muerto West (HMW), Salar del Hombre Muerto, Catamarca
- **Recurso:** Top 10 global con 9.5 Mt LCE, bajo perfil de impurezas (concentración mineral: 841 mg/L Li)
- **Estado:** 9,500 toneladas LCE acumuladas en pozas de evaporación
- **Data operacional:** 18 meses de mediciones y análisis ya disponibles
- **Fase 1:** 5,400 tpa de LCE (6% LiCl concentrate)
- **Fase 2:** Escalamiento a 21,000 tpa
- **Primera producción:** Programada para primer semestre 2026
- **Estrategia:** Producción de cloruro de litio de alta pureza optimizado para baterías LFP

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
├── Entrenado con 18 meses de data operacional existente
├── API FastAPI
└── Validación continua

CAPA 4: ACCIONES AUTOMATIZADAS
├── Alertas en tiempo real
├── Dashboard operativo
├── Reportes automáticos
└── Base de datos auditada
```

**Ventaja crítica:** Galan ya tiene 18 meses de datos operacionales reales de sus 9,500 toneladas LCE en pozas. Esto significa que el modelo puede entrenarse con datos REALES desde día 1, no solo sintéticos.

**Timeline acelerado:**
- Modelo con datos sintéticos: 7 días (completado)
- Reentrenamiento con data real: 2-3 semanas
- Validación en paralelo: 3 meses
- Producción completa: 6-7 meses (vs 12-18 meses típico)

El valor de tener 18 meses de data existente reduce el riesgo y acelera significativamente el deployment.

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

### 4.1 Fase 1 (5,400 tpa)

#### Inversión Inicial

| Concepto | Costo (USD) | Notas |
|----------|-------------|-------|
| Sensores IoT (5 pozas) | $25,000 | pH, conductividad, temp, densidad |
| Gateway + conectividad | $8,000 | 4G/Satelital para zona remota |
| Servidor edge computing | $5,000 | Procesamiento local |
| Desarrollo e integración | $40,000 | 3 meses, equipo interno + consultoría |
| **TOTAL CAPEX Fase 1** | **$78,000** | |
| **OPEX anual Fase 1** | **$12,000** | Conectividad, mantenimiento, software |

#### Ahorros y Beneficios Fase 1

**Ahorros directos (año 1):**
- Reducción análisis de laboratorio: $60,000 (75% menos análisis)
- Mejora en eficiencia de bombeo: $80,000 (15% mejora operativa)
- Reducción de reprocesamiento: $40,000 (menos salmuera fuera de spec)
- **Total ahorros Fase 1:** $180,000/año

**Beneficios indirectos:**
- Mejora en calidad de cloruro de litio → potencial premium de 2-5% en precio
- Datos para optimización continua → mejora acumulativa año tras año
- Cumplimiento RIGI más robusto → menos riesgo de perder beneficios fiscales

#### ROI Fase 1

```
ROI Año 1 = (Ahorros - Inversión - OPEX) / Inversión × 100

Año 1: ($180,000 - $78,000 - $12,000) / $78,000 = 115% ROI
Año 2: $180,000 / $12,000 = 1,400% ROI (solo OPEX)

Payback period: 5.2 meses
```

---

### 4.2 Fase 2 (Escalamiento a 21,000 tpa)

#### Inversión Incremental Fase 2

| Concepto | Costo (USD) | Notas |
|----------|-------------|-------|
| Sensores adicionales (10-15 pozas) | $125,000 | Réplica de Fase 1 |
| Gateways y networking adicional | $50,000 | 2-3 gateways más |
| Servidor más potente | $40,000 | Escalar capacidad |
| Integración y ajustes | $35,000 | Sin rediseño, solo expansión |
| **TOTAL CAPEX Fase 2** | **$250,000** | Inversión incremental |
| **OPEX anual incremental** | **$18,000** | Costos adicionales operativos |

#### Ahorros y Beneficios Fase 2

**Ahorros directos Fase 2 (año 1):**
- Reducción análisis laboratorio: $220,000 (4x operación pero con economías de escala)
- Mejora eficiencia bombeo: $280,000 (volumen 4x mayor = impacto mayor)
- Reducción reprocesamiento: $150,000 (mayor volumen, mayor ahorro)
- **Total ahorros Fase 2:** $650,000/año

**Por qué los ahorros no crecen linealmente (4x):**
- **Economías de escala:** Un laboratorio puede procesar muestras de 5 o 20 pozas con costo similar
- **Sistema ya desarrollado:** Sin costos de I+D, solo replicación
- **Eficiencias operativas:** Expertise de Fase 1 reduce tiempo de implementación
- **Modelo ML ya validado:** No requiere reentrenamiento extensivo

#### ROI Fase 2

```
ROI Año 1 Fase 2 = (Ahorros - Inversión - OPEX) / Inversión × 100

Año 1: ($650,000 - $250,000 - $18,000) / $250,000 = 153% ROI
Año 2+: $650,000 / $18,000 = 3,511% ROI (solo OPEX)

Payback period: 4.7 meses
```

---

### 4.3 ROI Consolidado (Fase 1 + Fase 2)

#### Inversión Total Acumulada

```
CAPEX Total: $78,000 (Fase 1) + $250,000 (Fase 2) = $328,000
OPEX Anual Total: $12,000 + $18,000 = $30,000/año
```

#### Ahorros Totales

```
Ahorros Anuales Totales: $180,000 + $650,000 = $830,000/año
```

#### ROI Consolidado

```
Año 1: ($830,000 - $30,000) / $328,000 = 244% ROI
Años siguientes: $830,000 / $30,000 = 2,667% ROI

Payback consolidado: 4.8 meses
```

### 4.4 Comparación de Escenarios

| Escenario | CAPEX | OPEX/año | Ahorros/año | ROI Año 1 | Payback |
|-----------|-------|----------|-------------|-----------|---------|
| **Status Quo (sin sistema)** | $0 | $480k | $0 | - | - |
| **Solo Fase 1** | $78k | $12k | $180k | 115% | 5.2 meses |
| **Fase 1 + Fase 2** | $328k | $30k | $830k | 244% | 4.8 meses |
| **Fase 2 directa (sin Fase 1)** | $400k+ | $40k | $600k | 140% | 8+ meses |

**Conclusión:** Implementar Fase 1 como piloto primero, luego escalar a Fase 2 genera el mejor ROI, minimiza riesgo, y aprovecha aprendizajes operacionales.

---

## 5. Ventajas de Escalamiento

### 5.1 Por qué Fase 2 es más rentable

1. **Sistema ya desarrollado:** $0 en I+D para Fase 2
2. **Arquitectura validada:** Sin riesgo técnico
3. **Modelo ML entrenado:** Solo requiere ajuste fino con nuevos datos
4. **Expertise operacional:** Equipo ya capacitado
5. **Economías de escala:**
   - Laboratorio: costo fijo compartido entre más pozas
   - Networking: infraestructura compartida
   - Soporte: mismo equipo técnico

### 5.2 Riesgos Reducidos

| Riesgo | Fase 1 | Fase 2 |
|--------|--------|--------|
| Técnico (modelo no funciona) | Medio | **Bajo** (ya validado) |
| Operacional (rechazo usuarios) | Medio | **Bajo** (ya adoptado) |
| Financiero (ROI no se cumple) | Bajo | **Muy bajo** (datos reales) |
| Regulatorio (RIGI) | Bajo | **Muy bajo** (proceso probado) |

---

## 6. Comparación con Alternativas

### Opción A: Status Quo (Análisis Manual)
- Costos altos recurrentes ($80k/año Fase 1, $320k/año Fase 2)
- Tiempo de decisión lento (24-48h)
- Sin escalabilidad
- Trazabilidad limitada

### Opción B: Outsourcing de Monitoreo
- Costos medios-altos ($60k/año Fase 1, $240k/año Fase 2)
- Dependencia de terceros
- Datos fuera de control de Galan
- Latencia en decisiones

### Opción C: Sistema Propuesto (ML + Automatización)
- Inversión controlada ($328k total)
- OPEX bajo ($30k/año consolidado)
- Tiempo real (menos de 5 min)
- Datos y conocimiento in-house
- Escalable sin grandes inversiones adicionales
- Trazabilidad total

---

## 7. Alineación Estratégica

### 7.1 Con Objetivos de Galan

- **Producto Premium:** Control de calidad para cloruro de litio alta pureza
- **Timeline 2026:** Sistema operativo antes de primera producción
- **RIGI Compliance:** Trazabilidad robusta para auditorías
- **Competitividad:** Eficiencia operativa en mercado global

### 7.2 Con Tendencias de la Industria

- **Minería 4.0:** Adopción de IoT + IA es tendencia global
- **ESG:** Optimización reduce consumo de recursos
- **Digitalización:** Cumple con expectativas de inversionistas

---

## 8. Plan de Implementación

### Fase 1: Piloto (Mes 1-3)
- Instrumentar 1 poza
- Entrenar modelo con datos históricos + sintéticos
- Validar predicciones vs. laboratorio

### Fase 2: Rollout Fase 1 (Mes 4-6)
- Instrumentar 5 pozas de Fase 1
- Automatización completa con n8n
- Capacitación de operadores

### Fase 3: Optimización (Mes 7-9)
- Ajuste fino del modelo con datos reales
- Expansión de funcionalidades
- Preparación para Fase 2

### Fase 4: Escalamiento Fase 2 (Mes 10-15)
- Instrumentar 15-20 pozas adicionales
- Replicación de arquitectura validada
- Economías de escala en operación

---

## 9. Escalabilidad

### 9.1 Arquitectura Modular

El sistema está diseñado para escalar sin rediseño:
- Cada poza adicional: $5,000-8,000 (solo sensores)
- Gateways compartidos: hasta 10 pozas por gateway
- Modelo ML: escala sin modificación
- n8n workflows: replicables

### 9.2 Expansión Funcional

Capacidades futuras sin cambio de arquitectura:
1. Mantenimiento predictivo de bombas y equipos
2. Optimización de rutas de bombeo entre pozas
3. Forecasting de producción semanal/mensual
4. Integración con ERP para planificación
5. Dashboard ejecutivo con KPIs en tiempo real

---

## 10. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Interferencia con SCADA | Baja | Alto | Arquitectura desacoplada, firewall |
| Predicciones incorrectas | Media | Medio | Validación paralela, umbrales de confianza |
| Fallo de conectividad | Alta | Bajo | Buffer local, sync diferida |
| Resistencia de operadores | Media | Medio | Capacitación, dashboard comparativo |
| Sensor drift/calibración | Media | Medio | Alertas de desviación, calibración trimestral |

---

## 11. Conclusión

El **Sistema Predictivo de Calidad de Salmuera** es una inversión estratégica que:

1. **Genera valor inmediato:** 115% ROI en Fase 1, 244% ROI consolidado
2. **Reduce riesgos:** Mejora calidad y cumplimiento regulatorio
3. **Es altamente escalable:** De 5 pozas (Fase 1) a 20 pozas (Fase 2) sin rediseño
4. **Construye capacidad:** Conocimiento y datos in-house
5. **Aprovecha activos existentes:** 18 meses de data operacional lista para usar

**Recomendación:** Implementar Fase 1 antes de primera producción (H1 2026) para maximizar beneficios desde el inicio de operaciones. Escalar a Fase 2 una vez validada la solución en Fase 1.

---

## Contacto

**Autor del Proyecto:**  
Fernando Molas García  
Candidato - Analista Sr. de Inteligencia Artificial  
Email: f.mg@outlook.com  
LinkedIn: [fernando-molas-garcia](https://www.linkedin.com/in/fernando-molas-garcia/)  
GitHub: [fmg75](https://github.com/fmg75)

**Propósito de este documento:**  
Demostración de capacidad de análisis de negocio y diseño de soluciones end-to-end para Galan Lithium.