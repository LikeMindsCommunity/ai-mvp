"""
Supabase database client module.
"""
from functools import lru_cache
from typing import Optional, Dict, Any
import json
import os

import httpx
from supabase import create_client, Client

from api.config import get_settings

settings = get_settings()

@lru_cache()
def get_supabase_client() -> Client:
    """Create and return a Supabase client instance.
    
    Returns:
        Client: The Supabase client instance.
    """
    if not settings.supabase_url or not settings.supabase_anon_key:
        raise ValueError("Supabase URL and anon key must be set in environment variables")
        
    return create_client(settings.supabase_url, settings.supabase_anon_key)

@lru_cache()
def get_supabase_admin_client() -> Client:
    """Create and return a Supabase admin client instance with service role key.
    
    This client bypasses RLS and should only be used for admin operations.
    
    Returns:
        Client: The Supabase admin client instance.
    """
    if not settings.supabase_url or not settings.supabase_service_key:
        raise ValueError("Supabase URL and service key must be set in environment variables")
        
    return create_client(settings.supabase_url, settings.supabase_service_key)

class SupabaseManager:
    """
    Manager for interacting with Supabase.
    
    This class provides access to Supabase clients. Most of the functionality has been 
    moved to dedicated service modules:
    - User authentication: api.infrastructure.auth.service
    - Project management: api.infrastructure.projects.service
    - Profile management: api.infrastructure.users.service
    - Code generation: api.infrastructure.code_generations.service
    """
    
    def __init__(self):
        """Initialize the manager with a cached client."""
        self.client = get_supabase_client()
        self._admin_client = None  # Lazy load admin client only when needed
    
    @property
    def admin_client(self) -> Client:
        """Get the admin client, creating it if needed."""
        if self._admin_client is None:
            self._admin_client = get_supabase_admin_client()
        return self._admin_client
    
    # User management methods are moved to auth/service.py
    # The following methods: sign_up, sign_in, sign_out are removed from here
    
    # Project management methods are moved to projects/service.py
    # The following methods: create_project, get_projects, get_project, update_project, delete_project, share_project are removed from here
    
    # Profile management methods are moved to users/service.py
    # The following methods: get_profile, update_profile are removed from here
            
    # Code generation methods are moved to code_generations/service.py
    # The following methods: create_code_generation, update_code_generation are removed from here 