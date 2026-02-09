from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, Text, 
    ForeignKey, UniqueConstraint, Index, JSON
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

def gen_uuid():
    return str(uuid.uuid4())

class Tenant(Base):
    """Hierarchical tenant structure."""
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    tenant_type = Column(String(50), nullable=False)  # 'root', 'provider', 'customer', 'sub_customer'
    parent_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"))
    status = Column(String(50), default="active")
    settings = Column(JSON, default={})
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    parent = relationship("Tenant", remote_side=[id], backref="children")
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    roles = relationship("Role", back_populates="tenant", cascade="all, delete-orphan")
    integrations = relationship("Integration", back_populates="tenant", cascade="all, delete-orphan")
    webhooks = relationship("Webhook", back_populates="tenant", cascade="all, delete-orphan")
    api_keys = relationship("ApiKey", back_populates="tenant", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="tenant", cascade="all, delete-orphan")

class User(Base):
    """User belonging to a specific tenant."""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    username = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    avatar_url = Column(String(500))
    role = Column(String(50), default="viewer")
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    user_roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    api_keys_created = relationship("ApiKey", back_populates="created_by")
    webhooks_created = relationship("Webhook", back_populates="created_by")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    __table_args__ = (
        UniqueConstraint('tenant_id', 'username', name='uq_tenant_username'),
        UniqueConstraint('tenant_id', 'email', name='uq_tenant_email'),
        Index('idx_users_tenant', 'tenant_id'),
    )

class Role(Base):
    """Role with permissions for a tenant."""
    __tablename__ = "roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    permissions = Column(JSON, default=[])  # ["alerts:read", "alerts:write", "cases:manage", etc.]
    is_system = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="roles")
    user_roles = relationship("UserRole", back_populates="role")
    
    __table_args__ = (
        UniqueConstraint('tenant_id', 'name', name='uq_tenant_role'),
        Index('idx_roles_tenant', 'tenant_id'),
    )

class UserRole(Base):
    """Many-to-many relationship between users and roles."""
    __tablename__ = "user_roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'role_id', name='uq_user_role'),
        Index('idx_user_roles_user', 'user_id'),
        Index('idx_user_roles_role', 'role_id'),
    )

class Integration(Base):
    """Third-party integrations configuration."""
    __tablename__ = "integrations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    provider = Column(String(100), nullable=False)  # 'slack', 'jira', 'pagerduty', 'webhook'
    name = Column(String(255), nullable=False)
    config = Column(JSON, nullable=False)  # Encrypted credentials
    settings = Column(JSON, default={})
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="integrations")
    
    __table_args__ = (
        Index('idx_integrations_tenant', 'tenant_id'),
        Index('idx_integrations_provider', 'provider'),
    )

class Webhook(Base):
    """Custom webhooks for events."""
    __tablename__ = "webhooks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    events = Column(JSON, nullable=False)  # ['alert.created', 'case.closed', etc.]
    headers = Column(JSON, default={})
    secret = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="webhooks")
    created_by = relationship("User", back_populates="webhooks_created")
    
    __table_args__ = (
        Index('idx_webhooks_tenant', 'tenant_id'),
    )

class ApiKey(Base):
    """API keys for programmatic access."""
    __tablename__ = "api_keys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    key_hash = Column(String(255), nullable=False)
    key_prefix = Column(String(10), nullable=False)
    permissions = Column(JSON, default=[])
    expires_at = Column(DateTime)
    last_used_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="api_keys")
    created_by = relationship("User", back_populates="api_keys_created")
    
    __table_args__ = (
        Index('idx_api_keys_tenant', 'tenant_id'),
        Index('idx_api_keys_prefix', 'key_prefix'),
    )

class AuditLog(Base):
    """Tenant-aware audit logs."""
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100))
    resource_id = Column(UUID(as_uuid=True))
    details = Column(JSON, default={})
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="audit_logs")
    user = relationship("User", back_populates="audit_logs")
    
    __table_args__ = (
        Index('idx_audit_tenant', 'tenant_id'),
        Index('idx_audit_user', 'user_id'),
        Index('idx_audit_created', 'created_at'),
    )

# Default Permissions
DEFAULT_PERMISSIONS = {
    "admin": [
        "alerts:*", "cases:*", "assets:*", "sensors:*", 
        "playbooks:*", "users:*", "roles:*", "settings:*",
        "integrations:*", "webhooks:*", "api_keys:*"
    ],
    "analyst": [
        "alerts:read", "alerts:write", "alerts:assign",
        "cases:read", "cases:write", "cases:assign",
        "assets:read", "sensors:read",
        "playbooks:execute"
    ],
    "viewer": [
        "alerts:read", "cases:read", "assets:read"
    ]
}
