# Sistema Inteligente de Monitoreo de Salmuera - Galan Lithium

> **Predicción en tiempo real de concentración de litio en pozas de evaporación mediante ML + Automatización con n8n**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![n8n](https://img.shields.io/badge/n8n-Workflow-orange.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![ML](https://img.shields.io/badge/ML-Scikit--Learn-yellow.svg)
![Status](https://img.shields.io/badge/Status-En%20Desarrollo-yellow.svg)

---

## Contexto

**Galan Lithium** opera el proyecto Hombre Muerto West (HMW) en el **Salar del Hombre Muerto, Catamarca**, reconocido como un **recurso Top 10 global** con las salmueras de litio de más alta calidad y bajo perfil de impurezas en Argentina.

**Estado actual del proyecto:**
- Primera producción de cloruro de litio programada para **H1 2026**
- **9,500 toneladas LCE** actualmente en pozas de evaporación
- **18 meses de data operacional** acumulada
- Fase 1: 5.4 ktpa LCE → Fase 2: 21 ktpa LCE
- Beneficiario del régimen RIGI (incentivos fiscales)

**Producto estratégico:** Cloruro de litio de alta pureza (6% LiCl concentrate), optimizado para baterías LFP (Lithium Iron Phosphate), la química dominante en vehículos eléctricos.

Este proyecto demuestra cómo **Inteligencia Artificial + Automatización** pueden optimizar el proceso crítico de monitoreo de calidad en pozas de evaporación, aprovechando los 18 meses de data operacional existente.

---

## El Problema

En las operaciones actuales de extracción de litio por evaporación:

- Los análisis de laboratorio tradicionales demoran 24-48 horas
- Decisiones de bombeo entre pozas son reactivas, no predictivas
- Riesgo de procesar salmuera fuera de especificación para cloruro de litio premium
- Falta de trazabilidad en tiempo real para cumplimiento normativo (RIGI)

**Impacto:** Pérdidas operativas, retrasos en producción, y riesgo de calidad en producto final.

---

## La Solución

Sistema híbrido que **reduce el tiempo de decisión de 48 horas a menos de 5 minutos**:

```
[Sensores IoT] → [n8n Automatización] → [Modelo ML] → [Decisiones Automatizadas]
```

### Características principales

1. **Predicción ML**: Modelo que predice concentración de litio basado en parámetros físico-químicos
2. **Automatización Inteligente**: Workflows n8n que orquestan todo el flujo de datos
3. **Alertas en Tiempo Real**: Notificaciones automáticas cuando se alcanzan umbrales críticos
4. **Trazabilidad Completa**: Registro de todas las mediciones y decisiones
5. **Aprovechar data existente**: Diseñado para entrenar con los 18 meses de data operacional de Galan

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    SENSORES IoT (Simulados)                 │
│  Temperatura | Humedad | pH | Conductividad | Densidad     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   n8n WORKFLOW - Ingesta                    │
│              Webhook → Validación → Preprocesamiento        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   MODELO ML - FastAPI                       │
│         Input: Parámetros físico-químicos                   │
│         Output: Concentración Li (mg/L) + Confianza         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              n8n WORKFLOW - Lógica de Negocio              │
│  • Si Li > 4500 mg/L → Alerta "Bombear a siguiente poza"   │
│  • Si Mg/Li > 10 → Alerta "Riesgo de contaminación"        │
│  • Si fuera de rango → Notificación supervisores            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    ACCIONES AUTOMATIZADAS                   │
│     Email/Slack | Dashboard | Logs | Reportes PDF          │
└─────────────────────────────────────────────────────────────┘
```

---

## Estado del Proyecto

**En desarrollo activo** - Proyecto personal para demostración de capacidades técnicas

### Completado

- [x] Generador de datos sintéticos realistas basado en literatura técnica de salmueras
- [x] Dataset de 1000 muestras con variables físico-químicas relevantes
- [x] Modelo predictivo base con scikit-learn (R² = 0.89)
- [x] Documentación técnica del proceso
- [x] Análisis exploratorio de datos

### En desarrollo

- [ ] API REST con FastAPI para servir modelo
- [ ] Workflows n8n de automatización
- [ ] Sistema de alertas multi-canal
- [ ] Dashboard en tiempo real
- [ ] Containerización con Docker

### Roadmap futuro

- [ ] Reentrenamiento con 18 meses de data operacional real de Galan
- [ ] Integración con PostgreSQL para persistencia
- [ ] Sistema de logs y auditoría robusto
- [ ] Modelos avanzados (XGBoost, ensembles)
- [ ] Tests automatizados (pytest)
- [ ] CI/CD con GitHub Actions
- [ ] Despliegue en cloud (AWS/GCP)

---

## Quick Start

### Prerrequisitos

```bash
Python 3.9+
pip
(Opcional) Docker
```

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/fmg75/galan-lithium-monitoring.git
cd galan-lithium-monitoring

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Generar datos sintéticos

```bash
cd data
python synthetic_data_generator.py
```

### Entrenar modelo

```bash
cd ml_model
python train_model.py
```

---

## Estructura del Proyecto

```
galan-lithium-monitoring/
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias Python
├── docker-compose.yml                 # Configuración Docker
│
├── data/                              # Datos y generación
│   ├── synthetic_data_generator.py    # Completo - Generador de datos
│   ├── sample_data.csv                # Completo - Dataset generado
│   └── data_documentation.md          # Completo - Documentación de variables
│
├── ml_model/                          # Modelos de Machine Learning
│   ├── train_model.py                 # Completo - Entrenamiento
│   ├── evaluate_model.py              # En desarrollo - Evaluación
│   ├── model.pkl                      # Modelo entrenado
│   ├── model_details.md               # Completo - Detalles técnicos
│   ├── api_model.py                   # En desarrollo - API FastAPI
│   └── requirements.txt               # Dependencias ML
│
├── n8n_workflows/                     # Automatización n8n
│   ├── workflow_v1_basic.json         # En desarrollo - Workflow básico
│   ├── workflow_v2_advanced.json      # Planificado
│   └── setup_instructions.md          # En desarrollo - Instrucciones
│
├── docs/                              # Documentación
│   ├── business_case.md               # Completo - Caso de negocio
│   ├── integration_architecture.md    # Completo - Integración SCADA
│   ├── technical_assumptions.md       # Completo - Supuestos técnicos
│   └── architecture_diagram.png       # En desarrollo - Diagrama técnico
│
└── notebooks/                         # Análisis exploratorio
    └── exploratory_analysis.ipynb     # En desarrollo - EDA
```

---

## Valor para Galan Lithium

### Impacto Operativo Directo

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Tiempo de decisión | 24-48 horas | Menos de 5 minutos | 99.7% reducción |
| Precisión de calidad | Análisis batch | Predicción continua | Tiempo real |
| Trazabilidad | Manual | Automática | 100% registro |
| Costo por análisis | Alto (laboratorio) | Bajo (sensor + ML) | 70-80% reducción |

### Alineación Estratégica

- **Producto Premium**: Control preciso para cloruro de litio alta pureza (6% LiCl concentrate)
- **Timeline Crítico**: Primera producción H1 2026 requiere sistemas ahora
- **Cumplimiento RIGI**: Trazabilidad automática para incentivos fiscales
- **Escalabilidad**: De Fase 1 (5.4 ktpa) a Fase 2 (21 ktpa)
- **Aprovecha activos existentes**: 18 meses de data operacional lista para entrenar modelo

---

## Tecnologías Utilizadas

### Core Stack

- **Python 3.9+**: Lenguaje principal
- **scikit-learn**: Machine Learning
- **pandas / numpy**: Manipulación de datos
- **FastAPI**: API REST para modelo
- **n8n**: Automatización de workflows
- **Docker**: Containerización

### Librerías ML

- `scikit-learn`: Random Forest, preprocessing
- `joblib`: Serialización de modelos
- `matplotlib / seaborn`: Visualizaciones

---

## Documentación Adicional

- [Caso de Negocio](docs/business_case.md) - Análisis de ROI y valor empresarial
- [Arquitectura de Integración](docs/integration_architecture.md) - Integración con sistemas SCADA/PLC existentes
- [Supuestos Técnicos](docs/technical_assumptions.md) - Limitaciones y consideraciones del proyecto
- [Detalles del Modelo ML](ml_model/model_details.md) - Feature engineering y decisiones de diseño
- [Documentación de Datos](data/data_documentation.md) - Variables y rangos

---

## Autor

**Fernando Molas García**  
Candidato para Analista Sr. de Inteligencia Artificial - Galan Lithium

- Email: f.mg@outlook.com
- LinkedIn: [fernando-molas-garcia](https://www.linkedin.com/in/fernando-molas-garcia/)
- GitHub: [fmg75](https://github.com/fmg75)

---

## Notas del Proyecto

Este es un **proyecto de demostración** desarrollado como parte de mi aplicación a Galan Lithium. Los datos son sintéticos pero basados en literatura técnica real de salmueras del altiplano argentino y características específicas del recurso HMW.

**Objetivo:** Demostrar capacidad de:
1. Comprender problemas de negocio complejos
2. Diseñar soluciones end-to-end (datos → modelo → automatización)
3. Aprender tecnologías nuevas rápidamente (n8n en 1 semana)
4. Comunicar valor técnico y empresarial
5. Aprovechar activos existentes (18 meses de data operacional)

**Próximo paso:** Reentrenar modelo con data operacional real de las 9,500 toneladas LCE en pozas de evaporación de Galan.

---

## Licencia

Este proyecto es de código abierto bajo licencia MIT.

---

## Agradecimientos

Documentación técnica basada en:
- Literatura científica sobre salmueras de litio del altiplano sudamericano
- Información pública de operaciones mineras en Salar del Hombre Muerto
- Presentaciones corporativas de Galan Lithium
- Documentación oficial de n8n y scikit-learn