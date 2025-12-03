"""
Script de prueba para la API de predicción
Prueba los diferentes endpoints y escenarios
"""

import requests
import json
from datetime import datetime

# Configuración
API_URL = "http://localhost:8000"

def print_response(title, response):
    """Imprimir respuesta formateada"""
    print("\n" + "="*60)
    print(f"{title}")
    print("="*60)
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, default=str))
    except:
        print(response.text)


def test_root():
    """Test endpoint raíz"""
    response = requests.get(f"{API_URL}/")
    print_response("TEST 1: Root Endpoint", response)
    return response.status_code == 200


def test_health():
    """Test health check"""
    response = requests.get(f"{API_URL}/health")
    print_response("TEST 2: Health Check", response)
    return response.status_code == 200


def test_model_info():
    """Test información del modelo"""
    response = requests.get(f"{API_URL}/model/info")
    print_response("TEST 3: Model Info", response)
    return response.status_code == 200


def test_prediction_basic():
    """Test predicción básica"""
    payload = {
        "poza_id": "POZA_1",
        "days_evaporation": 87.5,
        "temperature_c": 24.5,
        "humidity_percent": 18.2,
        "ph": 7.8,
        "conductivity_ms_cm": 98.3,
        "density_g_cm3": 1.182,
        "mg_li_ratio": 5.2,
        "ca_li_ratio": 1.3
    }
    
    response = requests.post(f"{API_URL}/predict", json=payload)
    print_response("TEST 4: Predicción Básica (Todos los parámetros)", response)
    return response.status_code == 200


def test_prediction_without_ratios():
    """Test predicción sin ratios Mg/Li, Ca/Li"""
    payload = {
        "poza_id": "POZA_2",
        "days_evaporation": 120.0,
        "temperature_c": 28.5,
        "humidity_percent": 15.0,
        "ph": 7.9,
        "conductivity_ms_cm": 115.0,
        "density_g_cm3": 1.210
    }
    
    response = requests.post(f"{API_URL}/predict", json=payload)
    print_response("TEST 5: Predicción Sin Ratios (Solo sensores inline)", response)
    return response.status_code == 200


def test_prediction_out_of_range():
    """Test predicción con valores fuera de rango"""
    payload = {
        "poza_id": "POZA_3",
        "days_evaporation": 200.0,  # Fuera de rango (max 180)
        "temperature_c": 40.0,       # Fuera de rango (max 35)
        "humidity_percent": 5.0,     # Fuera de rango (min 10)
        "ph": 7.5,
        "conductivity_ms_cm": 100.0,
        "density_g_cm3": 1.20
    }
    
    response = requests.post(f"{API_URL}/predict", json=payload)
    print_response("TEST 6: Predicción Fuera de Rango (Con warnings)", response)
    return response.status_code == 200


def test_prediction_low_concentration():
    """Test predicción con baja concentración esperada"""
    payload = {
        "poza_id": "POZA_4",
        "days_evaporation": 35.0,    # Pocos días
        "temperature_c": 18.0,        # Temperatura baja
        "humidity_percent": 35.0,     # Humedad alta
        "ph": 7.2,
        "conductivity_ms_cm": 60.0,   # Conductividad baja
        "density_g_cm3": 1.12,        # Densidad baja
        "mg_li_ratio": 12.0,          # Alto Mg (malo)
        "ca_li_ratio": 2.5
    }
    
    response = requests.post(f"{API_URL}/predict", json=payload)
    print_response("TEST 7: Predicción Baja Concentración", response)
    return response.status_code == 200


def test_prediction_high_concentration():
    """Test predicción con alta concentración esperada"""
    payload = {
        "poza_id": "POZA_5",
        "days_evaporation": 165.0,    # Muchos días
        "temperature_c": 32.0,         # Temperatura alta
        "humidity_percent": 12.0,      # Humedad baja
        "ph": 8.2,
        "conductivity_ms_cm": 140.0,   # Conductividad alta
        "density_g_cm3": 1.24,         # Densidad alta
        "mg_li_ratio": 4.5,            # Bajo Mg (bueno)
        "ca_li_ratio": 0.8
    }
    
    response = requests.post(f"{API_URL}/predict", json=payload)
    print_response("TEST 8: Predicción Alta Concentración", response)
    return response.status_code == 200


def test_invalid_input():
    """Test con input inválido"""
    payload = {
        "poza_id": "POZA_X",
        "days_evaporation": -10.0,  # Negativo (inválido)
        "temperature_c": "invalid",  # String en lugar de número
    }
    
    response = requests.post(f"{API_URL}/predict", json=payload)
    print_response("TEST 9: Input Inválido (Debe fallar)", response)
    return response.status_code == 422  # Unprocessable Entity


def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "#"*60)
    print("# INICIANDO TESTS DE API")
    print("#"*60)
    
    tests = [
        ("Root Endpoint", test_root),
        ("Health Check", test_health),
        ("Model Info", test_model_info),
        ("Predicción Básica", test_prediction_basic),
        ("Predicción Sin Ratios", test_prediction_without_ratios),
        ("Predicción Fuera de Rango", test_prediction_out_of_range),
        ("Baja Concentración", test_prediction_low_concentration),
        ("Alta Concentración", test_prediction_high_concentration),
        ("Input Inválido", test_invalid_input)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, "PASS" if result else "FAIL"))
        except Exception as e:
            print(f"\nERROR en {name}: {str(e)}")
            results.append((name, "ERROR"))
    
    # Resumen
    print("\n" + "#"*60)
    print("# RESUMEN DE TESTS")
    print("#"*60)
    for name, status in results:
        symbol = "✓" if status == "PASS" else "✗"
        print(f"{symbol} {name}: {status}")
    
    passed = sum(1 for _, status in results if status == "PASS")
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests pasaron")
    
    return passed == total


if __name__ == "__main__":
    try:
        print("Verificando que la API está corriendo...")
        response = requests.get(f"{API_URL}/health", timeout=2)
        print("API está activa!")
        
        run_all_tests()
        
    except requests.exceptions.ConnectionError:
        print("\nERROR: No se puede conectar a la API")
        print(f"Asegúrate de que está corriendo en {API_URL}")
        print("\nPara iniciar la API:")
        print("  cd ml_model")
        print("  python api_model.py")
    except Exception as e:
        print(f"\nERROR inesperado: {str(e)}")