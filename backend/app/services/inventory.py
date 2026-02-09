"""
Inventory Service - AI-powered inventory management

This service:
1. Receives equipment data from N8N (JSON)
2. Processes each item through AI (OpenAI, Anthropic, Ollama, Groq, DeepSeek)
3. Decides whether to add to inventory
4. Adds AI-generated comments
5. Stores results in database
"""

import json
import asyncio
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import UUID
from dataclasses import dataclass
from enum import Enum

import httpx
from pydantic import BaseModel, Field


class Decision(Enum):
    APPROVE = "approved"
    REJECT = "rejected"
    PENDING = "pending"
    FLAG = "flag"


class AssetType(Enum):
    SERVER = "server"
    WORKSTATION = "workstation"
    NETWORK = "network"
    CLOUD = "cloud"
    IOT = "iot"
    CONTAINER = "container"
    VM = "vm"
    OTHER = "other"


# Pydantic Models
class EquipmentData(BaseModel):
    """Equipment data from N8N"""
    external_id: Optional[str] = None
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    os: Optional[str] = None
    os_version: Optional[str] = None
    asset_type: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None
    owner: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    source: str = "n8n"  # Where this came from


class AIConfig(BaseModel):
    """AI configuration for inventory processing"""
    provider: str = "openai"  # openai, anthropic, ollama, groq, deepseek
    api_url: Optional[str] = None
    api_key: Optional[str] = None
    model: str = "gpt-4"
    temperature: float = 0.3
    max_tokens: int = 1000
    prompt_template: str = ""
    timeout_seconds: int = 30


class AIOutput(BaseModel):
    """AI processing result"""
    decision: Decision
    comments: str
    confidence: float
    suggested_tags: List[str] = Field(default_factory=list)
    suggested_risk_score: int = 0
    suggested_asset_type: Optional[str] = None


class InventoryItem(BaseModel):
    """Processed inventory item"""
    id: Optional[str] = None
    tenant_id: str
    source: str
    external_id: Optional[str] = None
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    os: Optional[str] = None
    os_version: Optional[str] = None
    asset_type: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None
    owner: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    risk_score: int = 0
    status: str = "pending"
    inventory_decision: str = ""
    inventory_comments: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    raw_data: Dict[str, Any] = Field(default_factory=dict)
    processed_by: str = "ai"


# Default AI Prompt Template
DEFAULT_PROMPT = """You are a cybersecurity expert analyzing equipment for inclusion in an inventory system.

Analyze the following equipment data and decide if it should be added to the inventory:

## Equipment Data:
- Hostname: {hostname}
- IP Address: {ip_address}
- MAC Address: {mac_address}
- Operating System: {os} {os_version}
- Asset Type: {asset_type}
- Manufacturer: {manufacturer}
- Model: {model}
- Serial Number: {serial_number}
- Location: {location}
- Department: {department}
- Owner: {owner}
- Tags: {tags}
- Source: {source}

## Decision Criteria:
1. Is this a legitimate enterprise asset?
2. Does it have proper identification (hostname, IP)?
3. Is the OS recognized and supported?
4. Are there any security concerns?

## Output Format (JSON only):
{{{{
    "decision": "approved" | "rejected" | "pending" | "flag",
    "comments": "Brief explanation of decision",
    "confidence": 0.0-1.0,
    "suggested_tags": ["tag1", "tag2"],
    "suggested_risk_score": 0-100,
    "suggested_asset_type": "server" | "workstation" | "network" | "cloud" | "iot" | "other"
}}}}

Respond with ONLY valid JSON, no other text."""


