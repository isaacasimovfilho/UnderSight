"""
Unit Tests for Auth Module
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from jose import jwt

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
    verify_token
)


class TestPasswordHashing:
    """Test password hashing functions."""
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "SecurePassword123!"
        
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert "$" in hashed  # Pepper separator
    
    def test_verify_correct_password(self):
        """Test verifying correct password."""
        password = "SecurePassword123!"
        hashed = get_password_hash(password)
        
        result = verify_password(password, hashed)
        
        assert result is True
    
    def test_verify_incorrect_password(self):
        """Test verifying incorrect password."""
        password = "SecurePassword123!"
        wrong_password = "WrongPassword456!"
        hashed = get_password_hash(password)
        
        result = verify_password(wrong_password, hashed)
        
        assert result is False
    
    def test_different_hashes_same_password(self):
        """Test that same password produces different hashes (due to salt)."""
        password = "SecurePassword123!"
        
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        assert hash1 != hash2  # Different salts
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTTokens:
    """Test JWT token functions."""
    
    @patch('app.core.security.SECRET_KEY', 'test-secret-key')
    @patch('app.core.security.ALGORITHM', 'HS256')
    @patch('app.core.security.ACCESS_TOKEN_EXPIRE_MINUTES', 30)
    def test_create_access_token(self):
        """Test creating access token."""
        data = {
            "sub": "user-123",
            "username": "testuser",
            "tenant_id": "tenant-123"
        }
        
        token = create_access_token(data)
        
        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)
    
    @patch('app.core.security.SECRET_KEY', 'test-secret-key')
    @patch('app.core.security.ALGORITHM', 'HS256')
    def test_decode_valid_token(self):
        """Test decoding valid token."""
        data = {
            "sub": "user-123",
            "username": "testuser"
        }
        
        token = create_access_token(data)
        decoded = decode_access_token(token)
        
        assert decoded is not None
        assert decoded["sub"] == "user-123"
        assert decoded["username"] == "testuser"
    
    @patch('app.core.security.SECRET_KEY', 'test-secret-key')
    @patch('app.core.security.ALGORITHM', 'HS256')
    def test_decode_expired_token(self):
        """Test decoding expired token."""
        data = {
            "sub": "user-123",
            "username": "testuser"
        }
        
        # Create token that expires immediately
        with patch('app.core.security.timedelta', return_value=timedelta(seconds=-1)):
            token = create_access_token(data)
        
        decoded = decode_access_token(token)
        
        assert decoded is None
    
    @patch('app.core.security.SECRET_KEY', 'test-secret-key')
    @patch('app.core.security.ALGORITHM', 'HS256')
    def test_decode_invalid_token(self):
        """Test decoding invalid token."""
        invalid_token = "invalid.token.here"
        
        decoded = decode_access_token(invalid_token)
        
        assert decoded is None
    
    @patch('app.core.security.SECRET_KEY', 'test-secret-key')
    @patch('app.core.security.ALGORITHM', 'HS256')
    def test_verify_valid_token(self):
        """Test verifying valid token."""
        data = {
            "sub": "user-123",
            "username": "testuser"
        }
        
        token = create_access_token(data)
        result = verify_token(token)
        
        assert result is True
    
    @patch('app.core.security.SECRET_KEY', 'test-secret-key')
    @patch('app.core.security.ALGORITHM', 'HS256')
    def test_verify_invalid_token(self):
        """Test verifying invalid token."""
        result = verify_token("invalid.token.here")
        
        assert result is False


class TestTokenPayload:
    """Test token payload contents."""
    
    @patch('app.core.security.SECRET_KEY', 'test-secret-key')
    @patch('app.core.security.ALGORITHM', 'HS256')
    @patch('app.core.security.ACCESS_TOKEN_EXPIRE_MINUTES', 60)
    def test_token_contains_required_fields(self):
        """Test that token contains required fields."""
        data = {
            "sub": "user-123",
            "username": "testuser",
            "email": "test@example.com",
            "tenant_id": "tenant-123",
            "role": "admin"
        }
        
        token = create_access_token(data)
        decoded = jwt.decode(
            token,
            "test-secret-key",
            algorithms=["HS256"]
        )
        
        assert decoded["sub"] == "user-123"
        assert decoded["username"] == "testuser"
        assert decoded["email"] == "test@example.com"
        assert decoded["tenant_id"] == "tenant-123"
        assert decoded["role"] == "admin"
        assert "exp" in decoded
        assert "iat" in decoded
