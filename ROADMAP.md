# SIEM Nova Geração - Roadmap

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                      SIEM PLATFORM v1.0                         │
├─────────────────────────────────────────────────────────────────┤
│  Phase 1     │  Phase 2     │  Phase 3   │  Phase 4  │ Phase 5 │
│  MVP Core    │  Core Feat.  │  Detection │  Response │ Polish  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Phase 1: MVP Core (2-3 semanas)

**Objetivo:** Ter infraestrutura + API básica funcionando

### 1.1 Infraestrutura
- [ ] Configurar Docker Compose com todos os serviços
- [ ] PostgreSQL schema completo
- [ ] OpenSearch indices templates
- [ ] Kafka topics setup
- [ ] Redis cache setup
- [ ] CI/CD pipeline básico (GitHub Actions)

### 1.2 Backend Foundation
- [ ] FastAPI app estrutura
- [ ] Database connection (SQLAlchemy)
- [ ] Settings/Config management
- [ ] Logging estruturado
- [ ] Health check endpoints

### 1.3 Autenticação
- [ ] JWT auth implementation
- [ ] User CRUD (create, read, update)
- [ ] Role-based access control (RBAC)
- [ ] Password hashing
- [ ] Token refresh

### 1.4 API Base
- [ ] OpenAPI/Swagger docs
- [ ] Error handling
- [ ] Request validation
- [ ] Rate limiting

### 1.5 Frontend Foundation
- [ ] React + Vite setup
- [ ] Tailwind CSS + shadcn/ui
- [ ] React Query setup
- [ ] Auth context + login page
- [ ] Layout + Navigation

### Entregável Phase 1
```
✅ Plataforma rodando em Docker
✅ Login funcional
✅ Dashboard vazio
✅ API documentada (Swagger)
```

---

## 🔧 Phase 2: Core Features (3-4 semanas)

**Objetivo:** Coleta de dados + visualização básica

### 2.1 Sensor Management
- [ ] Sensor CRUD API
- [ ] Sensor registration
- [ ] Heartbeat system
- [ ] Sensor status tracking

### 2.2 Asset Management
- [ ] Asset CRUD API
- [ ] Asset discovery
- [ ] Asset tagging
- [ ] Asset history

### 2.3 Collection System
- [ ] HTTP collector endpoint
- [ ] Syslog UDP/TCP receiver
- [ ] Kafka consumer
- [ ] Batch ingestion API
- [ ] Source type detection

### 2.4 Parser Engine
- [ ] Parser interface/base class
- [ ] JSON parser
- [ ] Syslog parser (RFC 3164)
- [ ] CEF parser
- [ ] Auto-detection de formato
- [ ] Parser registry

### 2.5 Frontend Pages
- [ ] Dashboard com métricas
- [ ] Assets page com tabela
- [ ] Sensors page
- [ ] Settings page
- [ ] Filtros e busca

### Entregável Phase 2
```
✅ Coleta de logs funcionando
✅ Assets inventory
✅ Dashboard com dados reais
✅ Parsing básico de formatos comuns
```

---

## 🛡️ Phase 3: Detection (4-6 semanas)

**Objetivo:** Detecção de ameaças e correlação

### 3.1 Alert System
- [ ] Alert CRUD API
- [ ] Alert severity levels
- [ ] Alert status workflow
- [ ] Alert assignment
- [ ] Alert notes/comments

### 3.2 Rule Engine
- [ ] Rule definition schema
- [ ] Rule evaluation engine
- [ ] Rule templates (YARA-like)
- [ ] Custom rules API
- [ ] Rule scheduling

### 3.3 Case Management
- [ ] Case CRUD API
- [ ] Case creation from alerts
- [ ] Case timeline
- [ ] Case assignment
- [ ] Case closure workflow
- [ ] Case notes/evidence

