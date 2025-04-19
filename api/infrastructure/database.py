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
    
    # User management methods
    async def sign_up(self, email: str, password: str, user_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Register a new user.
        
        Args:
            email: User email
            password: User password
            user_metadata: Additional user metadata
            
        Returns:
            Dict containing user data and session
        """
        try:
            data = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": user_metadata or {}
                }
            })
            return data
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Authentication error: {str(e)}")
    
    async def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """
        Sign in a user.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dict containing session data
        """
        try:
            data = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return data
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Authentication error: {str(e)}")
    
    async def sign_out(self, jwt: str) -> None:
        """
        Sign out a user.
        
        Args:
            jwt: User JWT token
        """
        try:
            # Set the auth token for the request
            self.client.auth.set_session(jwt)
            self.client.auth.sign_out()
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Authentication error: {str(e)}")

    # Project management methods
    async def create_project(self, user_id: str, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new project.
        
        Args:
            user_id: User ID
            name: Project name
            description: Project description
            
        Returns:
            Dict containing project data
        """
        try:
            # Create new project
            data = self.client.from_('projects').insert({
                'owner_id': user_id,
                'name': name,
                'description': description
            }).execute()
            
            return data
        except Exception as e:
            raise ValueError(f"Project creation error: {str(e)}")
    
    async def get_projects(self, user_id: str) -> Dict[str, Any]:
        """
        Get all projects for the specified user.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict containing projects data
        """
        try:
            # Fallback to regular client with RLS
            query = self.client.from_('projects').select('*').eq('owner_id', user_id)
            result = query.execute()
            return result
        except Exception as e:
            raise ValueError(f"Project retrieval error: {str(e)}")
    
    async def get_project(self, project_id: str, user_id: str) -> Dict[str, Any]:
        """
        Get a project by ID.
        
        Args:
            project_id: Project ID
            user_id: User ID
            
        Returns:
            Dict containing project data
        """
        try:
            # First try to get the project as an owner
            query = self.client.from_('projects').select('*').eq('id', project_id).eq('owner_id', user_id)
            result = query.execute()
            
            # If found as owner, return the project
            if result.data:
                return result
            
            # For now, return empty result
            return result
        except Exception as e:
            raise ValueError(f"Project retrieval error: {str(e)}")
    
    async def update_project(self, project_id: str, data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Update a project.
        
        Args:
            project_id: Project ID
            data: Project data to update
            user_id: User ID
            
        Returns:
            Dict containing updated project data
        """
        try:
            # First check if user is owner
            owner_check = self.client.from_('projects').select('id').eq('id', project_id).eq('owner_id', user_id).execute()
            
            if not owner_check.data:
                # User is not the owner
                return {"data": None}
            
            # User is owner, proceed with update
            result = self.client.from_('projects').update(data).eq('id', project_id).execute()
            return result
        except Exception as e:
            raise ValueError(f"Project update error: {str(e)}")
    
    async def delete_project(self, project_id: str, user_id: str) -> Dict[str, Any]:
        """
        Delete a project.
        
        Args:
            project_id: Project ID
            user_id: User ID
            
        Returns:
            Dict containing deletion result
        """
        try:
            # First check if user is owner
            owner_check = self.client.from_('projects').select('id').eq('id', project_id).eq('owner_id', user_id).execute()
            
            if not owner_check.data:
                # User is not the owner
                return {"data": None}
            
            # User is owner, proceed with deletion
            result = self.client.from_('projects').delete().eq('id', project_id).execute()
            return result
        except Exception as e:
            raise ValueError(f"Project deletion error: {str(e)}")
            
    # Update share_project method too
    async def share_project(self, project_id: str, user_email: str, role: str, owner_id: str) -> Dict[str, Any]:
        """
        Share a project with another user.
        
        Args:
            project_id: Project ID
            user_email: Email of user to share with
            role: Role to assign (viewer, editor, admin)
            owner_id: ID of the current user (owner)
            
        Returns:
            Dict containing sharing result
        """
        try:
            # Check if current user is owner
            owner_check = self.client.from_('projects').select('id').eq('id', project_id).eq('owner_id', owner_id).execute()
            
            if not owner_check.data:
                # User is not the owner
                return {"data": None}
            
            # Get user ID from email
            user_result = self.client.from_('profiles').select('id').eq('email', user_email).execute()
            
            if not user_result.data:
                raise ValueError(f"User with email {user_email} not found")
            
            target_user_id = user_result.data[0]['id']
            
            # Check if already shared
            existing_check = self.client.from_('project_members').select('*').eq('project_id', project_id).eq('user_id', target_user_id).execute()
            
            if existing_check.data:
                # Update existing share
                result = self.client.from_('project_members').update({
                    'role': role, 
                    'updated_at': 'now()'
                }).eq('project_id', project_id).eq('user_id', target_user_id).execute()
            else:
                # Add new share
                result = self.client.from_('project_members').insert({
                    'project_id': project_id,
                    'user_id': target_user_id,
                    'role': role
                }).execute()
            
            return result
        except Exception as e:
            raise ValueError(f"Project sharing error: {str(e)}")

    # Profile management methods
    async def get_profile(self, jwt: str) -> Dict[str, Any]:
        """
        Get user profile.
        
        Args:
            jwt: User JWT token
            
        Returns:
            Dict containing profile data
        """
        try:
            self.client.auth.set_session(jwt)
            
            data = self.client.rpc('get_my_profile').execute()
            return data
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Profile retrieval error: {str(e)}")
    
    async def update_profile(self, profile_data: Dict[str, Any], jwt: str) -> Dict[str, Any]:
        """
        Update user profile.
        
        Args:
            profile_data: Profile data to update
            jwt: User JWT token
            
        Returns:
            Dict containing updated profile data
        """
        try:
            self.client.auth.set_session(jwt)
            
            data = self.client.rpc('update_my_profile', profile_data).execute()
            return data
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Profile update error: {str(e)}")
            
    # Code generation methods
    async def create_code_generation(self, project_id: str, prompt: str, jwt: str) -> Dict[str, Any]:
        """
        Create a new code generation record.
        
        Args:
            project_id: Project ID
            prompt: Generation prompt
            jwt: User JWT token
            
        Returns:
            Dict containing code generation data
        """
        try:
            user = self.client.auth.get_user()
            
            data = self.client.from_('code_generations').insert({
                'project_id': project_id,
                'user_id': user.id,
                'prompt': prompt,
                'status': 'pending'
            }).execute()
            
            return data
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Code generation record creation error: {str(e)}")
    
    async def update_code_generation(self, generation_id: str, update_data: Dict[str, Any], jwt: str) -> Dict[str, Any]:
        """
        Update a code generation record.
        
        Args:
            generation_id: Generation ID
            update_data: Data to update
            jwt: User JWT token
            
        Returns:
            Dict containing updated code generation data
        """
        try:
            data = self.client.from_('code_generations').update(update_data).eq('id', generation_id).execute()
            return data
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Code generation update error: {str(e)}") 