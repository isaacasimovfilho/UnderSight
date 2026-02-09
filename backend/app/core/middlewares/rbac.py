"""
RBAC Middleware for UnderSight

Provides role-based access control for API endpoints.
"""

from typing import Callable, List, Optional
from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session


# Permission definitions
class Permissions:
    # Alerts permissions
    ALERTS_READ = "alerts:read"
    ALERTS_WRITE = "alerts:write"
    ALERTS_DELETE = "alerts:delete"
    
    # Cases permissions
    CASES_READ = "cases:read"
    CASES_WRITE = "cases:write"
    CASES_DELETE = "cases:delete"
    CASES_MANAGE = "cases:manage"
    
    # Assets permissions
    ASSETS_READ = "assets:read"
    ASSETS_WRITE = "assets:write"
    ASSETS_DELETE = "assets:delete"
    
    # Sensors permissions
    SENSORS_READ = "sensors:read"
    SENSORS_WRITE = "sensors:write"
    SENSORS_DELETE = "sensors:delete"
    
    # Inventory permissions
    INVENTORY_READ = "inventory:read"
    INVENTORY_WRITE = "inventory:write"
    INVENTORY_DELETE = "inventory:delete"
    INVENTORY_APPROVE = "inventory:approve"
    
    # Playbooks permissions
    PLAYBOOKS_READ = "playbooks:read"
    PLAYBOOKS_WRITE = "playbooks:write"
    PLAYBOOKS_EXECUTE = "playbooks:execute"
    
    # Users permissions
    USERS_READ = "users:read"
    USERS_WRITE = "users:write"
    
    # Roles permissions
    ROLES_READ = "roles:read"
    ROLES_WRITE = "roles:write"
    
    # Settings permissions
    SETTINGS_READ = "settings:read"
    SETTINGS_WRITE = "settings:write"
    
    # Integrations permissions
    INTEGRATIONS_READ = "integrations:read"
    INTEGRATIONS_WRITE = "integrations:write"
    
    # Webhooks permissions
    WEBHOOKS_READ = "webhooks:read"
    WEBHOOKS_WRITE = "webhooks:write"
    
    # API Keys permissions
    API_KEYS_READ = "api_keys:read"
    API_KEYS_WRITE = "api_keys:write"
    
    # Audit logs permissions
    AUDIT_LOGS_READ = "audit_logs:read"


# Role to permissions mapping
DEFAULT_ROLE_PERMISSIONS = {
    "admin": [
        Permissions.ALERTS_READ, Permissions.ALERTS_WRITE, Permissions.ALERTS_DELETE,
        Permissions.CASES_READ, Permissions.CASES_WRITE, Permissions.CASES_DELETE, Permissions.CASES_MANAGE,
        Permissions.ASSETS_READ, Permissions.ASSETS_WRITE, Permissions.ASSETS_DELETE,
        Permissions.SENSORS_READ, Permissions.SENSORS_WRITE, Permissions.SENSORS_DELETE,
        Permissions.INVENTORY_READ, Permissions.INVENTORY_WRITE, Permissions.INVENTORY_DELETE, Permissions.INVENTORY_APPROVE,
        Permissions.PLAYBOOKS_READ, Permissions.PLAYBOOKS_WRITE, Permissions.PLAYBOOKS_EXECUTE,
        Permissions.USERS_READ, Permissions.USERS_WRITE,
        Permissions.ROLES_READ, Permissions.ROLES_WRITE,
        Permissions.SETTINGS_READ, Permissions.SETTINGS_WRITE,
        Permissions.INTEGRATIONS_READ, Permissions.INTEGRATIONS_WRITE,
        Permissions.WEBHOOKS_READ, Permissions.WEBHOOKS_WRITE,
        Permissions.API_KEYS_READ, Permissions.API_KEYS_WRITE,
        Permissions.AUDIT_LOGS_READ,
    ],
    "analyst": [
        Permissions.ALERTS_READ, Permissions.ALERTS_WRITE,
        Permissions.CASES_READ, Permissions.CASES_WRITE,
        Permissions.ASSETS_READ,
        Permissions.SENSORS_READ,
        Permissions.INVENTORY_READ, Permissions.INVENTORY_WRITE, Permissions.INVENTORY_APPROVE,
        Permissions.PLAYBOOKS_READ, Permissions.PLAYBOOKS_EXECUTE,
        Permissions.USERS_READ,
    ],
    "viewer": [
        Permissions.ALERTS_READ,
        Permissions.CASES_READ,
        Permissions.ASSETS_READ,
        Permissions.SENSORS_READ,
        Permissions.INVENTORY_READ,
        Permissions.PLAYBOOKS_READ,
    ],
}


