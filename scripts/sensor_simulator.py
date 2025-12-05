"""
Simulador de Sensores IoT para Pozas de Evaporación
Envía datos sintéticos al webhook de n8n cada X segundos
"""

import requests
import time
import random
from datetime import datetime
import json
import sys

# Configuración
INTERVAL_SECONDS = 10  # Enviar datos cada 10 segundos
NUM_POZAS = 3  # Simular 3 pozas

# URLs según el modo
WEBHOOK_URLS = {
    'production': "http://localhost:5678/webhook/sensor-reading",
    'test': "http://localhost:5678/webhook-test/sensor-reading"
}

# Rangos realistas basados en el modelo
SENSOR_RANGES = {
    'days_evaporation': (30, 180),
    'temperature_c': (5, 30),
    'humidity_percent': (5, 40),
    'ph': (7.0, 8.5),
    'conductivity_ms_cm': (50, 150),
    'density_g_cm3': (1.10, 1.25),
    'mg_li_ratio': (3, 15),
    'ca_li_ratio': (0.5, 3)
}


def get_webhook_url(use_test_mode=True):
    """Retorna la URL del webhook según el modo"""
    return WEBHOOK_URLS['test'] if use_test_mode else WEBHOOK_URLS['production']


def generate_sensor_reading(poza_id: str, days: float) -> dict:
    """Genera una lectura sintética de sensores"""
    
    # Generar valores con algo de correlación natural
    # (a más días, más concentración esperada)
    progress = (days - 30) / (180 - 30)  # 0 a 1
    
    # Temperatura: más calor acelera evaporación
    temp = random.uniform(15, 30) if progress > 0.5 else random.uniform(5, 20)
    
    # Humedad: inversamente proporcional a evaporación
    humidity = random.uniform(5, 20) if progress > 0.5 else random.uniform(15, 40)
    
    # Conductividad y densidad aumentan con concentración
    conductivity = random.uniform(80, 150) if progress > 0.5 else random.uniform(50, 100)
    density = random.uniform(1.15, 1.25) if progress > 0.5 else random.uniform(1.10, 1.18)
    
    # pH relativamente estable
    ph = random.uniform(7.0, 8.5)
    
    # Ratios de impurezas (mejor si son bajos)
    mg_li = random.uniform(3, 8) if progress > 0.5 else random.uniform(5, 15)
    ca_li = random.uniform(0.5, 2) if progress > 0.5 else random.uniform(1, 3)
    
    return {
        "poza_id": poza_id,
        "timestamp": datetime.now().isoformat(),
        "days_evaporation": round(days, 1),
        "temperature_c": round(temp, 1),
        "humidity_percent": round(humidity, 1),
        "ph": round(ph, 2),
        "conductivity_ms_cm": round(conductivity, 1),
        "density_g_cm3": round(density, 3),
        "mg_li_ratio": round(mg_li, 2),
        "ca_li_ratio": round(ca_li, 2)
    }


def send_sensor_data(data: dict, webhook_url: str) -> dict:
    """Envía datos al webhook de n8n y retorna resultado completo"""
    try:
        response = requests.post(
            webhook_url,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'success': True,
                'status_code': response.status_code,
                'data': result
            }
        else:
            return {
                'success': False,
                'status_code': response.status_code,
                'error': response.text
            }
            
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'error': 'connection_refused',
            'message': f"No se pudo conectar a n8n en {webhook_url}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': 'unknown',
            'message': str(e)
        }