class AIService:
    """Service for AI-powered inventory processing"""
    
    PROVIDERS = {
        "openai": {
            "api_url": "https://api.openai.com/v1/chat/completions",
            "model_param": "model",
        },
        "anthropic": {
            "api_url": "https://api.anthropic.com/v1/complete",
            "model_param": "model",
        },
        "ollama": {
            "api_url": "http://localhost:11434/api/generate",
            "model_param": "model",
        },
        "groq": {
            "api_url": "https://api.groq.com/openai/v1/chat/completions",
            "model_param": "model",
        },
        "deepseek": {
            "api_url": "https://api.deepseek.com/chat/completions",
            "model_param": "model",
        },
    }
    
    def __init__(self, config: AIConfig):
        self.config = config
        self.provider = config.provider.lower()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get API headers based on provider"""
        headers = {"Content-Type": "application/json"}
        
        if self.provider == "openai":
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        elif self.provider == "anthropic":
            headers["x-api-key"] = self.config.api_key
            headers["anthropic-version"] = "2023-06-01"
        elif self.provider == "deepseek":
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        
        return headers
    
    def _build_prompt(self, data: EquipmentData) -> str:
        """Build the prompt from template"""
        prompt = self.config.prompt_template or DEFAULT_PROMPT
        
        # Replace variables
        replacements = {
            "{hostname}": data.hostname or "Unknown",
            "{ip_address}": data.ip_address or "Unknown",
            "{mac_address}": data.mac_address or "Unknown",
            "{os}": data.os or "Unknown",
            "{os_version}": data.os_version or "Unknown",
            "{asset_type}": data.asset_type or "Unknown",
            "{manufacturer}": data.manufacturer or "Unknown",
            "{model}": data.model or "Unknown",
            "{serial_number}": data.serial_number or "Unknown",
            "{location}": data.location or "Unknown",
            "{department}": data.department or "Unknown",
            "{owner}": data.owner or "Unknown",
            "{tags}": ", ".join(data.tags) if data.tags else "None",
            "{source}": data.source,
        }
        
        for old, new in replacements.items():
            prompt = prompt.replace(old, new)
        
        return prompt
    
    async def process_item(self, data: EquipmentData) -> AIOutput:
        """Process a single equipment item through AI"""
        start_time = datetime.utcnow()
        
        try:
            prompt = self._build_prompt(data)
            
            # Build request based on provider
            if self.provider == "ollama":
                payload = {
                    "model": self.config.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.config.temperature,
                        "num_predict": self.config.max_tokens,
                    }
                }
            elif self.provider in ["openai", "groq", "deepseek"]:
                payload = {
                    "model": self.config.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": self.config.temperature,
                    "max_tokens": self.config.max_tokens,
                }
            elif self.provider == "anthropic":
                payload = {
                    "model": self.config.model,
                    "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                    "temperature": self.config.temperature,
                    "max_tokens_to_sample": self.config.max_tokens,
                }
            else:
                # Generic OpenAI-compatible format
                payload = {
                    "model": self.config.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": self.config.temperature,
                }
            
            async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
                response = await client.post(
                    self.PROVIDERS.get(self.provider, {}).get("api_url", ""),
                    json=payload,
                    headers=self._get_headers()
                )
                response.raise_for_status()
                result = response.json()
            
            # Parse response
            if self.provider == "ollama":
                content = result.get("response", "")
            else:
                content = result["choices"][0]["message"]["content"]
            
            # Extract JSON from response
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            json_content = content[json_start:json_end]
            
            parsed = json.loads(json_content)
            
            return AIOutput(
                decision=Decision(parsed.get("decision", "pending")),
                comments=parsed.get("comments", ""),
                confidence=float(parsed.get("confidence", 0.5)),
                suggested_tags=parsed.get("suggested_tags", []),
                suggested_risk_score=int(parsed.get("suggested_risk_score", 0)),
                suggested_asset_type=parsed.get("suggested_asset_type"),
            )
            
        except Exception as e:
            # Log error and return pending
            return AIOutput(
                decision=Decision.PENDING,
                comments=f"AI processing failed: {str(e)}",
                confidence=0.0,
            )
    
    async def process_batch(self, items: List[EquipmentData]) -> List[AIOutput]:
        """Process multiple items"""
        tasks = [self.process_item(item) for item in items]
        return await asyncio.gather(*tasks)


class InventoryService:
    """Main inventory service"""
    
    def __init__(self, db_session, tenant_id: str, ai_config: Optional[AIConfig] = None):
        self.db = db_session
        self.tenant_id = tenant_id
        self.ai_service = AIService(ai_config) if ai_config else None
    
    async def receive_from_n8n(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Receive equipment data from N8N webhook"""
        # Handle single item or batch
        if "items" in payload:
            items = payload["items"]
        elif isinstance(payload, list):
            items = payload
        else:
            items = [payload]
        
        results = []
        for item_data in items:
            equipment = EquipmentData(**item_data)
            result = await self.process_item(equipment)
            results.append(result)
        
        return {
            "received": len(items),
            "processed": len(results),
            "results": [r.dict() for r in results]
        }
    
    async def process_item(self, equipment: EquipmentData) -> Dict[str, Any]:
        """Process a single equipment item"""
        start_time = datetime.utcnow()
        
        # Check if AI is enabled
        if self.ai_service:
            ai_result = await self.ai_service.process_item(equipment)
            
            # Map AI decision to status
            if ai_result.decision == Decision.APPROVE:
                status = "approved"
            elif ai_result.decision == Decision.REJECT:
                status = "rejected"
            elif ai_result.decision == Decision.FLAG:
                status = "pending"
            else:
                status = "pending"
            
            comments = ai_result.comments
            risk_score = ai_result.suggested_risk_score
            tags = equipment.tags + ai_result.suggested_tags
            asset_type = ai_result.suggested_asset_type or equipment.asset_type
        else:
            # No AI config - auto-approve
            status = "approved"
            comments = "Auto-approved: No AI configuration"
            risk_score = 0
            tags = equipment.tags
            asset_type = equipment.asset_type
        
        # Create inventory item
        item = {
            "tenant_id": self.tenant_id,
            "source": equipment.source,
            "external_id": equipment.external_id,
            "hostname": equipment.hostname,
            "ip_address": equipment.ip_address,
            "mac_address": equipment.mac_address,
            "os": equipment.os,
            "os_version": equipment.os_version,
            "asset_type": asset_type,
            "manufacturer": equipment.manufacturer,
            "model": equipment.model,
            "serial_number": equipment.serial_number,
            "location": equipment.location,
            "department": equipment.department,
            "owner": equipment.owner,
            "tags": list(set(tags)),  # Remove duplicates
            "risk_score": risk_score,
            "status": status,
            "inventory_decision": comments,
            "inventory_comments": comments,
            "metadata": equipment.metadata,
            "raw_data": equipment.dict(),
            "processed_by": "ai" if self.ai_service else "rule",
            "processed_at": datetime.utcnow(),
            "last_seen": datetime.utcnow(),
        }
        
        # TODO: Save to database
        # self.db.add(InventoryItem(**item))
        # await self.db.commit()
        
        processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        return {
            "status": "success",
            "item": item,
            "processing_time_ms": processing_time,
            "ai_decision": status,
            "comments": comments,
        }
    
    async def get_inventory(
        self,
        status: Optional[str] = None,
        asset_type: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """Get inventory items with filters"""
        # TODO: Query database with filters
        return {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
        }
    
    async def get_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get a single inventory item"""
        # TODO: Query database
        return None
    
    async def update_item(
        self,
        item_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an inventory item"""
        # TODO: Update in database
        return {"status": "success"}
    
    async def approve_item(self, item_id: str, comments: str = "") -> Dict[str, Any]:
        """Manually approve an item"""
        return await self.update_item(item_id, {
            "status": "approved",
            "inventory_comments": comments,
            "processed_by": "manual"
        })
    
    async def reject_item(self, item_id: str, comments: str = "") -> Dict[str, Any]:
        """Manually reject an item"""
        return await self.update_item(item_id, {
            "status": "rejected",
            "inventory_comments": comments,
            "processed_by": "manual"
        })


# Example usage:
"""
# Configure AI
config = AIConfig(
    provider="openai",
    api_key="sk-...",
    model="gpt-4",
    temperature=0.3,
    prompt_template=DEFAULT_PROMPT
)

# Receive from N8N
payload = {
    "items": [
        {
            "hostname": "web-server-01",
            "ip_address": "10.0.0.10",
            "mac_address": "00:11:22:33:44:55",
            "os": "Ubuntu",
            "os_version": "22.04",
            "asset_type": "server",
            "manufacturer": "Dell",
            "model": "PowerEdge R740",
            "location": "Data Center A",
            "department": "IT",
            "owner": "admin@company.com",
            "tags": ["production", "web"],
            "source": "n8n_scan"
        }
    ]
}

service = InventoryService(db, tenant_id, config)
result = await service.receive_from_n8n(payload)
"""
