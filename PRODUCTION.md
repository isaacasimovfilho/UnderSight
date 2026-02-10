# UnderSight SIEM - Production Deployment

## Quick Start

### 1. Configure Environment

```bash
# Copy environment template
cp .env.prod.example .env.prod

# Edit with your values
nano .env.prod
```

**Required changes:**
- `POSTGRES_PASSWORD` - Strong database password
- `SECRET_KEY` - At least 32 character secret key
- `JWT_SECRET_KEY` - JWT signing secret
- `JWT_REFRESH_SECRET_KEY` - Refresh token secret

### 2. Deploy

```bash
# Make deploy script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### 3. Access

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| OpenSearch | http://localhost:9200 |
| Dashboards | http://localhost:5601 |

## Services

| Service | Port | Description |
|---------|------|-------------|
| postgres | 5432 | PostgreSQL database |
| opensearch | 9200 | Search & analytics |
| kafka | 9092 | Message queue |
| redis | 6379 | Cache |
| backend | 8000 | API server |
| frontend | 3000 | Web UI |

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| POSTGRES_USER | Database user | Yes |
| POSTGRES_PASSWORD | Database password | Yes |
| POSTGRES_DB | Database name | Yes |
| SECRET_KEY | App secret key | Yes |
| JWT_SECRET_KEY | JWT secret | Yes |
| LOG_LEVEL | Logging level | No |

### Optional Integrations

```bash
# AI Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=...
GROQ_API_KEY=...
DEEPSEEK_API_KEY=...

# External Services
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
JIRA_API_URL=https://...
JIRA_API_KEY=...
VIRUSTOTAL_API_KEY=...
MISP_API_URL=https://...
MISP_API_KEY=...
```

## SSL/HTTPS Setup

### Using Nginx (Included)

1. Generate SSL certificates:
```bash
# Using Let's Encrypt (requires domain)
certbot certonly --standalone -d yourdomain.com

# Or self-signed for testing
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem
```

2. Enable HTTPS in nginx config:
```bash
# Uncomment HTTPS server block in nginx/nginx.conf
# And configure SSL paths
```

3. Restart nginx:
```bash
docker-compose -f docker-compose.prod.yml restart nginx
```

## Maintenance

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs

# Specific service
docker-compose -f docker-compose.prod.yml logs backend

# Follow mode
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Restart Services

```bash
# Restart all
docker-compose -f docker-compose.prod.yml restart

# Restart specific
docker-compose -f docker-compose.prod.yml restart backend
```

### Backup

```bash
# Create backup
./backup.sh

# Backups stored in ./backups/
```

### Update

```bash
# Pull latest changes
git pull origin main

# Rebuild and redeploy
./deploy.sh
```

### Scale (Optional)

```bash
# Scale backend workers
docker-compose -f docker-compose.prod.yml up -d --scale backend=2

# Scale frontend (requires nginx)
docker-compose -f docker-compose.prod.yml up -d --scale frontend=2
```

## Health Checks

### Manual Health Check

```bash
# Backend
curl http://localhost:8000/health

# OpenSearch
curl http://localhost:9200/_cluster/health

# PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U siem

# Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill container and restart
docker-compose -f docker-compose.prod.yml rm -sf backend
docker-compose -f docker-compose.prod.yml up -d backend
```

### Database Connection Issues

```bash
# Check database logs
docker-compose -f docker-compose.prod.yml logs postgres

# Verify connection
docker-compose -f docker-compose.prod.yml exec postgres psql -U siem -d siem_platform
```

### Reset Everything

```bash
# WARNING: This deletes all data!
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d
```

## Resource Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| Memory | 4 GB | 8+ GB |
| Storage | 50 GB | 100+ GB SSD |

## Security Recommendations

1. **Change all default passwords**
2. **Enable SSL/HTTPS in production**
3. **Restrict database ports to localhost**
4. **Use secrets management (Vault, AWS Secrets)**
5. **Regular backups**
6. **Monitor logs**
7. **Keep dependencies updated**
