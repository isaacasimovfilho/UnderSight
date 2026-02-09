-- Inventory Module Schema for UnderSight
-- Receives data from N8N, processes with AI, stores inventory

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- INVENTORY ITEMS
-- ============================================
CREATE TABLE inventory_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE NOT NULL,
    source VARCHAR(100) NOT NULL,  -- 'n8n', 'manual', 'import', 'agent'
    external_id VARCHAR(255),  -- ID from N8N/external system
    hostname VARCHAR(255),
    ip_address INET,
    mac_address MACADDR,
    os VARCHAR(255),
    os_version VARCHAR(100),
    asset_type VARCHAR(100),  -- 'server', 'workstation', 'network', 'cloud', 'iot'
    manufacturer VARCHAR(255),
    model VARCHAR(255),
    serial_number VARCHAR(255),
    location VARCHAR(500),
    department VARCHAR(255),
    owner VARCHAR(255),
    tags TEXT[] DEFAULT '{}',
    risk_score INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'approved', 'rejected', 'archived'
    inventory_decision TEXT,  -- AI decision reason
    inventory_comments TEXT,
    metadata JSONB DEFAULT '{}',
    raw_data JSONB,  -- Original data from N8N
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,  -- When AI processed it
    processed_by VARCHAR(50) DEFAULT 'ai'  -- 'ai', 'manual', 'rule'
);

CREATE INDEX idx_inventory_tenant ON inventory_items(tenant_id);
CREATE INDEX idx_inventory_hostname ON inventory_items(hostname);
CREATE INDEX idx_inventory_ip ON inventory_items(ip_address);
CREATE INDEX idx_inventory_status ON inventory_items(status);
CREATE INDEX idx_inventory_asset_type ON inventory_items(asset_type);
CREATE INDEX idx_inventory_external_id ON inventory_items(external_id);
CREATE INDEX idx_inventory_created_at ON inventory_items(created_at);

-- ============================================
-- AI PROCESSING LOG
-- ============================================
CREATE TABLE inventory_ai_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE NOT NULL,
    inventory_item_id UUID REFERENCES inventory_items(id) ON DELETE CASCADE,
    prompt_used TEXT NOT NULL,
    model_used VARCHAR(100) NOT NULL,
    input_data JSONB NOT NULL,
    output_decision VARCHAR(50) NOT NULL,
    output_comments TEXT,
    confidence_score DECIMAL(5,4),
    processing_time_ms INTEGER,
    api_response JSONB,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_logs_tenant ON inventory_ai_logs(tenant_id);
CREATE INDEX idx_ai_logs_item ON inventory_ai_logs(inventory_item_id);
CREATE INDEX idx_ai_logs_created ON inventory_ai_logs(created_at);

-- ============================================
-- AI CONFIGURATIONS
-- ============================================
CREATE TABLE inventory_ai_configs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    provider VARCHAR(50) NOT NULL,  -- 'openai', 'anthropic', 'ollama', 'groq', 'deepseek'
    api_url VARCHAR(500),
    api_key_encrypted VARCHAR(500),  -- Encrypted
    model VARCHAR(100) DEFAULT 'gpt-4',
    prompt_template TEXT NOT NULL,
    prompt_variables JSONB DEFAULT '[]',  -- ['hostname', 'ip', 'os', 'mac', etc]
    temperature DECIMAL(3,2) DEFAULT 0.3,
    max_tokens INTEGER DEFAULT 1000,
    is_enabled BOOLEAN DEFAULT true,
    auto_process BOOLEAN DEFAULT true,  -- Auto-process incoming items
    webhook_url VARCHAR(500),  -- Callback after processing
    settings JSONB DEFAULT '{}',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_configs_tenant ON inventory_ai_configs(tenant_id);
CREATE INDEX idx_ai_configs_enabled ON inventory_ai_configs(is_enabled);

-- ============================================
-- PROCESSING RULES (fallback if AI fails or for simple rules)
-- ============================================
CREATE TABLE inventory_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    priority INTEGER DEFAULT 100,  -- Lower = higher priority
    conditions JSONB NOT NULL,  -- {'field': 'os', 'operator': 'contains', 'value': 'Windows'}
    action VARCHAR(50) NOT NULL,  -- 'approve', 'reject', 'flag'
    comments TEXT,
    is_enabled BOOLEAN DEFAULT true,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_rules_tenant ON inventory_rules(tenant_id);
CREATE INDEX idx_rules_priority ON inventory_rules(priority);

-- ============================================
-- INVENTORY SOURCES
-- ============================================
CREATE TABLE inventory_sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE NOT NULL,
    name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50) NOT NULL,  -- 'n8n', 'api', 'agent', 'import', 'webhook'
    config JSONB NOT NULL,  -- Webhook URL, credentials, etc.
    is_enabled BOOLEAN DEFAULT true,
    last_sync_at TIMESTAMP,
    sync_status VARCHAR(50) DEFAULT 'idle',  -- 'idle', 'running', 'success', 'error'
    sync_error TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sources_tenant ON inventory_sources(tenant_id);

-- ============================================
-- SAMPLE DEFAULT AI PROMPT
-- ============================================
COMMENT ON TABLE inventory_items IS 'Items received from N8N or other sources, processed by AI';
COMMENT ON TABLE inventory_ai_logs IS 'Log of all AI processing for audit trail';
COMMENT ON TABLE inventory_ai_configs IS 'AI configuration per tenant';
COMMENT ON TABLE inventory_rules IS 'Fallback rules when AI is unavailable or for simple decisions';
COMMENT ON TABLE inventory_sources IS 'Configured data sources for inventory';

-- Grant insert permission to N8N webhook (simplified)
-- In production, use proper API key authentication
