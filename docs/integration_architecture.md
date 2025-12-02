# Arquitectura de Integración con Sistemas Existentes

## Visión General

Este documento describe cómo el sistema predictivo de concentración de litio se integra con la infraestructura operativa existente en plantas de procesamiento de salmuera, específicamente considerando sistemas SCADA/PLC típicos en operaciones mineras.

---

## 1. CONTEXTO: Infraestructura Típica en Minería de Litio

### Sistemas Preexistentes Esperados en Galan Lithium

```
┌─────────────────────────────────────────────────────────┐
│              CAPA OPERACIONAL (Existente)               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [PLC/RTU] ←→ Sensores de campo (Instrumentación)     │
│      ↕                                                  │
│  [SCADA] ←→ HMI (Visualización para operadores)       │
│      ↕                                                  │
│  [Historian] (Almacenamiento de datos de proceso)      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Componentes estándar:**
- **PLC (Programmable Logic Controller)**: Schneider Electric, Siemens, Allen-Bradley
- **SCADA**: Siemens WinCC, Wonderware, Ignition
- **Historian**: OSIsoft PI, Aveva Historian
- **Conectividad**: Ethernet industrial, Modbus, OPC-UA

---

## 2. ESTRATEGIA DE INTEGRACIÓN NO-INVASIVA

### Principio Fundamental: "No romper lo que funciona"

**Enfoque recomendado:** Capa analítica **paralela y complementaria** al SCADA existente

```
┌─────────────────────────────────────────────────────────┐
│                    POZAS DE EVAPORACIÓN                 │
│         Sensores: Conductividad, Densidad, Temp         │
└───────────────┬─────────────────────────────────────────┘
                │
                ├─────────────────────┬───────────────────┐
                │                     │                   │
                ▼                     ▼                   │
┌───────────────────────┐   ┌─────────────────────────┐  │
│   SISTEMA EXISTENTE   │   │   SISTEMA NUEVO (ML)    │  │
│                       │   │                         │  │
│  PLC → SCADA → HMI    │   │  Edge Gateway → n8n     │  │
│         ↓             │   │         ↓               │  │
│     Historian         │   │   Modelo ML → Alertas   │  │
│                       │   │         ↓               │  │
│  (Control operativo)  │   │   PostgreSQL + API      │  │
└───────────────────────┘   └─────────────────────────┘  │
                                      ↓                   │
                             ┌──────────────────┐         │
                             │  Dashboard ML    │←────────┘
                             │  (Visualización  │
                             │   predictiva)    │
                             └──────────────────┘
```

### Ventajas de este enfoque:

1. **Cero riesgo operativo**: SCADA continúa operando independientemente
2. **Desarrollo ágil**: Sistema ML puede iterarse sin afectar producción
3. **Validación en paralelo**: Comparar predicciones ML vs datos SCADA
4. **Adopción gradual**: Operadores usan ambos sistemas hasta confiar en ML

---

## 3. OPCIONES DE INTEGRACIÓN TÉCNICA

### Opción A: Integración Mínima (MVP - Recomendada para Fase 1)

**Lectura pasiva de datos desde Historian:**

```python
# Pseudocódigo: n8n workflow lee datos cada 15 min
GET http://historian.galan.local/api/v1/current
{
  "poza_1": {
    "conductivity": 98.3,
    "density": 1.18,
    "temperature": 24.5
  }
}

→ n8n procesa
→ Llama a Modelo ML
→ Almacena predicción en DB propia
→ Dashboard independiente muestra resultados
```

**Características:**
- No modifica SCADA existente
- Lee datos vía API REST del Historian (OSIsoft PI tiene API, Wonderware también)
- Sistema ML completamente separado
- **Tiempo de implementación:** 2-4 semanas

**Limitaciones:**
- No hay feedback automático al SCADA
- Operadores deben mirar dos pantallas
- Alertas ML van por canales separados (email/Slack)

---

### Opción B: Integración Media (Fase 2 - Recomendada)

**Escritura de predicciones de vuelta al Historian:**

```
[Modelo ML predice] 
    ↓
