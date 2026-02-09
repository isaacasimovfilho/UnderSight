# SIEM Nova Geração

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                       │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│   │  Dashboard  │  │  Cases UI   │  │  Threat Hunting    │ │
│   └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY (FastAPI)                   │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│   │  /collect   │  │  /detect    │  │  /respond          │ │
│   └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Kafka      │  │   OpenSearch │  │  PostgreSQL  │
│  (Events)    │  │   (Logs)     │  │  (Config)    │
└──────────────┘  └──────────────┘  └──────────────┘
```

## 📁 Estrutura do Projeto

```
siem/
├── backend/                    # Python/FastAPI
│   ├── app/
│   │   ├── api/               # Endpoints
│   │   │   ├── v1/
│   │   │   │   ├── alerts.py
│   │   │   │   ├── cases.py
│   │   │   │   ├── assets.py
│   │   │   │   ├── sensors.py
│   │   │   │   ├── collectors.py
│   │   │   │   ├── playbooks.py
│   │   │   │   └── users.py
│   │   │   └── __init__.py
│   │   ├── core/              # Config, security
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── __init__.py
│   │   ├── db/                # Database
│   │   │   ├── session.py
│   │   │   ├── models/
│   │   │   └── repositories/
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── sensor.py
│   │   │   ├── asset.py
│   │   │   ├── case.py
│   │   │   └── playbook.py
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   │   ├── parsing.py
│   │   │   ├── enrichment.py
│   │   │   ├── detection.py
│   │   │   └── correlation.py
│   │   ├── ml/                # ML models
│   │   ├── parsers/           # Log parsers
│   │   │   ├── base.py
│   │   │   ├── syslog.py
│   │   │   ├── json.py
│   │   │   └── cef.py
│   │   ├── main.py            # FastAPI app
│   │   └── __init__.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                  # React + TypeScript
│   ├── src/
│   │   ├── components/        # UI Components
│   │   │   ├── common/
│   │   │   ├── layout/
│   │   │   ├── dashboard/
│   │   │   ├── alerts/
│   │   │   ├── cases/
│   │   │   ├── assets/
│   │   │   └── hunt/
│   │   ├── pages/            # Pages/Routes
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Alerts.tsx
│   │   │   ├── Cases.tsx
│   │   │   ├── Assets.tsx
│   │   │   ├── Settings.tsx
│   │   │   └── Login.tsx
│   │   ├── services/         # API calls
│   │   │   ├── api.ts
│   │   │   ├── alerts.ts
│   │   │   └── auth.ts
│   │   ├── hooks/            # Custom hooks
│   │   ├── stores/           # State (Zustand)
│   │   ├── types/            # TypeScript types
│   │   ├── utils/            # Helpers
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── collectors/               # Log collectors (Go)
│   ├── syslog/
│   ├── http/
│   ├── kafka/
│   └── Dockerfile
│
├── sensors/                  # Endpoint agents
│   ├── windows/
│   ├── linux/
│   └── README.md
│
├── infrastructure/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── kubernetes/
│   │   ├── namespace.yaml
│   │   ├── backend-deployment.yaml
│   │   └── postgres-pvc.yaml
│   └── monitoring/
│       ├── prometheus.yml
│       └── grafana/
│
├── scripts/
│   ├── setup.sh
│   ├── migrate.sh
│   └── seed.sh
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   └── deployment.md
│
├── .env.example
├── docker-compose.yml
├── Makefile
├── README.md
└── LICENSE
```

## 🚀 Quick Start

```bash
# Clone e setup
git clone https://github.com/isaacasimovfilho/UnderSight.git
cd siem

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Ou com Docker
docker-compose up -d
```

## 📦 Tech Stack

| Camada | Tecnologia |
|--------|------------|
| Backend API | FastAPI (Python) |
| Frontend | React + TypeScript + Vite |
| Database (Logs) | OpenSearch |
| Database (Config) | PostgreSQL |
| Message Queue | Apache Kafka |
| Parsing | Python (custom) |
| ML | scikit-learn + OpenSearch ML |
| Auth | JWT + OAuth2 |
| Containerization | Docker + Docker Compose |
| Deployment | Kubernetes (opcional) |

## 📚 Documentação

- [Arquitetura](docs/architecture.md)
- [API Reference](docs/api.md)
- [Deployment](docs/deployment.md)

## 📄 Licença

MIT License
