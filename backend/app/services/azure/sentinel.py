"""
Microsoft Sentinel / Azure Monitor Integration Service
Fetches security events from Azure Log Analytics / Microsoft Sentinel
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class AzureCredential:
    """Azure credentials for Sentinel integration"""
    tenant_id: str
    client_id: str
    client_secret: str
    subscription_id: str
    workspace_name: str = "sentinel-workspace"


@dataclass
class SentinelEvent:
    """Sentinel/Log Analytics event"""
    timestamp: datetime
    event_type: str
    severity: str
    title: str
    description: str
    source_ip: Optional[str]
    destination_ip: Optional[str]
    user: Optional[str]
    computer: Optional[str]
    raw_data: Dict[str, Any]


class AzureSentinelService:
    """
    Service to fetch events from Microsoft Sentinel via Log Analytics API
    """
    
    def __init__(self, credentials: Optional[AzureCredential] = None):
        if credentials:
            self.credentials = credentials
        else:
            # Load from environment or use defaults for development
            self.credentials = AzureCredential(
                tenant_id=os.getenv('AZURE_TENANT_ID', ''),
                client_id=os.getenv('AZURE_CLIENT_ID', ''),
                client_secret=os.getenv('AZURE_CLIENT_SECRET', ''),
                subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID', ''),
                workspace_name=os.getenv('AZURE_WORKSPACE_NAME', 'sentinel-workspace')
            )
        
        self.access_token: Optional[str] = None
        self.token_expires: float = 0
        self.base_url = "https://management.azure.com"
        self.log_analytics_url = f"https://api.loganalytics.azure.com/v1/workspaces"
        
    def _get_access_token(self) -> Optional[str]:
        """Get Azure AD access token"""
        # Check if token is still valid
        if self.access_token and time.time() < self.token_expires - 60:
            return self.access_token
        
        if not all([self.credentials.tenant_id, self.credentials.client_id, self.credentials.client_secret]):
            logger.warning("Azure credentials not configured")
            return None
        
        try:
            url = f"https://login.microsoftonline.com/{self.credentials.tenant_id}/oauth2/v2.0/token"
            
            data = {
                "client_id": self.credentials.client_id,
                "client_secret": self.credentials.client_secret,
                "scope": "https://management.azure.com/.default",
                "grant_type": "client_credentials"
            }
            
            response = requests.post(url, data=data, timeout=30)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                self.token_expires = time.time() + token_data.get("expires_in", 3600) - 60
                logger.info("✅ Azure access token obtained")
                return self.access_token
            else:
                logger.error(f"❌ Failed to get access token: {response.status_code} - {response.text[:200]}")
                return None
        except Exception as e:
            logger.error(f"❌ Error getting access token: {e}")
            return None
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        token = self._get_access_token()
        if not token:
            return {}
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def query_logs(self, query: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Execute a Log Analytics query"""
        headers = self._get_headers()
        if not headers:
            return []
        
        try:
            # Calculate time range
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=hours)
            
            url = (
                f"{self.log_analytics_url}/"
                f"{self.credentials.subscription_id}/"
                f"resourceGroups/providers/Microsoft.OperationalInsights/"
                f"workspaces/{self.credentials.workspace_name}/"
                f"query"
            )
            
            params = {
                "api-version": "2022-01-01"
            }
            
            body = {
                "query": query,
                "timespan": f"{start_time.isoformat()}Z/{end_time.isoformat()}Z"
            }
            
            response = requests.post(
                url,
                headers=headers,
                params=params,
                json=body,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                rows = data.get("results", [])
                logger.info(f"✅ Query returned {len(rows)} results")
                return rows
            else:
                logger.error(f"❌ Query failed: {response.status_code} - {response.text[:200]}")
                return []
        except Exception as e:
            logger.error(f"❌ Error executing query: {e}")
            return []
    
    def get_security_events(self, hours: int = 24) -> List[SentinelEvent]:
        """Fetch security events from Sentinel"""
        # KQL query for security events
        query = """
        SecurityEvent
        | where TimeGenerated > ago(24h)
        | where EventID in (4625, 4648, 4672, 4674, 4688, 4689, 4697, 4703, 4719, 4720, 4722, 4724, 4728, 4732, 4735, 4742, 4755, 4756, 4767, 4768, 4769, 4771, 4776, 4964)
        | project TimeGenerated, EventID, Account, Computer, SourceIP, SeverityLevel, Activity, ExtendedProperties
        | order by TimeGenerated desc
        """
        
        rows = self.query_logs(query, hours)
        events = []
        
        for row in rows:
            try:
                event = SentinelEvent(
                    timestamp=row.get("TimeGenerated", datetime.utcnow().isoformat()),
                    event_type=f"SecurityEvent_{row.get('EventID', 'Unknown')}",
                    severity=self._map_severity(row.get("SeverityLevel", "Informational")),
                    title=f"Security Event: {row.get('Activity', 'Unknown')}",
                    description=row.get("Activity", ""),
                    source_ip=row.get("SourceIP"),
                    destination_ip=None,
                    user=row.get("Account"),
                    computer=row.get("Computer"),
                    raw_data=row
                )
                events.append(event)
            except Exception as e:
                logger.warning(f"⚠️ Error parsing event: {e}")
                continue
        
        return events
    
    def get_sentinel_alerts(self, hours: int = 24) -> List[SentinelEvent]:
        """Fetch alerts from Microsoft Sentinel"""
        query = """
        SecurityAlert
        | where TimeGenerated > ago(24h)
        | project TimeGenerated, AlertName, Severity, Description, CompromiseEntityIds, Tactics, ExtendedProperties
        | order by TimeGenerated desc
        """
        
        rows = self.query_logs(query, hours)
        alerts = []
        
        for row in rows:
            try:
                alert = SentinelEvent(
                    timestamp=row.get("TimeGenerated", datetime.utcnow().isoformat()),
                    event_type="SentinelAlert",
                    severity=self._map_severity(row.get("Severity", "Informational")),
                    title=row.get("AlertName", "Unknown Alert"),
                    description=row.get("Description", ""),
                    source_ip=None,
                    destination_ip=None,
                    user=row.get("CompromiseEntityIds", [{}])[0].get("Name") if row.get("CompromiseEntityIds") else None,
                    computer=None,
                    raw_data=row
                )
                alerts.append(alert)
            except Exception as e:
                logger.warning(f"⚠️ Error parsing alert: {e}")
                continue
        
        return alerts
    
    def get_all_events(self, hours: int = 24) -> List[SentinelEvent]:
        """Get all security events and alerts"""
        events = []
        events.extend(self.get_security_events(hours))
        events.extend(self.get_sentinel_alerts(hours))
        return events
    
    def _map_severity(self, severity: str) -> str:
        """Map Azure severity to our severity levels"""
        severity_map = {
            "Critical": "critical",
            "High": "high",
            "Medium": "medium",
            "Low": "low",
            "Informational": "info"
        }
        return severity_map.get(severity, "info")
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Azure connection"""
        token = self._get_access_token()
        
        if token:
            return {
                "status": "connected",
                "message": "✅ Azure connection successful",
                "subscription_id": self.credentials.subscription_id,
                "workspace": self.credentials.workspace_name
            }
        else:
            return {
                "status": "failed",
                "message": "❌ Failed to connect to Azure",
                "hint": "Check Azure credentials in environment variables"
            }


# Environment variable names
AZURE_ENV_VARS = [
    "AZURE_TENANT_ID",
    "AZURE_CLIENT_ID", 
    "AZURE_CLIENT_SECRET",
    "AZURE_SUBSCRIPTION_ID",
    "AZURE_WORKSPACE_NAME"
]


def check_azure_configured() -> bool:
    """Check if Azure credentials are configured"""
    return all([
        os.getenv("AZURE_TENANT_ID"),
        os.getenv("AZURE_CLIENT_ID"),
        os.getenv("AZURE_CLIENT_SECRET"),
        os.getenv("AZURE_SUBSCRIPTION_ID")
    ])


def get_azure_service() -> AzureSentinelService:
    """Get Azure Sentinel service instance"""
    if check_azure_configured():
        return AzureSentinelService()
    else:
        logger.warning("⚠️ Azure credentials not configured, returning mock service")
        return AzureSentinelService()
