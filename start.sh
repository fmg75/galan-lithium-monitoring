#!/bin/bash

# Script de inicio rápido para el Sistema de Monitoreo de Salmuera
# Galan Lithium - Hombre Muerto West

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_color() {
    color=$1
    message=$2
    echo -e "${color}${message}${NC}"
}

print_header() {
    echo ""
    echo "=========================================================================="
    print_color "$GREEN" "  🌊 GALAN LITHIUM - SISTEMA DE MONITOREO DE SALMUERA"
    echo "=========================================================================="
    echo ""
}

print_step() {
    print_color "$BLUE" "➜ $1"
}

print_success() {
    print_color "$GREEN" "✅ $1"
}

print_error() {
    print_color "$RED" "❌ $1"
}

print_warning() {
    print_color "$YELLOW" "⚠️  $1"
}

# Verificar dependencias
check_dependencies() {
    print_step "Verificando dependencias..."
    
    # Python
    if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
        print_error "Python no está instalado"
        exit 1
    fi
    print_success "Python instalado"
    
    # n8n
    if ! command -v n8n &> /dev/null; then
        print_warning "n8n no está instalado globalmente"
        print_warning "Instala con: npm install -g n8n"
        exit 1
    fi
    print_success "n8n instalado"
    
    # pip packages
    if ! python -c "import fastapi" 2>/dev/null; then
        print_warning "Dependencias de Python faltantes"
        print_step "Instalando dependencias..."
        cd ml_model && pip install -r requirements.txt && cd ..
    fi
    print_success "Dependencias Python OK"
    
    # Verificar modelo
    if [ ! -f "ml_model/model.pkl" ]; then
        print_error "Modelo ML no encontrado"
        print_step "Entrenando modelo..."
        cd ml_model && python train_model.py && cd ..
    fi
    print_success "Modelo ML listo"
}

# Iniciar n8n
start_n8n() {
    print_step "Iniciando n8n..."
    
    # Verificar si ya está corriendo
    if curl -s http://localhost:5678 > /dev/null 2>&1; then
        print_warning "n8n ya está corriendo en puerto 5678"
        return
    fi
    
    # Iniciar n8n en background
    nohup n8n start > logs/n8n.log 2>&1 &
    N8N_PID=$!
    echo $N8N_PID > logs/n8n.pid
    
    # Esperar a que inicie
    print_step "Esperando que n8n inicie (máx 30 segundos)..."
    for i in {1..30}; do
        if curl -s http://localhost:5678 > /dev/null 2>&1; then
            print_success "n8n iniciado (PID: $N8N_PID)"
            return
        fi
        sleep 1
    done
    
    print_error "n8n no pudo iniciar"
    exit 1
}

# Iniciar API FastAPI
start_api() {
    print_step "Iniciando API FastAPI..."
    
    # Verificar si ya está corriendo
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_warning "API ya está corriendo en puerto 8000"
        return
    fi
    
    # Iniciar API en background
    cd ml_model
    nohup python api_model.py > ../logs/api.log 2>&1 &
    API_PID=$!
    echo $API_PID > ../logs/api.pid
    cd ..
    
    # Esperar a que inicie
    print_step "Esperando que API inicie (máx 15 segundos)..."
    for i in {1..15}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            print_success "API iniciada (PID: $API_PID)"
            return
        fi
        sleep 1
    done
    
    print_error "API no pudo iniciar"
    exit 1
}

# Verificar workflow en n8n
check_workflow() {
    print_step "Verificando workflow en n8n..."
    
    # Dar tiempo para que n8n esté completamente listo
    sleep 2
    
    # Intentar hacer una petición al webhook
    if curl -s -X POST http://localhost:5678/webhook-test/sensor-reading \
        -H "Content-Type: application/json" \
        -d '{"poza_id":"TEST_INIT","days_evaporation":100,"temperature_c":25,"humidity_percent":15,"ph":7.8,"conductivity_ms_cm":120,"density_g_cm3":1.2}' \
        > /dev/null 2>&1; then
        print_success "Workflow configurado y activo"
    else
        print_warning "Workflow no está activo o no está importado"
        print_warning "Importa manualmente: n8n_workflows/workflow_v1_basic.json"
        echo ""
        print_color "$YELLOW" "Pasos:"
        echo "  1. Abre http://localhost:5678"
        echo "  2. Importa el workflow desde n8n_workflows/workflow_v1_basic.json"
        echo "  3. Activa el workflow (toggle verde)"
        echo ""
    fi
}

# Mostrar información de servicios
show_info() {
    echo ""
    echo "=========================================================================="
    print_color "$GREEN" "  ✅ SISTEMA INICIADO CORRECTAMENTE"
    echo "=========================================================================="
    echo ""
    print_color "$BLUE" "📊 Servicios disponibles:"
    echo ""
    echo "  🌐 n8n:           http://localhost:5678"
    echo "  🤖 API:           http://localhost:8000"
    echo "  📖 API Docs:      http://localhost:8000/docs"
    echo ""
    print_color "$BLUE" "📁 Logs:"
    echo ""
    echo "  • n8n:   tail -f logs/n8n.log"
    echo "  • API:   tail -f logs/api.log"
    echo ""
    print_color "$BLUE" "🧪 Tests rápidos:"
    echo ""
    echo "  • Test único:        python scripts/sensor_simulator.py test"
    echo "  • Generar alerta:    python scripts/sensor_simulator.py alert"
    echo "  • Monitoreo 24/7:    python scripts/sensor_simulator.py continuous"
    echo ""
    print_color "$BLUE" "🛑 Detener servicios:"
    echo ""
    echo "  • Todos:   ./stop.sh"
    echo "  • Manual:  kill \$(cat logs/n8n.pid) \$(cat logs/api.pid)"
    echo ""
    echo "=========================================================================="
    echo ""
}

# Función principal
main() {
    print_header
    
    # Crear directorio de logs si no existe
    mkdir -p logs
    
    # Verificar dependencias
    check_dependencies
    
    echo ""
    print_color "$GREEN" "🚀 Iniciando servicios..."
    echo ""
    
    # Iniciar servicios
    start_n8n
    start_api
    
    # Verificar workflow
    check_workflow
    
    # Mostrar información
    show_info
    
    # Preguntar si ejecutar simulador
    echo ""
    read -p "¿Ejecutar simulador en modo continuo? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_step "Iniciando simulador..."
        python scripts/sensor_simulator.py continuous --prod
    else
        print_color "$GREEN" "Sistema listo. Ejecuta manualmente el simulador cuando quieras."
    fi
}

# Manejar Ctrl+C
trap 'echo ""; print_warning "Ejecución interrumpida"; exit 130' INT

# Ejecutar
main