[n8n escribe predicción al Historian vía OPC-UA]
    ↓
[SCADA muestra predicción en HMI existente]
```

**Tecnología:** OPC-UA (estándar industrial para interoperabilidad)

```python
# Python OPC-UA Client
from opcua import Client

client = Client("opc.tcp://historian.galan.local:4840")
client.connect()

# Escribir predicción ML como nuevo tag
node = client.get_node("ns=2;s=Poza1.LiConcentration.Predicted")
node.set_value(3450.5)  # mg/L predicho por ML

client.disconnect()
```

**Características:**
- Predicciones ML aparecen en HMI de operadores
- Operadores ven todo en una sola pantalla
- Historian guarda tanto datos reales como predicciones
- **Tiempo de implementación:** 6-8 semanas

**Ventajas:**
- Adopción más fácil por operadores
- Datos centralizados
- Permite comparación histórica ML vs laboratorio

---

### Opción C: Integración Profunda (Fase 3 - Futuro)

**Sistema ML toma decisiones automáticas:**

```
[Modelo ML predice Li > 4500 mg/L]
    ↓
[n8n envía comando a PLC vía Modbus]
    ↓
[PLC abre válvula de bombeo automáticamente]
    ↓
[SCADA registra acción y notifica operador]
```

**IMPORTANTE:** Solo después de 6-12 meses de validación exitosa

**Características:**
- Control automático de proceso
- Requiere certificación de seguridad
- Operador mantiene override manual
- **Tiempo de implementación:** 12+ meses (incluye validación y certificación)

---

## 4. ARQUITECTURA DETALLADA (Opción B - Recomendada)

### 4.1 Capa de Sensores

```
POZA_1:
├── Sensor Conductividad (Modbus RTU, Address 1)
├── Sensor Densidad (Modbus RTU, Address 2)
└── Sensor Temperatura (4-20mA → PLC AI Module)

Conexión física:
Sensores → Cable RS485 (Modbus) → Gateway/PLC
```

### 4.2 Capa de Adquisición Dual

**Ruta 1 - SCADA (Existente):**
```
Sensores → PLC → SCADA → Historian → HMI
         (Control)  (Monitor) (Almacén)  (Visualización)
```

**Ruta 2 - ML (Nueva):**
```
Sensores → Edge Gateway → MQTT Broker → n8n → ML API
          (Agregación)   (Buffer)      (Orquest.) (Predicción)
```

### 4.3 Punto de Integración: Historian como Hub Central

```
┌──────────────────────────────────────────────────────┐
│              OSIsoft PI Historian                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Tags Reales (desde PLC):                           │
│  • Poza1.Conductivity.Real                          │
│  • Poza1.Density.Real                               │
│                                                      │
│  Tags Predichos (desde ML vía OPC-UA):              │
│  • Poza1.LiConcentration.Predicted                  │
│  • Poza1.LiConcentration.Confidence                 │
│  • Poza1.NextAction.Recommendation                  │
│                                                      │
└──────────────────────────────────────────────────────┘
         ↓                           ↓
    [HMI SCADA]              [Dashboard ML]
