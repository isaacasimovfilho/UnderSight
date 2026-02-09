#!/bin/bash

# Script para criar issues do UnderSight no GitHub
# Uso: GITHUB_TOKEN=xxx ./create-issues.sh

TOKEN="${GITHUB_TOKEN}"
REPO="isaacasimovfilho/UnderSight"
BASE_URL="https://api.github.com/repos/$REPO"

if [ -z "$TOKEN" ]; then
    echo "❌ Erro: GITHUB_TOKEN nao definido!"
    echo "Uso: GITHUB_TOKEN=xxx ./create-issues.sh"
    exit 1
fi

echo "🚀 Criando issues para $REPO..."
echo ""

# Criar labels
echo "Criando labels..."
curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/labels" \
  -d '{"name":"type: bug","color":"d73a4a"}' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/labels" \
  -d '{"name":"type: feature","color":"a2eeef"}' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/labels" \
  -d '{"name":"type: infra","color":"0366d6"}' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/labels" \
  -d '{"name":"priority: critical","color":"b60205"}' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/labels" \
  -d '{"name":"priority: high","color":"ff9900"}' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/labels" \
  -d '{"name":"priority: medium","color":"fbca04"}' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/labels" \
  -d '{"name":"phase: 1","color":"98c379"}' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/labels" \
  -d '{"name":"phase: 2","color":"61afef"}' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/labels" \
  -d '{"name":"phase: 3","color":"c678dd"}' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/labels" \
  -d '{"name":"phase: 4","color":"e06c75"}' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/labels" \
  -d '{"name":"phase: 5","color":"e5c07b"}' > /dev/null

echo "Labels criadas!"
echo ""

# Phase 1 Issues
echo "=== Phase 1: MVP Core ==="

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Infra] Configurar Docker Compose",
    "body": "Configurar Docker Compose com PostgreSQL, Open Redis, Backend eSearch, Kafka, Frontend.",
    "labels": ["type: infra", "priority: high", "phase: 1"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Infra] PostgreSQL schema completo",
    "body": "Criar schema do PostgreSQL para configuracoes e metadados.",
    "labels": ["type: infra", "priority: high", "phase: 1"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] FastAPI app estrutura base",
    "body": "Criar estrutura base do FastAPI application.",
    "labels": ["type: feature", "priority: high", "phase: 1"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] Sistema de Autenticacao JWT",
    "body": "Implementar autenticacao com JWT tokens.",
    "labels": ["type: feature", "priority: high", "phase: 1"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] User CRUD e RBAC",
    "body": "Implementar CRUD de usuarios e Role-Based Access Control.",
    "labels": ["type: feature", "priority: medium", "phase: 1"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Frontend] Setup React + Vite + TypeScript",
    "body": "Criar estrutura base do frontend com React, Vite, TypeScript.",
    "labels": ["type: infra", "priority: high", "phase: 1"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Frontend] Sistema de Auth e Login",
    "body": "Implementar sistema de autenticacao no frontend.",
    "labels": ["type: feature", "priority: high", "phase: 1"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Frontend] Layout e Navigation",
    "body": "Criar layout principal e navegacao.",
    "labels": ["type: feature", "priority: medium", "phase: 1"]
  }' > /dev/null

echo "Phase 1: 8 issues"

echo ""
echo "=== Phase 2: Core Features ==="

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] Sensor Management API",
    "body": "Implementar CRUD de sensors e sistema de heartbeat.",
    "labels": ["type: feature", "priority: high", "phase: 2"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] Asset Management API",
    "body": "Implementar CRUD de assets e descoberta.",
    "labels": ["type: feature", "priority: high", "phase: 2"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] Sistema de Coleta (HTTP/Syslog/Kafka)",
    "body": "Implementar endpoints para coleta de logs.",
    "labels": ["type: feature", "priority: high", "phase: 2"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] Parser Engine",
    "body": "Criar engine de parsing para diferentes formatos.",
    "labels": ["type: feature", "priority: high", "phase: 2"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Frontend] Dashboard com metricas",
    "body": "Criar dashboard com KPIs e metricas.",
    "labels": ["type: feature", "priority: medium", "phase: 2"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Frontend] Assets Page",
    "body": "Criar pagina de visualizacao de assets.",
    "labels": ["type: feature", "priority: medium", "phase: 2"]
  }' > /dev/null

echo "Phase 2: 6 issues"

echo ""
echo "=== Phase 3: Detection ==="

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] Alert System",
    "body": "Implementar sistema completo de alertas.",
    "labels": ["type: feature", "priority: high", "phase: 3"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] Case Management",
    "body": "Implementar gerenciamento de casos.",
    "labels": ["type: feature", "priority: high", "phase: 3"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] Rule Engine",
    "body": "Criar engine para regras de deteccao.",
    "labels": ["type: feature", "priority: medium", "phase: 3"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] Correlation Engine",
    "body": "Implementar engine de correlacao de eventos.",
    "labels": ["type: feature", "priority: medium", "phase: 3"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Frontend] Alerts Page completa",
    "body": "Criar pagina completa de alertas.",
    "labels": ["type: feature", "priority: high", "phase: 3"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Frontend] Cases Page completa",
    "body": "Criar pagina completa de cases.",
    "labels": ["type: feature", "priority: high", "phase: 3"]
  }' > /dev/null

echo "Phase 3: 6 issues"

echo ""
echo "=== Phase 4: Response ==="

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] Playbook Engine",
    "body": "Criar engine de playbooks para automacao.",
    "labels": ["type: feature", "priority: high", "phase: 4"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] Action Library",
    "body": "Criar biblioteca de acoes para playbooks.",
    "labels": ["type: feature", "priority: high", "phase: 4"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Backend] Integracoes externas",
    "body": "Criar integracoes com ferramentas externas.",
    "labels": ["type: feature", "priority: medium", "phase: 4"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Frontend] Playbooks Page",
    "body": "Criar pagina de gerenciamento de playbooks.",
    "labels": ["type: feature", "priority: medium", "phase: 4"]
  }' > /dev/null

echo "Phase 4: 4 issues"

echo ""
echo "=== Phase 5: Polish ==="

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Infra] Performance Tuning",
    "body": "Otimizacoes de performance.",
    "labels": ["type: infra", "priority: medium", "phase: 5"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Testing] Cobertura de testes",
    "body": "Alcancar 80%+ de cobertura de testes.",
    "labels": ["type: bug", "priority: medium", "phase: 5"]
  }' > /dev/null

curl -s -X POST -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "$BASE_URL/issues" \
  -d '{
    "title": "[Docs] Documentacao completa",
    "body": "Documentacao completa do projeto.",
    "labels": ["type: docs", "priority: low", "phase: 5"]
  }' > /dev/null

echo "Phase 5: 3 issues"
echo ""
echo "========================================"
echo "✅ TOTAL: 31 issues criadas!"
echo "========================================"
echo ""
echo "Verifique: https://github.com/$REPO/issues"