### 3.4 Correlation Engine
- [ ] Temporal correlation
- [ ] Entity correlation
- [ ] MITRE ATT&CK mapping
- [ ] Kill chain detection
- [ ] Auto-case creation

### 3.5 ML Detection
- [ ] OpenSearch ML integration
- [ ] Anomaly detection (estatístico)
- [ ] Behavioral analytics (UBA)
- [ ] Model training pipeline
- [ ] Alert scoring

### 3.6 Frontend Detection UI
- [ ] Alerts page completa
- [ ] Alert details com eventos
- [ ] Cases page completa
- [ ] Case investigation view
- [ ] Timeline visualization

### Entregável Phase 3
```
✅ Sistema de alertas funcional
✅ Cases com investigação
✅ Regras de detecção
✅ ML anomaly detection
✅ Correlação básica
```

---

## ⚡ Phase 4: Response (3-4 semanas)

**Objetivo:** Automação de resposta (SOAR básico)

### 4.1 Playbook Engine
- [ ] Playbook definition schema
- [ ] Playbook CRUD API
- [ ] Trigger system (alert, schedule, manual)
- [ ] Playbook execution engine
- [ ] Playbook history/audit

### 4.2 Action Library
- [ ] Action: Block IP (Firewall)
- [ ] Action: Isolate host (EDR)
- [ ] Action: Disable user (Identity)
- [ ] Action: Send email
- [ ] Action: Create ticket
- [ ] Action: Webhook
- [ ] Custom actions API

### 4.3 Integrations
- [ ] Firewall API integration
- [ ] EDR integration (CrowdStrike, Defender)
- [ ] Identity provider (Azure AD, Okta)
- [ ] Ticketing system (Jira, ServiceNow)
- [ ] Email gateway

### 4.4 SOAR Workflows
- [ ] Phishing investigation playbook
- [ ] Malware response playbook
- [ ] Brute force response playbook
- [ ] Data exfiltration playbook
- [ ] Scheduled scans

### 4.5 Frontend Response UI
- [ ] Playbooks page
- [ ] Playbook editor
- [ ] Execution history
- [ ] Action logs
- [ ] Response dashboard

### Entregável Phase 4
```
✅ SOAR básico funcional
✅ Playbooks automatizados
✅ Integrações de resposta
✅ Workflows prontos
```

---

## 📊 Phase 5: Polish & Scale (contínuo)

**Objetivo:** Performance, UX, e maturidade

### 5.1 Performance
- [ ] API optimization
- [ ] Database indexing
- [ ] OpenSearch tuning
- [ ] Kafka partition tuning
- [ ] Caching strategy
- [ ] Load testing

### 5.2 UX Improvements
- [ ] Dark mode
- [ ] Responsive design
- [ ] Advanced search (Lucene)
- [ ] Export functionality
- [ ] Bulk actions
- [ ] Keyboard shortcuts

### 5.3 Threat Intelligence
- [ ] Threat Intel feeds integration
- [ ] IOC matching
- [ ] VirusTotal integration
- [ ] AlienVault OTX
- [ ] MISP integration
- [ ] Custom feeds

### 5.4 Reporting
- [ ] Scheduled reports
- [ ] PDF/Excel export
- [ ] Compliance reports (PCI-DSS, GDPR)
- [ ] Executive dashboard
- [ ] Custom report builder

### 5.5 Testing
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] E2E tests (Playwright)
- [ ] Load tests
- [ ] Security audit

### 5.6 Documentation
- [ ] API documentation
- [ ] User guides
- [ ] Deployment guide
- [ ] Architecture docs
- [ ] Contributing guide

### 5.7 Multi-tenant (futuro)
- [ ] Tenant isolation
- [ ] RBAC avançado
- [ ] Usage quotas
- [ ] Billing integration

---

## 📋 Task Breakdown Detalhado

### Phase 1 Tasks

