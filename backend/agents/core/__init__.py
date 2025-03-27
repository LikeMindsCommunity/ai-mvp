"""
Core module for shared functionality across agents.

This module re-exports functionality from the infrastructure module
for backward compatibility and convenience.
"""

from ...infrastructure import (
    User, 
    get_current_user, 
    get_optional_user, 
    create_access_token,
    settings,
    trace,
    monitor,
)

__all__ = [
    "User", 
    "get_current_user", 
    "get_optional_user", 
    "create_access_token",
    "settings",
    "trace",
    "monitor",
] 