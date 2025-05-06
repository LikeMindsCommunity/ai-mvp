"""
Authentication module - provides user authentication and JWT token handling.
"""
from api.infrastructure.auth.jwt import get_current_user, create_access_token, user_to_dict
from api.infrastructure.auth.service import sign_up, sign_in, sign_out

__all__ = [
    'get_current_user',
    'create_access_token',
    'user_to_dict',
    'sign_up',
    'sign_in',
    'sign_out'
] 