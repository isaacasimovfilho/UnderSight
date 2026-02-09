#!/bin/bash

# UnderSight Development Setup Script
# Usage: ./setup-dev.sh

set -e

echo "🚀 UnderSight Development Setup"
echo "================================"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar dependências
check_dependencies() {
    log_info "Verificando dependências..."
    
    command -v docker >/dev/null 2>&1 || {
        log_error "Docker não encontrado! Instale o Docker primeiro."
        exit 1
    }
    
    command -v docker >/dev/null 2>&1 || {
        log_error "Docker Compose não encontrado!"
        exit 1
    }
    
    log_info "Docker encontrado: $(docker --version)"
}

# Criar arquivo .env
create_env() {
    log_info "Criando arquivo .env..."
    
    if [ ! -f .env ]; then
        cp .env.example .env
        log_info ".env criado! Configure as senhas."
    else
        log_warn ".env já existe."
    fi
}

# Iniciar serviços
start_services() {
    log_info "Iniciando serviços..."
    docker compose -f docker-compose.dev.yml down -v 2>/dev/null || true
    docker compose -f docker-compose.dev.yml up -d
    
    log_info "Serviços iniciados!"
}

# Mostrar status
show_status() {
    echo ""
    echo "================================"
    echo "📦 Serviços:"
    echo "================================"
    docker compose -f docker-compose.dev.yml ps
    
    echo ""
    echo "🌐 URLs:"
    echo "================================"
    echo "Frontend (Vite): http://localhost:3000"
    echo "Backend API: http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"
    echo "OpenSearch: http://localhost:9200"
    echo "OpenSearch Dashboards: http://localhost:5601"
    echo "PostgreSQL: localhost:5432"
    echo "Redis: localhost:6379"
    echo "Kafka: localhost:9092"
    
    echo ""
    echo "📋 Logs:"
    echo "================================"
    echo "docker compose -f docker-compose.dev.yml logs -f"
    
    echo ""
    echo "🛑 Parar serviços:"
    echo "================================"
    echo "docker compose -f docker-compose.dev.yml down"
}

# Parar serviços
stop_services() {
    log_info "Parando serviços..."
    docker compose -f docker-compose.dev.yml down
    log_info "Serviços parados!"
}

# Main
case "${1:-start}" in
    start)
        check_dependencies
        create_env
        start_services
        show_status
        ;;
    stop)
        stop_services
        ;;
    restart)
        stop_services
        start
        ;;
    status)
        docker compose -f docker-compose.dev.yml ps
        ;;
    logs)
        docker compose -f docker-compose.dev.yml logs -f "${2:-}"
        ;;
    *)
        echo "Uso: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