def print_detailed_result(sensor_data: dict, result: dict):
    """Imprime resultado detallado y formateado"""
    poza = sensor_data['poza_id']
    days = sensor_data['days_evaporation']
    
    if result['success']:
        pred = result['data']
        
        # Header con status
        status_icon = "✅"
        print(f"\n{status_icon} {poza} | Días: {days} | HTTP {result['status_code']}")
        
        # Datos de entrada (resumen)
        print(f"   📥 Entrada: T={sensor_data['temperature_c']}°C, "
              f"H={sensor_data['humidity_percent']}%, "
              f"Cond={sensor_data['conductivity_ms_cm']} mS/cm")
        
        # Predicción
        conc = pred['predicted_concentration_mg_l']
        quality = pred['quality_status']
        confidence = pred['confidence']
        
        # Color según concentración
        if conc > 4500:
            conc_icon = "🔴"
        elif conc > 3500:
            conc_icon = "🟡"
        else:
            conc_icon = "🟢"
        
        print(f"   {conc_icon} Predicción: {conc:.1f} mg/L | Estado: {quality} | Confianza: {confidence}")
        
        # Recomendación
        print(f"   💡 {pred['recommendation']}")
        
        # Advertencias (si existen)
        if pred.get('warnings') and len(pred['warnings']) > 0:
            print(f"   ⚠️  Advertencias:")
            for warning in pred['warnings']:
                print(f"      - {warning}")
        
        # Alerta especial si es alta concentración
        if conc > 4500:
            print(f"   🚨 ¡ALERTA! Concentración óptima para bombeo a siguiente etapa")
        
    else:
        # Error
        print(f"\n❌ {poza} | Días: {days} | ERROR")
        if 'status_code' in result:
            print(f"   HTTP {result['status_code']}: {result.get('error', 'Unknown error')}")
        else:
            print(f"   {result.get('message', 'Connection error')}")


def continuous_monitoring(use_test_mode=True):
    """Monitoreo continuo de múltiples pozas en paralelo"""
    webhook_url = get_webhook_url(use_test_mode)
    mode_label = "TEST" if use_test_mode else "PRODUCCIÓN"
    
    print("=" * 80)
    print("🌊 SIMULADOR DE SENSORES - GALAN LITHIUM HMW")
    print("=" * 80)
    print(f"📡 Webhook: {webhook_url}")
    print(f"🔧 Modo: {mode_label}")
    print(f"⏱️  Intervalo: {INTERVAL_SECONDS} segundos")
    print(f"🏊 Pozas: {NUM_POZAS}")
    print("=" * 80)
    print("\n🚀 Iniciando monitoreo continuo...\n")
    
    # Estado de cada poza (días de evaporación actuales)
    pozas_state = {
        f"POZA_{i+1}": random.uniform(30, 150)
        for i in range(NUM_POZAS)
    }
    
    iteration = 0
    total_alerts = 0
    
    try:
        while True:
            iteration += 1
            print(f"\n{'='*80}")
            print(f"📊 Iteración {iteration} - {datetime.now().strftime('%H:%M:%S')}")
            print(f"{'='*80}")
            
            iteration_alerts = 0
            
            for poza_id, current_days in pozas_state.items():
                # Generar y enviar lectura
                reading = generate_sensor_reading(poza_id, current_days)
                result = send_sensor_data(reading, webhook_url)
                
                # Mostrar resultado detallado
                print_detailed_result(reading, result)
                
                # Contar alertas
                if result['success'] and result['data'].get('predicted_concentration_mg_l', 0) > 4500:
                    iteration_alerts += 1
                    total_alerts += 1
                
                # Avanzar días (simulación de tiempo)
                pozas_state[poza_id] = min(
                    current_days + random.uniform(0.5, 2),
                    180
                )
                
                # Si llegó al límite, reiniciar poza
                if pozas_state[poza_id] >= 179:
                    print(f"   🔄 {poza_id} completó ciclo completo (180 días), reiniciando...")
                    pozas_state[poza_id] = random.uniform(30, 60)
            
            # Resumen de iteración
            print(f"\n📈 Resumen: {iteration_alerts} alerta(s) generada(s) en esta iteración")
            print(f"🎯 Total acumulado: {total_alerts} alerta(s)")
            print(f"\n⏳ Esperando {INTERVAL_SECONDS} segundos hasta próxima iteración...")
            time.sleep(INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Simulación detenida por el usuario")
        print("=" * 80)
        print(f"📊 Estadísticas finales:")
        print(f"   • Iteraciones completadas: {iteration}")
        print(f"   • Total de alertas generadas: {total_alerts}")
        print(f"   • Tiempo total: ~{iteration * INTERVAL_SECONDS} segundos")
        print("=" * 80)


def test_single_reading(use_test_mode=True):
    """Envía una sola lectura de prueba"""
    webhook_url = get_webhook_url(use_test_mode)
    
    print("=" * 80)
    print("🧪 TEST - Enviando lectura única")
    print("=" * 80)
    print(f"📡 Webhook: {webhook_url}\n")
    
    test_data = generate_sensor_reading("POZA_TEST", 100)
    
    print("📤 Datos a enviar:")
    print(json.dumps(test_data, indent=2))
    print()
    
    result = send_sensor_data(test_data, webhook_url)
    print_detailed_result(test_data, result)
    
    if result['success']:
        print("\n✅ Test exitoso!")
    else:
        print("\n❌ Test falló")
    
    print("=" * 80)


def test_high_concentration(use_test_mode=True):
    """Envía datos que deberían generar alerta de alta concentración"""
    webhook_url = get_webhook_url(use_test_mode)
    
    print("=" * 80)
    print("🚨 TEST - Datos para generar ALERTA")
    print("=" * 80)
    print(f"📡 Webhook: {webhook_url}\n")
    
    # Datos que generan alta concentración de Li
    test_data = {
        "poza_id": "POZA_ALERTA_TEST",
        "timestamp": datetime.now().isoformat(),
        "days_evaporation": 150,  # Muchos días
        "temperature_c": 28,      # Alta temperatura
        "humidity_percent": 8,    # Baja humedad
        "ph": 7.8,
        "conductivity_ms_cm": 140,  # Alta conductividad
        "density_g_cm3": 1.23,      # Alta densidad
        "mg_li_ratio": 4.5,         # Bajo ratio (bueno)
        "ca_li_ratio": 1.0
    }
    
    print("📤 Datos optimizados para generar alta concentración:")
    print(json.dumps(test_data, indent=2))
    print()
    
    result = send_sensor_data(test_data, webhook_url)
    print_detailed_result(test_data, result)
    
    if result['success']:
        conc = result['data']['predicted_concentration_mg_l']
        if conc > 4500:
            print("\n✅ ¡Perfecto! Se generó una ALERTA como esperado")
        else:
            print(f"\n⚠️  No se generó alerta (concentración: {conc:.1f} mg/L)")
    else:
        print("\n❌ Test falló")
    
    print("=" * 80)


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("  SIMULADOR DE SENSORES - GALAN LITHIUM HMW")
    print("=" * 80 + "\n")
    
    # Determinar si usar modo test o producción
    # Por defecto: test (webhook-test)
    use_test_mode = True
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        # Flag opcional: --prod para usar webhook de producción
        if '--prod' in sys.argv:
            use_test_mode = False
            print("🔧 Modo: PRODUCCIÓN (webhook sin -test)")
        else:
            print("🔧 Modo: TEST (webhook-test)")
        
        if mode == "test":
            test_single_reading(use_test_mode)
        elif mode == "alert":
            test_high_concentration(use_test_mode)
        elif mode == "continuous":
            continuous_monitoring(use_test_mode)
        else:
            print("❌ Modo desconocido. Usa: test, alert, o continuous")
    else:
        print("Modos disponibles:")
        print("  python sensor_simulator.py test        - Una lectura de prueba")
        print("  python sensor_simulator.py alert       - Generar alerta de prueba")
        print("  python sensor_simulator.py continuous  - Monitoreo continuo")
        print("\nOpciones:")
        print("  --prod                                 - Usar webhook de producción (/webhook/)")
        print("                                          (Por defecto usa /webhook-test/)")
        print()
        
        # Por defecto, modo continuo
        continuous_monitoring(use_test_mode)
