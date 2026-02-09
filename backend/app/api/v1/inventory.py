"""
Inventory API Endpoints

Routes:
- POST /api/v1/inventory/webhook/n8n - Receive from N8N
- GET /api/v1/inventory/items - List inventory
- GET /api/v1/inventory/items/{id} - Get single item
- PUT /api/v1/inventory/items/{id}/approve - Approve item
- PUT /api/v1/inventory/items/{id}/reject - Reject item
- GET /api/v1/inventory/config - Get AI config
- PUT /api/v1/inventory/config - Update AI config
- POST /api/v1/inventory/config/test - Test AI config
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.core.i18n import get_message


router = APIRouter(prefix="/inventory", tags=["Inventory"])


# ============= Pydantic Schemas =============

class EquipmentInput(BaseModel):
    """Equipment data from N8N"""
    external_id: Optional[str] = None
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    os: Optional[str] = None
    os_version: Optional[str] = None
    asset_type: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None
    owner: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
    source: str = "n8n"


class N8NWebhookInput(BaseModel):
    """N8N webhook payload"""
    items: List[EquipmentInput] = Field(default_factory=list)
    batch_id: Optional[str] = None
    timestamp: Optional[str] = None


class InventoryItemResponse(BaseModel):
    """Inventory item response"""
    id: str
    tenant_id: str
    source: str
    external_id: Optional[str]
    hostname: Optional[str]
    ip_address: Optional[str]
    mac_address: Optional[str]
    os: Optional[str]
    os_version: Optional[str]
    asset_type: Optional[str]
    manufacturer: Optional[str]
    model: Optional[str]
    serial_number: Optional[str]
    location: Optional[str]
    department: Optional[str]
    owner: Optional[str]
    tags: List[str]
    risk_score: int
    status: str
    inventory_decision: str
    inventory_comments: str
    processed_by: str
    created_at: datetime
    processed_at: Optional[datetime]


class InventoryListResponse(BaseModel):
    """Paginated inventory list"""
    items: List[InventoryItemResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AIConfigInput(BaseModel):
    """AI configuration input"""
    provider: str = Field(..., description="openai, anthropic, ollama, groq, deepseek")
    api_url: Optional[str] = None
    api_key_encrypted: Optional[str] = None
    model: str = "gpt-4"
    prompt_template: str = Field(default="")
    temperature: float = 0.3
    max_tokens: int = 1000
    is_enabled: bool = True
    auto_process: bool = True
    webhook_url: Optional[str] = None


class AIConfigResponse(BaseModel):
    """AI configuration response (without API key)"""
    id: str
    tenant_id: str
    name: str
    description: Optional[str]
    provider: str
    api_url: Optional[str]
    model: str
    prompt_template: str
    temperature: float
    max_tokens: int
    is_enabled: bool
    auto_process: bool
    webhook_url: Optional[str]
    created_at: datetime
    updated_at: datetime


class TestAIResponse(BaseModel):
    """Test AI configuration response"""
    success: bool
    decision: Optional[str]
    comments: Optional[str]
    confidence: Optional[float]
    processing_time_ms: int
    error: Optional[str]


# ============= API Endpoints =============

@router.post("/webhook/n8n", status_code=status.HTTP_202_ACCEPTED)
async def receive_from_n8n(
    payload: N8NWebhookInput,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_active_user)
):
    """
    Receive equipment data from N8N webhook.
    
    This endpoint accepts JSON from N8N containing equipment information.
    Each item is processed through AI to decide if it should be added to inventory.
    """
    # Import here to avoid circular imports
    from app.services.inventory import InventoryService, EquipmentData, AIConfig
    
    # TODO: Get tenant ID from user/tenant relationship
    tenant_id = str(current_user.tenant_id) if hasattr(current_user, 'tenant_id') else "default"
    
    # Create AI config (load from database in real implementation)
    ai_config = AIConfig(
        provider="openai",  # TODO: Load from database
        api_key="",  # TODO: Load from secure storage
        model="gpt-4",
    )
    
    # Create service
    # Note: In real implementation, pass actual DB session
    service = InventoryService(db=None, tenant_id=tenant_id, ai_config=ai_config)
    
    # Process items
    items = [EquipmentData(**item.dict()) for item in payload.items]
    result = await service.receive_from_n8n({
        "items": [item.dict() for item in items]
    })
    
    return {
        "status": "accepted",
        "batch_id": payload.batch_id,
        "received": result["received"],
        "message": f"Processing {result['received']} items"
    }


@router.get("/items", response_model=InventoryListResponse)
async def list_inventory(
    status_filter: Optional[str] = None,
    asset_type: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List inventory items with filters"""
    # TODO: Query from database
    return {
        "items": [],
        "total": 0,
        "page": page,
        "page_size": page_size,
        "total_pages": 0
    }


