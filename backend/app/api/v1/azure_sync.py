from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

from app.services.azure.sync import azure_sync_service

router = APIRouter(prefix="/azure", tags=["Azure Sentinel Sync"])


class SyncResponse(BaseModel):
    """Sync operation response"""
    status: str
    message: str
    timestamp: str


@router.get("/sync/status", response_model=Dict[str, Any])
async def sync_status():
    """Get sync service status"""
    return {
        "enabled": azure_sync_service.enabled,
        "scheduler_running": azure_sync_service.scheduler is not None,
        "sync_interval_minutes": azure_sync_service.sync_interval_minutes,
        "last_sync": None  # Could track last sync time
    }


@router.post("/sync/start", response_model=SyncResponse)
async def start_sync():
    """Start the automatic sync scheduler"""
    try:
        azure_sync_service.start_scheduler()
        return SyncResponse(
            status="success",
            message="✅ Azure Sentinel sync scheduler started",
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        return SyncResponse(
            status="error",
            message=f"❌ Failed to start sync: {str(e)}",
            timestamp=datetime.utcnow().isoformat()
        )


@router.post("/sync/stop", response_model=SyncResponse)
async def stop_sync():
    """Stop the automatic sync scheduler"""
    try:
        azure_sync_service.stop_scheduler()
        return SyncResponse(
            status="success",
            message="✅ Azure Sentinel sync scheduler stopped",
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        return SyncResponse(
            status="error",
            message=f"❌ Failed to stop sync: {str(e)}",
            timestamp=datetime.utcnow().isoformat()
        )


@router.post("/sync/trigger", response_model=SyncResponse)
async def trigger_manual_sync():
    """Trigger a manual sync immediately"""
    try:
        azure_sync_service.trigger_manual_sync()
        return SyncResponse(
            status="success",
            message="✅ Manual sync completed",
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        return SyncResponse(
            status="error",
            message=f"❌ Manual sync failed: {str(e)}",
            timestamp=datetime.utcnow().isoformat()
        )


@router.get("/sync/logs", response_model=dict)
async def get_sync_logs(lines: int = 50):
    """Get recent sync logs"""
    import subprocess
    try:
        result = subprocess.run(
            ['docker', 'logs', '--tail', str(lines), 'siem-backend'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Filter for sync-related logs
        logs = result.stdout.split('\n')
        sync_logs = [l for l in logs if 'azure' in l.lower() or 'sentinel' in l.lower()]
        
        return {
            "logs": sync_logs[-lines:],
            "total_lines": len(sync_logs)
        }
    except Exception as e:
        return {"logs": [], "error": str(e)}
