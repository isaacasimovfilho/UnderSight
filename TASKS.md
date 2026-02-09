# UnderSight - Tarefas de Implementação

## ✅ Já Implementado
- Estrutura base do projeto
- Docker Compose básico
- Backend FastAPI (estrutura)
- Frontend React (páginas)
- JWT Auth básico
- RBAC básico

## ❌ Gaps Identificados

### 1. Multitenant Architecture
- [ ] Sistema de tenants (Root → Provedor → Cliente → Cliente do cliente)
- [ ] Database schema para multitenant
- [ ] API endpoints com tenant isolation
- [ ] Frontend tenant selector

### 2. Multi-language Support (i18n)
- [ ] i18n no backend
- [ ] i18n no frontend (React-i18next)
- [ ] Arquivos de tradução (EN, PT, ES)
- [ ] Language selector UI

### 3. RBAC Avançado
- [ ] Roles por tenant
- [ ] Permissions granulares
- [ ] Hierarquia de acesso

### 4. Integrações Configuráveis
- [ ] Painel de configurações de integrações
- [ ] Opções para API keys/credentials
- [ ] Webhook configurations

### 5. Docker Improvements
- [ ] Bind mounts para desenvolvimento
- [ ] Environment variables otimizadas

---

## 📋 Tarefas a Executar

### Tarefa 1: Docker Compose com Bind Mounts
```yaml
# Adicionar volumes ao docker-compose.yml
volumes:
  - ./backend:/app:ro
  - ./frontend:/app:ro
  - postgres-data:/var/lib/postgresql/data
```

### Tarefa 2: Multitenant Schema
```sql
-- Tabelas necessárias
tenants (id, name, type, parent_id, settings)
tenant_users (id, tenant_id, user_id, role)
```

### Tarefa 3: i18n Backend
```python
# middlewares/i18n.py
# Translations para EN, PT, ES
```

### Tarefa 4: i18n Frontend
```bash
npm install react-i18next i18next
# Arquivos: locales/en.json, pt.json, es.json
```

### Tarefa 5: Settings Page Completa
- Integrações configuráveis
- Language selector
- Tenant management
