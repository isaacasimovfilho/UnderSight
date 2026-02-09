"""
Integration Services Base Module

Provides integration services for external tools:
- Slack: Send alerts and notifications
- Jira: Create and update tickets
- VirusTotal: Threat intelligence enrichment
- MISP: Threat intelligence platform

Each service can be configured via Settings page.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import json
import httpx


@dataclass
class IntegrationConfig:
    """Base configuration for integrations."""
    enabled: bool = False
    webhook_url: Optional[str] = None
    api_key: Optional[str] = None
    api_url: Optional[str] = None
    timeout_seconds: int = 30


@dataclass
class AlertData:
    """Alert data for integrations."""
    id: str
    title: str
    description: Optional[str] = None
    severity: str = "medium"
    status: str = "new"
    source: str = ""
    created_at: Optional[datetime] = None
    tags: List[str] = None
    metadata: Dict[str, Any] = None


class BaseIntegrationService(ABC):
    """Base class for integration services."""
    
    @abstractmethod
    async def send_alert(self, alert: AlertData) -> Dict[str, Any]:
        """Send an alert to the integration."""
        pass
    
    @abstractmethod
    async def test_connection(self) -> Dict[str, Any]:
        """Test the connection to the integration."""
        pass


class SlackService(BaseIntegrationService):
    """
    Slack Integration Service
    
    Configuration fields:
    - webhook_url: Slack webhook URL (required if not using API)
    - api_key: Slack Bot Token (for API-based sending)
    - channel: Default channel to send messages
    """
    
    def __init__(self, config: IntegrationConfig):
        self.config = config
    
    async def send_alert(self, alert: AlertData) -> Dict[str, Any]:
        """Send alert to Slack."""
        if not self.config.enabled:
            return {"success": False, "error": "Slack integration is disabled"}
        
        # Build Slack message
        severity_colors = {
            "critical": "#ff0000",
            "high": "#ff6600",
            "medium": "#ffcc00",
            "low": "#00cc00"
        }
        
        payload = {
            "attachments": [{
                "color": severity_colors.get(alert.severity, "#808080"),
                "title": f"🚨 {alert.title}",
                "text": alert.description or "No description",
                "fields": [
                    {"title": "Severity", "value": alert.severity.upper(), "short": True},
                    {"title": "Status", "value": alert.status.upper(), "short": True},
                    {"title": "Source", "value": alert.source or "Unknown", "short": True},
                    {"title": "Alert ID", "value": alert.id, "short": True},
                ],
                "footer": "UnderSight SIEM",
                "ts": int(alert.created_at.timestamp()) if alert.created_at else None
            }]
        }
        
        # Add tags if present
        if alert.tags:
            payload["attachments"][0]["fields"].append({
                "title": "Tags",
                "value": ", ".join(alert.tags),
                "short": False
            })
        
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
                if self.config.webhook_url:
                    response = await client.post(
                        self.config.webhook_url,
                        json=payload
                    )
                elif self.config.api_key:
                    # Use Slack API
                    response = await client.post(
                        "https://slack.com/api/chat.postMessage",
                        json={**payload, "token": self.config.api_key}
                    )
                else:
                    return {"success": False, "error": "No webhook URL or API key configured"}
                
                response.raise_for_status()
                return {"success": True, "response": response.json()}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Slack connection."""
        if not self.config.webhook_url and not self.config.api_key:
            return {"success": False, "error": "No webhook URL or API key configured"}
        
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
                # Simple test message
                test_payload = {"text": "UnderSight SIEM connection test"}
                
                if self.config.webhook_url:
                    response = await client.post(self.config.webhook_url, json=test_payload)
                else:
                    response = await client.post(
                        "https://slack.com/api/chat.postMessage",
                        json={**test_payload, "token": self.config.api_key}
                    )
                
                response.raise_for_status()
                return {"success": True, "message": "Slack connection successful"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}


