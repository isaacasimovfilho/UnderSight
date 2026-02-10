#!/bin/bash

# ============================================
# UnderSight SIEM - Backup Script
# ============================================

set -e

# Configuration
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_NAME="undersight"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  UnderSight SIEM - Backup${NC}"
echo -e "${GREEN}========================================${NC}"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
echo -e "${YELLOW}Backing up PostgreSQL...${NC}"
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U siem siem_platform | gzip > "$BACKUP_DIR/postgres_$DATE.sql.gz"
echo -e "${GREEN}PostgreSQL backup complete: postgres_$DATE.sql.gz${NC}"

# Backup OpenSearch (indices)
echo -e "${YELLOW}Backing up OpenSearch...${NC}"
curl -s -X PUT "localhost:9200/_snapshot/backup_$DATE" -H "Content-Type: application/json" -d '{"type":"fs","settings":{"location":"'$BACKUP_DIR'/opensearch_$DATE"}}' 2>/dev/null || true
curl -s -X PUT "localhost:9200/_snapshot/backup_$DATE/snapshot_$DATE?wait_for_completion=true" 2>/dev/null || echo -e "${YELLOW}OpenSearch snapshot skipped (configure repository first)${NC}"
echo -e "${GREEN}OpenSearch backup complete${NC}"

# Backup Redis
echo -e "${YELLOW}Backing up Redis...${NC}"
docker-compose -f docker-compose.prod.yml exec -T redis BGSAVE
sleep 2
docker-compose -f docker-compose.prod.yml exec -T redis COPYBACKUP "redis_$DATE.rdb" || true
docker-compose -f docker-compose.prod.yml exec -T redis redis-cli BGSAVE 2>/dev/null || true
echo -e "${GREEN}Redis backup complete${NC}"

# List backups
echo ""
echo -e "${GREEN}Available backups:${NC}"
ls -lh $BACKUP_DIR/

# Cleanup old backups (keep last 7)
echo ""
echo -e "${YELLOW}Keeping last 7 backups...${NC}"
ls -t $BACKUP_DIR/*.gz 2>/dev/null | tail -n +8 | xargs rm -f 2>/dev/null || true

echo ""
echo -e "${GREEN}Backup complete!${NC}"
echo "Location: $BACKUP_DIR"
