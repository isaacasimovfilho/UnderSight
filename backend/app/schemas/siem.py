from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


# ============ Base ============
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ============ User ============
class UserCreate(BaseSchema):
    username: str = Field(..., min_length=3, max_length=100)
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8)
    role: Optional[str] = "analyst"


class UserUpdate(BaseSchema):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseSchema):
    id: str
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None


# ============ Sensor ============
class SensorCreate(BaseSchema):
    name: str
    type: str  # linux, windows, network, cloud
    endpoint: Optional[str] = None
    version: Optional[str] = None
    license_key: Optional[str] = None
    config: Optional[dict] = None


class SensorUpdate(BaseSchema):
    name: Optional[str] = None
    status: Optional[str] = None
    endpoint: Optional[str] = None
    version: Optional[str] = None
    config: Optional[dict] = None


class SensorResponse(BaseSchema):
    id: str
    name: str
    type: str
    endpoint: Optional[str]
    status: str
    version: Optional[str]
    created_at: datetime
    updated_at: datetime


# ============ Asset ============
class AssetCreate(BaseSchema):
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    os: Optional[str] = None
    asset_type: Optional[str] = None
    tags: Optional[List[str]] = None


class AssetUpdate(BaseSchema):
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    os: Optional[str] = None
    risk_score: Optional[int] = None
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None


class AssetResponse(BaseSchema):
    id: str
    hostname: Optional[str]
    ip_address: Optional[str]
    mac_address: Optional[str]
    os: Optional[str]
    asset_type: Optional[str]
    risk_score: int
    tags: List[str]
    first_seen: datetime
    last_seen: datetime


# ============ Alert ============
class AlertCreate(BaseSchema):
    title: str
    description: Optional[str] = None
    severity: str = "medium"  # low, medium, high, critical
    source_type: str
    raw_event: dict
    mitre_tactics: Optional[List[str]] = None
    mitre_techniques: Optional[List[str]] = None


class AlertResponse(BaseSchema):
    id: str
    title: str
    description: Optional[str]
    severity: str
    status: str  # new, in_progress, resolved, closed
    source_type: str
    mitre_tactics: List[str]
    mitre_techniques: List[str]
    risk_score: int
    created_at: datetime
    updated_at: datetime


class AlertUpdate(BaseSchema):
    status: Optional[str] = None
    assignee_id: Optional[str] = None
    notes: Optional[str] = None


# ============ Case ============
class CaseCreate(BaseSchema):
    title: str
    description: Optional[str] = None
    severity: str = "medium"
    priority: int = 3
    alert_ids: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    mitre_tactics: Optional[List[str]] = None
    mitre_techniques: Optional[List[str]] = None


class CaseUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    assignee_id: Optional[str] = None
    tags: Optional[List[str]] = None
    closed_at: Optional[datetime] = None


class CaseResponse(BaseSchema):
    id: str
    title: str
    description: Optional[str]
    severity: str
    status: str
    priority: int
    assignee_id: Optional[str]
    tags: List[str]
    mitre_tactics: List[str]
    mitre_techniques: List[str]
    risk_score: int
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None


# ============ Playbook ============
class PlaybookCreate(BaseSchema):
    name: str
    description: Optional[str] = None
    trigger_type: str  # alert, schedule, manual
    trigger_condition: dict
    actions: List[dict]
    is_enabled: bool = True


class PlaybookUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    trigger_condition: Optional[dict] = None
    actions: Optional[List[dict]] = None
    is_enabled: Optional[bool] = None


class PlaybookResponse(BaseSchema):
    id: str
    name: str
    description: Optional[str]
    trigger_type: str
    trigger_condition: dict
    actions: List[dict]
    is_enabled: bool
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime


# ============ Event (Normalized) ============
class EventCreate(BaseSchema):
    raw: str
    source_type: str
    timestamp: Optional[datetime] = None
    metadata: Optional[dict] = None


class EventResponse(BaseSchema):
    id: str
    source_type: str
    @timestamp: datetime
    host: Optional[dict]
    source: Optional[dict]
    destination: Optional[dict]
    network: Optional[dict]
    process: Optional[dict]
    user: Optional[dict]
    tags: List[str]
    metadata: Optional[dict]


# ============ Pagination ============
class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
