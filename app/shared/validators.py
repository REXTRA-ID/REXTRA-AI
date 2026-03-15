import re

def validate_session_token(token: str) -> bool:
    """Validate session token format (UUID)"""
    pattern = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
    return bool(re.match(pattern, token))