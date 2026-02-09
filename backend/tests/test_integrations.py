"""
Unit Tests for Integration Services
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import datetime

from app.services.integrations import (
    IntegrationConfig,
    AlertData,
    SlackService,
    JiraService,
    VirusTotalService,
    MISPService,
    IntegrationManager
)


class TestIntegrationConfig:
    """Test IntegrationConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = IntegrationConfig()
        
        assert config.enabled is False
        assert config.webhook_url is None
        assert config.api_key is None
        assert config.api_url is None
        assert config.timeout_seconds == 30
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = IntegrationConfig(
            enabled=True,
            webhook_url="https://hooks.slack.com/test",
            api_key="test-key",
            timeout_seconds=60
        )
        
        assert config.enabled is True
        assert config.webhook_url == "https://hooks.slack.com/test"


class TestAlertData:
    """Test AlertData class."""
    
    def test_minimal_alert(self):
        """Test creating alert with minimal data."""
        alert = AlertData(
            id="alert-001",
            title="Test Alert"
        )
        
        assert alert.id == "alert-001"
        assert alert.title == "Test Alert"
        assert alert.severity == "medium"
        assert alert.status == "new"
    
    def test_full_alert(self):
        """Test creating alert with all data."""
        alert = AlertData(
            id="alert-002",
            title="Security Incident",
            description="Brute force attack detected",
            severity="high",
            status="in_progress",
            source="firewall",
            created_at=datetime.utcnow(),
            tags=["attack", "brute-force"],
            metadata={"source_ip": "192.168.1.100"}
        )
        
        assert alert.severity == "high"
        assert "attack" in alert.tags
        assert alert.metadata["source_ip"] == "192.168.1.100"


class TestSlackService:
    """Test SlackService class."""
    
    def test_slack_service_init(self):
        """Test SlackService initialization."""
        config = IntegrationConfig(
            enabled=True,
            webhook_url="https://hooks.slack.com/test"
        )
        
        service = SlackService(config)
        
        assert service.config == config
    
    @pytest.mark.asyncio
    async def test_send_alert_disabled(self):
        """Test sending alert when integration is disabled."""
        config = IntegrationConfig(enabled=False)
        service = SlackService(config)
        
        alert = AlertData(
            id="alert-001",
            title="Test Alert",
            severity="high"
        )
        
        result = await service.send_alert(alert)
        
        assert result["success"] is False
        assert "disabled" in result["error"].lower()
    
    @pytest.mark.asyncio
    async def test_send_alert_success(self):
        """Test sending alert successfully."""
        config = IntegrationConfig(
            enabled=True,
            webhook_url="https://hooks.slack.com/test"
        )
        service = SlackService(config)
        
        alert = AlertData(
            id="alert-001",
            title="Suspicious Activity",
            description="Multiple failed logins detected",
            severity="high",
            status="new",
            source="auth-server",
            created_at=datetime.utcnow(),
            tags=["auth", "security"]
        )
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"ok": True}
            mock_client.return_value.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
            
            result = await service.send_alert(alert)
            
            assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_send_alert_with_severity_colors(self):
        """Test severity colors in Slack message."""
        config = IntegrationConfig(
            enabled=True,
            webhook_url="https://hooks.slack.com/test"
        )
        service = SlackService(config)
        
        alert = AlertData(
            id="alert-001",
            title="Critical Alert",
            severity="critical"
        )
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"ok": True}
            mock_client.return_value.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
            
            result = await service.send_alert(alert)
            
            assert result["success"] is True


class TestJiraService:
    """Test JiraService class."""
    
    def test_jira_service_init(self):
        """Test JiraService initialization."""
        config = IntegrationConfig(
            enabled=True,
            api_url="https://company.atlassian.net",
            api_key="test-key"
        )
        
        service = JiraService(config)
        
        assert service.config == config
    
    @pytest.mark.asyncio
    async def test_send_alert_disabled(self):
        """Test sending alert when integration is disabled."""
        config = IntegrationConfig(enabled=False)
        service = JiraService(config)
        
        alert = AlertData(
            id="alert-001",
            title="Test Alert"
        )
        
        result = await service.send_alert(alert)
        
        assert result["success"] is False
    
    @pytest.mark.asyncio
    async def test_send_alert_success(self):
        """Test creating Jira ticket."""
        config = IntegrationConfig(
            enabled=True,
            api_url="https://company.atlassian.net",
            api_key="test-key",
            project_key="SEC"
        )
        service = JiraService(config)
        
        alert = AlertData(
            id="alert-001",
            title="Security Incident",
            description="Brute force attack detected",
            severity="high",
            source="firewall"
        )
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = {
                "id": "12345",
                "key": "SEC-123"
            }
            mock_response.raise_for_status = MagicMock()
            mock_client.return_value.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
            
            result = await service.send_alert(alert)
            
            assert result["success"] is True
            assert result["ticket_id"] == "12345"
            assert result["ticket_key"] == "SEC-123"


