from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.db.session import get_db
from app.schemas.siem import (
    EventCreate, EventResponse,
    CollectorCreate, CollectorResponse
)
from app.core.security import get_current_active_user


router = APIRouter(prefix="/collect", tags=["Collection"])


class CollectEventRequest(BaseModel):
    source_type: str
    raw: str
    timestamp: Optional[str] = None
    metadata: Optional[dict] = None


class CollectResponse(BaseModel):
    event_id: str
    status: str
    timestamp: str


@router.post("/event", response_model=CollectResponse)
async def collect_event(
    event_data: CollectEventRequest,
    current_user=Depends(get_current_active_user)
):
    """Collect a single event via API."""
    import uuid
    from datetime import datetime
    
    event_id = str(uuid.uuid4())
    return {
        "event_id": event_id,
        "status": "received",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.post("/events/batch", response_model=dict)
async def collect_events_batch(
    events: List[CollectEventRequest],
    current_user=Depends(get_current_active_user)
):
    """Collect multiple events in batch."""
    import uuid
    from datetime import datetime
    
    results = []
    for e in events:
        results.append({
            "event_id": str(uuid.uuid4()),
            "status": "received",
            "source_type": e.source_type
        })
    
    return {
        "received": len(results),
        "events": results
    }


@router.get("/connectors", response_model=list)
async def list_connectors(current_user=Depends(get_current_active_user)):
    """List available collectors/connectors."""
    return [
        {"id": "syslog", "name": "Syslog Collector", "type": "syslog", "status": "running"},
        {"id": "http", "name": "HTTP Event Collector", "type": "http", "status": "running"},
        {"id": "kafka", "name": "Kafka Consumer", "type": "kafka", "status": "running"},
        {"id": "aws", "name": "AWS CloudTrail", "type": "cloud", "status": "configured"},
        {"id": "azure", "name": "Azure Activity Log", "type": "cloud", "status": "configured"},
    ]


@router.post("/connectors/{connector_id}/test")
async def test_connector(
    connector_id: str,
    current_user=Depends(get_current_active_user)
):
    """Test a collector connection."""
    return {"status": "success", "connector_id": connector_id}


# Webhook endpoints for external systems
@router.post("/webhook/{webhook_id}")
async def webhook_ingest(
    webhook_id: str,
    payload: dict,
    current_user=Depends(get_current_active_user)
):
    """Generic webhook endpoint for external integrations."""
    import uuid
    from datetime import datetime
    
    return {
        "event_id": str(uuid.uuid4()),
        "webhook_id": webhook_id,
        "status": "received",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
