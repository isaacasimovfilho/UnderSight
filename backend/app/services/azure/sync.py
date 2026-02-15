"""
Azure Sentinel Sync Service
Automatic collection of security events from Microsoft Sentinel
"""

import os
import time
import logging
from datetime import datetime, timedelta
from typing import Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.services.azure.sentinel import get_azure_service
from app.services.opensearch.client import opensearch_service
from app.db.session import get_db

logger = logging.getLogger(__name__)


class AzureSyncService:
    """
    Service to automatically sync Azure Sentinel events
    """
    
    def __init__(self):
        self.scheduler: Optional[BackgroundScheduler] = None
        self.sync_interval_minutes = int(os.getenv('AZURE_SYNC_INTERVAL', '60'))
        self.enabled = os.getenv('AZURE_SYNC_ENABLED', 'false').lower() == 'true'
    
    def sync_events(self):
        """Sync events from Azure Sentinel"""
        from app.services.opensearch.client import LogDocument
        from app.services.azure.sentinel import SentinelEvent
        
        logger.info("🔄 Starting Azure Sentinel sync...")
        
        try:
            azure_service = get_azure_service()
            
            # Check if Azure is configured
            if not hasattr(azure_service, 'credentials') or not azure_service.credentials.tenant_id:
                logger.warning("⚠️ Azure not configured, skipping sync")
                return
            
            # Fetch events
            events = azure_service.get_all_events(hours=24)
            
            if not events:
                logger.info("ℹ️ No new events from Azure Sentinel")
                return
            
            logger.info(f"📥 Fetched {len(events)} events from Azure Sentinel")
            
            # Index events in OpenSearch
            indexed = 0
            for event in events:
                try:
                    log_doc = LogDocument(
                        timestamp=event.timestamp if isinstance(event.timestamp, datetime) 
                            else datetime.fromisoformat(str(event.timestamp).replace('Z', '+00:00')),
                        event_type=event.event_type,
                        source_type="azure_sentinel",
                        source_ip=event.source_ip,
                        destination_ip=event.destination_ip,
                        severity=event.severity,
                        message=f"{event.title}: {event.description[:500]}",
                        raw_data=event.raw_data,
                        tenant_id=None,
                        session_id=None,
                        tags=["azure", "sentinel", event.severity, event.event_type]
                    )
                    
                    if opensearch_service.index_log(log_doc):
                        indexed += 1
                except Exception as e:
                    logger.warning(f"⚠️ Failed to index event: {e}")
                    continue
            
            logger.info(f"✅ Indexed {indexed} events from Azure Sentinel")
            
        except Exception as e:
            logger.error(f"❌ Azure sync failed: {e}")
    
    def start_scheduler(self):
        """Start the sync scheduler"""
        if not self.enabled:
            logger.info("ℹ️ Azure sync is disabled (AZURE_SYNC_ENABLED=false)")
            return
        
        if self.scheduler:
            logger.info("ℹ️ Azure sync scheduler already running")
            return
        
        logger.info(f"🚀 Starting Azure Sentinel sync scheduler (every {self.sync_interval_minutes} minutes)")
        
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.sync_events,
            trigger=IntervalTrigger(minutes=self.sync_interval_minutes),
            id='azure_sentinel_sync',
            name='Azure Sentinel Event Sync',
            replace_existing=True
        )
        self.scheduler.start()
        
        # Run initial sync
        logger.info("🔄 Running initial sync...")
        self.sync_events()
    
    def stop_scheduler(self):
        """Stop the sync scheduler"""
        if self.scheduler:
            self.scheduler.shutdown()
            self.scheduler = None
            logger.info("🛑 Azure Sentinel sync scheduler stopped")
    
    def trigger_manual_sync(self):
        """Trigger a manual sync"""
        logger.info("🔄 Manual sync triggered")
        self.sync_events()
        return {"status": "success", "message": "Sync completed"}


# Singleton instance
azure_sync_service = AzureSyncService()
