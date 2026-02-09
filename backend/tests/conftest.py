"""
Pytest Configuration and Fixtures for UnderSight Tests
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import datetime, timedelta
from typing import Generator

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_db_session():
    """Mock database session."""
    session = MagicMock()
    session.add = MagicMock()
    session.commit = MagicMock()
    session.rollback = MagicMock()
    session.close = MagicMock()
    session.query = MagicMock()
    return session


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    redis = MagicMock()
    redis.get = MagicMock(return_value=None)
    redis.set = MagicMock()
    redis.delete = MagicMock()
    return redis


@pytest.fixture
def mock_current_user():
    """Mock current authenticated user."""
    return {
        "id": "user-123",
        "username": "testuser",
        "email": "test@example.com",
        "tenant_id": "tenant-123",
        "tenant_type": "customer",
        "role": "admin",
        "permissions": [
            "alerts:read", "alerts:write",
            "cases:read", "cases:write",
            "assets:read", "assets:write"
        ]
    }


@pytest.fixture
def mock_admin_user(mock_current_user):
    """Mock admin user with all permissions."""
    return {
        **mock_current_user,
        "role": "admin",
        "tenant_type": "provider",
        "permissions": [
            "alerts:read", "alerts:write", "alerts:delete",
            "cases:read", "cases:write", "cases:delete",
            "assets:read", "assets:write", "assets:delete",
            "users:read", "users:write",
            "settings:read", "settings:write",
            "inventory:read", "inventory:write"
        ]
    }


@pytest.fixture
def mock_viewer_user(mock_current_user):
    """Mock viewer user with read-only permissions."""
    return {
        **mock_current_user,
        "role": "viewer",
        "permissions": [
            "alerts:read",
            "cases:read",
            "assets:read"
        ]
    }


@pytest.fixture
def sample_alert_data():
    """Sample alert data for testing."""
    return {
        "id": "alert-001",
        "title": "Suspicious Login Attempt",
        "description": "Multiple failed login attempts detected from IP 192.168.1.100",
        "severity": "high",
        "status": "new",
        "source": "firewall",
        "created_at": datetime.utcnow().isoformat(),
        "tags": ["login", "brute-force"],
        "metadata": {
            "source_ip": "192.168.1.100",
            "destination_ip": "10.0.0.5",
            "attempt_count": 5
        }
    }


@pytest.fixture
def sample_inventory_item():
    """Sample inventory item for testing."""
    return {
        "id": "inv-001",
        "name": "AWS EC2 Instance",
        "type": "server",
        "source": "aws_inventory",
        "status": "pending",
        "data": {
            "instance_id": "i-1234567890abcdef0",
            "region": "us-east-1",
            "instance_type": "t3.medium",
            "tags": {"Environment": "production"}
        },
        "ai_decision": None,
        "ai_confidence": None,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }


@pytest.fixture
def sample_jwt_payload():
    """Sample JWT payload for testing."""
    return {
        "sub": "user-123",
        "username": "testuser",
        "email": "test@example.com",
        "tenant_id": "tenant-123",
        "tenant_type": "customer",
        "role": "admin",
        "permissions": ["alerts:read", "alerts:write"],
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }


@pytest.fixture
def mock_settings_config():
    """Mock settings configuration."""
    return {
        "language": "en",
        "theme": "dark",
        "timezone": "UTC",
        "notifications": {
            "email": True,
            "slack": False,
            "jira": True
        },
        "integrations": {
            "slack": {
                "webhook_url": "https://hooks.slack.com/test",
                "enabled": True
            },
            "jira": {
                "api_url": "https://company.atlassian.net",
                "api_key": "test-key",
                "project_key": "SEC",
                "enabled": True
            }
        }
    }


@pytest.fixture
def async_client():
    """Create async HTTP client for API testing."""
    import httpx
    return httpx.AsyncClient(timeout=30.0)


class MockResponse:
    """Mock HTTP response."""
    
    def __init__(self, status_code: int = 200, json_data: dict = None, text: str = ""):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text
    
    def json(self):
        return self._json_data
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


def create_mock_success_response(data: dict = None) -> MockResponse:
    """Create a successful mock response."""
    return MockResponse(status_code=200, json_data={"success": True, "data": data})


def create_mock_error_response(status_code: int = 400, error: str = "Error") -> MockResponse:
    """Create an error mock response."""
    return MockResponse(status_code=status_code, json_data={"success": False, "error": error})
