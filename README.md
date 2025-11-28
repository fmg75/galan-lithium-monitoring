# Sistema Inteligente de Monitoreo de Salmuera - Galan Lithium

> Predicción en tiempo real de concentración de litio en pozas de evaporación mediante Machine Learning y automatización con n8n.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![n8n](https://img.shields.io/badge/n8n-Workflow-orange.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![ML](https://img.shields.io/badge/ML-Scikit--Learn-yellow.svg)
![Status](https://img.shields.io/badge/Status-En%20Desarrollo-yellow.svg)

---

## Contexto

Galan Lithium opera el proyecto Hombre Muerto West en el Salar del Hombre Muerto, Catamarca, con primera producción programada para el primer semestre de 2026. Su estrategia se centra en producir cloruro de litio de alta pureza, un producto premium demandado por la industria de baterías.

Este proyecto muestra cómo la combinación de Inteligencia Artificial y automatización puede optimizar el proceso crítico de monitoreo de calidad en pozas de evaporación.

---

## El Problema

En las operaciones actuales de extracción de litio por evaporación:

- Los análisis de laboratorio tradicionales demoran entre 24 y 48 horas.
- Las decisiones de bombeo entre pozas son reactivas, no predictivas.
- Existe riesgo de procesar salmuera fuera de especificación para cloruro de litio premium.
- Falta trazabilidad en tiempo real para cumplimiento normativo (por ejemplo, RIGI).

Impacto: pérdidas operativas, retrasos en producción y riesgo en la calidad del producto final.

---

## La Solución

Sistema híbrido que reduce el tiempo de decisión desde 48 horas a menos de 5 minutos:

```
[Sensores IoT] → [Automatización n8n] → [Modelo de Machine Learning] → [Decisiones automatizadas]
```

### Características principales

1. Predicción de concentración de litio basada en variables físico-químicas.
2. Automatización con n8n de todo el flujo de datos y reglas de negocio.
3. Alertas en tiempo casi real cuando se alcanzan umbrales críticos.
4. Trazabilidad completa de mediciones y decisiones.

---

## Arquitectura

```text
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
│  • Si fuera de rango → Notificación a supervisores         │
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

Proyecto en desarrollo activo, como demostración de capacidades técnicas.

### Completado

- Generador de datos sintéticos realistas basado en literatura técnica de salmueras.
- Dataset de 1000 muestras con variables físico-químicas relevantes.
- Modelo predictivo base con scikit-learn (R² = 0,89).
- Documentación técnica del proceso.
- Análisis exploratorio de datos.

### En desarrollo

- API REST con FastAPI para servir el modelo.
- Workflows de automatización en n8n.
- Sistema de alertas multi-canal.
- Dashboard en tiempo real.
- Containerización con Docker.

### Roadmap futuro

- Integración con PostgreSQL para persistencia.
- Sistema de logs y auditoría robusto.
- Modelos avanzados (XGBoost, ensembles).
- Tests automatizados con pytest.
- CI/CD con GitHub Actions.
- Despliegue en la nube (AWS/GCP).

---

## Quick Start

### Prerrequisitos

- Python 3.9 o superior  
- pip  
- (Opcional) Docker

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/galan-lithium-monitoring.git
cd galan-lithium-monitoring

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scriptsctivate   # Windows

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

```text
galan-lithium-monitoring/
├── README.md                          # Descripción general del proyecto
├── requirements.txt                   # Dependencias Python
├── docker-compose.yml                 # Configuración Docker
│
├── data/                              # Datos y generación
│   ├── synthetic_data_generator.py    # Generador de datos sintéticos
│   ├── sample_data.csv                # Dataset generado
│   └── data_documentation.md          # Documentación de variables
│
├── ml_model/                          # Modelos de Machine Learning
│   ├── train_model.py                 # Entrenamiento
│   ├── evaluate_model.py              # Evaluación
│   ├── model.pkl                      # Modelo entrenado
│   ├── api_model.py                   # API FastAPI
│   └── requirements.txt               # Dependencias específicas de ML
│
├── n8n_workflows/                     # Automatización n8n
│   ├── workflow_v1_basic.json         # Workflow básico
│   ├── workflow_v2_advanced.json      # Workflow planificado
│   └── setup_instructions.md          # Instrucciones de configuración
│
├── docs/                              # Documentación
│   ├── architecture_diagram.png       # Diagrama técnico
│   ├── business_case.md               # Caso de negocio
│   └── technical_notes.md             # Notas técnicas
│
└── notebooks/                         # Análisis exploratorio
    └── exploratory_analysis.ipynb     # EDA
```

Leyenda:  
- Completado  
- En desarrollo  
- Planificado  

---

## Valor para Galan Lithium

### Impacto operativo

| Métrica              | Antes        | Después         | Mejora aproximada            |
|----------------------|-------------|-----------------|------------------------------|
| Tiempo de decisión   | 24-48 horas | < 5 minutos     | Reducción cercana al 99 %    |
| Precisión de calidad | Análisis batch | Predicción continua | Evaluación casi en tiempo real |
| Trazabilidad         | Manual      | Automática      | Registro completo            |
| Costo por análisis   | Alto (laboratorio) | Bajo (sensor + ML) | Reducción estimada del 70-80 % |

### Alineación estratégica

- Enfoque en producto premium: control preciso para cloruro de litio de alta pureza.
- Acompañamiento del cronograma: la primera producción en 2026 requiere sistemas de control desde etapas tempranas.
- Soporte a cumplimiento normativo y fiscal (por ejemplo, RIGI) mediante trazabilidad automática.
- Solución escalable desde Fase 1 hasta 21.000 tpa en Fase 2.

---

## Tecnologías Utilizadas

### Core stack

- Python 3.9+
- scikit-learn
- pandas y numpy
- FastAPI
- n8n
- Docker

### Librerías de Machine Learning

- scikit-learn: Random Forest, preprocesamiento.
- joblib: serialización de modelos.
- matplotlib y seaborn: visualización de datos.

---

## Documentación adicional

- Caso de negocio: `docs/business_case.md`  
- Documentación de datos: `data/data_documentation.md`  
- Configuración de n8n: `n8n_workflows/setup_instructions.md`

---

## Autor

**Fernando Molas García**  
Candidato a Analista Sr. de Inteligencia Artificial - Galan Lithium

- Email: f.mg@outlook.com  
- LinkedIn: [fernando-molas-garcia](https://www.linkedin.com/in/fernando-molas-garcia/)  
- GitHub: [fmg75](https://github.com/fmg75)

---

## Notas del Proyecto

Este es un proyecto de demostración desarrollado como parte de una postulación a Galan Lithium. Los datos son sintéticos, pero se basan en literatura técnica real de salmueras del altiplano argentino.

Objetivos principales:

1. Entender un problema de negocio complejo.
2. Diseñar una solución de punta a punta (datos → modelo → automatización).
3. Incorporar tecnologías nuevas en poco tiempo (por ejemplo, n8n).
4. Comunicar de forma clara tanto el valor técnico como el valor para el negocio.

---

## Licencia

Este proyecto se distribuye bajo la licencia MIT.