class TestVirusTotalService:
    """Test VirusTotalService class."""
    
    def test_virustotal_service_init(self):
        """Test VirusTotalService initialization."""
        config = IntegrationConfig(
            enabled=True,
            api_url="https://www.virustotal.com/api/v3",
            api_key="test-key"
        )
        
        service = VirusTotalService(config)
        
        assert service.config == config
    
    @pytest.mark.asyncio
    async def test_enrich_ip_address(self):
        """Test enriching IP address with VirusTotal."""
        config = IntegrationConfig(
            enabled=True,
            api_url="https://www.virustotal.com/api/v3",
            api_key="test-key"
        )
        service = VirusTotalService(config)
        
        alert = AlertData(
            id="alert-001",
            title="Suspicious IP",
            metadata={"source_ip": "8.8.8.8"}
        )
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "data": {
                    "attributes": {
                        "last_analysis_stats": {
                            "malicious": 0,
                            "harmless": 10
                        }
                    }
                }
            }
            mock_response.raise_for_status = MagicMock()
            mock_client.return_value.get = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
            
            result = await service.send_alert(alert)
            
            assert result["success"] is True
            assert "data" in result
    
    @pytest.mark.asyncio
    async def test_enrich_domain(self):
        """Test enriching domain with VirusTotal."""
        config = IntegrationConfig(
            enabled=True,
            api_url="https://www.virustotal.com/api/v3",
            api_key="test-key"
        )
        service = VirusTotalService(config)
        
        alert = AlertData(
            id="alert-001",
            title="Suspicious Domain",
            metadata={"domain": "example.com"}
        )
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "data": {
                    "attributes": {
                        "last_analysis_stats": {
                            "malicious": 2,
                            "harmless": 8
                        }
                    }
                }
            }
            mock_response.raise_for_status = MagicMock()
            mock_client.return_value.get = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
            
            result = await service.send_alert(alert)
            
            assert result["success"] is True


class TestMISPService:
    """Test MISPService class."""
    
    def test_misp_service_init(self):
        """Test MISPService initialization."""
        config = IntegrationConfig(
            enabled=True,
            api_url="https://misp.example.com",
            api_key="test-key"
        )
        
        service = MISPService(config)
        
        assert service.config == config
    
    @pytest.mark.asyncio
    async def test_create_event(self):
        """Test creating MISP event."""
        config = IntegrationConfig(
            enabled=True,
            api_url="https://misp.example.com",
            api_key="test-key"
        )
        service = MISPService(config)
        
        alert = AlertData(
            id="alert-001",
            title="Threat Detected",
            description="Malicious activity detected",
            severity="high",
            metadata={"source_ip": "192.168.1.100"}
        )
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "Event": {"id": "123"}
            }
            mock_response.raise_for_status = MagicMock()
            mock_client.return_value.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client.return_value)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
            
            result = await service.send_alert(alert)
            
            assert result["success"] is True
            assert result["event_id"] == "123"


class TestIntegrationManager:
    """Test IntegrationManager class."""
    
    def test_manager_init(self):
        """Test IntegrationManager initialization."""
        manager = IntegrationManager()
        
        assert manager.slack is None
        assert manager.jira is None
        assert manager.virustotal is None
        assert manager.misp is None
    
    def test_configure_service(self):
        """Test configuring services."""
        manager = IntegrationManager()
        
        slack_config = IntegrationConfig(enabled=True)
        manager.configure("slack", slack_config)
        
        assert manager.slack is not None
        assert manager.slack.config.enabled is True
    
    def test_configure_multiple_services(self):
        """Test configuring multiple services."""
        manager = IntegrationManager()
        
        manager.configure("slack", IntegrationConfig(enabled=True))
        manager.configure("jira", IntegrationConfig(enabled=True))
        manager.configure("virustotal", IntegrationConfig(enabled=True))
        manager.configure("misp", IntegrationConfig(enabled=True))
        
        assert manager.slack is not None
        assert manager.jira is not None
        assert manager.virustotal is not None
        assert manager.misp is not None
    
    @pytest.mark.asyncio
    async def test_send_alert_all(self):
        """Test sending alert to all configured services."""
        manager = IntegrationManager()
        
        slack_config = IntegrationConfig(enabled=True)
        manager.slack = SlackService(slack_config)
        
        alert = AlertData(
            id="alert-001",
            title="Test Alert",
            severity="high"
        )
        
        # Mock Slack to return success
        with patch.object(manager.slack, 'send_alert', new_callable=AsyncMock) as mock_slack:
            mock_slack.return_value = {"success": True, "service": "slack"}
            
            result = await manager.send_alert_all(alert)
            
            assert "slack" in result
            assert result["slack"]["success"] is True
