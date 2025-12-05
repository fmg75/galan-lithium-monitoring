# 🚀 Setup Local - Sistema Completo

## Requisitos

- Python 3.9+
- n8n instalado globalmente (`npm install -g n8n`)
- Modelo ML entrenado (`model.pkl` y `model_metadata.pkl`)

## Opciones Avanzadas

### Usar webhook de producción
Por defecto, el simulador usa `/webhook-test/`. Para usar `/webhook/`:
```bash
python scripts/sensor_simulator.py continuous --prod
```

### Ajustar intervalo de tiempo
Edita `sensor_simulator.py` línea 14:
```python
INTERVAL_SECONDS = 5  # Cambiar a 5 segundos
```

### Ajustar número de pozas
Edita `sensor_simulator.py` línea 15:
```python
NUM_POZAS = 5  # Simular 5 pozas
```

## Inicio Rápido (3 terminales)

### Terminal 1: n8n
```bash
n8n start
```
Abre: http://localhost:5678

### Terminal 2: API FastAPI
```bash
cd ml_model
python api_model.py
```
Verifica: http://localhost:8000/health

### Terminal 3: Simulador de Sensores
```bash
python scripts/sensor_simulator.py continuous
```

---

## Configuración Inicial

### 1. Instalar Dependencias

```bash
# Dependencias de la API
cd ml_model
pip install -r requirements.txt

# Dependencias del simulador
pip install requests
```

### 2. Verificar Modelo ML

```bash
cd ml_model
ls -la model*.pkl

# Si no existen, entrenar:
python train_model.py
```

### 3. Importar Workflow en n8n

1. Abre n8n: http://localhost:5678
2. Click **"+"** → Nuevo workflow
3. Menú **"..."** → **"Import from File"**
4. Selecciona `n8n_workflows/workflow_v1_basic.json`
5. **IMPORTANTE:** Click en **"Active"** (toggle verde)

---

## Testing del Sistema

### Test 1: API sola
```bash
curl http://localhost:8000/health

# Test de predicción
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "poza_id": "TEST",
    "days_evaporation": 100,
    "temperature_c": 25,
    "humidity_percent": 15,
    "ph": 7.8,
    "conductivity_ms_cm": 120,
    "density_g_cm3": 1.2,
    "mg_li_ratio": 5.0,
    "ca_li_ratio": 1.2
  }'
```

### Test 2: Workflow completo (una lectura)
```bash
python scripts/sensor_simulator.py test
```

**Esperado:**
```
✅ POZA_TEST | Días: 100.0 | HTTP 200
   📥 Entrada: T=25°C, H=15%, Cond=120 mS/cm
   🟡 Predicción: 3845.2 mg/L | Estado: Bueno | Confianza: ALTA
   💡 Concentración buena. Continuar evaporación 1-2 semanas más.
```

### Test 3: Generar alerta
```bash
python scripts/sensor_simulator.py alert
```

**Esperado:**
```
✅ POZA_ALERTA_TEST | Días: 150.0 | HTTP 200
   📥 Entrada: T=28°C, H=8%, Cond=140 mS/cm
   🔴 Predicción: 4687.5 mg/L | Estado: Óptimo | Confianza: ALTA
   💡 Concentración óptima alcanzada. Recomendar bombeo a siguiente etapa.
   🚨 ¡ALERTA! Concentración óptima para bombeo a siguiente etapa
```

### Test 4: Monitoreo continuo
```bash
python scripts/sensor_simulator.py continuous
```

**Esperado:**
```
================================================================================
📊 Iteración 1 - 19:45:23
================================================================================

✅ POZA_1 | Días: 78.9 | HTTP 200
   📥 Entrada: T=22.3°C, H=18.5%, Cond=95.2 mS/cm
   🟢 Predicción: 3245.8 mg/L | Estado: Bueno | Confianza: ALTA
   💡 Concentración en desarrollo. Continuar evaporación.

✅ POZA_2 | Días: 145.2 | HTTP 200
   📥 Entrada: T=27.1°C, H=9.8%, Cond=138.4 mS/cm
   🔴 Predicción: 4823.1 mg/L | Estado: Óptimo | Confianza: ALTA
   💡 Concentración óptima alcanzada. Recomendar bombeo a siguiente etapa.
   🚨 ¡ALERTA! Concentración óptima para bombeo a siguiente etapa

📈 Resumen: 1 alerta(s) generada(s) en esta iteración
🎯 Total acumulado: 1 alerta(s)

⏳ Esperando 10 segundos hasta próxima iteración...
```

---

## Verificar Resultados

### En n8n:
1. Ve a **Executions** (panel izquierdo)
2. Verás todas las ejecuciones del workflow con timestamps
3. Click en cualquiera para ver:
   - Datos de entrada (sensor readings)
   - Validación
   - Respuesta de la API
   - Decisión de alerta
   - Logs generados

### En la terminal del simulador:
- Output detallado con iconos de color
- 🟢 Verde: Concentración normal (< 3500 mg/L)
- 🟡 Amarillo: Concentración media (3500-4500 mg/L)
- 🔴 Rojo: Alta concentración (> 4500 mg/L) - ALERTA

### Estadísticas al detener (Ctrl+C):
```
📊 Estadísticas finales:
   • Iteraciones completadas: 15
   • Total de alertas generadas: 4
   • Tiempo total: ~150 segundos
```

---

## Troubleshooting

### "Connection refused" al webhook
```bash
# Verificar que n8n está corriendo
curl http://localhost:5678

# Verificar que el workflow está ACTIVO (toggle verde)
```

### "Model not found"
```bash
cd ml_model
python train_model.py
ls -la model*.pkl
```

### "Module not found"
```bash
cd ml_model
pip install -r requirements.txt
```

### Webhook URL incorrecta
En n8n, el webhook debería ser:
```
http://localhost:5678/webhook/sensor-reading
```

Si es diferente, editar en `sensor_simulator.py` línea 12:
```python
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/TU-PATH-AQUI"
```

---

## Detener Todo

```bash
# Terminal 1 (n8n): Ctrl+C
# Terminal 2 (API): Ctrl+C
# Terminal 3 (Simulador): Ctrl+C
```

---

## 🐳 Dockerización (Opcional)

Para deploy en producción o compartir con otros:

```bash
# Ver docker-compose.yml en la raíz del proyecto
docker-compose up -d
```

Instrucciones completas en `DOCKER_SETUP.md`

---

## Checklist de Verificación

- [ ] n8n corriendo en http://localhost:5678
- [ ] API respondiendo en http://localhost:8000/health
- [ ] Workflow importado y ACTIVO (toggle verde)
- [ ] Simulador puede enviar datos exitosamente
- [ ] Logs CSV generándose en `logs/predictions.csv`
- [ ] Alertas se generan para concentraciones >4500 mg/L

---

## Siguientes Pasos

1. ✅ Sistema funcionando → Capturar screenshots
2. 🔄 Workflow v2 → Email real, Slack, notificaciones
3. 💾 Base de datos → PostgreSQL en lugar de CSV
4. 📊 Dashboard → Visualización web en tiempo real
5. 🧪 Tests → pytest para cobertura completa
6. 🐳 Docker → Containerización para deploy

---

**Tiempo estimado de setup: 10-15 minutos** ⚡
