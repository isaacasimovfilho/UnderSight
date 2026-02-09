# UnderSight - Tarefas de Implementação

## ✅ Implementado
- [x] Estrutura base do projeto
- [x] Docker Compose básico
- [x] Backend FastAPI (estrutura)
- [x] Frontend React (páginas)
- [x] JWT Auth básico
- [x] RBAC básico
- [x] Multitenant Schema
- [x] Multitenant Models
- [x] i18n Backend (EN, PT, ES)
- [x] i18n Frontend (100+ traduções)
- [x] Docker Dev com bind mounts
- [x] Settings Page com integrações
- [x] Módulo de Inventário com IA

## 🔧 Em Andamento

## ❌ Gaps Restantes / Novas Features

### 📦 MÓDULO DE INVENTÁRIO (NOVO!)
- [x] **Schema PostgreSQL** - `03-inventory.sql`
- [x] **Serviço de IA** - `inventory.py`
- [x] **API Endpoints** - `inventory.py`
- [x] **Frontend Pages** - Inventory.tsx, InventorySettings.tsx
- [x] **Integração N8N** - Webhook `/api/v1/inventory/webhook/n8n`

### ✅ RBAC Middleware (NOVO!)
- [x] `backend/app/core/middlewares/rbac.py`
  - Classe `RBACMiddleware`
  - Funções: `require_permission`, `require_any_permission`, `require_all_permissions`
  - Permissões granulares por recurso
  - Mapeamento de roles: admin, analyst, viewer

### ✅ Tenant Isolation (NOVO!)
- [x] `backend/app/core/middlewares/tenant.py`
  - Classe `TenantContext`
  - Classe `TenantIsolationMiddleware`
  - Hierarquia: Root → Provider → Customer → Sub-customer
  - Filtros automáticos por tenant

### ✅ Integrações Backend (NOVO!)
- [x] `backend/app/services/integrations/__init__.py`
  - **SlackService** - Enviar alertas
  - **JiraService** - Criar tickets
  - **VirusTotalService** - Enrichment de ameaças
  - **MISPService** - Plataforma de threat intelligence
  - **IntegrationManager** - Enviar para todos

### ⏳ Frontend i18n
- [ ] Traduzir Dashboard, Alerts, Cases, Assets (partial - traduzido na página Settings)

### ⏳ Testing
- [ ] Unit tests
- [ ] Integration tests

---

## 📋 Tarefas Concluídas Recentemente

### RBAC Middleware
```python
# Uso:
@router.get("/alerts")
async def get_alerts(
    current_user: User = Depends(get_current_user),
    _ = Depends(require_permission(Permissions.ALERTS_READ))
):
    return {"alerts": []}
```

### Tenant Isolation
```python
# Hierarquia:
# Root → Provider → Customer → Sub-customer
# Cada nível só vê seus filhos
```

### Integrações
| Serviço | Configuração |
|---------|-------------|
| Slack | webhook_url, api_key |
| Jira | api_url, api_key, project_key |
| VirusTotal | api_url, api_key |
| MISP | api_url, api_key, verify_ssl |

---

## 📋 Tarefas do Módulo de Inventário (Concluídas)

### ✅ 1. Database Schema (03-inventory.sql)
```sql
-- Tabelas criadas:
- inventory_items (equipamentos processados)
- inventory_ai_logs (logs de processamento IA)
- inventory_ai_configs (configuração por tenant)
- inventory_rules (regras de fallback)
- inventory_sources (fontes de dados)
```

### ✅ 2. AI Service (inventory.py)
```python
# Provedores suportados:
- openai (GPT-4)
- anthropic (Claude)
- groq (Llama2, Mixtral)
- deepseek (DeepSeek)
- ollama (Local)

# Decisões IA:
- approved → Item aprovado automaticamente
- rejected → Item rejeitado
- pending → Pendente de revisão humana
- flag → Marcado para revisão
```

### ✅ 3. API Endpoints
```
POST /api/v1/inventory/webhook/n8n
  └─ Recebe JSON do N8N com equipamentos
  └─ Processa cada item através de IA
  └─ Retorna status de processamento

GET /api/v1/inventory/items
  └─ Lista inventário com filtros
  └─ Paginação

POST /api/v1/inventory/items/{id}/approve
  └─ Aprovar manualmente

POST /api/v1/inventory/items/{id}/reject
  └─ Rejeitar manualmente
```

### ✅ 4. Frontend Inventory Page
- Lista de equipamentos
- Filtros por status, tipo, busca
- Ações em lote (approve/reject)
- Stats cards (total, pending, approved, rejected)

### ✅ 5. Frontend Settings Page
- Configuração de provedor IA (OpenAI, Anthropic, Groq, DeepSeek, Ollama)
- Editor de prompt template
- Webhook URL para N8N
- Regras de fallback

---

## 📋 Tarefas a Executar (Próximas)

### Tarefa 5: RBAC Middleware
```python
# middlewares/rbac.py
class RBACMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Extract token
        # Get user permissions
        # Check against required permission
```

### Tarefa 6: Tenant Isolation Middleware
```python
# middlewares/tenant.py
class TenantMiddleware:
    def process_request(self, request):
        # Get tenant from user
        # Add tenant_id to all queries
        # Filter data by tenant
```

### Tarefa 7: Frontend i18n Complete
- [ ] i18n em Dashboard.tsx
- [ ] i18n em Alerts.tsx
- [ ] i18n em Cases.tsx
- [ ] i18n em Assets.tsx

### Tarefa 8: Integration Services
- [ ] SlackService
- [ ] JiraService
- [ ] VirusTotalService
- [ ] MISPService

### Tarefa 9: Test Suite
- [ ] pytest setup
- [ ] Fixtures para tests
- [ ] Coverage report

---

## 🔗 Links Úteis

- **Repositório:** https://github.com/isaacasimovfilho/UnderSight
- **Issues:** https://github.com/isaacasimovfilho/UnderSight/issues
- **Commits:** https://github.com/isaacasimovfilho/UnderSight/commits/main

## 📝 Notas

### N8N Integration
```json
// N8N deve enviar para:
POST {siem_url}/api/v1/inventory/webhook/n8n

// Formato esperado:
{
  "items": [
    {
      "hostname": "server-01",
      "ip_address": "10.0.0.10",
      "os": "Ubuntu",
      "os_version": "22.04",
      "asset_type": "server",
      "manufacturer": "Dell",
      "model": "PowerEdge",
      "location": "DC-A",
      "department": "IT",
      "tags": ["production", "web"]
    }
  ]
}
```

### AI Providers Configuração
| Provider | API Key Location | Model |
|----------|------------------|-------|
| OpenAI | Env/API | gpt-4, gpt-3.5-turbo |
| Anthropic | Env/API | Claude-3 |
| Groq | Env/API | Llama2, Mixtral |
| DeepSeek | Env/API | DeepSeek-Chat |
| Ollama | Localhost | Llama2, Codellama |