class JiraService(BaseIntegrationService):
    """
    Jira Integration Service
    
    Configuration fields:
    - api_url: Jira instance URL (e.g., https://your-domain.atlassian.net)
    - api_key: Jira API token or password
    - project_key: Default project key (e.g., SEC)
    - issue_type: Default issue type (e.g., "Incident", "Task")
    """
    
    def __init__(self, config: IntegrationConfig):
        self.config = config
    
    async def send_alert(self, alert: AlertData) -> Dict[str, Any]:
        """Create Jira ticket from alert."""
        if not self.config.enabled:
            return {"success": False, "error": "Jira integration is disabled"}
        
        if not self.config.api_url or not self.config.api_key:
            return {"success": False, "error": "Jira URL or API key not configured"}
        
        # Build Jira issue
        issue_data = {
            "fields": {
                "project": {"key": getattr(self.config, "project_key", "SEC")},
                "summary": f"[{alert.severity.upper()}] {alert.title}",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [{
                        "type": "paragraph",
                        "content": [{
                            "type": "text",
                            "text": alert.description or "No description"
                        }]
                    }]
                },
                "issuetype": {"name": getattr(self.config, "issue_type", "Incident")}
            }
        }
        
        # Add labels
        if alert.tags:
            issue_data["fields"]["labels"] = alert.tags
        
        # Add custom fields if available
        if alert.metadata:
            issue_data["fields"].update(alert.metadata)
        
        try:
            async with httpx.AsyncClient(
                timeout=self.config.timeout_seconds,
                auth=(self.config.api_key.split("@")[0] if "@" in self.config.api_key else self.config.api_key, 
                self.config.api_key.split("@")[1] if "@" in self.config.api_key else ""
            ) as client:
                # Note: Actual auth depends on Jira setup
                headers = {"Content-Type": "application/json"}
                
                response = await client.post(
                    f"{self.config.api_url}/rest/api/3/issue",
                    json=issue_data,
                    headers=headers
                )
                
                response.raise_for_status()
                result = response.json()
                return {
                    "success": True,
                    "ticket_id": result.get("id"),
                    "ticket_key": result.get("key")
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Jira connection."""
        if not self.config.api_url or not self.config.api_key:
            return {"success": False, "error": "Jira URL or API key not configured"}
        
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
                response = await client.get(
                    f"{self.config.api_url}/rest/api/3/myself"
                )
                response.raise_for_status()
                return {"success": True, "message": "Jira connection successful"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}


class VirusTotalService(BaseIntegrationService):
    """
    VirusTotal Integration Service
    
    Configuration fields:
    - api_url: https://www.virustotal.com/api/v3
    - api_key: VirusTotal API key
    """
    
    def __init__(self, config: IntegrationConfig):
        self.config = config
    
    async def send_alert(self, alert: AlertData) -> Dict[str, Any]:
        """Enrich alert with VirusTotal data."""
        if not self.config.enabled:
            return {"success": False, "error": "VirusTotal integration is disabled"}
        
        if not self.config.api_key:
            return {"success": False, "error": "VirusTotal API key not configured"}
        
        # Extract IP or domain from alert
        ioc_value = None
        ioc_type = None
        
        if alert.metadata:
            if "source_ip" in alert.metadata:
                ioc_value = alert.metadata["source_ip"]
                ioc_type = "ip_address"
            elif "destination_ip" in alert.metadata:
                ioc_value = alert.metadata["destination_ip"]
                ioc_type = "ip_address"
            elif "domain" in alert.metadata:
                ioc_value = alert.metadata["domain"]
                ioc_type = "domain"
            elif "hash" in alert.metadata:
                ioc_value = alert.metadata["hash"]
                ioc_type = "file"
        
        if not ioc_value:
            return {"success": False, "error": "No IoC found in alert"}
        
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
                headers = {"x-apikey": self.config.api_key}
                
                # Query based on IoC type
                if ioc_type == "ip_address":
                    response = await client.get(
                        f"https://www.virustotal.com/api/v3/ip_addresses/{ioc_value}",
                        headers=headers
                    )
                elif ioc_type == "domain":
                    response = await client.get(
                        f"https://www.virustotal.com/api/v3/domains/{ioc_value}",
                        headers=headers
                    )
                elif ioc_type == "file":
                    response = await client.get(
                        f"https://www.virustotal.com/api/v3/files/{ioc_value}",
                        headers=headers
                    )
                else:
                    return {"success": False, "error": f"Unsupported IoC type: {ioc_type}"}
                
                if response.status_code == 404:
                    return {"success": False, "error": "No VirusTotal data found"}
                
                response.raise_for_status()
                data = response.json()
                
                return {
                    "success": True,
                    "data": data.get("data", {})
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test VirusTotal connection."""
        if not self.config.api_key:
            return {"success": False, "error": "VirusTotal API key not configured"}
        
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
                headers = {"x-apikey": self.config.api_key}
                
                # Test with a known IP
                response = await client.get(
                    "https://www.virustotal.com/api/v3/ip_addresses/8.8.8.8",
                    headers=headers
                )
                
                if response.status_code == 403:
                    return {"success": False, "error": "API key invalid or no permission"}
                
                response.raise_for_status()
                return {"success": True, "message": "VirusTotal connection successful"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}


class MISPService(BaseIntegrationService):
    """
    MISP (Malware Information Sharing Platform) Integration Service
    
    Configuration fields:
    - api_url: MISP instance URL
    - api_key: MISP API key
    - verify_ssl: Whether to verify SSL certificates
    """
    
    def __init__(self, config: IntegrationConfig):
        self.config = config
    
    async def send_alert(self, alert: AlertData) -> Dict[str, Any]:
        """Create MISP event from alert."""
        if not self.config.enabled:
            return {"success": False, "error": "MISP integration is disabled"}
        
        if not self.config.api_url or not self.config.api_key:
            return {"success": False, "error": "MISP URL or API key not configured"}
        
        # Build MISP event
        event_data = {
            "Event": {
                "info": f"[{alert.severity.upper()}] {alert.title}",
                "description": alert.description or "",
                "threat_level_id": {
                    "critical": 1,
                    "high": 2,
                    "medium": 3,
                    "low": 4
                }.get(alert.severity, 4),
                "distribution": 0,  # Your organization only
                "analysis": 0  # Initial
            }
        }
        
        # Add attributes
        attributes = []
        
        if alert.metadata:
            if "source_ip" in alert.metadata:
                attributes.append({
                    "type": "ip-src",
                    "value": alert.metadata["source_ip"]
                })
            if "destination_ip" in alert.metadata:
                attributes.append({
                    "type": "ip-dst",
                    "value": alert.metadata["destination_ip"]
                })
            if "domain" in alert.metadata:
                attributes.append({
                    "type": "domain",
                    "value": alert.metadata["domain"]
                })
            if "hash" in alert.metadata:
                attributes.append({
                    "type": "hash-md5",
                    "value": alert.metadata["hash"]
                })
        
        if attributes:
            event_data["Event"]["Attribute"] = attributes
        
        try:
            async with httpx.AsyncClient(
                timeout=self.config.timeout_seconds,
                verify=getattr(self.config, "verify_ssl", True)
            ) as client:
                headers = {
                    "Authorization": self.config.api_key,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
                
                response = await client.post(
                    f"{self.config.api_url}/events/add",
                    json=event_data,
                    headers=headers
                )
                
                response.raise_for_status()
                data = response.json()
                
                return {
                    "success": True,
                    "event_id": data.get("Event", {}).get("id")
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test MISP connection."""
        if not self.config.api_url or not self.config.api_key:
            return {"success": False, "error": "MISP URL or API key not configured"}
        
        try:
            async with httpx.AsyncClient(
                timeout=self.config.timeout_seconds,
                verify=getattr(self.config, "verify_ssl", True)
            ) as client:
                headers = {
                    "Authorization": self.config.api_key,
                    "Accept": "application/json"
                }
                
                response = await client.get(
                    f"{self.config.api_url}/users/view",
                    headers=headers
                )
                
                if response.status_code == 401:
                    return {"success": False, "error": "Invalid API key"}
                
                response.raise_for_status()
                return {"success": True, "message": "MISP connection successful"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}


# Integration Manager
class IntegrationManager:
    """
    Manager for all integration services.
    """
    
    def __init__(self):
        self.slack: Optional[SlackService] = None
        self.jira: Optional[JiraService] = None
        self.virustotal: Optional[VirusTotalService] = None
        self.misp: Optional[MISPService] = None
    
    def configure(
        self,
        service: str,
        config: IntegrationConfig
    ):
        """Configure an integration service."""
        if service == "slack":
            self.slack = SlackService(config)
        elif service == "jira":
            self.jira = JiraService(config)
        elif service == "virustotal":
            self.virustotal = VirusTotalService(config)
        elif service == "misp":
            self.misp = MISPService(config)
    
    async def send_alert_all(
        self,
        alert: AlertData
    ) -> Dict[str, Any]:
        """Send alert to all enabled integrations."""
        results = {}
        
        if self.slack:
            results["slack"] = await self.slack.send_alert(alert)
        
        if self.jira:
            results["jira"] = await self.jira.send_alert(alert)
        
        if self.virustotal:
            results["virustotal"] = await self.virustotal.send_alert(alert)
        
        if self.misp:
            results["misp"] = await self.misp.send_alert(alert)
        
        return results