#### Week 1: Infra + Backend Base
```
Day 1-2: Setup
├── Configurar Docker Compose completo
├── PostgreSQL schema (users, sensors, assets, cases)
├── OpenSearch index templates
└── Kafka topics setup

Day 3-4: FastAPI Foundation
├── Estrutura de diretórios
├── Database session + models
├── Config management (Pydantic Settings)
├── Logging estruturado (loguru)
└── Health check endpoints

Day 5: Auth
├── JWT implementation
├── Password hashing (bcrypt)
├── User CRUD endpoints
├── RBAC basic
└── Login endpoint
```

#### Week 2: Frontend Foundation
```
Day 1-2: Setup + Auth
├── React + Vite + TypeScript
├── Tailwind CSS setup
├── shadcn/ui components
├── React Query setup
└── Auth context + Zustand

Day 3-4: Pages
├── Login page
├── Layout + Sidebar
├── Dashboard page (empty)
└── Navigation routing

Day 5: Polish
├── Error boundaries
├── Loading states
└── Basic theming
```

---

## 🎯 Milestones

### v0.1.0 - "Hello World" (Fim Week 1)
- [ ] Docker Compose funcionando
- [ ] Health check OK
- [ ] APIdocs disponível

### v0.2.0 - "Authenticated" (Fim Week 2)
- [ ] Login funcionando
- [ ] JWT tokens OK
- [ ] Frontend logado

### v0.3.0 - "Data Flow" (Fim Phase 2)
- [ ] Logs sendo coletados
- [ ] Parsing funcionando
- [ ] Dashboard com dados

### v0.4.0 - "Detection" (Fim Phase 3)
- [ ] Alertas sendo gerados
- [ ] Cases funcionando
- [ ] ML detection ativo

### v0.5.0 - "Response" (Fim Phase 4)
- [ ] Playbooks executando
- [ ] Integrações de resposta
- [ ] Automação funcionando

### v1.0.0 - "Production Ready" (Fim Phase 5)
- [ ] Tests passando
- [ ] Docs completas
- [ ] Performance otimizada
- [ ] Deploy ready

---

## 📊 Estimativas

| Phase | Semanas | Esforço |
|-------|---------|---------|
| Phase 1 | 2-3 | 3 pessoas |
| Phase 2 | 3-4 | 3 pessoas |
| Phase 3 | 4-6 | 2 pessoas |
| Phase 4 | 3-4 | 2 pessoas |
| Phase 5 | contínua | 1-2 pessoas |
| **Total** | **15-20** | - |

---

## 🔗 Dependencies

```
Phase 1 ──────────────────────────────────────┐
   │                                             │
   ▼                                             ▼
Phase 2 ──────────────────────────► Phase 3 ──► Phase 4 ──► Phase 5
(Infra)    (Collection/Parsing)    (Detection)  (Response)   (Polish)
```

---

## 📦 Entregáveis por Fase

### Phase 1
- Docker Compose
- FastAPI app
- React frontend
- API docs (Swagger)
- JWT auth

### Phase 2
- Coleta HTTP/Syslog/Kafka
- Parser engine (5+ formats)
- Asset management
- Dashboard com métricas

### Phase 3
- Alert system
- Case management
- Correlation engine
- ML detection

### Phase 4
- Playbook engine
- 5+ actions
- 4+ playbook templates
- Integration APIs

### Phase 5
- Performance optimized
- Docs completas
- Tests (80%+ coverage)
- Multi-tenant ready

---

## 🏷️ Labels para Issues

```
type: bug / feature / docs / infra / security
priority: critical / high / medium / low
phase: phase1 / phase2 / phase3 / phase4 / phase5
status: todo / in_progress / review / done
```

---

## 🚦 Definition of Done

Para cada task:
- [ ] Código revisado
- [ ] Tests escritos
- [ ] Docs atualizadas
- [ ] Funcionando localmente
- [ ] Merge na main branch
- [ ] CI/CD passando

---

*Documento vivo - atualizar conforme progresso*
*Criado: 2026-02-09*
