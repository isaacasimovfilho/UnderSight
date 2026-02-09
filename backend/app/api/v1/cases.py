from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.siem import CaseCreate, CaseUpdate, CaseResponse
from app.core.security import get_current_active_user


router = APIRouter(prefix="/cases", tags=["Cases"])


@router.get("/", response_model=dict)
async def list_cases(
    page: int = 1,
    page_size: int = 20,
    status_filter: Optional[str] = None,
    severity: Optional[str] = None,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all cases."""
    return {
        "items": [],
        "total": 0,
        "page": page,
        "page_size": page_size,
        "total_pages": 0
    }


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(
    case_id: str,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get case details."""
    return CaseResponse(
        id=case_id,
        title="Sample Case",
        description="Sample investigation",
        severity="high",
        status="open",
        priority=3,
        assignee_id=None,
        tags=["ransomware"],
        mitre_tactics=["impact"],
        mitre_techniques=["t1486"],
        risk_score=85,
        created_at="2026-02-09T05:00:00Z",
        updated_at="2026-02-09T05:00:00Z",
        closed_at=None
    )


@router.post("/", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_data: CaseCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create new case."""
    return CaseResponse(
        id="1",
        title=case_data.title,
        description=case_data.description,
        severity=case_data.severity,
        status="open",
        priority=case_data.priority,
        assignee_id=None,
        tags=case_data.tags or [],
        mitre_tactics=case_data.mitre_tactics or [],
        mitre_techniques=case_data.mitre_techniques or [],
        risk_score=50,
        created_at="2026-02-09T05:00:00Z",
        updated_at="2026-02-09T05:00:00Z",
        closed_at=None
    )


@router.put("/{case_id}", response_model=CaseResponse)
async def update_case(
    case_id: str,
    case_data: CaseUpdate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update case."""
    return CaseResponse(
        id=case_id,
        title=case_data.title or "Updated Case",
        description=case_data.description,
        severity=case_data.severity or "high",
        status=case_data.status or "open",
        priority=case_data.priority or 3,
        assignee_id=case_data.assignee_id,
        tags=case_data.tags or [],
        mitre_tactics=[],
        mitre_techniques=[],
        risk_score=50,
        created_at="2026-02-09T05:00:00Z",
        updated_at="2026-02-09T05:00:00Z",
        closed_at=case_data.closed_at
    )


@router.post("/{case_id}/close", response_model=CaseResponse)
async def close_case(
    case_id: str,
    resolution: str = "resolved",
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Close a case."""
    return CaseResponse(
        id=case_id,
        title="Closed Case",
        description="Case resolved",
        severity="high",
        status=resolution,
        priority=3,
        assignee_id=None,
        tags=[],
        mitre_tactics=[],
        mitre_techniques=[],
        risk_score=0,
        created_at="2026-02-09T05:00:00Z",
        updated_at="2026-02-09T05:00:00Z",
        closed_at="2026-02-09T06:00:00Z"
    )


@router.get("/{case_id}/timeline")
async def get_case_timeline(case_id: str, current_user=Depends(get_current_active_user)):
    """Get timeline of events for a case."""
    return {"events": []}
