from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import logging
import os
import json

from app.services.azure.sentinel import (
    get_azure_service,
    AzureSentinelService,
    AzureCredential,
    check_azure_configured
)
from app.services.opensearch.client import opensearch_service

router = APIRouter(prefix="/azure", tags=["Azure Sentinel"])

logger = logging.getLogger(__name__)

# Stats file path
STATS_FILE = "/tmp/azure_sync_stats.json"


def load_stats() -> dict:
    """Load sync stats from file"""
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {"events_fetched": 0, "events_indexed": 0, "last_sync": None}


def save_stats(events_fetched: int = 0, events_indexed: int = 0):
    """Save sync stats to file"""
    try:
        stats = {
            "events_fetched": events_fetched,
            "events_indexed": events_indexed,
            "last_sync": datetime.utcnow().isoformat()
        }
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f)
    except Exception as e:
        logger.warning(f"Failed to save stats: {e}")


class AzureConfigRequest(BaseModel):
    """Azure configuration request"""
    tenant_id: str
    client_id: str
    client_secret: str
    subscription_id: str
    workspace_name: str


class AzureStatusResponse(BaseModel):
    """Azure connection and sync status"""
    status: str
    message: str
    configured: bool
    events_fetched: int = 0
    events_indexed: int = 0
    last_sync: Optional[str] = None
    sync_enabled: bool = False
    sync_running: bool = False
    sync_interval: int = 60


class AzureSyncResponse(BaseModel):
    """Azure sync response"""
    status: str
    events_fetched: int
    events_indexed: int
    timestamp: str


def load_stats() -> dict:
    """Load sync stats from file"""
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {"events_fetched": 0, "events_indexed": 0, "last_sync": None}


def save_stats(events_fetched: int = 0, events_indexed: int = 0):
    """Save sync stats to file"""
    try:
        stats = {
            "events_fetched": events_fetched,
            "events_indexed": events_indexed,
            "last_sync": datetime.utcnow().isoformat()
        }
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f)
    except Exception as e:
        logger.warning(f"Failed to save stats: {e}")


@router.get("/status", response_model=AzureStatusResponse)
async def azure_status():
    """Check Azure Sentinel status and configuration"""
    configured = check_azure_configured()
    stats = load_stats()
    sync_running = False
    
    # Check sync service
    try:
        from app.services.azure.sync import azure_sync_service
        sync_running = azure_sync_service.scheduler is not None if azure_sync_service.scheduler else False
    except Exception:
        pass
    
    if not configured:
        return AzureStatusResponse(
            status="not_configured",
            message="⚠️ Azure credentials not configured",
            configured=False,
            sync_enabled=False,
            sync_running=False
        )
    
    service = get_azure_service()
    result = service.test_connection()
    
    return AzureStatusResponse(
        status=result.get("status", "unknown"),
        message=result.get("message", ""),
        configured=True,
        events_fetched=stats.get("events_fetched", 0),
        events_indexed=stats.get("events_indexed", 0),
        last_sync=stats.get("last_sync"),
        sync_enabled=True,
        sync_running=sync_running,
        sync_interval=60
    )


@router.post("/configure")
async def azure_configure(config: AzureConfigRequest):
    """Configure Azure Sentinel credentials"""
    # In production, store these securely
    # For now, just test connection
    credentials = AzureCredential(
        tenant_id=config.tenant_id,
        client_id=config.client_id,
        client_secret=config.client_secret,
        subscription_id=config.subscription_id,
        workspace_name=config.workspace_name
    )
    
    service = AzureSentinelService(credentials)
    result = service.test_connection()
    
    if result.get("status") == "connected":
        return {
            "status": "success",
            "message": "✅ Azure Sentinel configured successfully",
            "workspace": config.workspace_name
        }
    else:
        raise HTTPException(
            status_code=401,
            detail="Failed to connect to Azure. Check credentials."
        )


@router.get("/events", response_model=dict)
async def fetch_azure_events(hours: int = 24):
    """Fetch events from Azure Sentinel"""
    service = get_azure_service()
    
    if not check_azure_configured():
        raise HTTPException(
            status_code=400,
            detail="Azure Sentinel not configured. Configure credentials first."
        )
    
    try:
        events = service.get_all_events(hours)
        
        return {
            "count": len(events),
            "events": [
                {
                    "timestamp": e.timestamp.isoformat() if isinstance(e.timestamp, datetime) else e.timestamp,
                    "event_type": e.event_type,
                    "severity": e.severity,
                    "title": e.title,
                    "description": e.description,
                    "source_ip": e.source_ip,
                    "user": e.user,
                    "computer": e.computer
                }
                for e in events
            ]
        }
    except Exception as e:
        logger.error(f"❌ Error fetching Azure events: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync", response_model=AzureSyncResponse)
async def sync_azure_events(hours: int = 24):
    """Fetch events from Azure Sentinel and index in OpenSearch"""
    service = get_azure_service()
    
    if not check_azure_configured():
        raise HTTPException(
            status_code=400,
            detail="Azure Sentinel not configured."
        )
    
    try:
        events = service.get_all_events(hours)
        indexed = 0
        
        for event in events:
            if opensearch_service.client:
                try:
                    from app.services.opensearch.client import LogDocument
                    
                    log_doc = LogDocument(
                        timestamp=event.timestamp if isinstance(event.timestamp, datetime) 
                            else datetime.fromisoformat(event.timestamp.replace('Z', '+00:00')),
                        event_type=event.event_type,
                        source_type="azure_sentinel",
                        source_ip=event.source_ip,
                        destination_ip=event.destination_ip,
                        severity=event.severity,
                        message=f"{event.title}: {event.description[:500]}",
                        raw_data=event.raw_data,
                        tenant_id=None,
                        session_id=None,
                        tags=["azure", "sentinel", event.severity]
                    )
                    
                    opensearch_service.index_log(log_doc)
                    indexed += 1
                except Exception as e:
                    logger.warning(f"⚠️ Failed to index event: {e}")
        
        return AzureSyncResponse(
            status="success",
            events_fetched=len(events),
            events_indexed=indexed,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"❌ Error syncing Azure events: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Always save stats after sync attempt
        save_stats()


@router.get("/security-events", response_model=dict)
async def fetch_security_events(hours: int = 24):
    """Fetch security events (Windows events, etc.)"""
    service = get_azure_service()
    
    if not check_azure_configured():
        raise HTTPException(
            status_code=400,
            detail="Azure Sentinel not configured."
        )
    
    try:
        events = service.get_security_events(hours)
        
        return {
            "count": len(events),
            "events": events
        }
    except Exception as e:
        logger.error(f"❌ Error fetching security events: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts", response_model=dict)
async def fetch_sentinel_alerts(hours: int = 24):
    """Fetch Sentinel alerts"""
    service = get_azure_service()
    
    if not check_azure_configured():
        raise HTTPException(
            status_code=400,
            detail="Azure Sentinel not configured."
        )
    
    try:
        alerts = service.get_sentinel_alerts(hours)
        
        return {
            "count": len(alerts),
            "alerts": alerts
        }
    except Exception as e:
        logger.error(f"❌ Error fetching alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))
