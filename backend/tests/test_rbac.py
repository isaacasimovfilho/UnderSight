"""
Unit Tests for RBAC Middleware
"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from app.core.middlewares.rbac import (
    Permissions,
    DEFAULT_ROLE_PERMISSIONS,
    require_permission,
    require_any_permission,
    require_all_permissions,
    ResourceAccessControl,
    AccessAuditLogger
)


class TestPermissions:
    """Test Permissions class."""
    
    def test_all_permissions_defined(self):
        """Verify all resource permissions are defined."""
        assert hasattr(Permissions, 'ALERTS_READ')
        assert hasattr(Permissions, 'ALERTS_WRITE')
        assert hasattr(Permissions, 'ALERTS_DELETE')
        assert hasattr(Permissions, 'CASES_READ')
        assert hasattr(Permissions, 'CASES_WRITE')
        assert hasattr(Permissions, 'ASSETS_READ')
        assert hasattr(Permissions, 'ASSETS_WRITE')
        assert hasattr(Permissions, 'INVENTORY_READ')
        assert hasattr(Permissions, 'INVENTORY_WRITE')
        assert hasattr(Permissions, 'SETTINGS_READ')
        assert hasattr(Permissions, 'SETTINGS_WRITE')
    
    def test_permission_format(self):
        """Verify permissions follow resource:action format."""
        assert Permissions.ALERTS_READ == "alerts:read"
        assert Permissions.ALERTS_WRITE == "alerts:write"
        assert Permissions.CASES_READ == "cases:read"
        assert Permissions.USERS_READ == "users:read"


class TestDefaultRolePermissions:
    """Test default role permissions mapping."""
    
    def test_admin_has_all_permissions(self):
        """Admin role should have all permissions."""
        admin_perms = DEFAULT_ROLE_PERMISSIONS.get("admin", [])
        assert "alerts:read" in admin_perms
        assert "alerts:write" in admin_perms
        assert "alerts:delete" in admin_perms
        assert "cases:read" in admin_perms
        assert "cases:write" in admin_perms
        assert "settings:write" in admin_perms
    
    def test_analyst_permissions(self):
        """Analyst role should have read/write but not delete or settings."""
        analyst_perms = DEFAULT_ROLE_PERMISSIONS.get("analyst", [])
        assert "alerts:read" in analyst_perms
        assert "alerts:write" in analyst_perms
        assert "alerts:delete" not in analyst_perms
        assert "settings:write" not in analyst_perms
    
    def test_viewer_permissions(self):
        """Viewer role should have read-only permissions."""
        viewer_perms = DEFAULT_ROLE_PERMISSIONS.get("viewer", [])
        assert "alerts:read" in viewer_perms
        assert "alerts:write" not in viewer_perms
        assert "cases:read" in viewer_perms
        assert "settings:read" not in viewer_perms


class TestRequirePermission:
    """Test require_permission dependency."""
    
    @pytest.mark.asyncio
    async def test_permission_granted(self):
        """Test when user has required permission."""
        user = {
            "id": "user-1",
            "permissions": ["alerts:read", "cases:write"]
        }
        
        checker = require_permission(Permissions.ALERTS_READ)
        result = await checker(user)
        
        assert result == user
    
    @pytest.mark.asyncio
    async def test_permission_denied(self):
        """Test when user lacks required permission."""
        user = {
            "id": "user-1",
            "permissions": ["alerts:read"]  # Missing alerts:write
        }
        
        checker = require_permission(Permissions.ALERTS_WRITE)
        
        with pytest.raises(HTTPException) as exc_info:
            await checker(user)
        
        assert exc_info.value.status_code == 403
        assert "Permission denied" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_no_user(self):
        """Test when no user is provided."""
        checker = require_permission(Permissions.ALERTS_READ)
        
        with pytest.raises(HTTPException) as exc_info:
            await checker(None)
        
        assert exc_info.value.status_code == 401


class TestRequireAnyPermission:
    """Test require_any_permission dependency."""
    
    @pytest.mark.asyncio
    async def test_any_permission_granted(self):
        """Test when user has at least one required permission."""
        user = {
            "id": "user-1",
            "permissions": ["alerts:read", "cases:write"]
        }
        
        checker = require_any_permission(
            Permissions.ALERTS_READ,
            Permissions.INVENTORY_WRITE
        )
        result = await checker(user)
        
        assert result == user
    
    @pytest.mark.asyncio
    async def test_all_permissions_denied(self):
        """Test when user has none of required permissions."""
        user = {
            "id": "user-1",
            "permissions": ["alerts:read"]  # Missing both required
        }
        
        checker = require_any_permission(
            Permissions.INVENTORY_WRITE,
            Permissions.SETTINGS_WRITE
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await checker(user)
        
        assert exc_info.value.status_code == 403


class TestRequireAllPermissions:
    """Test require_all_permissions dependency."""
    
    @pytest.mark.asyncio
    async def test_all_permissions_granted(self):
        """Test when user has all required permissions."""
        user = {
            "id": "user-1",
            "permissions": ["alerts:read", "cases:write", "settings:read"]
        }
        
        checker = require_all_permissions(
            Permissions.ALERTS_READ,
            Permissions.CASES_WRITE
        )
        result = await checker(user)
        
        assert result == user
    
    @pytest.mark.asyncio
    async def test_missing_one_permission(self):
        """Test when user is missing one permission."""
        user = {
            "id": "user-1",
            "permissions": ["alerts:read"]  # Missing cases:write
        }
        
        checker = require_all_permissions(
            Permissions.ALERTS_READ,
            Permissions.CASES_WRITE
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await checker(user)
        
        assert exc_info.value.status_code == 403


class TestResourceAccessControl:
    """Test ResourceAccessControl helper class."""
    
    def test_check_own_resource(self):
        """User should always have access to own resources."""
        user = {"id": "user-123", "tenant_type": "customer"}
        resource = {"owner_id": "user-123", "tenant_id": "tenant-123"}
        
        has_access = ResourceAccessControl.check_resource_access(
            user, resource, "own"
        )
        assert has_access is True
    
    def test_tenant_access(self):
        """User should access resources in same tenant."""
        user = {"id": "user-123", "tenant_id": "tenant-123"}
        resource = {"tenant_id": "tenant-123", "owner_id": "other-user"}
        
        has_access = ResourceAccessControl.check_resource_access(
            user, resource, "tenant"
        )
        assert has_access is True
    
    def test_different_tenant_denied(self):
        """User should not access resources in different tenant."""
        user = {"id": "user-123", "tenant_id": "tenant-456"}
        resource = {"tenant_id": "tenant-123"}
        
        has_access = ResourceAccessControl.check_resource_access(
            user, resource, "tenant"
        )
        assert has_access is False
    
    def test_public_resource(self):
        """Public resources should be accessible to all."""
        user = {"id": "user-123"}
        resource = {"visibility": "public"}
        
        has_access = ResourceAccessControl.check_resource_access(
            user, resource, "public"
        )
        assert has_access is True


class TestAccessAuditLogger:
    """Test AccessAuditLogger class."""
    
    def test_log_access_event(self):
        """Test logging an access event."""
        logger = AccessAuditLogger()
        
        # Should not raise exception
        logger.log_access(
            user_id="user-123",
            action="read",
            resource="alerts",
            resource_id="alert-001",
            result="granted"
        )
    
    def test_log_access_with_details(self):
        """Test logging with additional details."""
        logger = AccessAuditLogger()
        
        logger.log_access(
            user_id="user-123",
            action="delete",
            resource="cases",
            resource_id="case-001",
            result="denied",
            reason="Insufficient permissions",
            ip_address="192.168.1.100"
        )
