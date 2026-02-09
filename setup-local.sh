#!/bin/bash

# UnderSight Local Setup (sem Docker)
# Usage: ./setup-local.sh

set -e

echo "🚀 UnderSight Local Setup (sem Docker)"
echo "======================================="

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# Instalar Backend
setup_backend() {
    log_info "Instalando Backend..."
    
    cd backend
    
    # Criar venv
    python3 -m venv venv
    source venv/bin/activate
    
    # Instalar dependências
    pip install -q -r requirements.txt
    
    cd ..
    log_info "Backend instalado!"
}

# Instalar Frontend
setup_frontend() {
    log_info "Instalando Frontend..."
    
    cd frontend
    
    npm install
    
    cd ..
    log_info "Frontend instalado!"
}

# Iniciar Backend
start_backend() {
    log_info "Iniciando Backend..."
    cd backend
    source venv/bin/activate
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    cd ..
    log_info "Backend rodando em http://localhost:8000"
}

# Iniciar Frontend
start_frontend() {
    log_info "Iniciando Frontend..."
    cd frontend
    npm run dev -- --host 0.0.0.0 --port 3000 &
    cd ..
    log_info "Frontend rodando em http://localhost:3000"
}

# Parar todos
stop_all() {
    pkill -f "uvicorn" || true
    pkill -f "vite" || true
    log_info "Serviços parados!"
}

# Mostrar help
show_help() {
    echo ""
    echo "Uso: ./setup-local.sh {install|start|stop|restart}"
    echo ""
    echo "Comandos:"
    echo "  install   - Instalar todas as dependências"
    echo "  start     - Iniciar backend e frontend"
    echo "  stop      - Parar todos os serviços"
    echo "  restart   - Reiniciar"
    echo ""
}

# Main
case "${1:-help}" in
    install)
        setup_backend
        setup_frontend
        ;;
    start)
        start_backend &
        sleep 2
        start_frontend
        echo ""
        echo "✅ Backend: http://localhost:8000"
        echo "✅ Frontend: http://localhost:3000"
        echo "✅ API Docs: http://localhost:8000/docs"
        ;;
    stop)
        stop_all
        ;;
    restart)
        stop_all
        sleep 1
        start_backend &
        sleep 2
        start_frontend
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac
