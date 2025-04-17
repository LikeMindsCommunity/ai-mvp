"""
Supabase database client module.
"""
from functools import lru_cache
from typing import Optional, Dict, Any

import httpx
from supabase import create_client, Client

from api.config import get_settings

settings = get_settings()

@lru_cache()
def get_supabase_client() -> Client:
    """
    Get a Supabase client instance.
    
    Returns:
        Client: Supabase client
    """
    return create_client(settings.supabase_url, settings.supabase_anon_key)


class SupabaseManager:
    """
    Manager for interacting with Supabase.
    """
    
    def __init__(self):
        """Initialize the manager."""
        self.client = get_supabase_client()
    
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
    async def create_project(self, name: str, description: Optional[str] = None, jwt: str = None) -> Dict[str, Any]:
        """
        Create a new project.
        
        Args:
            name: Project name
            description: Project description
            jwt: User JWT token
            
        Returns:
            Dict containing project data
        """
        try:
            if jwt:
                self.client.auth.set_session(jwt)
            
            data = self.client.rpc('create_project', {
                'name': name,
                'description': description
            }).execute()
            
            return data
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Project creation error: {str(e)}")
    
    async def get_projects(self, jwt: str) -> Dict[str, Any]:
        """
        Get all projects for the authenticated user.
        
        Args:
            jwt: User JWT token
            
        Returns:
            Dict containing projects data
        """
        try:
            self.client.auth.set_session(jwt)
            
            data = self.client.from_('projects').select('*').execute()
            return data
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Project retrieval error: {str(e)}")
    
    async def get_project(self, project_id: str, jwt: str) -> Dict[str, Any]:
        """
        Get a project by ID.
        
        Args:
            project_id: Project ID
            jwt: User JWT token
            
        Returns:
            Dict containing project data
        """
        try:
            self.client.auth.set_session(jwt)
            
            data = self.client.from_('projects').select('*').eq('id', project_id).single().execute()
            return data
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Project retrieval error: {str(e)}")
    
    async def update_project(self, project_id: str, project_data: Dict[str, Any], jwt: str) -> Dict[str, Any]:
        """
        Update a project.
        
        Args:
            project_id: Project ID
            project_data: Project data to update
            jwt: User JWT token
            
        Returns:
            Dict containing updated project data
        """
        try:
            self.client.auth.set_session(jwt)
            
            data = self.client.from_('projects').update(project_data).eq('id', project_id).execute()
            return data
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Project update error: {str(e)}")
    
    async def delete_project(self, project_id: str, jwt: str) -> Dict[str, Any]:
        """
        Delete a project.
        
        Args:
            project_id: Project ID
            jwt: User JWT token
            
        Returns:
            Dict containing deletion result
        """
        try:
            self.client.auth.set_session(jwt)
            
            data = self.client.from_('projects').delete().eq('id', project_id).execute()
            return data
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Project deletion error: {str(e)}")

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
            self.client.auth.set_session(jwt)
            
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
            self.client.auth.set_session(jwt)
            
            data = self.client.from_('code_generations').update(update_data).eq('id', generation_id).execute()
            return data
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Code generation update error: {str(e)}") 