```

---

## 5. PROTOCOLO DE COMUNICACIÓN

### Estándares Recomendados

| De | A | Protocolo | Puerto | Frecuencia |
|-----|---|-----------|--------|------------|
| Sensores | PLC | Modbus RTU | RS485 | Continuo |
| Sensores | Edge Gateway | Modbus TCP | 502 | 1-5 min |
| Edge Gateway | n8n | MQTT | 1883 | 5-15 min |
| n8n | ML API | HTTP REST | 8000 | On-demand |
| n8n | Historian | OPC-UA | 4840 | Cada predicción |
| SCADA | Historian | Propietario | - | Continuo |

### Ejemplo de mensaje MQTT

```json
{
  "timestamp": "2025-12-01T10:30:00Z",
  "source": "edge-gateway-01",
  "poza_id": "POZA_1",
  "measurements": {
    "conductivity_ms_cm": 98.3,
    "density_g_cm3": 1.182,
    "temperature_c": 24.5,
    "ph": 7.8
  },
  "metadata": {
    "sensor_status": "OK",
    "last_calibration": "2025-11-15"
  }
}
```

---

## 6. SEGURIDAD Y AISLAMIENTO

### 6.1 Segregación de Redes

```
┌────────────────────────────────────────────┐
│     RED OPERACIONAL (OT Network)           │
│     VLAN 10 - 192.168.10.0/24             │
│                                            │
│  PLC ←→ SCADA ←→ Historian                │
│                                            │
└────────────────┬───────────────────────────┘
                 │
            [Firewall]
           (DMZ - Zona desmilitarizada)
                 │
┌────────────────┴───────────────────────────┐
│     RED ANALÍTICA (IT Network)             │
│     VLAN 20 - 192.168.20.0/24             │
│                                            │
│  Edge Gateway → n8n → ML Server           │
│                                            │
└────────────────────────────────────────────┘
```

### 6.2 Reglas de Firewall

**OT → IT (Permitido):**
- Historian → n8n: TCP/443 (HTTPS) solo lectura
- Edge Gateway → n8n: TCP/1883 (MQTT)

**IT → OT (Restringido):**
- n8n → Historian: TCP/4840 (OPC-UA) solo escritura de tags ML
- Todo otro tráfico: **BLOQUEADO**

**Principio:** El sistema ML puede LEER datos operativos, pero solo puede ESCRIBIR tags específicos de predicciones, no comandos de control.

---

## 7. VALIDACIÓN Y MONITOREO

### 7.1 Dashboard Comparativo (Crítico para adopción)

**Panel principal debe mostrar:**

```
┌──────────────────────────────────────────────────────┐
│  POZA 1 - Monitoreo de Concentración Li              │
├──────────────────────────────────────────────────────┤
│                                                      │
│  [Gráfico de Tiempo Real]                           │
│   ┌────────────────────────────────────────────┐    │
│   │ — Predicción ML (línea azul)              │    │
│   │ ○ Análisis Laboratorio (puntos rojos)     │    │
│   │                                            │    │
│   │     ○ 3420 mg/L (lab, hace 6h)            │    │
│   │      \                                     │    │
│   │       —— 3450 mg/L (ML, ahora)            │    │
│   │                                            │    │
│   └────────────────────────────────────────────┘    │
│                                                      │
│  Error Actual: 30 mg/L (0.9%)  ✅ Dentro de rango   │
│  Confianza ML: 92%                                   │
│  Última calibración: 2h atrás                        │
│                                                      │
│  Recomendación: Continuar evaporación (48h más)     │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### 7.2 Métricas de Performance del Sistema Integrado

**KPIs a monitorear:**

```python
# En PostgreSQL + Dashboard
metrics = {
    # Precisión del modelo
    "mae_last_7_days": 42.5,      # mg/L
    "r2_last_30_days": 0.88,
    "predictions_vs_lab": 0.95,   # Correlación
    
    # Disponibilidad del sistema
    "uptime_ml_service": 99.2,    # %
    "uptime_edge_gateway": 98.7,  # %
    "sensor_failures": 2,         # últimos 30 días
    
    # Impacto operativo
    "decisions_accelerated": 147, # decisiones tomadas más rápido
    "false_alarms": 3,            # falsos positivos de alertas
    "time_saved_hours": 352       # vs proceso manual
}
```

---

## 8. ROADMAP DE IMPLEMENTACIÓN

### Fase 0: Preparación (Semana 1-2)
- Auditoría de infraestructura SCADA existente
- Identificar versión de Historian y APIs disponibles
- Definir tags a leer/escribir
- Configurar accesos de red y permisos

