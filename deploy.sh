#!/bin/bash

# ============================================
# UnderSight SIEM - Production Deploy Script
# ============================================

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.prod"
PROJECT_NAME="undersight"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  UnderSight SIEM - Production Deploy${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if .env.prod exists
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}Creating $ENV_FILE from template...${NC}"
    cp .env.prod.example $ENV_FILE
    echo -e "${RED}Please edit $ENV_FILE with your production values!${NC}"
    exit 1
fi

# Check for required variables
echo -e "${YELLOW}Checking environment configuration...${NC}"
if ! grep -q "POSTGRES_PASSWORD=your-secure-password" $ENV_FILE; then
    echo -e "${GREEN}Database password configured ✓${NC}"
else
    echo -e "${RED}ERROR: Set POSTGRES_PASSWORD in $ENV_FILE${NC}"
    exit 1
fi

if ! grep -q "SECRET_KEY=your-super-secret" $ENV_FILE; then
    echo -e "${GREEN}SECRET_KEY configured ✓${NC}"
else
    echo -e "${RED}ERROR: Set SECRET_KEY in $ENV_FILE${NC}"
    exit 1
fi

# Pull latest changes
echo -e "${YELLOW}Pulling latest changes...${NC}"
git pull origin main

# Build images
echo -e "${YELLOW}Building Docker images...${NC}"
docker-compose -f $COMPOSE_FILE build --no-cache

# Stop existing containers
echo -e "${YELLOW}Stopping existing containers...${NC}"
docker-compose -f $COMPOSE_FILE down

# Start services
echo -e "${YELLOW}Starting services...${NC}"
docker-compose -f $COMPOSE_FILE up -d

# Wait for services to be healthy
echo -e "${YELLOW}Waiting for services to be healthy...${NC}"
sleep 10

# Check service health
echo -e "${YELLOW}Checking service health...${NC}"

check_service() {
    local service=$1
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose -f $COMPOSE_FILE ps $service | grep -q "(healthy)"; then
            echo -e "${GREEN}$service is healthy ✓${NC}"
            return 0
        fi
        echo -e "${YELLOW}Waiting for $service... ($attempt/$max_attempts)${NC}"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo -e "${RED}$service failed to become healthy${NC}"
    return 1
}

# Check critical services
check_service postgres
check_service opensearch
check_service backend

# Run database migrations (if any)
echo -e "${YELLOW}Running database migrations...${NC}"
docker-compose -f $COMPOSE_FILE exec -T backend python -c "from app.core.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)" 2>/dev/null || echo -e "${YELLOW}Migrations not required or not configured${NC}"

# Display service status
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Services:"
docker-compose -f $COMPOSE_FILE ps
echo ""
echo -e "${GREEN}URLs:${NC}"
echo "  Frontend: http://localhost:3000"
echo "  API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo "  OpenSearch: http://localhost:9200"
echo "  Dashboards: http://localhost:5601"
echo ""
echo -e "${YELLOW}For HTTPS, configure nginx with SSL certificates${NC}"
echo ""

# Optional: Run tests
echo -e "${YELLOW}Run tests? (y/n)${NC}"
read -r response
if [[ "$response" == "y" ]]; then
    echo -e "${YELLOW}Running tests...${NC}"
    docker-compose -f $COMPOSE_FILE exec -T backend pytest /app/tests/ -v --tb=short || echo -e "${RED}Tests failed${NC}"
fi
