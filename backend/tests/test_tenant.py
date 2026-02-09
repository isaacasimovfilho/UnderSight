"""
Unit Tests for Tenant Isolation Middleware
"""

import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.core.middlewares.tenant import (
    TenantContext,
    TenantHierarchy,
    TenantQueryBuilder,
    TenantRepository,
    require_tenant_access
)


class TestTenantContext:
    """Test TenantContext class."""
    
    def setup_method(self):
        """Clear context before each test."""
        TenantContext.clear()
    
    def teardown_method(self):
        """Clear context after each test."""
        TenantContext.clear()
    
    def test_set_and_get_tenant(self):
        """Test setting and getting tenant ID."""
        TenantContext.set("tenant-123", "customer")
        
        assert TenantContext.get() == "tenant-123"
    
    def test_get_tenant_type(self):
        """Test getting tenant type."""
        TenantContext.set("tenant-123", "provider")
        
        assert TenantContext.get_type() == "provider"
    
    def test_clear_tenant(self):
        """Test clearing tenant context."""
        TenantContext.set("tenant-123", "customer")
        TenantContext.clear()
        
        assert TenantContext.get() is None
        assert TenantContext.get_type() is None
    
    def test_is_super_admin(self):
        """Test checking for super admin."""
        TenantContext.set("root-tenant", "root")
        assert TenantContext.is_super_admin() is True
        
        TenantContext.set("tenant-123", "customer")
        assert TenantContext.is_super_admin() is False
        
        TenantContext.set("tenant-456", "provider")
        assert TenantContext.is_super_admin() is False


class TestTenantHierarchy:
    """Test TenantHierarchy access control."""
    
    def test_same_tenant_access(self):
        """Same tenant should always have access."""
        assert TenantHierarchy.can_access(
            "tenant-123", "customer",
            "tenant-123", "customer"
        ) is True
    
    def test_root_access_all(self):
        """Root tenant can access everything."""
        assert TenantHierarchy.can_access(
            "root", "root",
            "tenant-123", "customer"
        ) is True
        
        assert TenantHierarchy.can_access(
            "root", "root",
            "tenant-456", "sub_customer"
        ) is True
    
    def test_provider_access(self):
        """Provider can access customers and sub-customers."""
        assert TenantHierarchy.can_access(
            "provider-1", "provider",
            "customer-1", "customer"
        ) is True
        
        assert TenantHierarchy.can_access(
            "provider-1", "provider",
            "sub-customer-1", "sub_customer"
        ) is True
        
        assert TenantHierarchy.can_access(
            "provider-1", "provider",
            "other-provider", "provider"
        ) is False
    
    def test_customer_access(self):
        """Customer can access sub-customers."""
        assert TenantHierarchy.can_access(
            "customer-1", "customer",
            "sub-customer-1", "sub_customer"
        ) is True
        
        assert TenantHierarchy.can_access(
            "customer-1", "customer",
            "other-customer", "customer"
        ) is False
        
        assert TenantHierarchy.can_access(
            "customer-1", "customer",
            "provider-1", "provider"
        ) is False
    
    def test_sub_customer_restricted(self):
        """Sub-customer can only access own resources."""
        assert TenantHierarchy.can_access(
            "sub-1", "sub_customer",
            "sub-1", "sub_customer"
        ) is True
        
        assert TenantHierarchy.can_access(
            "sub-1", "sub_customer",
            "sub-2", "sub_customer"
        ) is False
        
        assert TenantHierarchy.can_access(
            "sub-1", "sub_customer",
            "customer-1", "customer"
        ) is False


class TestTenantQueryBuilder:
    """Test TenantQueryBuilder class."""
    
    def test_root_sees_all(self):
        """Root tenant should see all data (no filter applied)."""
        user = {"tenant_id": "root", "tenant_type": "root"}
        mock_query = MagicMock()
        
        result = TenantQueryBuilder.filter_by_tenant(
            mock_query, MagicMock(), user
        )
        
        # Root should get same query without filter
        assert result == mock_query
    
    def test_customer_sees_own(self):
        """Customer should only see own data."""
        user = {"tenant_id": "customer-123", "tenant_type": "customer"}
        mock_model = MagicMock()
        mock_query = MagicMock()
        mock_query.filter = MagicMock(return_value=mock_query)
        
        TenantQueryBuilder.filter_by_tenant(
            mock_query, mock_model, user
        )
        
        # Should filter by tenant_id
        mock_query.filter.assert_called_once()
        call_args = mock_query.filter.call_args
        assert call_args[0][0].left.prop == mock_model.tenant_id
    
    def test_with_tenant(self):
        """Test with_tenant method."""
        mock_query = MagicMock()
        mock_model = MagicMock()
        mock_query.filter = MagicMock(return_value=mock_query)
        
        TenantQueryBuilder.with_tenant(
            mock_query, mock_model, "tenant-123"
        )
        
        mock_query.filter.assert_called_once()


class TestTenantRepository:
    """Test TenantRepository class."""
    
    def test_repository_init(self):
        """Test repository initialization."""
        user = {
            "tenant_id": "tenant-123",
            "tenant_type": "customer"
        }
        mock_db = MagicMock()
        
        repo = TenantRepository(mock_db, user)
        
        assert repo.tenant_id == "tenant-123"
        assert repo.tenant_type == "customer"
        assert repo.is_super_admin is False
    
    def test_repository_super_admin(self):
        """Test repository with super admin."""
        user = {
            "tenant_id": "root",
            "tenant_type": "root"
        }
        mock_db = MagicMock()
        
        repo = TenantRepository(mock_db, user)
        
        assert repo.is_super_admin is True


class TestRequireTenantAccess:
    """Test require_tenant_access dependency."""
    
    @pytest.mark.asyncio
    async def test_valid_tenant_level(self):
        """Test with valid tenant level."""
        user = {
            "id": "user-1",
            "tenant_type": "provider"
        }
        
        checker = require_tenant_access("provider")
        result = await checker(user)
        
        assert result == user
    
    @pytest.mark.asyncio
    async def test_insufficient_level(self):
        """Test with insufficient tenant level."""
        user = {
            "id": "user-1",
            "tenant_type": "customer"
        }
        
        checker = require_tenant_access("provider")
        
        with pytest.raises(HTTPException) as exc_info:
            await checker(user)
        
        assert exc_info.value.status_code == 403
        assert "provider" in exc_info.value.detail.lower()
    
    @pytest.mark.asyncio
    async def test_no_user(self):
        """Test with no user provided."""
        checker = require_tenant_access("provider")
        
        with pytest.raises(HTTPException) as exc_info:
            await checker(None)
        
        assert exc_info.value.status_code == 401
    
    @pytest.mark.asyncio
    async def test_root_access_all(self):
        """Test root can access any level."""
        user = {
            "id": "user-1",
            "tenant_type": "root"
        }
        
        checker = require_tenant_access("customer")
        result = await checker(user)
        
        assert result == user
    
    @pytest.mark.asyncio
    async def test_no_level_required(self):
        """Test when no specific level is required."""
        user = {
            "id": "user-1",
            "tenant_type": "sub_customer"
        }
        
        checker = require_tenant_access()
        result = await checker(user)
        
        assert result == user