### Fase 1: MVP Desacoplado (Semana 3-6)
- Instalar sensores adicionales si necesario
- Desplegar Edge Gateway
- Configurar lectura de datos desde Historian
- Modelo ML en servidor dedicado
- Dashboard independiente
- Validación en paralelo: ML vs Laboratorio

### Fase 2: Integración Ligera (Semana 7-12)
- Configurar escritura OPC-UA al Historian
- Agregar tags ML en HMI de SCADA
- Capacitar operadores en nuevo panel
- Ajuste de umbrales de alertas basado en feedback

### Fase 3: Optimización (Mes 4-6)
- Reentrenamiento de modelo con datos reales
- Refinamiento de feature engineering
- Integración de alertas ML en sistema de alarmas SCADA
- Reportes automáticos para gerencia

### Fase 4: Automatización Parcial (Mes 7-12)
- Solo si validación exitosa >95% precisión
- Piloto de control semi-automático en 1 poza
- Operador aprueba recomendaciones ML antes de ejecutar
- Monitoreo exhaustivo de impacto

---

## 9. CONSIDERACIONES ESPECÍFICAS DE GALAN LITHIUM

### 9.1 Ambiente Operativo

**Desafíos del Salar del Hombre Muerto:**
- Altitud: ~4,000 msnm → Equipos deben soportar baja presión atmosférica
- Temperatura: -10°C a 25°C → Protección térmica para electrónica
- Radiación UV alta → Gabinetes con protección UV
- Polvo y viento → Clasificación IP65+ para sensores outdoor
- Conectividad limitada → Buffer local y sincronización diferida

**Solución:**
```
Edge Gateway en gabinete IP65, climatizado
  ↓
Buffer SQLite local (48h de datos)
  ↓
Sincronización vía 4G cuando disponible
  ↓
Modelo ML puede correr localmente (edge inference)
```

### 9.2 Escalabilidad Fase 1 → Fase 2

**Fase 1 (5,400 tpa):** 5 pozas monitoreadas
- 1 Edge Gateway
- 1 Servidor ML
- Costo: ~$150k

**Fase 2 (21,000 tpa):** 15-20 pozas monitoreadas
- 2-3 Edge Gateways
- 1 Servidor ML más potente (mismo modelo, más carga)
- Costo incremental: ~$250k

**Arquitectura no requiere rediseño, solo replicación.**

---

## 10. RIESGOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Interferencia con SCADA | Baja | Alto | Arquitectura desacoplada, firewall |
| Predicciones incorrectas | Media | Medio | Validación paralela, umbrales de confianza |
| Fallo de conectividad | Alta | Bajo | Buffer local, sync diferida |
| Resistencia de operadores | Media | Medio | Capacitación, dashboard comparativo |
| Sensor drift/calibración | Media | Medio | Alertas de desviación, calibración trimestral |

---

## 11. CONCLUSIÓN

La integración propuesta respeta la infraestructura existente, minimiza riesgos operativos, y permite validación exhaustiva antes de cualquier automatización. 

**Principio clave:** El sistema ML debe **complementar y mejorar** las operaciones, no reemplazarlas abruptamente.

**Próximos pasos:**
1. Auditoría de SCADA actual en Galan
2. Prueba de concepto (PoC) en 1 poza durante 3 meses
3. Evaluación de resultados y ajustes
4. Rollout gradual a todas las pozas

---

## Referencias Técnicas

- OPC Foundation. (2024). OPC UA Specification Part 1: Overview and Concepts
- OSIsoft. (2024). PI System API Documentation
- Siemens. (2024). WinCC SCADA Integration Guidelines
- IEEE. (2023). Industrial Network Security Best Practices
- ISA-95. Enterprise-Control System Integration Standards

---

**Autor:** Fernando Molas García  
**Fecha:** Diciembre 2025  
**Versión:** 1.0  
**Propósito:** Documento técnico de integración para Galan Lithium