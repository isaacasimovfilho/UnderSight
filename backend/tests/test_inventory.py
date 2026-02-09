"""
Unit Tests for Inventory Module
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import datetime

from app.services.inventory import (
    AIService,
    InventoryService,
    InventoryAIService
)


class TestAIService:
    """Test AIService class."""
    
    def test_ai_service_init(self):
        """Test AIService initialization."""
        service = AIService(
            provider="openai",
            api_key="test-key",
            model="gpt-4"
        )
        
        assert service.provider == "openai"
        assert service.api_key == "test-key"
        assert service.model == "gpt-4"
    
    @pytest.mark.asyncio
    async def test_analyze_item_openai(self):
        """Test analyzing item with OpenAI."""
        service = AIService(
            provider="openai",
            api_key="test-key",
            model="gpt-4"
        )
        
        item = {
            "name": "AWS EC2 Instance",
            "type": "server",
            "data": {"instance_type": "t3.medium"}
        }
        
        # Mock OpenAI response
        with patch('openai.AsyncOpenAI') as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(
                return_value=MagicMock(
                    choices=[MagicMock(
                        message=MagicMock(
                            content='{"decision": "approve", "confidence": 0.9, "reason": "Standard server"}'
                        )
                    )]
                )
            )
            
            result = await service.analyze_item(item)
            
            assert "decision" in result
            assert "confidence" in result
    
    @pytest.mark.asyncio
    async def test_analyze_item_anthropic(self):
        """Test analyzing item with Anthropic."""
        service = AIService(
            provider="anthropic",
            api_key="test-key",
            model="claude-3-sonnet"
        )
        
        item = {
            "name": "Windows Server",
            "type": "server",
            "data": {"os": "Windows 2022"}
        }
        
        with patch('anthropic.AsyncAnthropic') as mock_client:
            mock_client.return_value.messages.create = AsyncMock(
                return_value=MagicMock(
                    content=[MagicMock(
                        text='{"decision": "flag", "confidence": 0.7, "reason": "Check compliance"}'
                    )]
                )
            )
            
            result = await service.analyze_item(item)
            
            assert "decision" in result
    
    @pytest.mark.asyncio
    async def test_analyze_item_groq(self):
        """Test analyzing item with Groq."""
        service = AIService(
            provider="groq",
            api_key="test-key",
            model="llama2-70b"
        )
        
        item = {
            "name": "Linux Server",
            "type": "server",
            "data": {"os": "Ubuntu 22.04"}
        }
        
        with patch('groq.Groq') as mock_client:
            mock_client.return_value.chat.completions.create = AsyncMock(
                return_value=MagicMock(
                    choices=[MagicMock(
                        message=MagicMock(
                            content='{"decision": "approve", "confidence": 0.95}'
                        )
                    )]
                )
            )
            
            result = await service.analyze_item(item)
            
            assert result["decision"] == "approve"
    
    @pytest.mark.asyncio
    async def test_analyze_item_ollama(self):
        """Test analyzing item with Ollama (local)."""
        service = AIService(
            provider="ollama",
            api_key="",
            model="llama3"
        )
        
        item = {
            "name": "Test Server",
            "type": "server",
            "data": {}
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "response": '{"decision": "approve", "confidence": 0.85}'
            }
            mock_client.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await service.analyze_item(item)
            
            assert "decision" in result
    
    def test_get_provider_info(self):
        """Test getting provider information."""
        service = AIService(
            provider="openai",
            api_key="test-key",
            model="gpt-4"
        )
        
        info = service.get_provider_info()
        
        assert info["provider"] == "openai"
        assert info["model"] == "gpt-4"
        assert "endpoints" in info
        assert info["endpoints"]["api"] == "https://api.openai.com/v1"


class TestInventoryService:
    """Test InventoryService class."""
    
    def test_inventory_service_init(self):
        """Test InventoryService initialization."""
        mock_db = MagicMock()
        mock_redis = MagicMock()
        
        service = InventoryService(mock_db, mock_redis)
        
        assert service.db == mock_db
        assert service.redis == mock_redis
    
    @pytest.mark.asyncio
    async def test_process_webhook_n8n(self):
        """Test processing webhook from N8N."""
        mock_db = MagicMock()
        mock_redis = MagicMock()
        
        service = InventoryService(mock_db, mock_redis)
        
        n8n_payload = {
            "items": [
                {
                    "name": "EC2 Instance",
                    "type": "server",
                    "source": "aws",
                    "data": {"instance_id": "i-123"}
                }
            ],
            "source": "aws_inventory",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        result = await service.process_webhook_n8n(n8n_payload)
        
        assert "processed" in result
        assert "items" in result
    
    def test_create_inventory_item(self):
        """Test creating inventory item."""
        mock_db = MagicMock()
        mock_redis = MagicMock()
        
        service = InventoryService(mock_db, mock_redis)
        
        item_data = {
            "name": "Test Server",
            "type": "server",
            "source": "manual",
            "data": {"ip": "192.168.1.1"}
        }
        
        # Should not raise exception
        service.create_item(item_data)
    
    def test_list_items(self):
        """Test listing inventory items."""
        mock_db = MagicMock()
        mock_redis = MagicMock()
        
        service = InventoryService(mock_db, mock_redis)
        
        # Mock query
        mock_query = MagicMock()
        mock_query.filter = MagicMock(return_value=mock_query)
        mock_query.order_by = MagicMock(return_value=mock_query)
        mock_query.limit = MagicMock(return_value=mock_query)
        mock_query.offset = MagicMock(return_value=mock_query)
        mock_query.all = MagicMock(return_value=[])
        
        mock_db.query.return_value = mock_query
        
        result = service.list_items(tenant_id="tenant-123")
        
        assert isinstance(result, list)
    
    def test_get_item_by_id(self):
        """Test getting item by ID."""
        mock_db = MagicMock()
        mock_redis = MagicMock()
        
        service = InventoryService(mock_db, mock_redis)
        
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        result = service.get_item("item-123")
        
        assert result is None
    
    def test_update_item_status(self):
        """Test updating item status."""
        mock_db = MagicMock()
        mock_redis = MagicMock()
        
        service = InventoryService(mock_db, mock_redis)
        
        # Mock item
        mock_item = MagicMock()
        mock_item.id = "item-123"
        mock_item.status = "pending"
        
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_item
        
        result = service.update_status("item-123", "approved")
        
        assert mock_item.status == "approved"
        mock_db.commit.assert_called()


class TestInventoryAIService:
    """Test InventoryAIService class."""
    
    def test_ai_service_init(self):
        """Test InventoryAIService initialization."""
        mock_ai_service = MagicMock()
        
        service = InventoryAIService(mock_ai_service)
        
        assert service.ai_service == mock_ai_service
    
    @pytest.mark.asyncio
    async def test_analyze_item(self):
        """Test analyzing item with AI."""
        mock_ai = AsyncMock()
        mock_ai.analyze_item = AsyncMock(return_value={
            "decision": "approve",
            "confidence": 0.9,
            "reason": "Standard configuration"
        })
        
        service = InventoryAIService(mock_ai)
        
        item = {
            "name": "Web Server",
            "type": "server",
            "data": {"web_server": "nginx"}
        }
        
        result = await service.analyze_item(item)
        
        assert result["decision"] == "approve"
        assert result["confidence"] == 0.9
    
    @pytest.mark.asyncio
    async def test_batch_analyze(self):
        """Test batch analysis."""
        mock_ai = AsyncMock()
        mock_ai.analyze_item = AsyncMock(return_value={
            "decision": "approve",
            "confidence": 0.8
        })
        
        service = InventoryAIService(mock_ai)
        
        items = [
            {"name": "Server 1", "type": "server"},
            {"name": "Server 2", "type": "server"}
        ]
        
        results = await service.batch_analyze(items)
        
        assert len(results) == 2
        assert all("decision" in r for r in results)
