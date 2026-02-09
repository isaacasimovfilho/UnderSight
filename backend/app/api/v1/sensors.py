from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.siem import SensorCreate, SensorUpdate, SensorResponse
from app.core.security import get_current_active_user, require_role


router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.get("/", response_model=dict)
async def list_sensors(
    page: int = 1,
    page_size: int = 20,
    sensor_type: Optional[str] = None,
    status_filter: Optional[str] = None,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all sensors."""
    return {
        "items": [],
        "total": 0,
        "page": page,
        "page_size": page_size,
        "total_pages": 0
    }


@router.get("/{sensor_id}", response_model=SensorResponse)
async def get_sensor(
    sensor_id: str,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get sensor details."""
    return SensorResponse(
        id=sensor_id,
        name="linux-sensor-01",
        type="linux",
        endpoint="10.0.0.10:5044",
        status="online",
        version="1.0.0",
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-02-09T05:00:00Z"
    )


@router.post("/", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
async def create_sensor(
    sensor_data: SensorCreate,
    current_user=Depends(require_role(["admin", "engineer"])),
    db: Session = Depends(get_db)
):
    """Create new sensor."""
    return SensorResponse(
        id="1",
        name=sensor_data.name,
        type=sensor_data.type,
        endpoint=sensor_data.endpoint,
        status="offline",
        version=sensor_data.version,
        created_at="2026-02-09T05:00:00Z",
        updated_at="2026-02-09T05:00:00Z"
    )


@router.put("/{sensor_id}", response_model=SensorResponse)
async def update_sensor(
    sensor_id: str,
    sensor_data: SensorUpdate,
    current_user=Depends(require_role(["admin", "engineer"])),
    db: Session = Depends(get_db)
):
    """Update sensor."""
    return SensorResponse(
        id=sensor_id,
        name=sensor_data.name or "updated-sensor",
        type="linux",
        endpoint=sensor_data.endpoint,
        status=sensor_data.status or "offline",
        version=sensor_data.version,
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-02-09T05:00:00Z"
    )


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sensor(
    sensor_id: str,
    current_user=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Delete sensor."""
    pass


@router.post("/{sensor_id}/register")
async def register_sensor(
    sensor_id: str,
    license_key: str,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Register a sensor with license key."""
    return {"status": "registered", "sensor_id": sensor_id}


@router.post("/{sensor_id}/heartbeat")
async def sensor_heartbeat(
    sensor_id: str,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Receive sensor heartbeat."""
    return {"status": "ok", "sensor_id": sensor_id}