class RBACMiddleware:
    """
    Middleware for role-based access control.
    
    Usage:
        @app.get("/alerts", dependencies=[Depends(require_permission(Permissions.ALERTS_READ))])
    """
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
    
    async def __call__(self, request: Request, call_next):
        # Skip OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # Get token from header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return await call_next(request)
        
        # Token will be validated by the auth endpoint
        # This middleware is for annotation-based access control
        
        return await call_next(request)


def require_permission(permission: str):
    """
    Dependency to require a specific permission.
    
    Usage:
        from app.core.middlewares.rbac import require_permission, Permissions
        
        @router.get("/alerts")
        async def get_alerts(
            current_user: User = Depends(get_current_user),
            _ = Depends(require_permission(Permissions.ALERTS_READ))
        ):
            return {"alerts": []}
    """
    async def permission_checker(
        current_user: dict,
        db: Session = Depends(get_db)
    ) -> dict:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        user_permissions = current_user.get("permissions", [])
        
        # Admin has all permissions
        if current_user.get("role") == "admin":
            return current_user
        
        # Check permission
        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {permission} required"
            )
        
        return current_user
    
    return permission_checker


def require_any_permission(*permissions: str):
    """
    Dependency to require any of the specified permissions.
    
    Usage:
        from app.core.middlewares.rbac import require_any_permission, Permissions
        
        @router.get("/cases")
        async def get_cases(
            current_user: User = Depends(get_current_user),
            _ = Depends(require_any_permission(
                Permissions.CASES_READ,
                Permissions.CASES_MANAGE
            ))
        ):
            return {"cases": []}
    """
    async def permission_checker(
        current_user: dict,
        db: Session = Depends(get_db)
    ) -> dict:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        user_permissions = current_user.get("permissions", [])
        
        # Admin has all permissions
        if current_user.get("role") == "admin":
            return current_user
        
        # Check if user has any of the required permissions
        if not any(p in user_permissions for p in permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: one of {permissions} required"
            )
        
        return current_user
    
    return permission_checker


def require_all_permissions(*permissions: str):
    """
    Dependency to require all of the specified permissions.
    
    Usage:
        from app.core.middlewares.rbac import require_all_permissions, Permissions
        
        @router.delete("/alerts/{id}")
        async def delete_alert(
            alert_id: str,
            current_user: User = Depends(get_current_user),
            _ = Depends(require_all_permissions(
                Permissions.ALERTS_READ,
                Permissions.ALERTS_DELETE
            ))
        ):
            return {"status": "deleted"}
    """
    async def permission_checker(
        current_user: dict,
        db: Session = Depends(get_db)
    ) -> dict:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        user_permissions = current_user.get("permissions", [])
        
        # Admin has all permissions
        if current_user.get("role") == "admin":
            return current_user
        
        # Check if user has all required permissions
        if not all(p in user_permissions for p in permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: all of {permissions} required"
            )
        
        return current_user
    
    return permission_checker


# Resource-level access control
class ResourceAccessControl:
    """
    Helper class for resource-level access control.
    
    Ensures users can only access resources within their tenant.
    """
    
    @staticmethod
    def can_access_resource(
        user: dict,
        resource_tenant_id: str,
        permission: str
    ) -> bool:
        """
        Check if user can access a resource.
        
        Args:
            user: Current user dict with tenant_id
            resource_tenant_id: Tenant ID of the resource
            permission: Required permission
            
        Returns:
            True if access is allowed
        """
        # Super admin can access everything
        if user.get("is_super_admin"):
            return True
        
        # Check tenant access
        if str(user.get("tenant_id")) != str(resource_tenant_id):
            return False
        
        # Check permission
        user_permissions = user.get("permissions", [])
        if user.get("role") == "admin":
            return True
        
        return permission in user_permissions
    
    @staticmethod
    def filter_by_tenant(
        user: dict,
        query: any,
        resource_field: str = "tenant_id"
    ) -> any:
        """
        Filter a query to only include resources from user's tenant.
        
        Args:
            user: Current user dict
            query: SQLAlchemy query
            resource_field: Field name for tenant_id in the model
            
        Returns:
            Query filtered by tenant
        """
        # Super admin sees everything
        if user.get("is_super_admin"):
            return query
        
        # Filter by tenant
        return query.filter(
            getattr(query.column_descriptions[0]['entity'], resource_field) == user.get("tenant_id")
        )


# Audit logging for access attempts
class AccessAuditLogger:
    """
    Logs access attempts for security auditing.
    """
    
    @staticmethod
    async def log_attempt(
        db: Session,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: Optional[str],
        success: bool,
        details: Optional[dict] = None
    ):
        """
        Log an access attempt.
        """
        # TODO: Implement audit logging
        pass
