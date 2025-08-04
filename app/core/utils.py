"""
Shared utilities for the Lagentry OAuth Backend
"""

import re
import hashlib
import secrets
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_email(email: str) -> str:
    """Sanitize email address"""
    return email.lower().strip()


def generate_token_hash(token: str) -> str:
    """Generate hash of token for secure storage"""
    return hashlib.sha256(token.encode()).hexdigest()


def mask_token(token: str, visible_chars: int = 20) -> str:
    """Mask token for display (show first N characters)"""
    if len(token) <= visible_chars:
        return token
    return token[:visible_chars] + "..."


def is_valid_url(url: str) -> bool:
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def parse_query_params(url: str) -> Dict[str, List[str]]:
    """Parse query parameters from URL"""
    try:
        parsed = urlparse(url)
        return parse_qs(parsed.query)
    except Exception:
        return {}


def generate_random_string(length: int = 32) -> str:
    """Generate random string"""
    return secrets.token_urlsafe(length)


def format_datetime(dt: datetime) -> str:
    """Format datetime for display"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def is_token_expired(expires_at: datetime, buffer_minutes: int = 5) -> bool:
    """Check if token is expired (with buffer)"""
    buffer_time = timedelta(minutes=buffer_minutes)
    return datetime.now() + buffer_time >= expires_at


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two dictionaries (dict2 overrides dict1)"""
    result = dict1.copy()
    result.update(dict2)
    return result


def filter_dict(data: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
    """Filter dictionary to only include allowed keys"""
    return {k: v for k, v in data.items() if k in allowed_keys}


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from dictionary"""
    return data.get(key, default)


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def normalize_provider_name(provider: str) -> str:
    """Normalize provider name"""
    return provider.lower().strip()


def validate_provider(provider: str, allowed_providers: List[str]) -> bool:
    """Validate provider name"""
    normalized = normalize_provider_name(provider)
    return normalized in [p.lower() for p in allowed_providers]


def create_error_response(message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create standardized error response"""
    response = {
        "error": True,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    if details:
        response["details"] = details
    return response


def create_success_response(data: Dict[str, Any], message: str = "Success") -> Dict[str, Any]:
    """Create standardized success response"""
    return {
        "error": False,
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }


def log_activity_summary(provider: str, action: str, user_email: str, success: bool) -> str:
    """Create activity log summary"""
    status = "SUCCESS" if success else "FAILED"
    return f"[{provider.upper()}] {action} for {user_email}: {status}"


def format_bytes(bytes_value: int) -> str:
    """Format bytes to human readable string"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} TB"


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """Validate required fields and return missing ones"""
    missing = []
    for field in required_fields:
        if field not in data or data[field] is None:
            missing.append(field)
    return missing


def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values from dictionary"""
    return {k: v for k, v in data.items() if v is not None}


def get_nested_value(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Get nested value from dictionary using dot notation"""
    keys = path.split('.')
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current


def set_nested_value(data: Dict[str, Any], path: str, value: Any) -> Dict[str, Any]:
    """Set nested value in dictionary using dot notation"""
    keys = path.split('.')
    current = data
    
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value
    return data 