@router.get("/items/{item_id}", response_model=InventoryItemResponse)
async def get_inventory_item(
    item_id: str,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a single inventory item"""
    # TODO: Query from database
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found"
    )


@router.post("/items/{item_id}/approve")
async def approve_item(
    item_id: str,
    comments: Optional[str] = None,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Manually approve an inventory item"""
    # TODO: Update in database
    return {
        "status": "success",
        "item_id": item_id,
        "decision": "approved",
        "approved_by": str(current_user.id),
        "comments": comments
    }


@router.post("/items/{item_id}/reject")
async def reject_item(
    item_id: str,
    comments: Optional[str] = None,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Manually reject an inventory item"""
    # TODO: Update in database
    return {
        "status": "success",
        "item_id": item_id,
        "decision": "rejected",
        "rejected_by": str(current_user.id),
        "comments": comments
    }


@router.get("/config", response_model=AIConfigResponse)
async def get_ai_config(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current AI configuration"""
    # TODO: Load from database
    return {
        "id": "",
        "tenant_id": "",
        "name": "Default AI Config",
        "description": "Default AI configuration for inventory processing",
        "provider": "openai",
        "api_url": "https://api.openai.com/v1",
        "model": "gpt-4",
        "prompt_template": "",
        "temperature": 0.3,
        "max_tokens": 1000,
        "is_enabled": True,
        "auto_process": True,
        "webhook_url": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


@router.put("/config")
async def update_ai_config(
    config: AIConfigInput,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update AI configuration"""
    # TODO: Save to database (encrypt API key)
    return {
        "status": "success",
        "message": "Configuration updated",
        "config": {
            "provider": config.provider,
            "model": config.model,
            "is_enabled": config.is_enabled,
            "auto_process": config.auto_process
        }
    }


@router.post("/config/test", response_model=TestAIResponse)
async def test_ai_config(
    config: AIConfigInput,
    current_user=Depends(get_current_active_user)
):
    """Test AI configuration with a sample item"""
    from app.services.inventory import AIService, EquipmentData
    
    # Create test item
    test_item = EquipmentInput(
        hostname="test-server-01",
        ip_address="10.0.0.100",
        os="Ubuntu Linux",
        os_version="22.04",
        asset_type="server",
        manufacturer="Dell",
        model="PowerEdge R740",
        source="test"
    )
    
    # Create AI service
    ai_service = AIService(
        provider=config.provider,
        api_url=config.api_url,
        api_key=config.api_key_encrypted or "",
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        prompt_template=config.prompt_template or ""
    )
    
    # Test with single item
    result = await ai_service.process_item(test_item)
    
    return {
        "success": result.decision.value != "pending",
        "decision": result.decision.value,
        "comments": result.comments,
        "confidence": result.confidence,
        "processing_time_ms": 0,  # TODO: Measure
        "error": None if result.decision.value != "pending" else "Processing failed"
    }


@router.get("/stats")
async def get_inventory_stats(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get inventory statistics"""
    # TODO: Query from database
    return {
        "total_items": 0,
        "pending": 0,
        "approved": 0,
        "rejected": 0,
        "by_asset_type": {},
        "by_os": {},
        "recent_activity": []
    }


@router.post("/bulk/approve")
async def bulk_approve(
    item_ids: List[str],
    comments: Optional[str] = None,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Bulk approve inventory items"""
    return {
        "status": "success",
        "approved_count": len(item_ids),
        "item_ids": item_ids
    }


@router.post("/bulk/reject")
async def bulk_reject(
    item_ids: List[str],
    comments: Optional[str] = None,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Bulk reject inventory items"""
    return {
        "status": "success",
        "rejected_count": len(item_ids),
        "item_ids": item_ids
    }
