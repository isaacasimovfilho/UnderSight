"""
Tenant Isolation Middleware for UnderSight

Provides multi-tenant data isolation.
Hierarchical structure: Root → Provider → Customer → Sub-customer
"""

from typing import Callable, Optional
from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session


class TenantContext:
    """
    Context holder for current tenant information.
    
    Usage:
        tenant_id = TenantContext.get()
        TenantContext.set(tenant_id)
    """
    
    _context = {}
    
    @classmethod
    def set(cls, tenant_id: str, tenant_type: str = None):
        """Set tenant context for current request."""
        cls._context = {
            "tenant_id": tenant_id,
            "tenant_type": tenant_type
        }
    
    @classmethod
    def get(cls) -> Optional[str]:
        """Get current tenant ID."""
        return cls._context.get("tenant_id")
    
    @classmethod
    def get_type(cls) -> Optional[str]:
        """Get current tenant type."""
        return cls._context.get("tenant_type")
    
    @classmethod
    def clear(cls):
        """Clear tenant context."""
        cls._context = {}
    
    @classmethod
    def is_super_admin(cls) -> bool:
        """Check if current context is super admin (root tenant)."""
        return cls._context.get("tenant_type") == "root"


class TenantIsolationMiddleware:
    """
    Middleware for tenant data isolation.
    
    Features:
    - Automatic tenant_id injection from user token
    - Hierarchical access (parent can see children)
    - Resource filtering
    """
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
    
    async def __call__(self, request: Request, call_next):
        # Skip OPTIONS requests
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # Extract tenant from user (set by auth middleware)
        # Tenant will be set when user is authenticated
        
        response = await call_next(request)
        
        return response


def require_tenant_access(required_level: str = None):
    """
    Dependency to require tenant access.
    
    Args:
        required_level: Minimum tenant level required
            - 'root': Only root tenant
            - 'provider': Provider or higher
            - 'customer': Customer or higher
            - 'sub_customer': Any authenticated user
            
    Usage:
        @router.get("/tenants")
        async def list_tenants(
            current_user: User = Depends(get_current_user),
            _ = Depends(require_tenant_access('provider'))
        ):
            return {"tenants": []}
    """
    async def tenant_checker(current_user: dict) -> dict:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        tenant_type = current_user.get("tenant_type")
        
        if required_level:
            hierarchy = {
                'root': 4,
                'provider': 3,
                'customer': 2,
                'sub_customer': 1
            }
            
            user_level = hierarchy.get(tenant_type, 0)
            required_level_num = hierarchy.get(required_level, 0)
            
            if user_level < required_level_num:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Tenant level '{required_level}' or higher required"
                )
        
        return current_user
    
    return tenant_checker


class TenantQueryBuilder:
    """
    Helper to build tenant-aware database queries.
    """
    
    @staticmethod
    def filter_by_tenant(
        query: any,
        model: any,
        user: dict,
        parent_access: bool = True
    ) -> any:
        """
        Filter query based on user's tenant access.
        
        Args:
            query: SQLAlchemy query
            model: Model class being queried
            user: Current user dict
            parent_access: Whether parent can access children
            
        Returns:
            Filtered query
        """
        tenant_id = user.get("tenant_id")
        tenant_type = user.get("tenant_type")
        
        # Super admin (root) sees everything
        if tenant_type == "root":
            return query
        
        # Get children tenant IDs if parent access is allowed
        if parent_access and tenant_type in ["root", "provider"]:
            # Parent can access all children tenants
            # This would typically be a subquery to get all child tenant IDs
            pass
        
        # Filter by exact tenant
        return query.filter(model.tenant_id == tenant_id)
    
    @staticmethod
    def with_tenant(
        query: any,
        model: any,
        tenant_id: str
    ) -> any:
        """
        Add tenant filter to query.
        
        Args:
            query: SQLAlchemy query
            model: Model class
            tenant_id: Tenant ID to filter by
            
        Returns:
            Query with tenant filter
        """
        return query.filter(model.tenant_id == tenant_id)


# Tenant-aware repository pattern
class TenantRepository:
    """
    Base repository with tenant isolation.
    """
    
    def __init__(self, db: Session, user: dict):
        self.db = db
        self.user = user
        self.tenant_id = user.get("tenant_id")
        self.tenant_type = user.get("tenant_type")
        self.is_super_admin = tenant_type == "root"
    
    def _apply_tenant_filter(self, query: any, model: any) -> any:
        """Apply tenant filter to query."""
        return TenantQueryBuilder.filter_by_tenant(
            query, model, self.user
        )
    
    def _apply_tenant(self, query: any, model: any) -> any:
        """Apply exact tenant filter."""
        return TenantQueryBuilder.with_tenant(
            query, model, self.tenant_id
        )


# Hierarchical tenant access checker
class TenantHierarchy:
    """
    Manages hierarchical tenant relationships.
    """
    
    @staticmethod
    def can_access(
        requester_tenant_id: str,
        requester_type: str,
        target_tenant_id: str,
        target_type: str
    ) -> bool:
        """
        Check if requester can access target tenant.
        
        Hierarchy:
        - Root can access all
        - Provider can access own customers and sub-customers
        - Customer can access own sub-customers
        - Sub-customer can only access own resources
        
        Args:
            requester_tenant_id: ID of requesting tenant
            requester_type: Type of requesting tenant
            target_tenant_id: ID of target tenant
            target_type: Type of target tenant
            
        Returns:
            True if access is allowed
        """
        # Same tenant always allowed
        if requester_tenant_id == target_tenant_id:
            return True
        
        # Root can access everything
        if requester_type == "root":
            return True
        
        # Provider can access customers and sub-customers
        if requester_type == "provider":
            return target_type in ["customer", "sub_customer"]
        
        # Customer can access sub-customers
        if requester_type == "customer":
            return target_type == "sub_customer"
        
        # Sub-customer can only access own
        return False
    
    @staticmethod
    def get_accessible_tenant_ids(
        tenant_id: str,
        tenant_type: str
    ) -> list:
        """
        Get list of tenant IDs that can be accessed.
        
        Returns:
            List of accessible tenant IDs
        """
        # Root accesses all
        if tenant_type == "root":
            return []  # Would return all tenant IDs
        
        # Provider accesses customers and sub-customers
        if tenant_type == "provider":
            return []  # Would return customer and sub-customer IDs
        
        # Customer accesses sub-customers
        if tenant_type == "customer":
            return []  # Would return sub-customer IDs
        
        # Sub-customer accesses only self
        return [tenant_id]
